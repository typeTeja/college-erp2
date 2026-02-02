"""
Student Domain Router

API endpoints for the student domain.
Note: This is a simplified version. Full endpoints can be added as needed.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Optional

from app.api.deps import get_session, get_current_user
from app.domains.student.services import StudentService
from app.domains.student.schemas import (
    StudentCreate, StudentRead,
    ParentCreate, ParentRead,
    EnrollmentCreate, EnrollmentRead
)
from app.domains.system.models import User
from app.domains.student.exceptions import (
    StudentNotFoundError, ParentNotFoundError, EnrollmentNotFoundError
)


router = APIRouter()


# ----------------------------------------------------------------------
# Student Endpoints
# ----------------------------------------------------------------------

@router.get("/students", response_model=List[StudentRead])
def list_students(
    batch_id: Optional[int] = None,
    status: Optional[str] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List all students"""
    service = StudentService(session)
    students = service.list_students(batch_id=batch_id, status=status)
    return students


@router.get("/students/{student_id}", response_model=StudentRead)
def get_student(
    student_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get student by ID"""
    service = StudentService(session)
    try:
        student = service.get_student(student_id)
        return student
    except StudentNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/students", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(
    student_data: StudentCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new student"""
    service = StudentService(session)
    student = service.create_student(student_data)
    return student


# ----------------------------------------------------------------------
# Parent Endpoints
# ----------------------------------------------------------------------

@router.get("/students/{student_id}/parents", response_model=List[ParentRead])
def list_parents(
    student_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List all parents for a student"""
    service = StudentService(session)
    parents = service.list_parents(student_id=student_id)
    return parents


# ----------------------------------------------------------------------
# Enrollment Endpoints
# ----------------------------------------------------------------------

@router.get("/enrollments", response_model=List[EnrollmentRead])
def list_enrollments(
    student_id: Optional[int] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List all enrollments"""
    service = StudentService(session)
    enrollments = service.list_enrollments(student_id=student_id)
    return enrollments
