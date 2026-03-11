"""route tickets."""

import logging
import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.ticket import TicketCreate, TicketRead, TicketUpdate
from app.services import ticket as ticket_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/tickets", status_code=status.HTTP_201_CREATED)  # type: ignore[untyped-decorator]
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)) -> TicketRead:
    """Create a new ticket.

    - **title**: the ticket title
    - **description**: the ticket description
    - **status**: the ticket status (default: open)
    """
    return ticket_service.create_ticket(ticket, db)


@router.get("/tickets", status_code=status.HTTP_200_OK)  # type: ignore[untyped-decorator]
def get_tickets(db: Session = Depends(get_db)) -> list[TicketRead]:
    """Get all tickets.

    Returns a list of all tickets.
    """
    return ticket_service.get_tickets(db)


@router.get("/tickets/{ticket_id}", status_code=status.HTTP_200_OK)  # type: ignore[untyped-decorator]
def get_ticket(ticket_id: uuid.UUID, db: Session = Depends(get_db)) -> TicketRead:
    """Get a ticket by id.

    - **ticket_id**: the ticket UUID
    """
    return ticket_service.get_ticket_by_id(ticket_id, db)


@router.put("/tickets/{ticket_id}", status_code=status.HTTP_200_OK)  # type: ignore[untyped-decorator]
def update_ticket(ticket_id: uuid.UUID, ticket: TicketUpdate, db: Session = Depends(get_db)) -> TicketRead:
    """Update a ticket.

    - **ticket_id**: the ticket UUID
    - **title**: the ticket title
    - **description**: the ticket description
    - **status**: the ticket status
    """
    return ticket_service.update_ticket(ticket_id, ticket, db)


@router.patch("/tickets/{ticket_id}/close", status_code=status.HTTP_200_OK)  # type: ignore[untyped-decorator]
def close_ticket(ticket_id: uuid.UUID, db: Session = Depends(get_db)) -> TicketRead:
    """Close a ticket.

    - **ticket_id**: the ticket UUID to close
    """
    return ticket_service.close_ticket(ticket_id, db)
