"""
Student Promotion API - With Correct Transaction Order

CRITICAL TRANSACTION ORDER:
1. Write StudentSemesterHistory (immutable record)
2. Write StudentPromotionLog (audit trail)
3. Update Student record (current state)
4. Commit (all or nothing)

This ensures audit trail exists even if transaction fails
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from datetime import datetime
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError

from app.api import deps
from app.models.user import User
from app.models.student import Student
from app.models.academic.student_history import (
    StudentSemesterHistory,
    StudentPromotionLog,
    StudentRegulationMigration,
    PromotionEligibility
)
from app.models.academic.batch import AcademicBatch
from app.models.academic.regulation import Regulation
from app.schemas.academic.student_history import (
    StudentSemesterHistoryCreate,
    StudentSemesterHistoryUpdate,
    StudentSemesterHistoryRead,
    StudentPromotionLogRead,
    PromotionEligibilityResponse,
    PromoteStudentRequest,
    PromoteStudentResponse,
    StudentRegulationMigrationCreate,
    StudentRegulationMigrationRead
)

router = APIRouter()


def check_admin(current_user: User):
    """Check if user has admin privileges"""
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"] for role in current_user.roles)
    if not is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return True


# ============================================================================
# Student Semester History Endpoints
# ============================================================================

@router.get("/students/{student_id}/history", response_model=List[StudentSemesterHistoryRead], tags=["Student History"])
def get_student_history(
    student_id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Get complete semester history for a student"""
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    stmt = select(StudentSemesterHistory).where(
        StudentSemesterHistory.student_id == student_id
    ).order_by(StudentSemesterHistory.semester_no)
    
    return session.exec(stmt).all()


@router.post("/students/{student_id}/history", response_model=StudentSemesterHistoryRead, tags=["Student History"])
def create_semester_history(
    student_id: int,
    data: StudentSemesterHistoryCreate,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Create semester history record (admin only)"""
    check_admin(current_user)
    
    # Verify student exists
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Verify student_id matches
    if data.student_id != student_id:
        raise HTTPException(status_code=400, detail="Student ID mismatch")
    
    # Check for duplicate
    existing = session.exec(
        select(StudentSemesterHistory)
        .where(StudentSemesterHistory.student_id == student_id)
        .where(StudentSemesterHistory.academic_year_id == data.academic_year_id)
        .where(StudentSemesterHistory.semester_no == data.semester_no)
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"History already exists for semester {data.semester_no}"
        )
    
    history = StudentSemesterHistory(**data.model_dump())
    session.add(history)
    session.commit()
    session.refresh(history)
    
    return history


# ============================================================================
# Promotion Endpoints
# ============================================================================

@router.get("/students/{student_id}/promotion-eligibility", response_model=PromotionEligibilityResponse, tags=["Promotion"])
def check_promotion_eligibility(
    student_id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Check if student is eligible for promotion to next year
    
    Based on regulation rules and earned credits
    """
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Get batch and regulation
    batch = session.get(AcademicBatch, student.batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    
    regulation = session.get(Regulation, batch.regulation_id)
    if not regulation:
        raise HTTPException(status_code=404, detail="Regulation not found")
    
    # Check eligibility
    eligibility = PromotionEligibility.check_year_promotion(
        student_id=student_id,
        current_year=student.current_year,
        regulation=regulation,
        session=session
    )
    
    return PromotionEligibilityResponse(**eligibility)


@router.post("/students/{student_id}/promote", response_model=PromoteStudentResponse, tags=["Promotion"])
def promote_student(
    student_id: int,
    request: PromoteStudentRequest,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Promote student to next year
    
    CRITICAL TRANSACTION ORDER:
    1. Write StudentSemesterHistory (immutable record)
    2. Write StudentPromotionLog (audit trail)
    3. Update Student record (current state)
    4. Commit (all or nothing)
    """
    check_admin(current_user)
    
    # Verify student_id matches
    if request.student_id != student_id:
        raise HTTPException(status_code=400, detail="Student ID mismatch")
    
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Get batch and regulation
    batch = session.get(AcademicBatch, student.batch_id)
    regulation = session.get(Regulation, batch.regulation_id)
    
    # Check eligibility
    eligibility = PromotionEligibility.check_year_promotion(
        student_id=student_id,
        current_year=student.current_year,
        regulation=regulation,
        session=session
    )
    
    if not eligibility["eligible"] and not request.force:
        raise HTTPException(
            status_code=400,
            detail=f"Student not eligible for promotion: {eligibility['message']}"
        )
    
    try:
        with session.begin_nested():  # Atomic transaction
            # Calculate new year/semester
            from_year = student.current_year
            to_year = student.current_year + 1
            from_semester = student.current_semester
            to_semester = (to_year - 1) * 2 + 1  # First semester of next year
            
            # 1️⃣ WRITE HISTORY FIRST (immutable record)
            history = StudentSemesterHistory(
                student_id=student.id,
                batch_id=student.batch_id,
                academic_year_id=student.academic_year_id,
                regulation_id=batch.regulation_id,
                program_year=from_year,
                semester_no=from_semester,
                total_credits=eligibility["year_total_credits"],
                earned_credits=eligibility["year_earned_credits"],
                failed_credits=eligibility["year_failed_credits"],
                status="PROMOTED"
            )
            session.add(history)
            session.flush()  # Ensure history is written
            
            # 2️⃣ WRITE LOG SECOND (audit trail)
            log = StudentPromotionLog(
                student_id=student.id,
                batch_id=student.batch_id,
                regulation_id=batch.regulation_id,
                from_year=from_year,
                to_year=to_year,
                from_semester=from_semester,
                to_semester=to_semester,
                status="PROMOTED",
                reason=eligibility["message"],
                year_total_credits=eligibility["year_total_credits"],
                year_earned_credits=eligibility["year_earned_credits"],
                year_failed_credits=eligibility["year_failed_credits"],
                year_percentage=eligibility["year_percentage"],
                decided_by=current_user.id
            )
            session.add(log)
            session.flush()  # Ensure log is written
            
            # 3️⃣ UPDATE STUDENT LAST (current state)
            student.current_year = to_year
            student.current_semester = to_semester
            session.add(student)
        
        # 4️⃣ COMMIT (all or nothing)
        session.commit()
        session.refresh(student)
        
        return PromoteStudentResponse(
            success=True,
            message=f"Student promoted from Year {from_year} to Year {to_year}",
            from_year=from_year,
            to_year=to_year,
            from_semester=from_semester,
            to_semester=to_semester,
            year_percentage=eligibility["year_percentage"]
        )
        
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Promotion failed: {str(e)}"
        )


@router.post("/students/{student_id}/detain", response_model=PromoteStudentResponse, tags=["Promotion"])
def detain_student(
    student_id: int,
    reason: str = Query(..., description="Reason for detention"),
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Detain student (keep in same year)
    
    Same transaction order as promotion
    """
    check_admin(current_user)
    
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    batch = session.get(AcademicBatch, student.batch_id)
    regulation = session.get(Regulation, batch.regulation_id)
    
    # Get year summary
    eligibility = PromotionEligibility.check_year_promotion(
        student_id=student_id,
        current_year=student.current_year,
        regulation=regulation,
        session=session
    )
    
    try:
        with session.begin_nested():
            # 1️⃣ WRITE HISTORY FIRST
            history = StudentSemesterHistory(
                student_id=student.id,
                batch_id=student.batch_id,
                academic_year_id=student.academic_year_id,
                regulation_id=batch.regulation_id,
                program_year=student.current_year,
                semester_no=student.current_semester,
                total_credits=eligibility["year_total_credits"],
                earned_credits=eligibility["year_earned_credits"],
                failed_credits=eligibility["year_failed_credits"],
                status="DETAINED"
            )
            session.add(history)
            session.flush()
            
            # 2️⃣ WRITE LOG SECOND
            log = StudentPromotionLog(
                student_id=student.id,
                batch_id=student.batch_id,
                regulation_id=batch.regulation_id,
                from_year=student.current_year,
                to_year=student.current_year,  # Same year
                from_semester=student.current_semester,
                to_semester=student.current_semester,  # Same semester
                status="DETAINED",
                reason=reason,
                year_total_credits=eligibility["year_total_credits"],
                year_earned_credits=eligibility["year_earned_credits"],
                year_failed_credits=eligibility["year_failed_credits"],
                year_percentage=eligibility["year_percentage"],
                decided_by=current_user.id
            )
            session.add(log)
            session.flush()
            
            # 3️⃣ Student stays in same year (no update needed)
        
        session.commit()
        
        return PromoteStudentResponse(
            success=True,
            message=f"Student detained in Year {student.current_year}. Reason: {reason}",
            from_year=student.current_year,
            to_year=student.current_year,
            from_semester=student.current_semester,
            to_semester=student.current_semester,
            year_percentage=eligibility["year_percentage"]
        )
        
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Detention failed: {str(e)}"
        )


# ============================================================================
# Promotion Logs Endpoints
# ============================================================================

@router.get("/students/{student_id}/promotion-logs", response_model=List[StudentPromotionLogRead], tags=["Promotion"])
def get_promotion_logs(
    student_id: int,
    session: Session = Depends(deps.get_session),
    current_user: User = Depends(deps.get_current_user)
):
    """Get all promotion/detention logs for a student"""
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    stmt = select(StudentPromotionLog).where(
        StudentPromotionLog.student_id == student_id
    ).order_by(StudentPromotionLog.decided_at.desc())
    
    return session.exec(stmt).all()
