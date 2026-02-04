from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, func
from typing import List, Optional
from datetime import datetime, date

from app.api.deps import get_session, get_current_user, get_current_active_superuser
from app.domains.auth.models import AuthUser as User
from app.domains.student.models import ODCHotel, ODCRequest, StudentODCApplication, ODCBilling, ODCPayout, Student
from .odc_schemas import (
    ODCHotelCreate, ODCHotelRead,
    ODCRequestCreate, ODCRequestRead,
    ODCApplicationRead, SelectionUpdate,
    StudentFeedbackSubmit, HotelFeedbackSubmit,
    ODCBillingCreate, ODCBillingRead, BillingMarkPaid,
    ODCPayoutRead, PayoutBatchProcess
)
from app.shared.enums import ODCStatus, PayoutStatus, BillingStatus

router = APIRouter()

# ----------------------------------------------------------------------
# Hotels
# ----------------------------------------------------------------------

@router.get("/hotels", response_model=List[ODCHotelRead])
def get_hotels(session: Session = Depends(get_session)):
    return session.exec(select(ODCHotel).where(ODCHotel.is_active == True)).all()

@router.post("/hotels", response_model=ODCHotelRead)
def create_hotel(data: ODCHotelCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_active_superuser)):
    hotel = ODCHotel(**data.model_dump())
    session.add(hotel)
    session.commit()
    session.refresh(hotel)
    return hotel

# ----------------------------------------------------------------------
# Requests
# ----------------------------------------------------------------------

@router.get("/requests", response_model=List[ODCRequestRead])
def get_requests(session: Session = Depends(get_session)):
    statement = select(ODCRequest).order_by(ODCRequest.event_date.desc())
    results = session.exec(statement).all()
    # Manual mapping for hotel_name if needed, though Relationship usually handles it
    return results

@router.post("/requests", response_model=ODCRequestRead)
def create_request(data: ODCRequestCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_active_superuser)):
    request = ODCRequest(**data.model_dump(), created_by_id=current_user.id)
    session.add(request)
    session.commit()
    session.refresh(request)
    return request

# ----------------------------------------------------------------------
# Applications
# ----------------------------------------------------------------------

@router.get("/my-applications", response_model=List[ODCApplicationRead])
def get_my_applications(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    # Find student record for user
    student = session.exec(select(Student).where(Student.user_id == current_user.id)).first()
    if not student:
        return []
    
    statement = select(StudentODCApplication).where(StudentODCApplication.student_id == student.id)
    apps = session.exec(statement).all()
    
    # Enrichment for read schema
    results = []
    for app in apps:
        base = app.model_dump()
        base["event_name"] = app.request.event_name
        base["event_date"] = app.request.event_date
        results.append(base)
    return results

@router.post("/requests/{request_id}/apply", response_model=ODCApplicationRead)
def apply_for_odc(request_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    student = session.exec(select(Student).where(Student.user_id == current_user.id)).first()
    if not student:
        raise HTTPException(status_code=400, detail="User is not a student")
    
    # Check if already applied
    existing = session.exec(select(StudentODCApplication).where(
        StudentODCApplication.request_id == request_id,
        StudentODCApplication.student_id == student.id
    )).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already applied for this ODC")
    
    # Check vacancies
    request = session.get(ODCRequest, request_id)
    if request.status != ODCStatus.OPEN:
         raise HTTPException(status_code=400, detail="ODC request is no longer open")

    application = StudentODCApplication(
        request_id=request_id,
        student_id=student.id,
        status=ODCStatus.OPEN
    )
    session.add(application)
    session.commit()
    session.refresh(application)
    
    # Return with enriched data
    base = application.model_dump()
    base["event_name"] = application.request.event_name
    base["event_date"] = application.request.event_date
    return base

@router.get("/requests/{request_id}/applications", response_model=List[ODCApplicationRead])
def get_request_applications(request_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_active_superuser)):
    statement = select(StudentODCApplication).where(StudentODCApplication.request_id == request_id)
    return session.exec(statement).all()

@router.post("/applications/select")
def select_students(data: SelectionUpdate, session: Session = Depends(get_session), current_user: User = Depends(get_current_active_superuser)):
    for app_id in data.application_ids:
        app = session.get(StudentODCApplication, app_id)
        if app:
            app.status = data.status
            if data.remarks:
                app.admin_remarks = data.remarks
            session.add(app)
    session.commit()
    return {"message": f"Updated {len(data.application_ids)} applications"}

# ----------------------------------------------------------------------
# Feedback
# ----------------------------------------------------------------------

@router.post("/applications/{app_id}/student-feedback")
def student_feedback(app_id: int, data: StudentFeedbackSubmit, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    app = session.get(StudentODCApplication, app_id)
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    app.student_feedback = data.student_feedback
    app.student_rating = data.student_rating
    session.add(app)
    session.commit()
    return {"message": "Feedback submitted"}

# ----------------------------------------------------------------------
# Billing
# ----------------------------------------------------------------------

@router.get("/billing", response_model=List[ODCBillingRead])
def get_billing(session: Session = Depends(get_session)):
    return session.exec(select(ODCBilling)).all()

@router.post("/billing", response_model=ODCBillingRead)
def create_billing(data: ODCBillingCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_active_superuser)):
    request = session.get(ODCRequest, data.request_id)
    
    # Calculate totals
    attended_count = session.exec(select(func.count(StudentODCApplication.id)).where(
        StudentODCApplication.request_id == data.request_id,
        StudentODCApplication.status == ODCStatus.COMPLETED # Or wherever attended is tracked
    )).one() or 0
    
    invoice_number = f"INV-ODC-{data.request_id}-{datetime.now().strftime('%Y%m%d')}"
    
    billing = ODCBilling(
        **data.model_dump(),
        invoice_number=invoice_number,
        total_students=attended_count,
        amount_per_student=request.pay_amount,
        total_amount=attended_count * request.pay_amount,
        created_by_id=current_user.id
    )
    session.add(billing)
    session.commit()
    session.refresh(billing)
    return billing

# ----------------------------------------------------------------------
# Payouts
# ----------------------------------------------------------------------

@router.get("/payouts/pending", response_model=List[ODCApplicationRead])
def get_pending_payouts(session: Session = Depends(get_session)):
    statement = select(StudentODCApplication).where(StudentODCApplication.payout_status == PayoutStatus.PENDING)
    return session.exec(statement).all()

@router.post("/payouts/process")
def process_payouts(data: PayoutBatchProcess, session: Session = Depends(get_session), current_user: User = Depends(get_current_active_superuser)):
    for app_id in data.application_ids:
        app = session.get(StudentODCApplication, app_id)
        if app and app.payout_status == PayoutStatus.PENDING:
            payout = ODCPayout(
                application_id=app_id,
                amount=app.payout_amount or app.request.pay_amount,
                payment_method=data.payment_method,
                payout_date=data.payout_date,
                processed_by_id=current_user.id,
                notes=data.notes
            )
            app.payout_status = PayoutStatus.PAID
            session.add(payout)
            session.add(app)
    session.commit()
    return {"message": "Payouts processed"}
