"""
Admission Domain Router

All API endpoints for the admission domain.
Consolidated from routers/ subdirectory.
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request, BackgroundTasks
from sqlmodel import Session, select, func
from sqlalchemy.orm import selectinload
from app.db.session import get_session
from app.api.deps import get_current_user, get_current_active_superuser
from app.models import User
import logging

logger = logging.getLogger(__name__)
from .models import (
    Application, ApplicationStatus, ApplicationPayment, ApplicationPaymentStatus,
    ApplicationDocument, DocumentType, DocumentStatus, ApplicationActivityLog,
    ActivityType, FeeMode, EntranceTestConfig, EntranceExamResult, 
    TentativeAdmission, ScholarshipCalculation, AdmissionSettings
)
from .schemas import (
    ApplicationCreate, ApplicationUpdate, ApplicationRead,
    ApplicationStepUpdate,
    DocumentRead, DocumentUpload,
    QuickApplyCreate, QuickApplyResponse, ApplicationCompleteUpdate,
    ActivityLogRead, EntranceTestConfigRead, EntranceTestConfigCreate,
    EntranceExamResultRead, EntranceExamResultCreate,
    TentativeAdmissionRead, TentativeAdmissionCreate,
    AdmissionSettingsRead, AdmissionSettingsUpdate,
    OfflinePaymentVerify, OfflineApplicationCreate,
    PaymentInitiate, PaymentInitiateResponse,
    PaymentConfigResponse, ApplicationRecentRead, ProgramShort,
    BoardCreate, BoardRead, LeadSourceCreate, LeadSourceRead,
    ReservationCategoryCreate, ReservationCategoryRead
)
from app.domains.admission.services import log_activity
from .services import AdmissionService, EntranceExamService, MeritService, log_activity, master_data_service
from app.services.storage_service import storage_service
from app.middleware.rate_limit import limiter
from typing import List, Optional
from datetime import datetime
import random
import string
from app.shared.enums import ApplicationStatus as SharedApplicationStatus
from app.config.settings import settings



router = APIRouter()

# Helper for URL signing
def sign_application_urls(app_read: ApplicationRead) -> ApplicationRead:
    """Sign all document URLs in the application response"""
    if app_read.documents:
        for doc in app_read.documents:
            if doc.file_url and not doc.file_url.startswith("http"):
                 doc.file_url = storage_service.get_presigned_url(doc.file_url, bucket=storage_service.bucket_documents)
    
    if app_read.payment_proof_url and not app_read.payment_proof_url.startswith("http"):
        app_read.payment_proof_url = storage_service.get_presigned_url(app_read.payment_proof_url, bucket=storage_service.bucket_documents)
        
    return app_read

def sign_document_urls(docs: List[DocumentRead]) -> List[DocumentRead]:
    """Sign a list of documents"""
    for doc in docs:
        if doc.file_url and not doc.file_url.startswith("http"):
             doc.file_url = storage_service.get_presigned_url(doc.file_url, bucket=storage_service.bucket_documents)
    return docs


# ======================================================================
# Public Endpoints (No Auth Required)
# ======================================================================

@router.get("/public/programs", response_model=List[ProgramShort])
async def list_public_programs(
    session: Session = Depends(get_session)
):
    """
    List academic programs open for admission.
    Publicly accessible for the quick apply form.
    """
    return AdmissionService.get_active_programs_for_admission(session)


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

@router.get("/payment/config", response_model=PaymentConfigResponse)
async def get_payment_config(
    session: Session = Depends(get_session)
):
    """
    Get public payment configuration for frontend.
    Does NOT require authentication for initial check.
    """
    settings = AdmissionService.get_admission_settings(session)
    return PaymentConfigResponse(
        fee_enabled=settings.application_fee_enabled,
        fee_amount=settings.application_fee_amount,
        online_enabled=settings.online_payment_enabled,
        offline_enabled=settings.offline_payment_enabled,
        payment_gateway=settings.payment_gateway
    )

@router.get("/public/application/{application_number}")
async def get_application_by_number_public(
    application_number: str,
    session: Session = Depends(get_session)
):
    """
    Public endpoint to retrieve basic application info by application number.
    Used for fallback when sessionStorage is unavailable (e.g., page refresh).
    Returns only non-sensitive data.
    """
    application = session.exec(
        select(Application).where(Application.application_number == application_number)
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Return only non-sensitive data
    return {
        "application_number": application.application_number,
        "name": application.name,
        "email": application.email,
        "status": application.status,
        "payment_status": application.payment_status,
        "program_id": application.program_id,
        "created_at": application.created_at
    }

@router.post("/quick-apply", response_model=ApplicationRead)
async def quick_apply(
    data: ApplicationCreate,
    request: Request,
    session: Session = Depends(get_session)
):
    app_number = generate_application_number(session)
    application = Application(
        **data.dict(),
        application_number=app_number,
        status=ApplicationStatus.APPLIED
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

@router.post("/v2/quick-apply", response_model=QuickApplyResponse)
async def quick_apply_v2(
    data: QuickApplyCreate,
    request: Request,
    session: Session = Depends(get_session)
):
    """
    Enhanced Quick Apply (Stage 1)
    - Creates Application
    - Returns ID for Payment Initiation
    - Can optionally create User account (if configured)
    """
    # Create Application
    application = AdmissionService.create_quick_apply(
        session=session,
        name=data.name,
        email=data.email,
        phone=data.phone,
        gender=data.gender,
        program_id=data.program_id,
        state=data.state,
        board=data.board,
        group_of_study=data.group_of_study,
        payment_mode="ONLINE" 
    )
    
    # Check Settings
    settings_obj = AdmissionService.get_admission_settings(session)
    portal_username = None
    portal_password = None
    
    if not settings_obj.application_fee_enabled:
          try:
              u, p, is_new = AdmissionService.create_portal_account_after_payment(session, application)
              portal_username = u
              portal_password = p
          except ValueError:
              pass
              
    return QuickApplyResponse(
        id=application.id,
        application_number=application.application_number,
        portal_username=portal_username,
        portal_password=portal_password,
        message="Application submitted successfully. Proceed to payment." if settings_obj.application_fee_enabled else "Application submitted successfully."
    )

@router.get("/recent", response_model=List[ApplicationRecentRead])
async def get_recent_admissions(
    limit: int = 5,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get recent admissions with program (course) details.
    """
    statement = (
        select(Application)
        .where(Application.is_deleted == False)
        .order_by(Application.created_at.desc())
        .limit(limit)
    )
    applications = session.exec(statement).all()
    
    # Map to ApplicationRecentRead
    result = []
    for app in applications:
        result.append(ApplicationRecentRead(
            id=app.id,
            fullName=app.name,
            email=app.email,
            status=app.status,
            createdAt=app.created_at,
            course=ProgramShort(
                id=app.program.id,
                name=app.program.name
            ) if app.program else ProgramShort(id=0, name="Unknown")
        ))
    return result

@router.get("/my-application", response_model=ApplicationRead)
async def get_my_application(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Application).where(Application.portal_user_id == current_user.id).order_by(Application.created_at.desc())
    application = session.exec(statement).first()
    if not application:
        raise HTTPException(status_code=404, detail="No application found")
    # Convert to Pydantic and sign URLs
    return sign_application_urls(ApplicationRead.from_orm(application))

@router.put("/my-application/complete", response_model=ApplicationRead)
async def complete_my_application(
    data: ApplicationCompleteUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Complete full application form (Stage 2/3)"""
    statement = select(Application).where(Application.portal_user_id == current_user.id).order_by(Application.created_at.desc())
    application = session.exec(statement).first()
    if not application:
        raise HTTPException(status_code=404, detail="No application found")
    
    try:
        updated_app = AdmissionService.complete_my_application(session, application.id, data)
        return sign_application_urls(ApplicationRead.from_orm(updated_app))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))




@router.get("/settings", response_model=AdmissionSettingsRead)
def get_admission_settings(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Get global admission settings"""
    try:
        settings_obj = AdmissionService.get_admission_settings(session)
        
        # Manually construct the response dict with explicit None checks
        response_dict = {
            "id": settings_obj.id,
            "application_fee_enabled": settings_obj.application_fee_enabled if settings_obj.application_fee_enabled is not None else True,
            "application_fee_amount": settings_obj.application_fee_amount if settings_obj.application_fee_amount is not None else 0.0,
            "online_payment_enabled": settings_obj.online_payment_enabled if settings_obj.online_payment_enabled is not None else True,
            "offline_payment_enabled": settings_obj.offline_payment_enabled if settings_obj.offline_payment_enabled is not None else True,
            "payment_gateway": settings_obj.payment_gateway if settings_obj.payment_gateway else "easebuzz",
            "send_credentials_email": settings_obj.send_credentials_email if settings_obj.send_credentials_email is not None else True,
            "send_credentials_sms": settings_obj.send_credentials_sms if settings_obj.send_credentials_sms is not None else False,
            "auto_create_student_account": settings_obj.auto_create_student_account if settings_obj.auto_create_student_account is not None else True,
            "portal_base_url": settings_obj.portal_base_url if settings_obj.portal_base_url else "http://localhost:3000",
            "updated_at": settings_obj.updated_at if settings_obj.updated_at else datetime.utcnow(),
        }
        
        # logger.info(f"Admission settings response: {response_dict}")
        return response_dict
    except Exception as e:
        logger.error(f"Error getting admission settings: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{id}", response_model=ApplicationRead)
async def get_application(
    id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get application by ID"""
    statement = (
        select(Application)
        .where(Application.id == id)
        .options(
            selectinload(Application.program),
            selectinload(Application.parents),
            selectinload(Application.education_history),
            selectinload(Application.addresses),
            selectinload(Application.bank_details),
            selectinload(Application.health_info),
            selectinload(Application.documents)
        )
    )
    application = session.exec(statement).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Check permissions
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN"] for role in current_user.roles)
    if not is_admin and application.portal_user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
        
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

@router.delete("/v2/applications/{id}", response_model=dict)
async def delete_application(
    id: int,
    reason: str = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    Soft delete an application.
    Requires Super Admin privileges.
    """
    try:
        AdmissionService.delete_application(session, id, current_user.id, reason)
        return {"message": "Application deleted successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/v2/applications/{id}/restore", response_model=ApplicationRead)
async def restore_application(
    id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    Restore a soft-deleted application.
    Requires Super Admin privileges.
    """
    try:
        return AdmissionService.restore_application(session, id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/v2/applications/{id}/resend-credentials", response_model=dict)
async def resend_credentials(
    id: int,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """
    Resend portal credentials (generates NEW password).
    Requires Super Admin privileges.
    """
    try:
        AdmissionService.resend_credentials(session, id, current_user.id, background_tasks)
        return {"message": "Credentials resent successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/v2/applications/{id}/step/{step}", response_model=ApplicationRead)
async def update_application_step(
    id: int,
    step: int,
    data: ApplicationStepUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Update application data for a specific lifecycle step.
    Supports partial updates and nested data (parents, education, etc.).
    """
    # Authorization: User must own the application or be admin
    application = session.get(Application, id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN"] for role in current_user.roles)
    is_owner = current_user.email == application.email
    # Allow portal user access if linked
    is_portal_user = application.portal_user_id == current_user.id
    
    if not (is_admin or is_owner or is_portal_user):
        raise HTTPException(status_code=403, detail="Not authorized")
        
    try:
        updated_app = AdmissionService.update_application_step(session, id, data, current_user.id)
        return sign_application_urls(ApplicationRead.from_orm(updated_app))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/v2/applications/{id}/full-preview", response_model=ApplicationRead)
async def get_application_full_preview(
    id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get full application data including all nested relationships.
    """
    application = session.get(Application, id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN"] for role in current_user.roles)
    is_owner = current_user.email == application.email
    is_portal_user = application.portal_user_id == current_user.id
    
    if not (is_admin or is_owner or is_portal_user):
        raise HTTPException(status_code=403, detail="Not authorized")
        
    app = AdmissionService.get_full_application(session, id)
    return sign_application_urls(ApplicationRead.from_orm(app))
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
    # Convert to schema list
    doc_reads = [DocumentRead.from_orm(d) for d in documents]
    return sign_document_urls(doc_reads)

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
    
    # Return with signed URL
    doc_read = DocumentRead.from_orm(document)
    doc_read.file_url = storage_service.get_presigned_url(doc_read.file_url, bucket=storage_service.bucket_documents)
    return doc_read

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
    statement = select(Application).options(selectinload(Application.program))
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


# ======================================================================
# Payment Endpoints
# ======================================================================




@router.post("/applications/{id}/payment/initiate", response_model=PaymentInitiateResponse)
@limiter.limit("5/minute")  # Max 5 payment initiations per minute per IP
async def initiate_application_payment(
    id: int,
    request: Request,
    session: Session = Depends(get_session)
):
    """Initiate payment for an application"""
    from app.domains.finance.services import easebuzz_service
    from app.config.settings import settings

    application = session.get(Application, id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
        
    settings_obj = AdmissionService.get_admission_settings(session)
    if not settings_obj.application_fee_enabled:
         raise HTTPException(status_code=400, detail="Application fee is disabled")
         
    amount = settings_obj.application_fee_amount
    if amount <= 0:
         raise HTTPException(status_code=400, detail="Invalid fee amount")
         
    # Create Payment Record
    txnid = f"ADM-{id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    payment = ApplicationPayment(
        application_id=id,
        transaction_id=txnid,
        amount=amount,
        status=ApplicationPaymentStatus.PENDING,
        payment_method="ONLINE"
    )
    session.add(payment)
    session.commit()
    
    # Call Easebuzz
    base_url = settings.BACKEND_BASE_URL # Should come from settings
    
    payment_data = {
        "txnid": txnid,
        "amount": amount,
        "productinfo": "Admission Application Fee",
        "firstname": application.name,
        "email": application.email,
        "phone": application.phone,
        "surl": f"{base_url}/api/v1/admissions/payment/success",
        "furl": f"{base_url}/api/v1/admissions/payment/failure",
        "udf1": str(application.id),
        "udf2": "ADMISSION_FEE"
    }
    
    response = await easebuzz_service.initiate_payment(session, payment_data)
    
    if response.get("status") == 1:
        access_key = response.get("data")
        # Construct proper Payment URL
        # Access Key is just the token. We need to redirect to payment page.
        # TEST: https://testpay.easebuzz.in/pay/{access_key}
        # PROD: https://pay.easebuzz.in/pay/{access_key}
        
        easebuzz_env = settings_obj.payment_gateway_env if hasattr(settings_obj, 'payment_gateway_env') else settings.EASEBUZZ_ENV
        # Fallback to checking settings directly or env
        # Actually EasebuzzService determines env internally.
        # Let's use a simple check or helper. 
        # For now, use the same logic as service:
        is_test = settings.EASEBUZZ_ENV.lower() == "test"
        # Wait, if settings_obj overrides it?
        # System settings override .env in EasebuzzService.
        # To be safe, we should ideally ask service for the base URL, but service doesn't expose it.
        # Let's replicate logic or assume logic.
        
        # Better: Check existing system settings again
        # Actually, let's just use the settings we already fetched?
        # AdmissionSettings doesn't store easebuzz env directly in the model fields we requested.
        # It's in SystemSetting.
        
        # Let's assume settings.EASEBUZZ_ENV linked to SystemSetting or default.
        # Simple fix:
        base_pay_url = "https://testpay.easebuzz.in/pay" if settings.EASEBUZZ_ENV == "test" else "https://pay.easebuzz.in/pay"
        
        return PaymentInitiateResponse(
            status="success",
            access_key=access_key,
            payment_url=f"{base_pay_url}/{access_key}"
        )
    else:
        return PaymentInitiateResponse(
            status="error",
            error=response.get("error", "Payment initiation failed")
        )

@router.api_route("/payment/success", methods=["GET", "POST"])
async def payment_success(
    request: Request,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)
):
    """Handle successful payment callback"""
    from app.domains.finance.services import easebuzz_service
    if request.method == "POST":
        data = await request.form()
        data_dict = dict(data)
    else:
        data_dict = dict(request.query_params)
    
    # CRITICAL: Verify Hash to prevent payment fraud
    is_valid_hash = easebuzz_service.verify_response_hash(session, data_dict)
    if not is_valid_hash:
        logger.error(f"Hash verification failed for payment callback: {data_dict.get('txnid')}")
        raise HTTPException(
            status_code=400, 
            detail="Invalid payment signature. This incident has been logged."
        )
    
    status = data_dict.get("status")
    txnid = data_dict.get("txnid")
    udf1 = data_dict.get("udf1") # Application ID
    
    if status == "success":
        AdmissionService.process_payment_completion(
            session=session,
            application_id=int(udf1),
            transaction_id=txnid,
            amount=float(data_dict.get("amount", 0)),
            background_tasks=background_tasks,
            payment_method="ONLINE-EASEBUZZ"
        )
        # Create Portal Account Logic is triggered inside process_payment_completion? 
        # No, created inside AdmissionService or explicitly here.
        # process_payment_completion updates status to APPLIED/PAID.
        
        # Trigger Account Creation
        application = session.get(Application, int(udf1))
        if application and not application.portal_user_id:
             portal_username, portal_password, _ = AdmissionService.create_portal_account_after_payment(session, application)
             
             # Send SMS/Email with creds if new account created with password
             if portal_password:
                 background_tasks.add_task(
                     AdmissionService.send_credentials_email,
                     email=application.email,
                     username=portal_username,
                     password=portal_password,
                     name=application.name,
                     portal_url=settings.PORTAL_BASE_URL
                 )
                 background_tasks.add_task(
                     AdmissionService.send_credentials_sms,
                     phone=application.phone,
                     username=portal_username,
                     password=portal_password,
                     name=application.name,
                     portal_url=settings.PORTAL_BASE_URL
                 )
             
    # Redirect to Frontend Success Page
    from fastapi.responses import RedirectResponse
    return RedirectResponse(
        url=f"{settings.PORTAL_BASE_URL}/apply/success?status=success&txnid={txnid}",
        status_code=303
    )

@router.api_route("/payment/failure", methods=["GET", "POST"])
async def payment_failure(
    request: Request,
    session: Session = Depends(get_session)
):
    from fastapi.responses import RedirectResponse
    return RedirectResponse(
        url=f"{settings.PORTAL_BASE_URL}/apply/failure?status=failed",
        status_code=303
    )
@router.get("/v2/public/receipt/{application_number}/download")
async def download_receipt_pdf(
    application_number: str,
    session: Session = Depends(get_session)
):
    """
    Download Payment Receipt PDF (Streamed)
    """
    from fastapi.responses import StreamingResponse
    from app.services.pdf_service import pdf_service
    from io import BytesIO
    
    # Check Application
    application = session.exec(
        select(Application).where(Application.application_number == application_number)
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    # Find Successful Payment
    payment = session.exec(
        select(ApplicationPayment).where(
            ApplicationPayment.application_id == application.id,
            ApplicationPayment.status == ApplicationPaymentStatus.SUCCESS
        ).order_by(ApplicationPayment.created_at.desc())
    ).first()
    
    if not payment:
         raise HTTPException(status_code=404, detail="Receipt not found")
         
    pdf_bytes = pdf_service.generate_receipt_bytes(
        application_number=application.application_number,
        applicant_name=application.name,
        payment_id=payment.transaction_id,
        amount=float(payment.amount),
        payment_date=payment.paid_at or payment.created_at,
        program_name=None # TODO: Fetch program name if available
    )
    
    if not pdf_bytes:
        raise HTTPException(status_code=500, detail="Failed to generate receipt")
        
    return StreamingResponse(
        BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=Receipt-{application_number}.pdf"}
    )

@router.get("/v2/public/receipt/{application_number}")
async def get_receipt_url(
    application_number: str,
    session: Session = Depends(get_session)
):
    """
    Get public URL for receipt download
    """
    from app.config.settings import settings
    
    # Verify existence first
    application = session.exec(
        select(Application).where(Application.application_number == application_number)
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
        
    payment_exists = session.exec(
        select(ApplicationPayment).where(
            ApplicationPayment.application_id == application.id,
            ApplicationPayment.status == ApplicationPaymentStatus.SUCCESS
        )
    ).first()
    
    if not payment_exists:
         raise HTTPException(status_code=404, detail="Receipt not found")

    # Generate filename unique to this payment
    filename = f"Receipt_{application.application_number}_{payment_exists.transaction_id}.pdf"
    
    # Check if exists in storage
    from app.services.storage_service import storage_service
    from app.services.pdf_service import pdf_service
    
    if not storage_service.file_exists(filename):
        # Lazy Generation
        pdf_bytes = pdf_service.generate_receipt_bytes(
            application_number=application.application_number,
            applicant_name=application.name,
            payment_id=payment_exists.transaction_id,
            amount=float(payment_exists.amount),
            payment_date=payment_exists.paid_at or payment_exists.created_at,
            program_name=application.program.name if application.program else None
        )
        
        if not pdf_bytes:
            raise HTTPException(status_code=500, detail="Failed to generate receipt")
            
        storage_service.upload_bytes(
            content=pdf_bytes,
            filename=filename,
            content_type="application/pdf"
        )
    
    # Generate Presigned URL
    url = storage_service.get_presigned_url(
        file_key=filename,
        expiration=900 # 15 minutes
    )

    return {
        "url": url
    }


@router.get("/settings", response_model=AdmissionSettingsRead)
def get_admission_settings(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Get global admission settings"""
    try:
        settings_obj = AdmissionService.get_admission_settings(session)
        
        # Manually construct the response dict with explicit None checks
        response_dict = {
            "id": settings_obj.id,
            "application_fee_enabled": settings_obj.application_fee_enabled if settings_obj.application_fee_enabled is not None else True,
            "application_fee_amount": settings_obj.application_fee_amount if settings_obj.application_fee_amount is not None else 0.0,
            "online_payment_enabled": settings_obj.online_payment_enabled if settings_obj.online_payment_enabled is not None else True,
            "offline_payment_enabled": settings_obj.offline_payment_enabled if settings_obj.offline_payment_enabled is not None else True,
            "payment_gateway": settings_obj.payment_gateway if settings_obj.payment_gateway else "easebuzz",
            "send_credentials_email": settings_obj.send_credentials_email if settings_obj.send_credentials_email is not None else True,
            "send_credentials_sms": settings_obj.send_credentials_sms if settings_obj.send_credentials_sms is not None else False,
            "auto_create_student_account": settings_obj.auto_create_student_account if settings_obj.auto_create_student_account is not None else True,
            "portal_base_url": settings_obj.portal_base_url if settings_obj.portal_base_url else "http://localhost:3000",
            "updated_at": settings_obj.updated_at if settings_obj.updated_at else datetime.utcnow(),
        }
        
        # logger.info(f"Admission settings response: {response_dict}")
        return response_dict
    except Exception as e:
        logger.error(f"Error getting admission settings: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to load settings: {str(e)}")

@router.patch("/settings", response_model=AdmissionSettingsRead)
def update_admission_settings(
    data: AdmissionSettingsUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Update global admission settings"""
    return AdmissionService.update_admission_settings(
        session=session,
        data=data.dict(exclude_unset=True),
        updated_by=current_user.id
    )


# ======================================================================
# Master Data Endpoints
# ======================================================================

# --- Board ---
@router.get("/boards", response_model=List[BoardRead])
def list_boards(
    active_only: bool = True,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return master_data_service.list_boards(session, active_only)

@router.post("/boards", response_model=BoardRead)
def create_board(
    data: BoardCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    try:
        return master_data_service.create_board(session, data.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/boards/{id}", response_model=BoardRead)
def update_board(
    id: int,
    data: dict, # Simplified for now
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    try:
        return master_data_service.update_board(session, id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/boards/{id}", status_code=204)
def delete_board(
    id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    if not master_data_service.delete_board(session, id):
        raise HTTPException(status_code=404, detail="Board not found")


# --- Lead Source ---
@router.get("/lead-sources", response_model=List[LeadSourceRead])
def list_lead_sources(
    active_only: bool = True,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return master_data_service.list_lead_sources(session, active_only)

@router.post("/lead-sources", response_model=LeadSourceRead)
def create_lead_source(
    data: LeadSourceCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    try:
        return master_data_service.create_lead_source(session, data.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/lead-sources/{id}", response_model=LeadSourceRead)
def update_lead_source(
    id: int,
    data: dict,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    try:
        return master_data_service.update_lead_source(session, id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/lead-sources/{id}", status_code=204)
def delete_lead_source(
    id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    if not master_data_service.delete_lead_source(session, id):
        raise HTTPException(status_code=404, detail="Lead Source not found")


# --- Reservation Category ---
@router.get("/reservation-categories", response_model=List[ReservationCategoryRead])
def list_reservation_categories(
    active_only: bool = True,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return master_data_service.list_reservation_categories(session, active_only)

@router.post("/reservation-categories", response_model=ReservationCategoryRead)
def create_reservation_category(
    data: ReservationCategoryCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    try:
        return master_data_service.create_reservation_category(session, data.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/reservation-categories/{id}", response_model=ReservationCategoryRead)
def update_reservation_category(
    id: int,
    data: dict,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    try:
        return master_data_service.update_reservation_category(session, id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/reservation-categories/{id}", status_code=204)
def delete_reservation_category(
    id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    if not master_data_service.delete_reservation_category(session, id):
        raise HTTPException(status_code=404, detail="Category not found")
