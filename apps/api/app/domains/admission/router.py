"""
Admission Domain Router

All API endpoints for the admission domain.
Consolidated from routers/ subdirectory.
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request, BackgroundTasks
from sqlmodel import Session, select, func
from app.db.session import get_session
from app.api.deps import get_current_user, get_current_active_superuser
from app.models import User
from .models import (
    Application, ApplicationStatus, ApplicationPayment, ApplicationPaymentStatus,
    ApplicationDocument, DocumentType, DocumentStatus, ApplicationActivityLog,
    ActivityType, FeeMode, EntranceTestConfig, EntranceExamResult, 
    TentativeAdmission, ScholarshipCalculation, AdmissionSettings
)
from .schemas import (
    ApplicationCreate, ApplicationUpdate, ApplicationRead,
    DocumentRead, DocumentUpload,
    QuickApplyCreate, QuickApplyResponse, ApplicationCompleteUpdate,
    ActivityLogRead, EntranceTestConfigRead, EntranceTestConfigCreate,
    EntranceExamResultRead, EntranceExamResultCreate,
    TentativeAdmissionRead, TentativeAdmissionCreate,
    AdmissionSettingsRead, AdmissionSettingsUpdate,
    OfflinePaymentVerify, OfflineApplicationCreate
)
from app.services.activity_logger import log_activity
from .services import AdmissionService, EntranceExamService, MeritService
from app.services.storage_service import storage_service
from app.middleware.rate_limit import limiter
from typing import List, Optional
from datetime import datetime
import random
import string
from app.shared.enums import ApplicationStatus as SharedApplicationStatus


router = APIRouter()


# ======================================================================
# Utility Functions
# ======================================================================

def generate_application_number(session: Session) -> str:
    year = datetime.now().year
    prefix = f"APP-{year}-"
    random_str = ''.join(random.choices(string.digits, k=4))
    return f"{prefix}{random_str}"

def get_client_ip(request: Request) -> str:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0]
    return request.client.host if request.client else "unknown"


# ======================================================================
# Application Endpoints
# ======================================================================

@router.post("/quick-apply", response_model=ApplicationRead)
@limiter.limit("5/minute")
async def quick_apply(
    data: ApplicationCreate,
    request: Request,
    session: Session = Depends(get_session)
):
    app_number = generate_application_number(session)
    application = Application(
        **data.dict(),
        application_number=app_number,
        status=ApplicationStatus.PENDING_PAYMENT
    )
    session.add(application)
    session.flush()
    log_activity(
        session=session,
        application_id=application.id,
        activity_type=ActivityType.APPLICATION_CREATED,
        description=f"Application created via quick apply form",
        ip_address=get_client_ip(request),
        extra_data={"fee_mode": data.fee_mode.value}
    )
    session.commit()
    session.refresh(application)
    return application

@router.get("/my-application", response_model=ApplicationRead)
async def get_my_application(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Application).where(Application.portal_user_id == current_user.id).order_by(Application.created_at.desc())
    application = session.exec(statement).first()
    if not application:
        raise HTTPException(status_code=404, detail="No application found")
    return application

@router.put("/{id}", response_model=ApplicationRead)
async def update_application(
    id: int,
    data: ApplicationUpdate,
    request: Request,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    application = session.get(Application, id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN"] for role in current_user.roles)
    is_owner = current_user.email == application.email
    if not (is_admin or is_owner):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(application, key, value)
    
    application.updated_at = datetime.utcnow()
    session.add(application)
    session.commit()
    session.refresh(application)
    return application

@router.get("/{id}/documents", response_model=List[DocumentRead])
async def list_documents(
    id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get all documents for an application with download URLs"""
    application = session.get(Application, id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN"] for role in current_user.roles)
    is_owner = current_user.email == application.email
    if not (is_admin or is_owner):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    statement = select(ApplicationDocument).where(ApplicationDocument.application_id == id)
    documents = session.exec(statement).all()
    return documents

@router.post("/{id}/documents/upload", response_model=DocumentRead)
async def upload_document(
    id: int,
    document_type: DocumentType,
    file: UploadFile = File(...),
    request: Request = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Upload a document for an application"""
    application = session.get(Application, id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN"] for role in current_user.roles)
    is_owner = current_user.email == application.email
    if not (is_admin or is_owner):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Implementation simplified, using storage_service
    prefix = f"admissions/application/{id}"
    file_key, file_size, mime_type = await storage_service.upload_file(
        file=file, prefix=prefix, bucket=storage_service.bucket_documents
    )
    
    document = ApplicationDocument(
        application_id=id, document_type=document_type,
        file_url=file_key, file_name=file.filename,
        file_size=file_size, status=DocumentStatus.UPLOADED
    )
    session.add(document)
    session.commit()
    session.refresh(document)
    return document

@router.get("/{id}/timeline", response_model=List[ActivityLogRead])
async def get_timeline(
    id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get activity timeline for an application"""
    application = session.get(Application, id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN"] for role in current_user.roles)
    is_owner = current_user.email == application.email
    if not (is_admin or is_owner):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    statement = select(ApplicationActivityLog).where(
        ApplicationActivityLog.application_id == id
    ).order_by(ApplicationActivityLog.created_at.desc())
    return session.exec(statement).all()


# ======================================================================
# Enhanced Admission Endpoints
# ======================================================================

# Entrance Test Configuration
@router.post("/enhanced/test-config", response_model=EntranceTestConfigRead)
async def create_test_config(
    data: EntranceTestConfigCreate,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_active_superuser)
):
    return EntranceExamService.create_test_config(session, data.dict())

@router.get("/enhanced/test-config", response_model=list[EntranceTestConfigRead])
async def list_test_configs(
    session: Session = Depends(get_session)
):
    return EntranceExamService.list_test_configs(session)

# Scholarship & Merit
@router.post("/enhanced/calculate-merit/{application_id}", response_model=dict)
async def calculate_merit(
    application_id: int,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_active_superuser)
):
    calc = MeritService.calculate_scholarship(session, application_id, current_user.id)
    return {"message": "Merit calculated", "calculation_id": calc.id}


# ======================================================================
# Admin Endpoints
# ======================================================================

@router.get("/admin/applications", response_model=List[ApplicationRead])
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

@router.get("/admin/settings", response_model=AdmissionSettingsRead)
async def get_settings(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    return AdmissionService.get_admission_settings(session)

@router.put("/admin/settings", response_model=AdmissionSettingsRead)
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

@router.delete("/admin/cleanup/test-data")
async def cleanup_test_data(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    count = AdmissionService.cleanup_test_applications(session, current_user.id)
    return {"message": "Cleanup completed", "deleted_count": count}

@router.post("/admin/{id}/payment/offline-verify", response_model=ApplicationRead)
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

@router.post("/admin/{id}/confirm", response_model=ApplicationRead)
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
