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
    ApplicationRead, SelectionUpdate,
    StudentFeedbackSubmit, HotelFeedbackSubmit, FeedbackRead,
    BillingCreate, BillingRead, BillingMarkPaid,
    PayoutRead, PayoutBatchProcess, PayoutSummary
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

@router.get("/requests/{request_id}/applications", response_model=List[ApplicationRead])
def get_request_applications(
    request_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Get all applications for a specific ODC Request (Admin only)"""
    service = ODCService(session)
    return service.get_request_applications(request_id)

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

# --- Feedback ---

@router.post("/applications/{application_id}/student-feedback", response_model=ApplicationRead)
def submit_student_feedback(
    application_id: int,
    feedback_data: StudentFeedbackSubmit,
    session: Session = Depends(get_session),
    current_student: Student = Depends(get_current_active_student)
):
    """Submit student feedback for attended ODC event (Student only)"""
    service = ODCService(session)
    try:
        return service.submit_student_feedback(application_id, current_student.id, feedback_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/applications/{application_id}/hotel-feedback", response_model=ApplicationRead)
def submit_hotel_feedback(
    application_id: int,
    feedback_data: HotelFeedbackSubmit,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Submit hotel/admin feedback for student (Admin only)"""
    service = ODCService(session)
    try:
        return service.submit_hotel_feedback(application_id, feedback_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- Billing ---

@router.post("/billing", response_model=BillingRead)
def generate_billing(
    billing_data: BillingCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Generate billing/invoice for completed ODC event (Admin only)"""
    service = ODCService(session)
    try:
        return service.generate_billing(billing_data.request_id, current_user.id, billing_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/billing", response_model=List[BillingRead])
def list_billings(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """List all billings (Admin only)"""
    service = ODCService(session)
    return service.get_billings()

@router.put("/billing/{billing_id}/mark-paid", response_model=BillingRead)
def mark_billing_paid(
    billing_id: int,
    payment_data: BillingMarkPaid,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Mark billing as paid (Admin only)"""
    service = ODCService(session)
    try:
        return service.mark_billing_paid(billing_id, payment_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- Payouts ---

@router.get("/payouts/pending", response_model=List[ApplicationRead])
def get_pending_payouts(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Get all pending payouts (Admin only)"""
    service = ODCService(session)
    return service.get_pending_payouts()

@router.post("/payouts/process", response_model=List[PayoutRead])
def process_payouts(
    payout_data: PayoutBatchProcess,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Process batch payouts (Admin only)"""
    service = ODCService(session)
    try:
        return service.process_payouts(current_user.id, payout_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

