from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from app.db.session import get_session
from app.models.program import Program, ProgramType, ProgramStatus
from app.schemas.program import ProgramCreate, ProgramRead
from app.services.program_service import ProgramService
from typing import List, Optional, Dict, Any

router = APIRouter()

from app.api.deps import get_current_active_superuser, get_current_user
from app.models.user import User
from app.shared.enums import ProgramStatus, ProgramType


@router.post("/", response_model=ProgramRead)
def create_program(
    program_in: ProgramCreate, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Create a new program and generate its structure (Admin only)"""
    program = ProgramService.create_program(session, program_in)
    return program

@router.get("/", response_model=List[ProgramRead])
def get_programs(
    type: Optional[ProgramType] = None,
    status: Optional[ProgramStatus] = None,
    skip: int = 0, 
    limit: int = 100,
    session: Session = Depends(get_session),
    # Allow public access for listing programs (needed for Apply page)
    # current_user: User = Depends(get_current_user) 
):
    """List programs with filtering (Authenticated users)"""
    return ProgramService.get_programs(session, skip, limit, type, status)

@router.get("/{id}", response_model=ProgramRead)
def get_program(
    id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get a specific program by ID (Authenticated users)"""
    program = ProgramService.get_program(session, id)
    if not program:
        raise HTTPException(status_code=404, detail="Program not found")
    return program

@router.put("/{id}/structure")
def update_structure(
    id: int, 
    structure_data: Dict[str, Any], 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Update program structure (Admin only)"""
    return ProgramService.update_structure(session, id, structure_data)

@router.delete("/{id}")
def delete_program(
    id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Delete a program (Admin only)"""
    ProgramService.delete_program(session, id)
    return {"message": "Program deleted successfully"}
