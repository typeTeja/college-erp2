"""
Fee Management API Endpoints

Provides comprehensive fee management functionality including:
- Fee structure CRUD
- Student fee assignment
- Payment recording
- Concession management
- Fine calculation and waiver
- Fee summaries and reports
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.api.deps import get_session, get_current_active_superuser
from app.models.user import User
from app.models.fee import (
    FeeStructure, StudentFee, StudentFeeInstallment,
    FeePayment, FeeConcession, FeeFine
)
from app.schemas.fee import (
    FeeStructureCreate, FeeStructureResponse,
    StudentFeeCreate, StudentFeeResponse, StudentFeeSummary,
    FeePaymentCreate, FeePaymentResponse,
    FeeConcessionCreate, FeeConcessionResponse,
    StudentFeeInstallmentResponse
)
from app.services.fee_service import FeeService

router = APIRouter(prefix="/fees", tags=["Fee Management"])


# ============================================================================
# Fee Structure Endpoints
# ============================================================================

@router.post("/structures", response_model=FeeStructureResponse)
def create_fee_structure(
    *,
    session: Session = Depends(get_session),
    fee_structure_data: FeeStructureCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Create a new fee structure"""
    return FeeService.create_fee_structure(session, fee_structure_data)


@router.get("/structures", response_model=List[FeeStructureResponse])
def list_fee_structures(
    *,
    session: Session = Depends(get_session),
    program_id: Optional[int] = Query(None),
    academic_year: Optional[str] = Query(None),
    slab: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 100
):
    """List all fee structures with optional filters"""
    stmt = select(FeeStructure)
    
    if program_id:
        stmt = stmt.where(FeeStructure.program_id == program_id)
    if academic_year:
        stmt = stmt.where(FeeStructure.academic_year == academic_year)
    if slab:
        stmt = stmt.where(FeeStructure.slab == slab)
    
    stmt = stmt.offset(skip).limit(limit)
    return session.exec(stmt).all()


@router.get("/structures/{fee_structure_id}", response_model=FeeStructureResponse)
def get_fee_structure(
    *,
    session: Session = Depends(get_session),
    fee_structure_id: int
):
    """Get a specific fee structure"""
    fee_structure = session.get(FeeStructure, fee_structure_id)
    if not fee_structure:
        raise HTTPException(status_code=404, detail="Fee structure not found")
    return fee_structure


@router.delete("/structures/{fee_structure_id}")
def delete_fee_structure(
    *,
    session: Session = Depends(get_session),
    fee_structure_id: int,
    current_user: User = Depends(get_current_active_superuser)
):
    """Delete a fee structure"""
    fee_structure = session.get(FeeStructure, fee_structure_id)
    if not fee_structure:
        raise HTTPException(status_code=404, detail="Fee structure not found")
    
    session.delete(fee_structure)
    session.commit()
    return {"message": "Fee structure deleted successfully"}


# ============================================================================
# Student Fee Assignment Endpoints
# ============================================================================

@router.post("/student-fees", response_model=StudentFeeResponse)
def assign_fee_to_student(
    *,
    session: Session = Depends(get_session),
    assignment_data: StudentFeeCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Assign a fee structure to a student"""
    return FeeService.assign_fee_to_student(
        session,
        student_id=assignment_data.student_id,
        fee_structure_id=assignment_data.fee_structure_id,
        academic_year=assignment_data.academic_year,
        concession_percentage=assignment_data.concession_percentage,
        old_dues=assignment_data.old_dues
    )


@router.get("/student-fees", response_model=List[StudentFeeResponse])
def list_student_fees(
    *,
    session: Session = Depends(get_session),
    student_id: Optional[int] = Query(None),
    academic_year: Optional[str] = Query(None),
    is_blocked: Optional[bool] = Query(None),
    skip: int = 0,
    limit: int = 100
):
    """List student fees with optional filters"""
    stmt = select(StudentFee)
    
    if student_id:
        stmt = stmt.where(StudentFee.student_id == student_id)
    if academic_year:
        stmt = stmt.where(StudentFee.academic_year == academic_year)
    if is_blocked is not None:
        stmt = stmt.where(StudentFee.is_blocked == is_blocked)
    
    stmt = stmt.offset(skip).limit(limit)
    return session.exec(stmt).all()


@router.get("/student-fees/{student_fee_id}", response_model=StudentFeeResponse)
def get_student_fee(
    *,
    session: Session = Depends(get_session),
    student_fee_id: int
):
    """Get a specific student fee"""
    student_fee = session.get(StudentFee, student_fee_id)
    if not student_fee:
        raise HTTPException(status_code=404, detail="Student fee not found")
    return student_fee


@router.get("/students/{student_id}/fee-summary")
def get_student_fee_summary(
    *,
    session: Session = Depends(get_session),
    student_id: int,
    academic_year: Optional[str] = Query(None)
):
    """Get comprehensive fee summary for a student"""
    return FeeService.get_student_fee_summary(session, student_id, academic_year)


# ============================================================================
# Installment Endpoints
# ============================================================================

@router.get("/student-fees/{student_fee_id}/installments", response_model=List[StudentFeeInstallmentResponse])
def get_student_installments(
    *,
    session: Session = Depends(get_session),
    student_fee_id: int
):
    """Get all installments for a student fee"""
    stmt = select(StudentFeeInstallment).where(
        StudentFeeInstallment.student_fee_id == student_fee_id
    ).order_by(StudentFeeInstallment.installment_number)
    
    return session.exec(stmt).all()


@router.post("/student-fees/{student_fee_id}/generate-installments", response_model=List[StudentFeeInstallmentResponse])
def generate_installments(
    *,
    session: Session = Depends(get_session),
    student_fee_id: int,
    current_user: User = Depends(get_current_active_superuser)
):
    """Generate installments for a student fee"""
    return FeeService.generate_installments(session, student_fee_id)


# ============================================================================
# Payment Endpoints
# ============================================================================

@router.post("/payments", response_model=FeePaymentResponse)
def record_payment(
    *,
    session: Session = Depends(get_session),
    payment_data: FeePaymentCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Record a fee payment"""
    return FeeService.record_payment(session, payment_data, current_user.id)


@router.get("/payments", response_model=List[FeePaymentResponse])
def list_payments(
    *,
    session: Session = Depends(get_session),
    student_fee_id: Optional[int] = Query(None),
    payment_status: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 100
):
    """List fee payments with optional filters"""
    stmt = select(FeePayment)
    
    if student_fee_id:
        stmt = stmt.where(FeePayment.student_fee_id == student_fee_id)
    if payment_status:
        stmt = stmt.where(FeePayment.payment_status == payment_status)
    
    stmt = stmt.offset(skip).limit(limit).order_by(FeePayment.created_at.desc())
    return session.exec(stmt).all()


@router.get("/payments/{payment_id}", response_model=FeePaymentResponse)
def get_payment(
    *,
    session: Session = Depends(get_session),
    payment_id: int
):
    """Get a specific payment"""
    payment = session.get(FeePayment, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


# ============================================================================
# Concession Endpoints
# ============================================================================

@router.post("/concessions", response_model=FeeConcessionResponse)
def apply_concession(
    *,
    session: Session = Depends(get_session),
    concession_data: FeeConcessionCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Apply a fee concession"""
    return FeeService.apply_concession(session, concession_data, current_user.id)


@router.get("/concessions", response_model=List[FeeConcessionResponse])
def list_concessions(
    *,
    session: Session = Depends(get_session),
    student_fee_id: Optional[int] = Query(None),
    skip: int = 0,
    limit: int = 100
):
    """List fee concessions"""
    stmt = select(FeeConcession)
    
    if student_fee_id:
        stmt = stmt.where(FeeConcession.student_fee_id == student_fee_id)
    
    stmt = stmt.offset(skip).limit(limit)
    return session.exec(stmt).all()


# ============================================================================
# Fine Management Endpoints
# ============================================================================

@router.post("/installments/{installment_id}/calculate-fine")
def calculate_fine(
    *,
    session: Session = Depends(get_session),
    installment_id: int,
    fine_per_day: float = 10.0,
    current_user: User = Depends(get_current_active_superuser)
):
    """Calculate fine for an overdue installment"""
    from decimal import Decimal
    fine_amount = FeeService.calculate_fine(session, installment_id, Decimal(str(fine_per_day)))
    return {
        "installment_id": installment_id,
        "fine_amount": float(fine_amount),
        "fine_per_day": fine_per_day
    }


@router.post("/installments/{installment_id}/waive-fine", response_model=StudentFeeInstallmentResponse)
def waive_fine(
    *,
    session: Session = Depends(get_session),
    installment_id: int,
    waiver_reason: str,
    current_user: User = Depends(get_current_active_superuser)
):
    """Waive fine for an installment"""
    return FeeService.waive_fine(session, installment_id, waiver_reason, current_user.id)


# ============================================================================
# Reports & Analytics Endpoints
# ============================================================================

@router.get("/reports/defaulters")
def get_fee_defaulters(
    *,
    session: Session = Depends(get_session),
    academic_year: Optional[str] = Query(None),
    min_due_amount: float = 0.0
):
    """Get list of fee defaulters"""
    stmt = select(StudentFee).where(
        StudentFee.total_pending > min_due_amount,
        StudentFee.is_blocked == False
    )
    
    if academic_year:
        stmt = stmt.where(StudentFee.academic_year == academic_year)
    
    defaulters = session.exec(stmt).all()
    
    return [
        {
            "student_id": sf.student_id,
            "student_fee_id": sf.id,
            "academic_year": sf.academic_year,
            "total_pending": float(sf.total_pending),
            "total_paid": float(sf.total_paid),
            "total_fee": float(sf.total_annual_fee)
        }
        for sf in defaulters
    ]


@router.get("/reports/collection-summary")
def get_collection_summary(
    *,
    session: Session = Depends(get_session),
    academic_year: str
):
    """Get fee collection summary for an academic year"""
    stmt = select(StudentFee).where(StudentFee.academic_year == academic_year)
    student_fees = session.exec(stmt).all()
    
    total_fee = sum(sf.total_annual_fee for sf in student_fees)
    total_collected = sum(sf.total_paid for sf in student_fees)
    total_pending = sum(sf.total_pending for sf in student_fees)
    total_concession = sum(sf.concession_amount for sf in student_fees)
    
    return {
        "academic_year": academic_year,
        "total_students": len(student_fees),
        "total_fee": float(total_fee),
        "total_collected": float(total_collected),
        "total_pending": float(total_pending),
        "total_concession": float(total_concession),
        "collection_percentage": float((total_collected / total_fee * 100) if total_fee > 0 else 0)
    }
