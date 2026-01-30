from app.storage.redis import get_session, save_session, clear_session
from app.services.ticket_engine import run_intake_engine
from app.services.ticket_repository import insert_ticket


QUESTION_MAP = {
    "requester_name": "May I have your name?",
    "apartment_number": "Please share your apartment number.",
    "issue_description": "Please describe the issue you are facing.",
}


def handle_whatsapp_message(
    session_id: str,
    message_text: str,
    sender_number: str | None = None
) -> str:
    """
    FINAL, STABLE WhatsApp intake handler.
    """

    message_text = message_text.strip()
    session_data = get_session(session_id) or {}

    # Auto-fill contact number ONCE
    if sender_number and not session_data.get("contact_number"):
        session_data["contact_number"] = sender_number

    expected_field = session_data.get("expected_field")

    # =========================
    # CASE 1: Expecting a reply to a specific question
    # =========================
    if expected_field:
        # Save ONLY the expected field
        session_data[expected_field] = message_text
        session_data.pop("expected_field", None)

        ticket = run_intake_engine(
            source="whatsapp",
            raw_text=None,              # ⛔ DO NOT re-run LLM
            existing_data=session_data
        )

    # =========================
    # CASE 2: Fresh or free-form message
    # =========================
    else:
        ticket = run_intake_engine(
            source="whatsapp",
            raw_text=message_text,
            existing_data=session_data
        )

    # =========================
    # SUBMITTED → SAVE & RESET SESSION
    # =========================
    if ticket.status == "submitted":
        insert_ticket(ticket.model_dump(mode="json"))
        clear_session(session_id)

        return (
            "✅ *Request Submitted Successfully!*\n\n"
            "Our Sariah Services team has received your request.\n"
            "We will take action shortly.\n\n"
            "Thank you."
        )

    # =========================
    # ASK NEXT REQUIRED FIELD
    # =========================
    next_field = ticket.missing_fields[0]

    session_data = ticket.model_dump(mode="json")
    session_data["expected_field"] = next_field

    save_session(session_id, session_data)

    return QUESTION_MAP.get(
        next_field,
        "Could you please provide the required details?"
    )
