"""ticket pydantic schemas."""

from pydantic import BaseModel, field_validator

from app.enums import TicketStatus
from app.mixins.common import BaseReadSchemaMixin


def validate_title(v: str) -> None:
    """Core title validation logic."""
    if not v or not v.strip():
        raise ValueError("Le titre ne doit pas être vide")


class TicketCreateUpdate(BaseModel):  # type: ignore[misc]
    """Ticket CreateUpdate."""

    title: str
    description: str
    status: TicketStatus = TicketStatus.OPEN

    @field_validator("title", mode="before")
    @classmethod
    def title_validator(cls, v: str) -> str:
        """Title validator."""
        validate_title(v)
        return v


class TicketCreate(TicketCreateUpdate):  # type: ignore[misc]
    """Ticket creation."""


class TicketUpdate(TicketCreateUpdate):  # type: ignore[misc]
    """Ticket update."""

    title: str
    description: str | None = None
    status: TicketStatus | None = None


class TicketRead(BaseReadSchemaMixin):
    """Ticket read."""

    title: str
    description: str
    status: TicketStatus
