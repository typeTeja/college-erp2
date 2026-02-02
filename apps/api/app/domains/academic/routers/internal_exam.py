"""
Internal Exam API Endpoints

Provides comprehensive internal exam management functionality
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.api.deps import get_session, get_current_active_superuser
from app.models.user import User
from app.domains.academic.models import (
    InternalExam, InternalExamSubject, StudentInternalMarks,
    InternalMarksConsolidated
)
from app.schemas.academic.internal_exam import (
    InternalExamCreate, InternalExamResponse,
    InternalExamSubjectCreate, InternalExamSubjectResponse,
    BulkSubjectCreate, BulkMarksEntry, MarksVerification,
    StudentInternalMarksResponse, InternalMarksConsolidatedResponse,
    ExamStatistics
)
from app.domains.academic.services.internal_exam_service import InternalExamService

router = APIRouter(prefix="/exams/internal", tags=["Internal Exams"])


# ============================================================================
# Exam Management Endpoints
# ============================================================================

@router.post("", response_model=InternalExamResponse)
def create_internal_exam(
    *,
    session: Session = Depends(get_session),
    exam_data: InternalExamCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Create a new internal exam"""
    return InternalExamService.create_exam(
        session,
        exam_data.model_dump(),
        current_user.id
    )


@router.get("", response_model=List[InternalExamResponse])
def list_internal_exams(
    *,
    session: Session = Depends(get_session),
    batch_id: Optional[int] = Query(None),
    academic_year: Optional[str] = Query(None),
    exam_type: Optional[str] = Query(None),
    is_published: Optional[bool] = Query(None),
    skip: int = 0,
    limit: int = 100
):
    """List internal exams with filters"""
    stmt = select(InternalExam)
    
    if batch_id:
        stmt = stmt.where(InternalExam.batch_id == batch_id)
    if academic_year:
        stmt = stmt.where(InternalExam.academic_year == academic_year)
    if exam_type:
        stmt = stmt.where(InternalExam.exam_type == exam_type)
    if is_published is not None:
        stmt = stmt.where(InternalExam.is_published == is_published)
    
    stmt = stmt.offset(skip).limit(limit).order_by(InternalExam.created_at.desc())
    return session.exec(stmt).all()


@router.get("/{exam_id}", response_model=InternalExamResponse)
def get_internal_exam(
    *,
    session: Session = Depends(get_session),
    exam_id: int
):
    """Get a specific internal exam"""
    exam = session.get(InternalExam, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam


@router.delete("/{exam_id}")
def delete_internal_exam(
    *,
    session: Session = Depends(get_session),
    exam_id: int,
    current_user: User = Depends(get_current_active_superuser)
):
    """Delete an internal exam"""
    exam = session.get(InternalExam, exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    if exam.is_published:
        raise HTTPException(status_code=400, detail="Cannot delete published exam")
    
    session.delete(exam)
    session.commit()
    return {"message": "Exam deleted successfully"}


# ============================================================================
# Subject Management Endpoints
# ============================================================================

@router.post("/{exam_id}/subjects", response_model=List[InternalExamSubjectResponse])
def add_subjects_to_exam(
    *,
    session: Session = Depends(get_session),
    exam_id: int,
    subjects_data: BulkSubjectCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Add subjects to an internal exam"""
    subjects = InternalExamService.add_subjects_to_exam(
        session,
        exam_id,
        [s.model_dump() for s in subjects_data.subjects]
    )
    return subjects


@router.get("/{exam_id}/subjects", response_model=List[InternalExamSubjectResponse])
def get_exam_subjects(
    *,
    session: Session = Depends(get_session),
    exam_id: int
):
    """Get all subjects for an exam"""
    stmt = select(InternalExamSubject).where(
        InternalExamSubject.internal_exam_id == exam_id
    )
    return session.exec(stmt).all()


# ============================================================================
# Marks Entry Endpoints
# ============================================================================

@router.post("/marks/entry", response_model=List[StudentInternalMarksResponse])
def enter_marks(
    *,
    session: Session = Depends(get_session),
    marks_data: BulkMarksEntry,
    current_user: User = Depends(get_current_active_superuser)
):
    """Bulk marks entry"""
    marks = InternalExamService.enter_marks(
        session,
        [m.model_dump() for m in marks_data.marks],
        current_user.id
    )
    return marks


@router.get("/marks/subject/{exam_subject_id}", response_model=List[StudentInternalMarksResponse])
def get_marks_by_subject(
    *,
    session: Session = Depends(get_session),
    exam_subject_id: int
):
    """Get all marks for a specific exam subject"""
    stmt = select(StudentInternalMarks).where(
        StudentInternalMarks.internal_exam_subject_id == exam_subject_id
    )
    return session.exec(stmt).all()


@router.post("/marks/verify", response_model=List[StudentInternalMarksResponse])
def verify_marks(
    *,
    session: Session = Depends(get_session),
    verification_data: MarksVerification,
    current_user: User = Depends(get_current_active_superuser)
):
    """Verify entered marks"""
    marks = InternalExamService.verify_marks(
        session,
        verification_data.marks_ids,
        current_user.id
    )
    return marks


# ============================================================================
# Results & Publishing Endpoints
# ============================================================================

@router.post("/{exam_id}/publish", response_model=InternalExamResponse)
def publish_results(
    *,
    session: Session = Depends(get_session),
    exam_id: int,
    current_user: User = Depends(get_current_active_superuser)
):
    """Publish exam results and consolidate marks"""
    return InternalExamService.publish_results(
        session,
        exam_id,
        current_user.id
    )


@router.get("/results/student/{student_id}", response_model=List[InternalMarksConsolidatedResponse])
def get_student_results(
    *,
    session: Session = Depends(get_session),
    student_id: int,
    academic_year: Optional[str] = Query(None)
):
    """Get consolidated results for a student"""
    return InternalExamService.get_student_results(
        session,
        student_id,
        academic_year
    )


@router.post("/results/consolidate")
def consolidate_marks(
    *,
    session: Session = Depends(get_session),
    student_id: int,
    batch_semester_id: int,
    academic_year: str,
    current_user: User = Depends(get_current_active_superuser)
):
    """Manually consolidate marks for a student"""
    result = InternalExamService.consolidate_marks(
        session,
        student_id,
        batch_semester_id,
        academic_year
    )
    return result


@router.get("/results/semester/{semester_id}", response_model=List[InternalMarksConsolidatedResponse])
def get_semester_results(
    *,
    session: Session = Depends(get_session),
    semester_id: int,
    academic_year: str
):
    """Get all results for a semester"""
    stmt = select(InternalMarksConsolidated).where(
        InternalMarksConsolidated.batch_semester_id == semester_id,
        InternalMarksConsolidated.academic_year == academic_year
    ).order_by(InternalMarksConsolidated.rank)
    
    return session.exec(stmt).all()


# ============================================================================
# Statistics Endpoints
# ============================================================================

@router.get("/{exam_id}/statistics", response_model=ExamStatistics)
def get_exam_statistics(
    *,
    session: Session = Depends(get_session),
    exam_id: int
):
    """Get statistics for an exam"""
    return InternalExamService.get_exam_statistics(session, exam_id)


@router.get("/analytics/performance")
def get_performance_analytics(
    *,
    session: Session = Depends(get_session),
    batch_id: int,
    academic_year: str
):
    """Get performance analytics for a batch"""
    # Get all exams for the batch
    stmt = select(InternalExam).where(
        InternalExam.batch_id == batch_id,
        InternalExam.academic_year == academic_year,
        InternalExam.is_published == True
    )
    exams = session.exec(stmt).all()
    
    analytics = []
    for exam in exams:
        stats = InternalExamService.get_exam_statistics(session, exam.id)
        analytics.append(stats)
    
    return {
        "batch_id": batch_id,
        "academic_year": academic_year,
        "total_exams": len(exams),
        "exams": analytics
    }
