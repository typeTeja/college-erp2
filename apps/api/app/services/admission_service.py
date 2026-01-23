"""
Admission Service
Handles Quick Apply, Progressive Application, and Admission Settings
"""
from typing import Optional
from datetime import datetime
import secrets
import string
from sqlmodel import Session, select
from passlib.context import CryptContext

from app.models.admissions import Application, ApplicationStatus, ApplicationActivityLog, ActivityType
from app.models.admission_settings import AdmissionSettings
from app.models.user import User
from app.models.role import Role
from app.config.settings import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AdmissionService:
    """Service for handling admission workflow operations"""
    
    @staticmethod
    def get_admission_settings(session: Session) -> AdmissionSettings:
        """Get or create admission settings"""
        settings_obj = session.exec(select(AdmissionSettings)).first()
        if not settings_obj:
            # Create default settings if none exist
            settings_obj = AdmissionSettings()
            session.add(settings_obj)
            session.commit()
            session.refresh(settings_obj)
        return settings_obj
    
    @staticmethod
    def generate_application_number(session: Session) -> str:
        """Generate unique application number"""
        year = datetime.now().year
        # Count applications this year
        count = session.exec(
            select(Application).where(
                Application.application_number.like(f"APP{year}%")
            )
        ).all()
        next_number = len(count) + 1
        return f"APP{year}{next_number:05d}"
    
    @staticmethod
    def generate_portal_credentials() -> tuple[str, str]:
        """
        Generate secure portal credentials
        Returns: (username, plain_password)
        """
        # Generate random username (8 characters)
        username = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(8))
        
        # Generate secure password (12 characters)
        alphabet = string.ascii_letters + string.digits + "!@#$%"
        password = ''.join(secrets.choice(alphabet) for _ in range(12))
        
        return username, password
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password for storage"""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_quick_apply(
        session: Session,
        name: str,
        email: str,
        phone: str,
        gender: str,
        program_id: int,
        state: str,
        board: str,
        group_of_study: str,
        payment_mode: str = "ONLINE",
    ) -> Application:
        """
        Create Quick Apply application WITHOUT portal account
        Portal account will be created after payment completion
        
        Returns: application
        """
        # Get admission settings
        admission_settings = AdmissionService.get_admission_settings(session)
        
        # Generate application number
        app_number = AdmissionService.generate_application_number(session)
        
        # Determine initial status based on payment requirement
        if admission_settings.application_fee_enabled:
            initial_status = ApplicationStatus.PENDING_PAYMENT
        else:
            initial_status = ApplicationStatus.QUICK_APPLY_SUBMITTED
        
        # Create application
        application = Application(
            application_number=app_number,
            name=name,
            email=email,
            phone=phone,
            gender=gender,
            program_id=program_id,
            state=state,
            board=board,
            group_of_study=group_of_study,
            status=initial_status,
            quick_apply_completed_at=datetime.utcnow(),
            application_fee=admission_settings.application_fee_amount if admission_settings.application_fee_enabled else 0,
            fee_mode=payment_mode,
        )
        
        session.add(application)
        session.flush()  # Get application ID
        
        # Log activity
        activity_log = ApplicationActivityLog(
            application_id=application.id,
            activity_type=ActivityType.APPLICATION_CREATED,
            description=f"Quick Apply submitted by {name} - Payment Mode: {payment_mode}",
        )
        session.add(activity_log)
        
        session.commit()
        session.refresh(application)
        
        return application
    
    @staticmethod
    def update_login_timestamp(session: Session, application: Application):
        """Update portal login timestamp"""
        if not application.portal_first_login:
            application.portal_first_login = datetime.utcnow()
            application.status = ApplicationStatus.LOGGED_IN
        
        application.portal_last_login = datetime.utcnow()
        session.add(application)
        session.commit()
    
    @staticmethod
    def start_full_form(session: Session, application: Application):
        """Mark that applicant started full form"""
        if not application.full_form_started_at:
            application.full_form_started_at = datetime.utcnow()
            application.status = ApplicationStatus.FORM_IN_PROGRESS
            
            # Log activity
            activity_log = ApplicationActivityLog(
                application_id=application.id,
                activity_type=ActivityType.FORM_COMPLETED,
                description="Applicant started completing full application form",
            )
            session.add(activity_log)
            
            session.add(application)
            session.commit()
    
    @staticmethod
    def complete_full_form(
        session: Session,
        application: Application,
        **form_data
    ) -> Application:
        """
        Complete full application form with Stage 2 data
        
        Args:
            session: Database session
            application: Application object
            **form_data: Dictionary of form fields to update
        """
        # Update application with form data
        for key, value in form_data.items():
            if hasattr(application, key):
                setattr(application, key, value)
        
        # Mark form as completed
        application.full_form_completed_at = datetime.utcnow()
        
        # Get admission settings to determine next status
        admission_settings = AdmissionService.get_admission_settings(session)
        
        if admission_settings.application_fee_enabled:
            application.status = ApplicationStatus.PENDING_PAYMENT
        else:
            # Skip payment if fee is disabled
            application.status = ApplicationStatus.FORM_COMPLETED
        
        # Log activity
        activity_log = ApplicationActivityLog(
            application_id=application.id,
            activity_type=ActivityType.FORM_COMPLETED,
            description="Full application form completed",
        )
        session.add(activity_log)
        
        session.add(application)
        session.commit()
        session.refresh(application)
        
        return application
    
    @staticmethod
    def get_payment_configuration(session: Session) -> dict:
        """Get payment configuration for frontend"""
        settings_obj = AdmissionService.get_admission_settings(session)
        
        return {
            "fee_enabled": settings_obj.application_fee_enabled,
            "fee_amount": settings_obj.application_fee_amount,
            "online_enabled": settings_obj.online_payment_enabled,
            "offline_enabled": settings_obj.offline_payment_enabled,
            "payment_gateway": settings_obj.payment_gateway,
        }
    
    @staticmethod
    def create_portal_account_after_payment(
        session: Session,
        application: Application
    ) -> tuple[str, str]:
        """
        Create student portal account AFTER payment completion
        
        Returns: (portal_username, portal_password)
        """
        # Get admission settings
        admission_settings = AdmissionService.get_admission_settings(session)
        
        if not admission_settings.auto_create_student_account:
            raise ValueError("Auto account creation is disabled")
        
        # Check if account already exists
        if application.portal_user_id:
            raise ValueError("Portal account already exists for this application")
        
        # Generate credentials
        portal_username, portal_password = AdmissionService.generate_portal_credentials()
        
        # Create user account
        student_role = session.exec(select(Role).where(Role.name == "STUDENT")).first()
        if not student_role:
            raise ValueError("STUDENT role not found in database")
        
        portal_user = User(
            username=portal_username,
            email=application.email,
            phone=application.phone,
            full_name=application.name,
            hashed_password=AdmissionService.hash_password(portal_password),
            is_active=True,
        )
        session.add(portal_user)
        session.flush()
        
        # Link user to application
        application.portal_user_id = portal_user.id
        application.portal_password_hash = AdmissionService.hash_password(portal_password)
        application.status = ApplicationStatus.QUICK_APPLY_SUBMITTED
        
        # Assign student role
        from app.models.user_role import UserRole
        user_role = UserRole(user_id=portal_user.id, role_id=student_role.id)
        session.add(user_role)
        
        # Log activity
        activity_log = ApplicationActivityLog(
            application_id=application.id,
            activity_type=ActivityType.PAYMENT_COMPLETED,
            description="Portal account created after payment completion",
        )
        session.add(activity_log)
        
        session.add(application)
        session.commit()
        session.refresh(application)
        
        return portal_username, portal_password
    @staticmethod
    def process_payment_completion(
        session: Session,
        application_id: int,
        transaction_id: str,
        amount: float,
        payment_date: datetime = None,
        background_tasks = None # Type: BackgroundTasks
    ) -> bool:
        """
        Process successful payment (Offline or Online)
        1. Update Status
        2. Create Portal Account
        3. Send Emails
        """
        try:
            from app.services.email_service import email_service
            
            application = session.get(Application, application_id)
            if not application:
                return False
            
            # Update Payment Status
            application.status = ApplicationStatus.PAYMENT_COMPLETED # Or PAID based on enum
            application.payment_status = 'PAID' # Ensure this matches schema/enum
            application.payment_id = transaction_id
            application.payment_date = payment_date or datetime.utcnow()
            
            session.add(application)
            session.flush()
            
            # Create Portal Account
            portal_username, portal_password = (None, None)
            try:
                portal_username, portal_password = AdmissionService.create_portal_account_after_payment(
                    session=session,
                    application=application
                )
            except ValueError as e:
                # Account might already exist, just continue
                print(f"Account creation skipped: {e}")
                
            session.commit()
            session.refresh(application)
            
            if background_tasks:
                # Send Payment Success Email
                background_tasks.add_task(
                    email_service.send_payment_success,
                    to_email=application.email,
                    name=application.name,
                    application_number=application.application_number,
                    amount=amount,
                    transaction_id=transaction_id
                )
                
                # Send Credentials Email
                if portal_username and portal_password:
                     background_tasks.add_task(
                        email_service.send_portal_credentials,
                        to_email=application.email,
                        name=application.name,
                        application_number=application.application_number,
                        username=portal_username,
                        password=portal_password
                    )
            
            return True
        except Exception as e:
            print(f"Error processing payment completion: {str(e)}")
            return False
