from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.api.deps import get_current_user, get_session, get_current_active_superuser, get_current_active_student
from app.models.user import User
from ..models.student import Student
from ..models.odc import ODCStatus
from ..schemas.odc import ODCHotelCreate, ODCRequestCreate, SelectionUpdate
from ..services.odc import odc_service
from app.shared.enums import ODCStatus


router = APIRouter()

@router.get("/hotels")
def list_hotels(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List all ODC Hotels"""
    return odc_service.get_hotels(session, skip, limit)

@router.post("/requests")
def create_request(
    request_data: ODCRequestCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Create a new ODC Event Request (Admin only)"""
    return odc_service.create_request(session, request_data.model_dump(), current_user.id)

@router.get("/requests")
def list_requests(
    status: ODCStatus = ODCStatus.OPEN,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List ODC Requests (Default: Open)"""
    return odc_service.get_requests(session, status)

@router.post("/requests/{request_id}/apply")
def apply_for_odc(
    request_id: int,
    session: Session = Depends(get_session),
    current_student: Student = Depends(get_current_active_student)
):
    """Apply for an ODC Request (Student only)"""
    try:
        return odc_service.apply_for_odc(session, current_student.id, request_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
