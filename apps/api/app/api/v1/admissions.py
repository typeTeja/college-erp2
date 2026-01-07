from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Request
from sqlmodel import Session, select, func
from app.db.session import get_session
from app.api.deps import get_current_user, get_current_active_superuser
from app.models.user import User
from app.models.role import Role
from app.models.student import Student, StudentStatus
from app.models.admissions import (
    Application, ApplicationStatus, ApplicationPayment, ApplicationPaymentStatus,
    ApplicationDocument, DocumentType, DocumentStatus, ApplicationActivityLog,
    ActivityType, FeeMode
)
from app.models.academic.batch import AcademicBatch, ProgramYear, BatchSemester
from app.schemas.admissions import (
    ApplicationCreate, ApplicationUpdate, ApplicationRead,
    DocumentRead, DocumentUpload, DocumentVerify,
    ActivityLogRead, OfflinePaymentVerify
)
from app.services.activity_logger import log_activity
from app.services.admission_status import can_transition
from app.services.email_service import email_service
from app.middleware.rate_limit import limiter
from typing import List, Optional
from datetime import datetime
import random
import string
import os

router = APIRouter()

def generate_application_number(session: Session) -> str:
    """Generate a unique application number like APP-2025-XXXX"""
    year = datetime.now().year
    prefix = f"APP-{year}-"
    # Simple strategy: find max existing and increment
    # For now, just using a random string for simplicity and uniqueness
    random_str = ''.join(random.choices(string.digits, k=4))
    return f"{prefix}{random_str}"

def get_client_ip(request: Request) -> str:
    """Extract client IP address from request"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0]
    return request.client.host if request.client else "unknown"

@router.post("/quick-apply", response_model=ApplicationRead)
@limiter.limit("5/minute")  # Rate limit: 5 requests per minute per IP
async def quick_apply(
    data: ApplicationCreate,
    request: Request,
    session: Session = Depends(get_session)
):
    """Public endpoint for high-conversion lead capture (Stage 1)"""
    app_number = generate_application_number(session)
    
    application = Application(
        **data.dict(),
        application_number=app_number,
        status=ApplicationStatus.PENDING_PAYMENT
    )
    
    session.add(application)
    session.flush()
    
    # Log activity
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
    
    # Send application confirmation email
    try:
        email_service.send_application_confirmation(
            to_email=application.email,
            name=application.name,
            application_number=application.application_number,
            fee_mode=data.fee_mode.value,
            amount=500.0  # TODO: Make configurable
        )
    except Exception as e:
        print(f"Failed to send confirmation email: {str(e)}")
    
    return application

@router.get("/recent", response_model=List[ApplicationRead | dict])
async def get_recent_admissions(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    limit: int = 5
):
    """Admin endpoint for dashboard: Recent applications joined with courses"""
    statement = select(Application).order_by(Application.created_at.desc()).limit(limit)
    results = session.exec(statement).all()
    
    # Map to dashboard expected format if needed
    formatted_results = []
    for app in results:
        formatted_results.append({
            "id": app.id,
            "fullName": app.name,
            "email": app.email,
            "status": app.status,
            "createdAt": app.created_at,
            "course": {
                "id": app.program.id,
                "name": app.program.name
            } if app.program else None
        })
    return formatted_results

@router.get("/", response_model=List[ApplicationRead])
async def list_applications(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser),
    status: Optional[ApplicationStatus] = None
):
    """Admin endpoint to see all applications with optional status filter"""
    statement = select(Application)
    if status:
        statement = statement.where(Application.status == status)
    
    results = session.exec(statement).all()
    return results

@router.get("/{id}", response_model=ApplicationRead)
async def get_application(
    id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get details of a specific application"""
    application = session.get(Application, id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Check permission: Only admin or the email/phone owner can view
    # For now, simple check if user is admin or email matches
    if current_user.email != application.email and not any(role.name in ["SUPER_ADMIN", "ADMIN"] for role in current_user.roles):
        raise HTTPException(status_code=403, detail="Not authorized to view this application")
    
    return application

@router.put("/{id}", response_model=ApplicationRead)
async def update_application(
    id: int,
    data: ApplicationUpdate,
    request: Request,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Stage 2: Complete full application form (Secured endpoint)"""
    application = session.get(Application, id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Security: Only the applicant (by email) or admin can update
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN"] for role in current_user.roles)
    is_owner = current_user.email == application.email
    
    if not (is_admin or is_owner):
        raise HTTPException(status_code=403, detail="Not authorized to update this application")
    
    # Update fields
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(application, key, value)
    
    application.updated_at = datetime.utcnow()
    
    # Auto-transition to FORM_COMPLETED if all required fields are present
    if application.status == ApplicationStatus.PAID or (application.fee_mode == FeeMode.OFFLINE and application.offline_payment_verified):
        if application.aadhaar_number and application.father_name and application.address:
            old_status = application.status
            application.status = ApplicationStatus.FORM_COMPLETED
            
            # Log status change
            if old_status != ApplicationStatus.FORM_COMPLETED:
                log_activity(
                    session=session,
                    application_id=application.id,
                    activity_type=ActivityType.FORM_COMPLETED,
                    description=f"Full application form completed",
                    performed_by=current_user.id,
                    ip_address=get_client_ip(request)
                )
    
    session.add(application)
    session.commit()
    session.refresh(application)
    return application

@router.post("/{id}/payment/offline-verify", response_model=ApplicationRead)
async def verify_offline_payment(
    id: int,
    data: OfflinePaymentVerify,
    request: Request,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Admin endpoint to verify offline payment"""
    application = session.get(Application, id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    if application.fee_mode != FeeMode.OFFLINE:
        raise HTTPException(status_code=400, detail="Application is not in offline payment mode")
    
    application.payment_proof_url = data.payment_proof_url
    application.offline_payment_verified = data.verified
    application.offline_payment_verified_by = current_user.id
    application.offline_payment_verified_at = datetime.utcnow()
    
    if data.verified:
        application.status = ApplicationStatus.PAID
        
        # Log activity
        log_activity(
            session=session,
            application_id=application.id,
            activity_type=ActivityType.OFFLINE_PAYMENT_VERIFIED,
            description=f"Offline payment verified by {current_user.full_name}",
            performed_by=current_user.id,
            ip_address=get_client_ip(request),
            extra_data={"payment_proof_url": data.payment_proof_url}
        )
    
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
    
    # Check permission
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN"] for role in current_user.roles)
    is_owner = current_user.email == application.email
    
    if not (is_admin or is_owner):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    statement = select(ApplicationDocument).where(ApplicationDocument.application_id == id)
    documents = session.exec(statement).all()
    
    # Generate download URLs for documents stored in MinIO
    from app.services.storage_service import storage_service
    
    for doc in documents:
        # Check if file_url is an S3 key (doesn't start with /uploads/)
        if doc.file_url and not doc.file_url.startswith('/uploads/'):
            try:
                # Determine bucket
                bucket = storage_service.bucket_images if doc.document_type == DocumentType.PHOTO else storage_service.bucket_documents
                
                # Generate presigned download URL (5 minutes expiry)
                download_url = storage_service.generate_presigned_download_url(
                    key=doc.file_url,
                    bucket=bucket,
                    filename=doc.file_name,
                    expiration=300
                )
                # Temporarily store download URL in file_url for response
                # (In production, you might want to add a download_url field to the schema)
                doc.file_url = download_url
            except Exception as e:
                print(f"Error generating download URL for document {doc.id}: {str(e)}")
    
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
    
    # Check permission
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN"] for role in current_user.roles)
    is_owner = current_user.email == application.email
    
    if not (is_admin or is_owner):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Import storage service
    from app.services.storage_service import storage_service
    from app.models.file_metadata import FileMetadata, FileModule
    
    # Determine bucket based on document type
    if document_type == DocumentType.PHOTO:
        bucket = storage_service.bucket_images
    else:
        bucket = storage_service.bucket_documents
    
    # Generate prefix for S3 key
    prefix = f"admissions/application/{id}"
    
    # Define allowed extensions based on document type
    allowed_extensions = {'.pdf', '.jpg', '.jpeg', '.png'}
    if document_type == DocumentType.PHOTO:
        allowed_extensions = {'.jpg', '.jpeg', '.png'}
    
    # Upload file to MinIO
    try:
        file_key, file_size, mime_type = await storage_service.upload_file(
            file=file,
            prefix=prefix,
            bucket=bucket,
            allowed_extensions=allowed_extensions,
            max_size=10485760  # 10MB
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    
    # Create file metadata record
    file_metadata = FileMetadata(
        file_key=file_key,
        bucket_name=bucket,
        original_filename=file.filename,
        file_size=file_size,
        mime_type=mime_type,
        is_public=False,
        module=FileModule.ADMISSIONS,
        entity_type="Application",
        entity_id=id,
        uploaded_by=current_user.id,
        description=f"Application document: {document_type.value}"
    )
    
    session.add(file_metadata)
    session.flush()
    
    # Create document record (keep existing structure for compatibility)
    document = ApplicationDocument(
        application_id=id,
        document_type=document_type,
        file_url=file_key,  # Store S3 key instead of local path
        file_name=file.filename,
        file_size=file_size,
        status=DocumentStatus.UPLOADED
    )
    
    session.add(document)
    session.flush()
    
    # Log activity
    log_activity(
        session=session,
        application_id=id,
        activity_type=ActivityType.DOCUMENT_UPLOADED,
        description=f"Document uploaded: {document_type.value}",
        performed_by=current_user.id,
        ip_address=get_client_ip(request) if request else None,
        extra_data={
            "document_type": document_type.value, 
            "file_name": file.filename,
            "file_key": file_key,
            "file_metadata_id": file_metadata.id
        }
    )
    
    session.commit()
    session.refresh(document)
    return document

@router.put("/documents/{doc_id}/verify", response_model=DocumentRead)
async def verify_document(
    doc_id: int,
    data: DocumentVerify,
    request: Request,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Admin endpoint to verify or reject a document"""
    document = session.get(ApplicationDocument, doc_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    document.status = data.status
    document.rejection_reason = data.rejection_reason
    document.verified_by = current_user.id
    document.verified_at = datetime.utcnow()
    
    # Log activity
    activity_type = ActivityType.DOCUMENT_VERIFIED if data.status == DocumentStatus.VERIFIED else ActivityType.DOCUMENT_REJECTED
    log_activity(
        session=session,
        application_id=document.application_id,
        activity_type=activity_type,
        description=f"Document {data.status.value}: {document.document_type.value}",
        performed_by=current_user.id,
        ip_address=get_client_ip(request),
        extra_data={"document_id": doc_id, "rejection_reason": data.rejection_reason}
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
    
    # Check permission
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN"] for role in current_user.roles)
    is_owner = current_user.email == application.email
    
    if not (is_admin or is_owner):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    statement = select(ApplicationActivityLog).where(
        ApplicationActivityLog.application_id == id
    ).order_by(ApplicationActivityLog.created_at.desc())
    
    logs = session.exec(statement).all()
    return logs

@router.post("/{id}/confirm", response_model=ApplicationRead)
async def confirm_admission(
    id: int,
    request: Request,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Admin confirms admission: Triggers Student and User account creation with validation"""
    application = session.get(Application, id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    if application.status == ApplicationStatus.ADMITTED:
        raise HTTPException(status_code=400, detail="Applicant already admitted")
    
    # Pre-confirmation validation
    errors = []
    
    # 1. Check if Stage 2 is completed
    if not (application.aadhaar_number and application.father_name and application.address):
        errors.append("Stage 2 form is not completed")
    
    # 2. Check if fee is paid
    if application.fee_mode == FeeMode.ONLINE:
        # Check if there's a successful payment
        has_payment = any(p.status == ApplicationPaymentStatus.SUCCESS for p in application.payments)
        if not has_payment:
            errors.append("No successful online payment found")
    elif application.fee_mode == FeeMode.OFFLINE:
        if not application.offline_payment_verified:
            errors.append("Offline payment not verified")
    
    # 3. Check if mandatory documents are verified (optional for now)
    # TODO: Implement document requirement logic based on program/state
    
    if errors:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot confirm admission: {'; '.join(errors)}"
        )

    # 1. Create User account (if not exists)
    statement = select(User).where(User.email == application.email)
    user = session.exec(statement).first()
    
    if not user:
        # Get STUDENT role
        role_stmt = select(Role).where(Role.name == "STUDENT")
        student_role = session.exec(role_stmt).first()
        if not student_role:
             student_role = Role(name="STUDENT", description="Student Role")
             session.add(student_role)
             session.flush()
             
        user = User(
            username=application.email,
            email=application.email,
            full_name=application.name,
            hashed_password="TEMP_PASSWORD_RESET_REQUIRED",  # User must set password
            is_active=False,  # Inactive until password is set
            roles=[student_role]
        )
        session.add(user)
        session.flush()

    # 1.1 Find Academic Batch and Structure
    current_year_val = datetime.now().year
    
    # Simple logic: Admission is for current year batch
    # TODO: Make this smarter based on academic calendar
    batch = session.exec(
        select(AcademicBatch)
        .where(AcademicBatch.program_id == application.program_id)
        .where(AcademicBatch.joining_year == current_year_val)
    ).first()
    
    if not batch:
        raise HTTPException(
            status_code=400,
            detail=f"No academic batch found for Program {application.program_id} and Year {current_year_val}. Please create a batch first."
        )
        
    # Get 1st Year (System derived)
    program_year = session.exec(
        select(ProgramYear)
        .where(ProgramYear.batch_id == batch.id)
        .where(ProgramYear.year_no == 1)
    ).first()
    
    if not program_year:
         raise HTTPException(status_code=500, detail="Batch structure incomplete: Missing 1st Year")

    # Get 1st Semester
    batch_semester = session.exec(
        select(BatchSemester)
        .where(BatchSemester.batch_id == batch.id)
        .where(BatchSemester.year_no == 1)
        .where(BatchSemester.semester_no == 1)
    ).first()
    
    if not batch_semester:
        raise HTTPException(status_code=500, detail="Batch structure incomplete: Missing Semester 1")

    # 2. Create Student profile
    admission_number = f"ADM-{datetime.now().year}-{str(application.id).zfill(4)}"
    student = Student(
        admission_number=admission_number,
        name=application.name,
        email=application.email,
        phone=application.phone,
        user_id=user.id,
        program_id=application.program_id,
        
        # Strict Academic Hierarchy
        batch_id=batch.id,
        program_year_id=program_year.id,
        batch_semester_id=batch_semester.id,
        # Section and Practical Batch assigned later
        
        gender=application.gender if hasattr(Gender, application.gender) else Gender.MALE, # Safe fallback or parsing needed
        aadhaar_number=application.aadhaar_number,
        hostel_required=application.hostel_required,
        status=StudentStatus.ACTIVE
    )
    session.add(student)
    session.flush()

    # 3. Update Application status
    application.status = ApplicationStatus.ADMITTED
    application.student_id = student.id
    application.updated_at = datetime.utcnow()
    
    # Log activity
    log_activity(
        session=session,
        application_id=application.id,
        activity_type=ActivityType.ADMISSION_CONFIRMED,
        description=f"Admission confirmed by {current_user.full_name}. Student ID: {admission_number}",
        performed_by=current_user.id,
        ip_address=get_client_ip(request),
        extra_data={"student_id": student.id, "admission_number": admission_number}
    )
    
    session.add(application)
    session.commit()
    session.refresh(application)
    
    # Generate password setup token and send email
    try:
        from app.services.password_service import PasswordToken
        
        # Generate token
        token = PasswordToken.create_token(user.id, user.email, expires_hours=24)
        
        # Generate password setup link
        base_url = str(request.base_url).rstrip('/')
        password_setup_link = f"{base_url.replace('/api/v1', '')}/auth/setup-password?token={token}"
        
        # Get program name
        program_name = application.program.name if application.program else "N/A"
        
        # Send admission confirmation email with password setup link
        email_service.send_admission_confirmation(
            to_email=application.email,
            name=application.name,
            admission_number=admission_number,
            program_name=program_name,
            password_setup_link=password_setup_link
        )
    except Exception as e:
        print(f"Failed to send admission confirmation email: {str(e)}")
    
    return application
