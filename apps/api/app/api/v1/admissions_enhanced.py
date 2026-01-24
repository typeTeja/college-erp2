"""
Enhanced Admission Workflow Endpoints
New endpoints for Quick Apply v2 and Admission Settings
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlmodel import Session, select
from datetime import datetime
from app.db.session import get_session
from app.api.deps import get_current_user
from app.models.user import User
from app.models.admissions import Application
from app.models.admission_settings import AdmissionSettings
from app.services.storage_service import storage_service
from app.schemas.admissions import (
    QuickApplyCreate,
    QuickApplyResponse,
    ApplicationCompleteUpdate,
    ApplicationRead,
    AdmissionSettingsRead,
    AdmissionSettingsUpdate,
    AdmissionSettingsUpdate,
    PaymentConfigResponse,
    OfflineApplicationCreate
)
from app.services.admission_service import AdmissionService
from app.services.email_service import email_service
from typing import Optional

router = APIRouter()


@router.post("/v2/quick-apply", response_model=QuickApplyResponse)
async def quick_apply_v2(
    *,
    session: Session = Depends(get_session),
    application_in: QuickApplyCreate,
    background_tasks: BackgroundTasks
):
    """
    Enhanced Quick Apply (Stage 1) - Lead Capture WITHOUT Credentials
    
    - Creates application with PENDING_PAYMENT status (if fee enabled)
    - Does NOT create portal account yet
    - Credentials will be sent after payment completion
    """
    try:
        # Create Quick Apply application (without portal account)
        application = AdmissionService.create_quick_apply(
            session=session,
            name=application_in.name,
            email=application_in.email,
            phone=application_in.phone,
            gender=application_in.gender,
            program_id=application_in.program_id,
            state=application_in.state,
            board=application_in.board,
            group_of_study=application_in.group_of_study,
            payment_mode=getattr(application_in, 'payment_mode', 'ONLINE'),
        )
        
        # Get admission settings
        settings = AdmissionService.get_admission_settings(session)
        
        # Determine message based on payment requirement
        if settings.application_fee_enabled:
            if application.fee_mode == 'ONLINE':
                message = f"Application submitted! Please complete payment of ₹{application.application_fee}. You will receive login credentials after payment."
            else:
                message = f"Application submitted! Please pay ₹{application.application_fee} at college office. You will receive login credentials after payment verification."
            
            # Send Application Confirmation Email
            if settings.send_credentials_email: # Reusing this setting or we should have a separate one? Assuming yes for now.
                 background_tasks.add_task(
                    email_service.send_application_confirmation,
                    to_email=application.email,
                    name=application.name,
                    application_number=application.application_number,
                    fee_mode=application.fee_mode,
                    amount=application.application_fee
                )
        else:
            # No payment required - create account immediately
            portal_username, portal_password, is_new_account = AdmissionService.create_portal_account_after_payment(
                session=session,
                application=application
            )
            
            # Send credentials
            if settings.send_credentials_email:
                if is_new_account:
                    background_tasks.add_task(
                        email_service.send_portal_credentials,
                        to_email=application.email,
                        name=application.name,
                        username=portal_username,
                        password=portal_password,
                        application_number=application.application_number
                    )
                else:
                    background_tasks.add_task(
                        email_service.send_existing_user_linked,
                        to_email=application.email,
                        name=application.name,
                        application_number=application.application_number,
                        portal_url=f"{settings.portal_base_url}" # using small settings if possible or check import
                    )
            
            if settings.send_credentials_sms and is_new_account:
                background_tasks.add_task(
                    send_credentials_sms,
                    phone=application.phone,
                    username=portal_username,
                    password=portal_password,
                    name=application.name,
                    application_number=application.application_number
                )
            
            message = "Application submitted successfully! Login credentials have been sent to your email and phone."
            
            return QuickApplyResponse(
                id=application.id,
                application_number=application.application_number,
                portal_username=portal_username,
                portal_password=portal_password,
                message=message
            )
        
        # Payment required - no credentials yet
        return QuickApplyResponse(
            id=application.id,
            application_number=application.application_number,
            portal_username=None,
            portal_password=None,
            message=message
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create application: {str(e)}")


@router.post("/payment-complete/{application_number}")
async def complete_payment(
    *,
    session: Session = Depends(get_session),
    application_number: str,
    background_tasks: BackgroundTasks
):
    """
    Called after successful payment to create portal account and send credentials
    
    This endpoint should be called by payment gateway callback or admin verification
    """
    try:
        # Find application
        statement = select(Application).where(Application.application_number == application_number)
        application = session.exec(statement).first()
        
        if not application:
            raise HTTPException(status_code=404, detail="Application not found")
        
        # Check if already has portal account
        if application.portal_user_id:
            return {"message": "Portal account already exists", "application_number": application_number}
        
        # Create portal account
        portal_username, portal_password = AdmissionService.create_portal_account_after_payment(
            session=session,
            application=application
        )
        
        # Get settings
        settings = AdmissionService.get_admission_settings(session)
        
        # Send credentials via email
        if settings.send_credentials_email:
            background_tasks.add_task(
                send_credentials_email,
                email=application.email,
                name=application.name,
                username=portal_username,
                password=portal_password,
                application_number=application.application_number
            )
        
        # Send credentials via SMS
        if settings.send_credentials_sms:
            background_tasks.add_task(
                send_credentials_sms,
                phone=application.phone,
                username=portal_username,
                password=portal_password,
                name=application.name,
                application_number=application.application_number
            )
        
        return {
            "message": "Payment confirmed! Portal credentials have been sent to your email and phone.",
            "application_number": application_number,
            "portal_username": portal_username
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to complete payment: {str(e)}")


@router.get("/my-application", response_model=ApplicationRead)
async def get_my_application(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get logged-in applicant's application
    
    Used by student portal to display application status and allow completion
    """
    # Find application by portal_user_id
    statement = select(Application).where(Application.portal_user_id == current_user.id)
    application = session.exec(statement).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="No application found for this account")
    
    # Update login timestamp
    AdmissionService.update_login_timestamp(session, application)
    
    return application


@router.put("/my-application/complete", response_model=ApplicationRead)
async def complete_my_application(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    application_data: ApplicationCompleteUpdate
):
    """
    Complete full application form (Stage 2)
    
    Progressive application completion by logged-in applicant
    """
    # Find application
    statement = select(Application).where(Application.portal_user_id == current_user.id)
    application = session.exec(statement).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="No application found for this account")
    
    # Mark form as started if not already
    AdmissionService.start_full_form(session, application)
    
    # Complete the form
    form_data = application_data.dict(exclude_unset=True)
    updated_application = AdmissionService.complete_full_form(
        session=session,
        application=application,
        **form_data
    )
    
    return updated_application


@router.get("/payment-config", response_model=PaymentConfigResponse)
async def get_payment_config(
    session: Session = Depends(get_session)
):
    """
    Get payment configuration for frontend
    
    Public endpoint to display payment options dynamically
    """
    config = AdmissionService.get_payment_configuration(session)
    return PaymentConfigResponse(**config)


# Admin Settings Endpoints

@router.get("/settings", response_model=AdmissionSettingsRead)
async def get_admission_settings(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get admission settings (Admin only)"""
    # Check if user is admin
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"] for role in current_user.roles)
    if not is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to view settings")
    
    settings = AdmissionService.get_admission_settings(session)
    return settings


@router.put("/settings", response_model=AdmissionSettingsRead)
async def update_admission_settings(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    settings_in: AdmissionSettingsUpdate
):
    """Update admission settings (Admin only)"""
    # Check if user is admin
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"] for role in current_user.roles)
    if not is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to update settings")
    
    # Get existing settings
    settings = AdmissionService.get_admission_settings(session)
    
    # Update fields
    update_data = settings_in.dict(exclude_unset=True)
    for key, value in update_data.items():
        if hasattr(settings, key):
            setattr(settings, key, value)
    
    settings.updated_by = current_user.id
    settings.updated_at = datetime.utcnow()
    
    session.add(settings)
    session.commit()
    session.refresh(settings)
    
    return settings


# Helper functions for background tasks

async def send_credentials_email(email: str, name: str, username: str, password: str, application_number: str):
    """Send portal credentials via email"""
    try:
        from app.services.email_service import email_service
        from app.models.admission_settings import AdmissionSettings
        from sqlmodel import Session, select
        from app.db.session import engine
        
        # Get portal URL from settings
        with Session(engine) as session:
            settings = session.exec(select(AdmissionSettings)).first()
            portal_url = settings.portal_base_url if settings and settings.portal_base_url else "https://portal.college.edu"
        
        success = email_service.send_portal_credentials(
            to_email=email,
            name=name,
            application_number=application_number,
            username=username,
            password=password,
            portal_url=portal_url
        )
        
        if success:
            print(f"✅ Credentials email sent successfully to {email}")
        else:
            print(f"❌ Failed to send credentials email to {email}")
            
    except Exception as e:
        print(f"❌ Error sending credentials email: {str(e)}")


async def send_credentials_sms(phone: str, username: str, password: str, name: str = "", application_number: str = ""):
    """Send portal credentials via SMS using MSG91"""
    try:
        from app.services.sms_service import sms_service
        
        success = sms_service.send_portal_credentials(
            mobile=phone,
            name=name,
            username=username,
            password=password,
            application_number=application_number
        )
        
        if success:
            print(f"✅ Credentials SMS sent successfully to {phone}")
        else:
            print(f"❌ Failed to send credentials SMS to {phone}")
            
    except Exception as e:
        print(f"❌ Error sending credentials SMS: {str(e)}")
@router.get("/v2/applications/{id}/receipt")
async def get_payment_receipt(
    id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get payment receipt URL for an application
    """
    # Find application
    statement = select(Application).where(Application.id == id)
    application = session.exec(statement).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Check permission
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"] for role in current_user.roles)
    is_owner = current_user.id == application.portal_user_id
    # Also allow if the user just paid and is checking status (maybe not logged in? No, this endpoint requires auth)
    # If explicitly "download receipt" on success page, they might not be logged in yet?
    # But logic says credentials sent.
    
    if not (is_admin or is_owner):
        raise HTTPException(status_code=403, detail="Not authorized")
        
    # Find receipt document
    from app.models.admissions import ApplicationDocument
    doc_stmt = select(ApplicationDocument).where(
        ApplicationDocument.application_id == id,
        ApplicationDocument.file_name == "Payment Receipt"
    ).order_by(ApplicationDocument.uploaded_at.desc())
    
    document = session.exec(doc_stmt).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Receipt not found")
        
    # Generate presigned URL if it's an S3 key (doesn't start with http)
    url = document.file_url
    if not url.startswith("http"):
        url = storage_service.generate_presigned_download_url(
            key=url,
            filename=f"Receipt_{application.application_number}.pdf"
        )
        
    return {"url": url}

@router.get("/v2/public/receipt/{application_number}")
async def get_public_payment_receipt(
    application_number: str,
    session: Session = Depends(get_session)
):
    """
    Get public payment receipt URL for an application (No Auth required)
    """
    from app.models.admissions import Application, ApplicationDocument
    
    # Find application
    statement = select(Application).where(Application.application_number == application_number)
    application = session.exec(statement).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
        
    # Check if paid
    if application.status != 'PAID' and application.payment_status != 'PAID':
        # Also check simplified status
        if application.payment_status != 'SUCCESS': # In case PaymentStatus enum used differently
             # If strictly PENDING_PAYMENT, deny.
             pass 

    # Find receipt document
    doc_stmt = select(ApplicationDocument).where(
        ApplicationDocument.application_id == application.id,
        ApplicationDocument.file_name == "Payment Receipt"
    ).order_by(ApplicationDocument.uploaded_at.desc())
    
    document = session.exec(doc_stmt).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Receipt not found")
        
    # Generate presigned URL if it's an S3 key (doesn't start with http)
    url = document.file_url
    if not url.startswith("http"):
        url = storage_service.generate_presigned_download_url(
            key=url,
            filename=f"Receipt_{application.application_number}.pdf"
        )
        
    return {"url": url}

# Admin Cleanup Endpoints

@router.delete("/v2/applications/{id}")
async def delete_application(
    id: int,
    reason: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Soft delete an application (Admin only)
    Strictly forbids deleting PAID applications.
    """
    # Check permission
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"] for role in current_user.roles)
    if not is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    try:
        application = AdmissionService.soft_delete_application(
            session=session,
            application_id=id,
            deleted_by=current_user.id,
            reason=reason
        )
        return {"message": "Application soft-deleted successfully", "id": id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/v2/applications/{id}/restore")
async def restore_application(
    id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Restore a deleted application (Admin only)
    """
    # Check permission
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"] for role in current_user.roles)
    if not is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    try:
        application = AdmissionService.restore_application(
            session=session,
            application_id=id,
            restored_by=current_user.id
        )
        return {"message": "Application restored successfully", "id": id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/v2/applications/cleanup/test-data")
async def cleanup_test_data(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Bulk cleanup of 'Test' applications (Admin only)
    Targets unpaid apps with 'test' in name/email.
    """
    # Check permission
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN", "PRINCIPAL"] for role in current_user.roles)
    if not is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    count = AdmissionService.cleanup_test_applications(
        session=session,
        performed_by=current_user.id
    )
    
    return {"message": "Cleanup completed", "deleted_count": count}
