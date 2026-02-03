"""
Academic Domain Router

API endpoints for the academic domain.
Note: This is a simplified version. Full endpoints can be added as needed.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Optional

from app.api.deps import get_session, get_current_user
from app.domains.academic.services import AcademicService
from app.domains.academic.schemas import (
    AcademicYearCreate, AcademicYearRead,
    BatchCreate, BatchRead,
    RegulationCreate, RegulationRead,
    SectionCreate, SectionRead
)
from app.domains.auth.models import AuthUser as User
from app.domains.academic.exceptions import (
    AcademicYearNotFoundError, BatchNotFoundError,
    RegulationNotFoundError, SectionNotFoundError
)


router = APIRouter()


# ----------------------------------------------------------------------
# Academic Year Endpoints
# ----------------------------------------------------------------------

@router.get("/academic-years", response_model=List[AcademicYearRead])
def list_academic_years(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List all academic years"""
    service = AcademicService(session)
    years = service.list_academic_years()
    return years


@router.post("/academic-years", response_model=AcademicYearRead, status_code=status.HTTP_201_CREATED)
def create_academic_year(
    year_data: AcademicYearCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new academic year"""
    service = AcademicService(session)
    year = service.create_academic_year(year_data)
    return year


# ----------------------------------------------------------------------
# Batch Endpoints
# ----------------------------------------------------------------------

@router.get("/batches", response_model=List[BatchRead])
def list_batches(
    program_id: Optional[int] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List all batches"""
    service = AcademicService(session)
    batches = service.list_batches(program_id=program_id)
    return batches


@router.get("/batches/{batch_id}", response_model=BatchRead)
def get_batch(
    batch_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get batch by ID"""
    service = AcademicService(session)
    try:
        batch = service.get_batch(batch_id)
        return batch
    except BatchNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ----------------------------------------------------------------------
# Regulation Endpoints
# ----------------------------------------------------------------------

@router.get("/regulations", response_model=List[RegulationRead])
def list_regulations(
    program_id: Optional[int] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List all regulations"""
    service = AcademicService(session)
    regulations = service.list_regulations(program_id=program_id)
    return regulations


# ----------------------------------------------------------------------
# Section Endpoints
# ----------------------------------------------------------------------

@router.get("/sections", response_model=List[SectionRead])
def list_sections(
    batch_id: Optional[int] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List all sections"""
    service = AcademicService(session)
    sections = service.list_sections(batch_id=batch_id)
    return sections
