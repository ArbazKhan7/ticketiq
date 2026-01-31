from fastapi import APIRouter, Request, Response

from app.adapters.whatsapp import (
    handle_whatsapp_message,
    send_whatsapp_message,
)
from app.core.config import settings

router = APIRouter()

# =========================================================
# VERIFY WEBHOOK (GET)
# =========================================================
@router.get("/webhook/whatsapp")
async def verify_webhook(request: Request):
    params = request.query_params

    if (
        params.get("hub.mode") == "subscribe"
        and params.get("hub.verify_token") == settings.meta_verify_token
    ):
        return Response(
            content=params.get("hub.challenge"),
            status_code=200
        )

    return Response(status_code=403)


# =========================================================
# RECEIVE MESSAGE (POST)
# =========================================================
@router.post("/webhook/whatsapp")
async def receive_whatsapp_message(request: Request):
    payload = await request.json()
    print("META PAYLOAD >>>", payload)

    entry = payload.get("entry", [])
    if not entry:
        return Response(status_code=200)

    changes = entry[0].get("changes", [])
    if not changes:
        return Response(status_code=200)

    value = changes[0].get("value", {})
    messages = value.get("messages", [])

    if not messages:
        return Response(status_code=200)

    message = messages[0]
    text = message.get("text", {}).get("body")
    from_number = message.get("from")

    if not text or not from_number:
        return Response(status_code=200)

    # 🧠 PROCESS MESSAGE
    reply = handle_whatsapp_message(
        session_id=from_number,
        message_text=text,
        sender_number=from_number,
    )

    # 📤 SEND BACK TO WHATSAPP
    send_whatsapp_message(
        to=from_number,
        text=reply,
    )

    return Response(status_code=200)
