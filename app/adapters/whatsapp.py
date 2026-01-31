import requests

from app.storage.redis import get_session, save_session, clear_session
from app.services.ticket_engine import run_intake_engine
from app.services.ticket_repository import insert_ticket
from app.core.config import settings


QUESTION_MAP = {
    "requester_name": "May I have your name?",
    "apartment_number": "Please share your apartment number.",
    "issue_description": "Please describe the issue you are facing.",
}


# =========================================================
# META CLOUD API — SEND MESSAGE
# =========================================================
def send_whatsapp_message(to: str, text: str):
    url = f"https://graph.facebook.com/v19.0/{settings.meta_phone_number_id}/messages"

    headers = {
        "Authorization": f"Bearer {settings.meta_access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }

    resp = requests.post(url, headers=headers, json=payload)
    print("META SEND RESPONSE:", resp.status_code, resp.text)


# =========================================================
# WHATSAPP INTAKE HANDLER (STABLE)
# =========================================================
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
    # CASE 1: Expecting a reply
    # =========================
    if expected_field:
        session_data[expected_field] = message_text
        session_data.pop("expected_field", None)

        ticket = run_intake_engine(
            source="whatsapp",
            raw_text=None,        # DO NOT re-run LLM
            existing_data=session_data
        )

    # =========================
    # CASE 2: Fresh message
    # =========================
    else:
        ticket = run_intake_engine(
            source="whatsapp",
            raw_text=message_text,
            existing_data=session_data
        )

    # =========================
    # SUBMITTED → SAVE & RESET
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
    # ASK NEXT QUESTION
    # =========================
    next_field = ticket.missing_fields[0]

    session_data = ticket.model_dump(mode="json")
    session_data["expected_field"] = next_field

    save_session(session_id, session_data)

    return QUESTION_MAP.get(
        next_field,
        "Could you please provide the required details?"
    )
