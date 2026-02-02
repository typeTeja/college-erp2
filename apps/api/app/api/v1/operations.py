from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from app.api.deps import get_session, get_current_user
from app.models import User
from app.models.staff import Staff
from app.models.operations import MaintenanceTicket, Shift, TicketStatus
from app.schemas.operations import (
from app.shared.enums import TicketStatus

    MaintenanceTicketCreate, MaintenanceTicketRead, MaintenanceTicketUpdate,
    ShiftCreate, ShiftRead
)

router = APIRouter()

# --- Shifts ---
@router.post("/shifts", response_model=ShiftRead)
def create_shift(shift: ShiftCreate, session: Session = Depends(get_session)):
    new_shift = Shift.from_orm(shift)
    session.add(new_shift)
    session.commit()
    session.refresh(new_shift)
    return new_shift

@router.get("/shifts", response_model=List[ShiftRead])
def get_shifts(session: Session = Depends(get_session)):
    return session.exec(select(Shift)).all()

# --- Tickets ---
@router.post("/tickets", response_model=MaintenanceTicketRead)
def create_ticket(
    ticket: MaintenanceTicketCreate, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    new_ticket = MaintenanceTicket.from_orm(ticket)
    new_ticket.reported_by_id = current_user.id
    session.add(new_ticket)
    session.commit()
    session.refresh(new_ticket)
    return new_ticket

@router.get("/tickets", response_model=List[MaintenanceTicketRead])
def get_tickets(
    session: Session = Depends(get_session),
    status: Optional[TicketStatus] = None,
    limit: int = 50
):
    query = select(MaintenanceTicket)
    if status:
        query = query.where(MaintenanceTicket.status == status)
    return session.exec(query.order_by(MaintenanceTicket.created_at.desc()).limit(limit)).all()

@router.put("/tickets/{ticket_id}", response_model=MaintenanceTicketRead)
def update_ticket(
    ticket_id: int,
    ticket_update: MaintenanceTicketUpdate,
    session: Session = Depends(get_session),
):
    ticket = session.get(MaintenanceTicket, ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    data = ticket_update.dict(exclude_unset=True)
    for k, v in data.items():
        setattr(ticket, k, v)
        
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket
