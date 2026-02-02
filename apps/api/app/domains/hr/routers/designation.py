from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.api.deps import get_session, get_current_active_superuser
from ..models.designation import Designation
from ..schemas.designation import DesignationRead, DesignationCreate

router = APIRouter(prefix="/designations", tags=["HR - Designations"])

@router.post("/", response_model=DesignationRead)
def create_designation(
    *,
    session: Session = Depends(get_session),
    designation_data: DesignationCreate,
    current_user = Depends(get_current_active_superuser)
):
    """Create a new designation (Admin only)"""
    designation = Designation(**designation_data.model_dump())
    session.add(designation)
    session.commit()
    session.refresh(designation)
    return designation

@router.get("/", response_model=List[DesignationRead])
def list_designations(
    *,
    session: Session = Depends(get_session),
    is_active: bool = Query(True),
    is_teaching: Optional[bool] = Query(None)
):
    """List designations"""
    stmt = select(Designation).where(Designation.is_active == is_active)
    if is_teaching is not None:
        stmt = stmt.where(Designation.is_teaching == is_teaching)
    return session.exec(stmt.all())

@router.get("/{designation_id}", response_model=DesignationRead)
def get_designation(
    *,
    session: Session = Depends(get_session),
    designation_id: int
):
    """Get designation by ID"""
    designation = session.get(Designation, designation_id)
    if not designation:
        raise HTTPException(status_code=404, detail="Designation not found")
    return designation
