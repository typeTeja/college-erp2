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
from app.schemas.admissions import (
    QuickApplyCreate,
    QuickApplyResponse,
    ApplicationCompleteUpdate,
    ApplicationRead,
    AdmissionSettingsRead,
    AdmissionSettingsUpdate,
    PaymentConfigResponse
)
from app.services.admission_service import AdmissionService
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
    Enhanced Quick Apply (Stage 1) - Lead Capture with Auto Account Creation
    
    - Creates application with QUICK_APPLY_SUBMITTED status
    - Auto-creates student portal account
    - Sends login credentials via Email & SMS
    """
    try:
        # Create Quick Apply application
        application, portal_username, portal_password = AdmissionService.create_quick_apply(
            session=session,
            name=application_in.name,
            email=application_in.email,
            phone=application_in.phone,
            gender=application_in.gender,
            program_id=application_in.program_id,
            state=application_in.state,
            board=application_in.board,
            group_of_study=application_in.group_of_study,
        )
        
        # Get admission settings to check notification preferences
        settings = AdmissionService.get_admission_settings(session)
        
        # Send credentials via email (background task)
        if settings.send_credentials_email and portal_username:
            background_tasks.add_task(
                send_credentials_email,
                email=application.email,
                name=application.name,
                username=portal_username,
                password=portal_password,
                application_number=application.application_number
            )
        
        # Send credentials via SMS (background task)
        if settings.send_credentials_sms and portal_username:
            background_tasks.add_task(
                send_credentials_sms,
                phone=application.phone,
                username=portal_username,
                password=portal_password,
                name=application.name,
                application_number=application.application_number
            )
        
        return QuickApplyResponse(
            application_number=application.application_number,
            portal_username=portal_username,
            portal_password=portal_password,  # Only sent once in response
            message="Application submitted successfully! Login credentials have been sent to your email and phone."
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create application: {str(e)}")


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
    *,
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
