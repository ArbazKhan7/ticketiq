import requests
from app.core.config import settings


def send_whatsapp_message(to_number: str, message: str):
    url = f"https://graph.facebook.com/v19.0/{settings.meta_phone_number_id}/messages"

    headers = {
        "Authorization": f"Bearer {settings.meta_access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message},
    }

    response = requests.post(url, headers=headers, json=payload)
    print("META SEND RESPONSE:", response.status_code, response.text)
