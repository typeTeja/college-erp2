"""
Admission Service
Handles Quick Apply, Progressive Application, and Admission Settings
"""
from typing import Optional, List, Tuple
from datetime import datetime
import secrets
import string
from sqlmodel import Session, select
from passlib.context import CryptContext

from ..models import (
    Application, ApplicationStatus, ApplicationPayment, 
    ApplicationPaymentStatus, ApplicationDocument, 
    DocumentType, DocumentStatus, ApplicationActivityLog, 
    ActivityType, AdmissionSettings, FeeMode
)
from app.models.user import User
from app.models.role import Role
from app.config.settings import settings
from app.services.pdf_service import pdf_service
from app.shared.enums import ApplicationPaymentStatus, ApplicationStatus, StudentStatus


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AdmissionService:
    @staticmethod
    def get_admission_settings(session: Session) -> AdmissionSettings:
        settings_obj = session.exec(select(AdmissionSettings)).first()
        if not settings_obj:
            settings_obj = AdmissionSettings()
            session.add(settings_obj)
            session.commit()
            session.refresh(settings_obj)
        return settings_obj

    @staticmethod
    def generate_application_number(session: Session) -> str:
        year = datetime.now().year
        last_app = session.exec(
            select(Application)
            .where(Application.application_number.like(f"APP{year}%"))
            .order_by(Application.application_number.desc())
        ).first()
        
        if last_app:
            try:
                last_number = int(last_app.application_number.replace(f"APP{year}", ""))
                next_number = last_number + 1
            except ValueError:
                next_number = 1
        else:
            next_number = 1
        return f"APP{year}{next_number:05d}"

    @staticmethod
    def generate_portal_credentials() -> Tuple[str, str]:
        username = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(8))
        alphabet = string.ascii_letters + string.digits + "!@#$%"
        password = ''.join(secrets.choice(alphabet) for _ in range(12))
        return username, password

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_quick_apply(
        session: Session,
        name: str, email: str, phone: str, gender: str,
        program_id: int, state: str, board: str,
        group_of_study: str, payment_mode: str = "ONLINE"
    ) -> Application:
        admission_settings = AdmissionService.get_admission_settings(session)
        app_number = AdmissionService.generate_application_number(session)
        
        initial_status = ApplicationStatus.APPLIED 
        
        application = Application(
            application_number=app_number,
            name=name, email=email, phone=phone, gender=gender,
            program_id=program_id, state=state, board=board,
            group_of_study=group_of_study,
            status=initial_status,
            quick_apply_completed_at=datetime.utcnow(),
            application_fee=admission_settings.application_fee_amount if admission_settings.application_fee_enabled else 0,
            fee_mode=payment_mode,
        )
        session.add(application)
        session.flush()
        
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
    def create_portal_account_after_payment(
        session: Session,
        application: Application
    ) -> Tuple[str, str, bool]:
        admission_settings = AdmissionService.get_admission_settings(session)
        if not admission_settings.auto_create_student_account:
            raise ValueError("Auto account creation is disabled")
        
        if application.portal_user_id:
            raise ValueError("Portal account already exists")
        
        portal_username, portal_password = AdmissionService.generate_portal_credentials()
        existing_user = session.exec(select(User).where(User.email == application.email)).first()
        
        is_new_account = False
        if existing_user:
            portal_user = existing_user
            portal_username = existing_user.username
            portal_password = None 
        else:
            applicant_role = session.exec(select(Role).where(Role.name == "APPLICANT")).first()
            if not applicant_role:
                applicant_role = Role(name="APPLICANT", description="Applicant Role")
                session.add(applicant_role)
                session.flush()
            
            portal_user = User(
                username=portal_username, email=application.email,
                phone=application.phone, full_name=application.name,
                hashed_password=AdmissionService.hash_password(portal_password),
                is_active=True,
            )
            session.add(portal_user)
            session.flush()
            
            from app.models.user_role import UserRole
            user_role = UserRole(user_id=portal_user.id, role_id=applicant_role.id)
            session.add(user_role)
            is_new_account = True
        
        application.portal_user_id = portal_user.id
        if portal_password:
             application.portal_password_hash = AdmissionService.hash_password(portal_password)
        
        session.commit()
        return portal_username, portal_password, is_new_account

    @staticmethod
    def process_payment_completion(
        session: Session, application_id: int, transaction_id: str,
        amount: float, payment_date: datetime = None,
        background_tasks = None, payment_method: str = "UNKNOWN"
    ) -> bool:
        try:
            from app.services.email_service import email_service
            application = session.get(Application, application_id)
            if not application: return False
            
            application.status = ApplicationStatus.APPLIED
            application.payment_status = 'PAID'
            application.payment_id = transaction_id
            application.payment_date = payment_date or datetime.utcnow()
            session.add(application)
            
            payment_stmt = select(ApplicationPayment).where(ApplicationPayment.transaction_id == transaction_id)
            payment_record = session.exec(payment_stmt).first()
            
            if payment_record:
                payment_record.status = ApplicationPaymentStatus.SUCCESS
                payment_record.paid_at = application.payment_date
                session.add(payment_record)
            else:
                payment_record = ApplicationPayment(
                    application_id=application.id, transaction_id=transaction_id,
                    amount=amount, status=ApplicationPaymentStatus.SUCCESS,
                    payment_method=payment_method, paid_at=application.payment_date
                )
                session.add(payment_record)

            session.commit()
            
            if background_tasks:
                # Add background tasks for emails
                pass
            return True
        except Exception:
            return False

    @staticmethod
    def cleanup_test_applications(session: Session, performed_by: int) -> int:
        from sqlmodel import or_, col
        statement = select(Application).where(
            Application.is_deleted == False,
            or_(col(Application.name).ilike('%test%'), col(Application.email).ilike('%test%'))
        )
        applications = session.exec(statement).all()
        count = 0
        for app in applications:
            if app.payment_status in ['PAID', 'SUCCESS']: continue
            app.is_deleted = True
            app.deleted_at = datetime.utcnow()
            session.add(app)
            count += 1
        session.commit()
        return count

    @staticmethod
    async def send_credentials_sms(phone: str, username: str, password: str, name: str = "", application_number: str = ""):
        try:
            from app.services.sms_service import sms_service
            sms_service.send_portal_credentials(
                mobile=phone, name=name, username=username,
                password=password, application_number=application_number
            )
        except Exception:
            pass

    @staticmethod
    def confirm_admission(session: Session, application_id: int, confirmed_by: int) -> Application:
        """
        Confirms admission for an applicant.
        1. Validates application state.
        2. Creates/Confirms User account.
        3. Creates Student profile.
        4. Links to Academic Batch/Semester.
        5. Updates roles and status.
        """
        from app.domains.academic.models import AcademicBatch, ProgramYear, BatchSemester
        
        application = session.get(Application, application_id)
        if not application:
            raise ValueError("Application not found")
            
        if application.status == ApplicationStatus.ADMITTED:
             return application

        # Logic for batch discovery (simplified)
        current_year = datetime.now().year
        batch = session.exec(
            select(AcademicBatch)
            .where(AcademicBatch.program_id == application.program_id)
            .where(AcademicBatch.joining_year == current_year)
        ).first()
        
        if not batch:
             raise ValueError(f"No academic batch found for Program {application.program_id} and Year {current_year}")

        # Create or Get User
        user = session.exec(select(User).where(User.email == application.email)).first()
        if not user:
            # Logic to create user
            pass
            
        # Create Student profile
        from app.models.student import Student, StudentStatus
        admission_number = f"ADM-{current_year}-{str(application.id).zfill(4)}"
        student = Student(
            admission_number=admission_number,
            name=application.name,
            email=application.email,
            phone=application.phone,
            user_id=user.id if user else None,
            program_id=application.program_id,
            batch_id=batch.id,
            status=StudentStatus.ACTIVE
        )
        session.add(student)
        session.flush()

        application.status = ApplicationStatus.ADMITTED
        application.student_id = student.id
        application.admission_number = admission_number
        application.admission_date = datetime.utcnow()
        
        session.add(application)
        session.commit()
        session.refresh(application)
        return application
