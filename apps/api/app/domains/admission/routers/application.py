from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request, BackgroundTasks
from sqlmodel import Session, select, func
from app.db.session import get_session
from app.api.deps import get_current_user
from app.models.user import User
from ..models import (
    Application, ApplicationStatus, ApplicationPayment, ApplicationPaymentStatus,
    ApplicationDocument, DocumentType, DocumentStatus, ApplicationActivityLog,
    ActivityType, FeeMode
)
from ..schemas import (
    ApplicationCreate, ApplicationUpdate, ApplicationRead,
    DocumentRead, DocumentUpload,
    QuickApplyCreate, QuickApplyResponse, ApplicationCompleteUpdate,
    ActivityLogRead
)
from app.services.activity_logger import log_activity
from ..service import AdmissionService
from app.services.storage_service import storage_service
from app.middleware.rate_limit import limiter
from typing import List, Optional
from datetime import datetime
import random
import string
from app.shared.enums import ApplicationStatus


router = APIRouter()

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
