from app.storage.redis import get_session, save_session, clear_session
from app.services.ticket_engine import run_intake_engine
from app.services.ticket_repository import insert_ticket


# Mandatory fields in order
REQUIRED_FIELDS_ORDER = [
    "requester_name",
    "apartment_number",
    "issue_description",
]


QUESTION_MAP = {
    "requester_name": "May I have your name?",
    "apartment_number": "Please share your apartment number.",
    "issue_description": "Please describe the issue you are facing."
}


def handle_whatsapp_message(
    session_id: str,
    message_text: str,
    sender_number: str | None = None
) -> str:
    """
    Production-grade WhatsApp intake handler.
    """

    message_text = message_text.strip()

    # 1️⃣ Load session
    session_data = get_session(session_id) or {}

    # Always auto-fill contact number if available
    if sender_number and not session_data.get("contact_number"):
        session_data["contact_number"] = sender_number

    # 2️⃣ Detect NEW session
    is_new_session = not session_data or (
    "expected_field" not in session_data
    and "missing_fields" not in session_data
)


    # ==========================
    # MODE 1 — NEW SESSION
    # ==========================
    if is_new_session:
        ticket = run_intake_engine(
            source="whatsapp",
            raw_text=message_text,
            existing_data={}
        )

    # ==========================
    # MODE 2 — EXPECTING ONE FIELD
    # ==========================
    elif "expected_field" in session_data:

        expected_field = session_data["expected_field"]

        # Only set explicitly answered field
        session_data[expected_field] = message_text
        session_data.pop("expected_field", None)

        ticket = run_intake_engine(
            source="whatsapp",
            raw_text=None,               # ⛔ DO NOT re-run LLM
            existing_data=session_data
        )

    # ==========================
    # MODE 3 — NORMAL MESSAGE
    # ==========================
    else:
        ticket = run_intake_engine(
            source="whatsapp",
            raw_text=message_text,
            existing_data=session_data
        )

    # ==========================
    # SUBMITTED → SAVE & EXIT
    # ==========================
    if ticket.status == "submitted":
        insert_ticket(ticket.model_dump(mode="json"))
        clear_session(session_id)

        return (
            "✅ *Request Submitted Successfully!*\n\n"
            "Our Sariah Services team has received your request.\n"
            "We will take action shortly.\n\n"
            "Thank you."
        )

    # ==========================
    # ASK NEXT REQUIRED FIELD
    # ==========================
    next_field = ticket.missing_fields[0]

    session_data = ticket.model_dump(mode="json")
    session_data["expected_field"] = next_field

    save_session(session_id, session_data)

    return QUESTION_MAP.get(
        next_field,
        "Could you please provide the required details?"
    )
