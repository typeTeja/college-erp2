"""
University Exam API Endpoints

Provides comprehensive university exam management functionality
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from pydantic import BaseModel

from app.api.deps import get_session, get_current_active_superuser
from app.models.user import User
from app.models.academic.university_exam import (
    UniversityExam, UniversityExamRegistration, UniversityExamResult, SemesterResult
)
from app.services.university_exam_service import UniversityExamService

router = APIRouter(prefix="/exams/university", tags=["University Exams"])


# Schemas
class UniversityExamCreate(BaseModel):
    exam_name: str
    exam_code: str
    academic_year: str
    semester: int
    registration_start: str
    registration_end: str
    exam_start_date: str
    exam_end_date: str
    exam_fee: float
    late_fee: float = 0.0


class RegistrationRequest(BaseModel):
    student_id: int
    exam_id: int
    batch_semester_id: int
    subject_ids: List[int]
    force: bool = False


class ResultImportRequest(BaseModel):
    results: List[dict]


# ============================================================================
# Exam Management
# ============================================================================

@router.post("")
def create_university_exam(
    *,
    session: Session = Depends(get_session),
    exam_data: UniversityExamCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Create university exam"""
    exam = UniversityExam(**exam_data.model_dump(), created_by=current_user.id)
    session.add(exam)
    session.commit()
    session.refresh(exam)
    return exam


@router.get("")
def list_university_exams(
    *,
    session: Session = Depends(get_session),
    academic_year: Optional[str] = Query(None),
    semester: Optional[int] = Query(None),
    skip: int = 0,
    limit: int = 100
):
    """List university exams"""
    stmt = select(UniversityExam)
    if academic_year:
        stmt = stmt.where(UniversityExam.academic_year == academic_year)
    if semester:
        stmt = stmt.where(UniversityExam.semester == semester)
    stmt = stmt.offset(skip).limit(limit)
    return session.exec(stmt).all()


# ============================================================================
# Registration
# ============================================================================

@router.get("/eligibility/{student_id}/{exam_id}")
def check_eligibility(
    *,
    session: Session = Depends(get_session),
    student_id: int,
    exam_id: int
):
    """Check student eligibility"""
    return UniversityExamService.check_eligibility(session, student_id, exam_id)


@router.post("/register")
def register_for_exam(
    *,
    session: Session = Depends(get_session),
    request: RegistrationRequest
):
    """Register student for exam"""
    return UniversityExamService.register_student(
        session,
        request.student_id,
        request.exam_id,
        request.batch_semester_id,
        request.subject_ids,
        request.force
    )


@router.get("/registrations")
def list_registrations(
    *,
    session: Session = Depends(get_session),
    student_id: Optional[int] = Query(None),
    exam_id: Optional[int] = Query(None),
    skip: int = 0,
    limit: int = 100
):
    """List exam registrations"""
    stmt = select(UniversityExamRegistration)
    if student_id:
        stmt = stmt.where(UniversityExamRegistration.student_id == student_id)
    if exam_id:
        stmt = stmt.where(UniversityExamRegistration.university_exam_id == exam_id)
    stmt = stmt.offset(skip).limit(limit)
    return session.exec(stmt).all()


# ============================================================================
# Results
# ============================================================================

@router.post("/results/import")
def import_results(
    *,
    session: Session = Depends(get_session),
    request: ResultImportRequest,
    current_user: User = Depends(get_current_active_superuser)
):
    """Import exam results"""
    return UniversityExamService.import_results(
        session,
        request.results,
        current_user.id
    )


@router.get("/results/student/{student_id}")
def get_student_results(
    *,
    session: Session = Depends(get_session),
    student_id: int
):
    """Get student results"""
    stmt = select(UniversityExamResult).where(
        UniversityExamResult.student_id == student_id
    )
    return session.exec(stmt).all()


@router.post("/results/consolidate")
def consolidate_semester_result(
    *,
    session: Session = Depends(get_session),
    student_id: int,
    batch_semester_id: int,
    academic_year: str
):
    """Consolidate semester result"""
    return UniversityExamService.calculate_semester_result(
        session,
        student_id,
        batch_semester_id,
        academic_year
    )


@router.get("/semester-results/{student_id}")
def get_semester_results(
    *,
    session: Session = Depends(get_session),
    student_id: int
):
    """Get all semester results for student"""
    stmt = select(SemesterResult).where(SemesterResult.student_id == student_id)
    return session.exec(stmt).all()


@router.get("/transcripts/{student_id}")
def get_transcript(
    *,
    session: Session = Depends(get_session),
    student_id: int
):
    """Get complete transcript"""
    stmt = select(SemesterResult).where(
        SemesterResult.student_id == student_id
    ).order_by(SemesterResult.semester)
    
    results = session.exec(stmt).all()
    
    overall_cgpa = results[-1].cgpa if results else 0.0
    total_credits = sum(r.total_credits for r in results)
    credits_earned = sum(r.credits_earned for r in results)
    
    return {
        "student_id": student_id,
        "semester_results": results,
        "overall_cgpa": overall_cgpa,
        "total_credits": total_credits,
        "credits_earned": credits_earned,
        "percentage": results[-1].percentage if results else 0.0
    }
