"""business logic."""

import uuid

from sqlalchemy.orm import Session

from app.enums import TicketStatus
from app.exceptions.business import TicketAlreadyClosedError, TicketNotFoundError
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketRead, TicketUpdate


def create_ticket(ticket: TicketCreate, db: Session) -> TicketRead:
    """Create a ticket.

    :param ticket: TicketCreate - the ticket data to create
    :param db: Session - the database session
    :return: TicketRead - the created ticket
    """
    db_ticket = Ticket(**ticket.model_dump())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return TicketRead.model_validate(db_ticket)


def get_tickets(db: Session) -> list[TicketRead]:
    """Get all tickets.

    :param db: Session - the database session
    :return: list[TicketRead] - the list of tickets
    """
    tickets = db.query(Ticket).all()
    return [TicketRead.model_validate(ticket) for ticket in tickets]


def get_ticket_by_id(ticket_id: uuid.UUID, db: Session) -> TicketRead:
    """Get a ticket by id.

    :param ticket_id: uuid.UUID - the ticket id
    :param db: Session - the database session
    :return: TicketRead - the ticket
    """
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise TicketNotFoundError(ticket_id)
    return TicketRead.model_validate(ticket)


def update_ticket(ticket_id: uuid.UUID, ticket: TicketUpdate, db: Session) -> TicketRead:
    """Update a ticket.

    :param ticket_id: uuid.UUID - the ticket id
    :param ticket: TicketUpdate - the ticket data to update
    :param db: Session - the database session
    :return: TicketRead - the updated ticket
    """
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not db_ticket:
        raise TicketNotFoundError(ticket_id)
    for field, value in ticket.model_dump(exclude_unset=True).items():
        setattr(db_ticket, field, value)
    db.commit()
    db.refresh(db_ticket)
    return TicketRead.model_validate(db_ticket)


def close_ticket(ticket_id: uuid.UUID, db: Session) -> TicketRead:
    """Close a ticket by setting its status to CLOSED.

    :param ticket_id: uuid.UUID - the ticket id
    :param db: Session - the database session
    :return: TicketRead - the closed ticket
    """
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not db_ticket:
        raise TicketNotFoundError(ticket_id)
    if db_ticket.status == TicketStatus.CLOSED:
        raise TicketAlreadyClosedError(ticket_id)
    db_ticket.status = TicketStatus.CLOSED
    db.commit()
    db.refresh(db_ticket)
    return TicketRead.model_validate(db_ticket)
