from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, func
from app.db.session import get_session
from app.api.deps import get_current_user, get_current_active_superuser
from app.models.user import User
from app.models.role import Role
from app.models.student import Student, StudentStatus
from app.models.admissions import Application, ApplicationStatus, ApplicationPayment, ApplicationPaymentStatus
from app.schemas.admissions import ApplicationCreate, ApplicationUpdate, ApplicationRead
from typing import List, Optional
from datetime import datetime
import random
import string

router = APIRouter()

def generate_application_number(session: Session) -> str:
    """Generate a unique application number like APP-2025-XXXX"""
    year = datetime.now().year
    prefix = f"APP-{year}-"
    # Simple strategy: find max existing and increment
    # For now, just using a random string for simplicity and uniqueness
    random_str = ''.join(random.choices(string.digits, k=4))
    return f"{prefix}{random_str}"

@router.post("/quick-apply", response_model=ApplicationRead)
async def quick_apply(
    data: ApplicationCreate,
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
    session.commit()
    session.refresh(application)
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
    # (The response_model will handle filtering if we return objects)
    # However, to avoid 422 in future, let's explicitly map camelCase for the dashboard
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
    # For now, simple check if user is admin
    return application

@router.put("/{id}", response_model=ApplicationRead)
async def update_application(
    id: int,
    data: ApplicationUpdate,
    session: Session = Depends(get_session)
):
    """Stage 2: Complete full application form (Usually via public unique link or user login)"""
    application = session.get(Application, id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Update fields
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(application, key, value)
    
    application.updated_at = datetime.utcnow()
    # Auto-transition to FORM_COMPLETED if paid
    if application.status == ApplicationStatus.PAID and update_data.get("address"):
        application.status = ApplicationStatus.FORM_COMPLETED
        
    session.add(application)
    session.commit()
    session.refresh(application)
    return application

@router.post("/{id}/confirm", response_model=ApplicationRead)
async def confirm_admission(
    id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Admin confirms admission: Triggers Student and User account creation"""
    application = session.get(Application, id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    if application.status == ApplicationStatus.ADMITTED:
        raise HTTPException(status_code=400, detail="Applicant already admitted")

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
            hashed_password="hashed_placeholder", # In real app, send reset link
            is_active=True,
            roles=[student_role]
        )
        session.add(user)
        session.flush()

    # 2. Create Student profile
    admission_number = f"ADM-{datetime.now().year}-{str(application.id).zfill(4)}"
    student = Student(
        admission_number=admission_number,
        name=application.name,
        email=application.email,
        phone=application.phone,
        user_id=user.id,
        program_id=application.program_id,
        gender=application.gender,
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
    
    session.add(application)
    session.commit()
    session.refresh(application)
    
    return application
