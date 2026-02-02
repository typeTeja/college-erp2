from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from app.api.deps import get_session, get_current_active_superuser
from app.models.user import User
from ..models.fee import (
    FeeStructure, StudentFee, StudentFeeInstallment,
    FeePayment, FeeConcession, FeeFine
)
from ..services.fee import fee_service

router = APIRouter()

# Fee Structure Endpoints
@router.post("/structures")
def create_fee_structure(
    *,
    session: Session = Depends(get_session),
    fee_structure_data: dict,
    current_user: User = Depends(get_current_active_superuser)
):
    """Create a new fee structure"""
    return fee_service.create_fee_structure(session, fee_structure_data)

@router.get("/structures")
def list_fee_structures(
    *,
    session: Session = Depends(get_session),
    program_id: Optional[int] = Query(None),
    academic_year: Optional[str] = Query(None)
):
    """List fee structures"""
    stmt = select(FeeStructure)
    if program_id:
        stmt = stmt.where(FeeStructure.program_id == program_id)
    if academic_year:
        stmt = stmt.where(FeeStructure.academic_year == academic_year)
    return session.exec(stmt).all()

# Student Fee Assignment
@router.post("/student-fees")
def assign_fee_to_student(
    *,
    session: Session = Depends(get_session),
    assignment_data: dict,
    current_user: User = Depends(get_current_active_superuser)
):
    """Assign fee to student"""
    return fee_service.assign_fee_to_student(
        session,
        student_id=assignment_data["student_id"],
        fee_structure_id=assignment_data["fee_structure_id"],
        academic_year=assignment_data["academic_year"]
    )

@router.get("/student/{student_id}/summary")
def get_student_fee_summary(
    *,
    session: Session = Depends(get_session),
    student_id: int,
    academic_year: Optional[str] = Query(None)
):
    """Get fee summary for a student"""
    return fee_service.get_student_fee_summary(session, student_id, academic_year)
