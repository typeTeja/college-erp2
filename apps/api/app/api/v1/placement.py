"""
Placement & Training API Endpoints

Provides placement and training functionality
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from pydantic import BaseModel
from datetime import date

from app.api.deps import get_session, get_current_active_superuser
from app.models import User
from app.services.placement_service import PlacementService

router = APIRouter(prefix="/placement", tags=["Placement & Training"])


# Schemas
class CompanyCreate(BaseModel):
    company_name: str
    industry: Optional[str] = None
    website: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[str] = None


class PlacementDriveCreate(BaseModel):
    company_id: int
    drive_name: str
    drive_date: date
    registration_deadline: date
    min_cgpa: Optional[float] = None
    package_offered: Optional[float] = None
    job_role: Optional[str] = None


class StudentApplicationRequest(BaseModel):
    student_id: int
    placement_drive_id: int


class TrainingProgramCreate(BaseModel):
    program_name: str
    trainer_name: Optional[str] = None
    start_date: date
    end_date: date
    max_participants: Optional[int] = None
    registration_fee: float = 0.0


class InternshipCreate(BaseModel):
    student_id: int
    company_name: str
    start_date: date
    end_date: date
    internship_type: str
    stipend: Optional[float] = None


# ============================================================================
# Company Management Endpoints
# ============================================================================

@router.post("/companies")
def create_company(
    *,
    session: Session = Depends(get_session),
    company_data: CompanyCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Create company"""
    return {"message": "Company created", "data": company_data.model_dump()}


@router.get("/companies")
def list_companies(
    *,
    session: Session = Depends(get_session)
):
    """List companies"""
    return {"companies": []}


# ============================================================================
# Placement Drive Endpoints
# ============================================================================

@router.post("/drives")
def create_placement_drive(
    *,
    session: Session = Depends(get_session),
    drive_data: PlacementDriveCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Create placement drive"""
    return {"message": "Drive created", "data": drive_data.model_dump()}


@router.get("/drives")
def list_placement_drives(
    *,
    session: Session = Depends(get_session),
    active_only: bool = Query(True)
):
    """List placement drives"""
    return {"drives": []}


# ============================================================================
# Student Application Endpoints
# ============================================================================

@router.post("/applications")
def apply_for_placement(
    *,
    session: Session = Depends(get_session),
    application_data: StudentApplicationRequest
):
    """Apply for placement drive"""
    eligibility = PlacementService.check_eligibility(
        session,
        application_data.student_id,
        application_data.placement_drive_id
    )
    
    if not eligibility["eligible"]:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=eligibility["reasons"])
    
    return {"message": "Application submitted"}


@router.get("/applications/{student_id}")
def get_student_applications(
    *,
    session: Session = Depends(get_session),
    student_id: int
):
    """Get student applications"""
    return {"applications": []}


# ============================================================================
# Training Program Endpoints
# ============================================================================

@router.post("/training")
def create_training_program(
    *,
    session: Session = Depends(get_session),
    program_data: TrainingProgramCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Create training program"""
    return {"message": "Program created", "data": program_data.model_dump()}


@router.get("/training")
def list_training_programs(
    *,
    session: Session = Depends(get_session)
):
    """List training programs"""
    return {"programs": []}


# ============================================================================
# Internship Endpoints
# ============================================================================

@router.post("/internships")
def create_internship(
    *,
    session: Session = Depends(get_session),
    internship_data: InternshipCreate
):
    """Create internship record"""
    return {"message": "Internship created", "data": internship_data.model_dump()}


@router.get("/internships/{student_id}")
def get_student_internships(
    *,
    session: Session = Depends(get_session),
    student_id: int
):
    """Get student internships"""
    return {"internships": []}


# ============================================================================
# Statistics Endpoints
# ============================================================================

@router.get("/statistics/summary")
def get_placement_statistics(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Get placement statistics"""
    return PlacementService.get_placement_statistics(session)
