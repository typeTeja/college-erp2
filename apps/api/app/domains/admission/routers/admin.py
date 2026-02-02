from fastapi import APIRouter, Depends, HTTPException, status, Request, BackgroundTasks
from sqlmodel import Session, select
from app.db.session import get_session
from app.api.deps import get_current_active_superuser
from app.models import User
from ..models import (
    Application, ApplicationStatus, AdmissionSettings, ActivityType
)
from ..schemas import (
    ApplicationRead, AdmissionSettingsRead, AdmissionSettingsUpdate,
    OfflinePaymentVerify, OfflineApplicationCreate
)
from ..service import AdmissionService
from app.services.activity_logger import log_activity
from typing import List, Optional
from datetime import datetime
from app.shared.enums import ApplicationStatus


router = APIRouter()

@router.get("/applications", response_model=List[ApplicationRead])
async def list_applications(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser),
    status: Optional[ApplicationStatus] = None,
    show_deleted: bool = False
):
    statement = select(Application)
    if show_deleted:
        statement = statement.where(Application.is_deleted == True)
    else:
        statement = statement.where(Application.is_deleted == False)
        
    if status:
        statement = statement.where(Application.status == status)
    
    return session.exec(statement).all()

@router.get("/settings", response_model=AdmissionSettingsRead)
async def get_settings(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    return AdmissionService.get_admission_settings(session)

@router.put("/settings", response_model=AdmissionSettingsRead)
async def update_settings(
    data: AdmissionSettingsUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    settings_obj = AdmissionService.get_admission_settings(session)
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(settings_obj, key, value)
    settings_obj.updated_at = datetime.utcnow()
    session.add(settings_obj)
    session.commit()
    session.refresh(settings_obj)
    return settings_obj

@router.delete("/cleanup/test-data")
async def cleanup_test_data(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    count = AdmissionService.cleanup_test_applications(session, current_user.id)
    return {"message": "Cleanup completed", "deleted_count": count}

@router.post("/{id}/payment/offline-verify", response_model=ApplicationRead)
async def verify_offline_payment(
    id: int,
    data: OfflinePaymentVerify,
    request: Request,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Admin endpoint to verify offline payment"""
    application = session.get(Application, id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    application.offline_payment_verified = data.verified
    if data.verified:
        txnid = data.transaction_id or f"CASH-{id}-{datetime.now().strftime('%Y%m%d%H%M')}"
        AdmissionService.process_payment_completion(
            session=session, application_id=application.id,
            transaction_id=txnid, amount=application.application_fee,
            background_tasks=background_tasks
        )
    session.add(application)
    session.commit()
    session.refresh(application)
    return application

@router.post("/{id}/confirm", response_model=ApplicationRead)
async def confirm_admission(
    id: int,
    request: Request,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Admin confirms admission: Triggers Student and User account creation"""
    # Logic from audited router.py
    # ... Simplified for briefness in this implementation ...
    return AdmissionService.confirm_admission(session, id, current_user.id)
