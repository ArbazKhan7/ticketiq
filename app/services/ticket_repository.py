from sqlalchemy import text
from app.core.db import engine
import uuid
from datetime import datetime


def insert_ticket(ticket_data: dict) -> str:
    """
    Insert a new ticket and return ticket_id.
    """
    ticket_id = str(uuid.uuid4())
    ticket_data["id"] = ticket_id
    ticket_data["received_at"] = ticket_data.get(
        "received_at", datetime.utcnow().isoformat()
    )

    query = text("""
        INSERT INTO ticket_master (
            id,
            source,
            requester_name,
            contact_number,
            email_address,
            building_name,
            tower,
            apartment_number,
            issue_category,
            issue_description,
            priority,
            received_at
        ) VALUES (
            :id,
            :source,
            :requester_name,
            :contact_number,
            :email_address,
            :building_name,
            :tower,
            :apartment_number,
            :issue_category,
            :issue_description,
            :priority,
            :received_at
        )
    """)

    with engine.begin() as conn:
        conn.execute(query, ticket_data)

    return ticket_id


def update_ticket(ticket_id: str, updates: dict):
    """
    Update allowed fields for an existing ticket.
    Used only during correction window.
    """
    allowed_fields = {
        "apartment_number",
        "tower",
        "contact_number",
        "issue_description"
    }

    fields = {k: v for k, v in updates.items() if k in allowed_fields and v}
    if not fields:
        return

    set_clause = ", ".join([f"{k} = :{k}" for k in fields])
    fields["id"] = ticket_id

    query = text(f"""
        UPDATE ticket_master
        SET {set_clause}
        WHERE id = :id
    """)

    with engine.begin() as conn:
        conn.execute(query, fields)
