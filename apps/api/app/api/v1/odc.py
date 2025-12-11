from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.db.session import get_session
from app.api.deps import get_current_user, get_current_active_superuser, get_current_active_student
from app.models.user import User
from app.models.student import Student
from app.models.odc import ODCHotel, ODCRequest, StudentODCApplication, ODCStatus
from app.schemas.odc import (
    ODCHotelCreate, ODCHotelRead,
    ODCRequestCreate, ODCRequestRead,
    ApplicationRead, SelectionUpdate
)
from app.services.odc_service import ODCService

router = APIRouter()

# --- Hotels ---

@router.post("/hotels", response_model=ODCHotelRead)
def create_hotel(
    hotel_data: ODCHotelCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Create a new ODC Hotel (Admin only)"""
    service = ODCService(session)
    return service.create_hotel(hotel_data)

@router.get("/hotels", response_model=List[ODCHotelRead])
def list_hotels(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List all ODC Hotels"""
    service = ODCService(session)
    return service.get_hotels(skip, limit)

# --- Requests ---

@router.post("/requests", response_model=ODCRequestRead)
def create_request(
    request_data: ODCRequestCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Create a new ODC Event Request (Admin only)"""
    service = ODCService(session)
    return service.create_request(request_data, current_user.id)

@router.get("/requests", response_model=List[ODCRequestRead])
def list_requests(
    status: ODCStatus = ODCStatus.OPEN,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List ODC Requests (Default: Open)"""
    service = ODCService(session)
    return service.get_requests(status)

# --- Applications ---

@router.post("/requests/{request_id}/apply", response_model=ApplicationRead)
def apply_for_odc(
    request_id: int,
    session: Session = Depends(get_session),
    current_student: Student = Depends(get_current_active_student)
):
    """Apply for an ODC Request (Student only)"""
    service = ODCService(session)
    try:
        return service.apply_for_odc(current_student.id, request_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/my-applications", response_model=List[ApplicationRead])
def get_my_applications(
    session: Session = Depends(get_session),
    current_student: Student = Depends(get_current_active_student)
):
    """Get current student's applications"""
    service = ODCService(session)
    return service.get_student_applications(current_student.id)

@router.post("/applications/select", response_model=List[ApplicationRead])
def select_students(
    selection_data: SelectionUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Bulk update application status (Select/Reject) (Admin only)"""
    service = ODCService(session)
    return service.update_selections(selection_data)
