from app.models.ticket import Ticket
from app.utils.validators import find_missing_fields

def test_missing_fields():
    ticket = Ticket(
        source="whatsapp",
        requester_name="Perwez",
        apartment_number="234",
        issue_description="AC not working"
    )

    missing = find_missing_fields(ticket)
    print("Missing fields:", missing)


def test_missing_when_incomplete():
    ticket = Ticket(
        source="whatsapp",
        issue_description="AC not working"
    )

    missing = find_missing_fields(ticket)
    print("Missing fields:", missing)


if __name__ == "__main__":
    test_missing_fields()
    test_missing_when_incomplete()
