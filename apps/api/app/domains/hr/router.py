"""
HR Domain Router

All API endpoints for the HR domain including:
- Designation management
- Staff management
- Faculty management
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Optional

from app.api.deps import get_session, get_current_user
from app.domains.hr.services import HRService
from app.domains.hr.schemas import (
    DesignationCreate, DesignationUpdate, DesignationRead,
    StaffCreate, StaffUpdate, StaffRead,
    FacultyCreate, FacultyUpdate, FacultyRead
)
from app.models import User
from app.domains.hr.exceptions import (
    DesignationNotFoundError, StaffNotFoundError, FacultyNotFoundError,
    DuplicateEmailError, DuplicateMobileError
)


router = APIRouter()


# ----------------------------------------------------------------------
# Designation Endpoints
# ----------------------------------------------------------------------

@router.get("/designations", response_model=List[DesignationRead])
def list_designations(
    is_teaching: Optional[bool] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List all designations"""
    service = HRService(session)
    designations = service.list_designations(is_teaching=is_teaching)
    return designations


@router.post("/designations", response_model=DesignationRead, status_code=status.HTTP_201_CREATED)
def create_designation(
    designation_data: DesignationCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new designation"""
    service = HRService(session)
    designation = service.create_designation(designation_data)
    return designation


# ----------------------------------------------------------------------
# Staff Endpoints
# ----------------------------------------------------------------------

@router.get("/staff", response_model=List[StaffRead])
def list_staff(
    department: Optional[str] = None,
    is_active: Optional[bool] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List all staff"""
    service = HRService(session)
    staff = service.list_staff(department=department, is_active=is_active)
    return staff


@router.get("/staff/{staff_id}", response_model=StaffRead)
def get_staff(
    staff_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get staff by ID"""
    service = HRService(session)
    try:
        staff = service.get_staff(staff_id)
        return staff
    except StaffNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/staff", response_model=StaffRead, status_code=status.HTTP_201_CREATED)
def create_staff(
    staff_data: StaffCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new staff member"""
    service = HRService(session)
    try:
        staff = service.create_staff(staff_data)
        return staff
    except (DuplicateEmailError, DuplicateMobileError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/staff/{staff_id}", response_model=StaffRead)
def update_staff(
    staff_id: int,
    staff_data: StaffUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Update a staff member"""
    service = HRService(session)
    try:
        staff = service.update_staff(staff_id, staff_data)
        return staff
    except StaffNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ----------------------------------------------------------------------
# Faculty Endpoints
# ----------------------------------------------------------------------

@router.get("/faculty", response_model=List[FacultyRead])
def list_faculty(
    department: Optional[str] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List all faculty"""
    service = HRService(session)
    faculty = service.list_faculty(department=department)
    return faculty


@router.get("/faculty/{faculty_id}", response_model=FacultyRead)
def get_faculty(
    faculty_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get faculty by ID"""
    service = HRService(session)
    try:
        faculty = service.get_faculty(faculty_id)
        return faculty
    except FacultyNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/faculty", response_model=FacultyRead, status_code=status.HTTP_201_CREATED)
def create_faculty(
    faculty_data: FacultyCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new faculty member"""
    service = HRService(session)
    try:
        faculty = service.create_faculty(faculty_data)
        return faculty
    except DuplicateEmailError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/faculty/{faculty_id}", response_model=FacultyRead)
def update_faculty(
    faculty_id: int,
    faculty_data: FacultyUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Update a faculty member"""
    service = HRService(session)
    try:
        faculty = service.update_faculty(faculty_id, faculty_data)
        return faculty
    except FacultyNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
