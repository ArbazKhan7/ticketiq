from app.models.ticket import Ticket

# Define required fields for a valid ticket
REQUIRED_FIELDS_ORDER = [
    "requester_name",
    "apartment_number",
    "issue_description"
]


def find_missing_fields(ticket: Ticket) -> list[str]:
    """
    Given a Ticket object, return a list of missing required fields
    in the order they should be asked.
    """
    missing = []

    for field in REQUIRED_FIELDS_ORDER:
        value = getattr(ticket, field)
        if value is None or (isinstance(value, str) and not value.strip()):
            missing.append(field)

    return missing
