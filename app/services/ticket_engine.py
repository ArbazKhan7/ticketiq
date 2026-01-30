from app.models.ticket import Ticket
from app.services.llm_extractor import extract_ticket_fields
from app.utils.validators import find_missing_fields


def run_intake_engine(
    source: str,
    raw_text: str,
    existing_data: dict | None = None
) -> Ticket:

    if existing_data is None:
        existing_data = {}

    # Step 1: Extract fields ONLY if text exists
    if raw_text:
        extracted = extract_ticket_fields(raw_text)
    else:
        extracted = {}

    # Step 2: Merge safely
    clean_existing = {k: v for k, v in existing_data.items() if k != "source"}

    merged_data = {
        **clean_existing,
        **{k: v for k, v in extracted.items() if v}
    }

    # Step 3: Build ticket
    ticket = Ticket(
        source=source,
        **merged_data
    )

    # Step 4: Missing fields
    missing_fields = find_missing_fields(ticket)
    ticket.missing_fields = missing_fields

    # Step 5: Status
    if not missing_fields:
        ticket.status = "submitted"

    return ticket
