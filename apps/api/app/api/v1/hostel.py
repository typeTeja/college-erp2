from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.db.session import get_session
from app.api.deps import get_current_user
from app.models.user import User
from app.models.hostel import HostelBlock, HostelRoom, BedAllocation, GatePass, HostelComplaint
from app.schemas.hostel import (
    HostelBlockCreate, HostelBlockRead, 
    HostelRoomCreate, HostelRoomRead,
    BedAllocationCreate, BedAllocationRead,
    GatePassCreate, GatePassRead,
    HostelComplaintCreate, HostelComplaintRead
)
from typing import List, Optional
from datetime import datetime

router = APIRouter()

# --- Blocks ---
@router.get("/blocks", response_model=List[HostelBlockRead])
def list_blocks(session: Session = Depends(get_session)):
    return session.exec(select(HostelBlock)).all()

@router.post("/blocks", response_model=HostelBlockRead)
def create_block(data: HostelBlockCreate, session: Session = Depends(get_session)):
    block = HostelBlock.model_validate(data)
    session.add(block)
    session.commit()
    session.refresh(block)
    return block

# --- Rooms ---
@router.get("/rooms", response_model=List[HostelRoomRead])
def list_rooms(block_id: Optional[int] = None, session: Session = Depends(get_session)):
    statement = select(HostelRoom)
    if block_id:
        statement = statement.where(HostelRoom.block_id == block_id)
    return session.exec(statement).all()

@router.post("/rooms", response_model=HostelRoomRead)
def create_room(data: HostelRoomCreate, session: Session = Depends(get_session)):
    room = HostelRoom.model_validate(data)
    session.add(room)
    session.commit()
    session.refresh(room)
    return room

# --- Allocations ---
@router.post("/allocate", response_model=BedAllocationRead)
def allocate_bed(data: BedAllocationCreate, session: Session = Depends(get_session)):
    room = session.get(HostelRoom, data.room_id)
    if not room or room.current_occupancy >= room.capacity:
        raise HTTPException(status_code=400, detail="Room is full or does not exist")
    
    allocation = BedAllocation.model_validate(data)
    room.current_occupancy += 1
    session.add(allocation)
    session.add(room)
    session.commit()
    session.refresh(allocation)
    return allocation

# --- GatePass ---
@router.post("/gatepass", response_model=GatePassRead)
def request_gatepass(data: GatePassCreate, session: Session = Depends(get_session)):
    gp = GatePass.model_validate(data)
    session.add(gp)
    session.commit()
    session.refresh(gp)
    return gp

# --- Complaints ---
@router.get("/complaints", response_model=List[HostelComplaintRead])
def list_complaints(session: Session = Depends(get_session)):
    return session.exec(select(HostelComplaint)).all()

@router.post("/complaints", response_model=HostelComplaintRead)
def raise_complaint(data: HostelComplaintCreate, session: Session = Depends(get_session)):
    complaint = HostelComplaint.model_validate(data)
    session.add(complaint)
    session.commit()
    session.refresh(complaint)
    return complaint
