import json
from openai import OpenAI
from app.core.config import settings

# Initialize OpenAI client
client = OpenAI(api_key=settings.openai_api_key)


SYSTEM_PROMPT = """
You are an information extraction engine for a facility management company.

Your task:
- Extract structured ticket fields from tenant messages.
- Return ONLY valid JSON.
- Do NOT guess or invent information.
- If a field is not present, return null.
- Use simple strings only.

Fields to extract:
- requester_name
- contact_number
- email_address
- building_name
- tower
- apartment_number
- issue_category
- issue_description
- priority
"""


def extract_ticket_fields(raw_text: str) -> dict:
    """
    Uses OpenAI to extract ticket fields from unstructured text.
    Returns a dict with extracted values or None.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": raw_text}
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    try:
        extracted = json.loads(content)
    except json.JSONDecodeError:
        # Fail safe: return empty extraction
        return {}

    return extracted
