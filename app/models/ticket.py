from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class Ticket(BaseModel):
    # ---- Core Identifiers ----
    source: Literal["whatsapp", "email"]
    received_at: datetime = Field(default_factory=datetime.utcnow)

    # ---- Requester Info ----
    requester_name: Optional[str] = None
    contact_number: Optional[str] = None
    email_address: Optional[str] = None

    # ---- Property Info ----
    building_name: Optional[str] = None
    tower: Optional[str] = None
    apartment_number: Optional[str] = None
    emirate: Optional[str] = None

    # ---- Issue Details ----
    issue_category: Optional[str] = None
    issue_description: Optional[str] = None
    priority: Optional[Literal["low", "medium", "high", "urgent"]] = None

    # ---- System Fields ----
    status: Literal[
        "incomplete",
        "submitted"
    ] = "incomplete"

    missing_fields: list[str] = Field(default_factory=list)
