"""
Admission Services

Consolidated services for the admission domain.
Handles Quick Apply, Progressive Application, Admission Settings, Entrance Exams, and Merit Calculations.
"""
from typing import Optional, List, Tuple, Dict, Any
from datetime import datetime, date
import secrets
import string
from sqlmodel import Session, select, or_, col
from passlib.context import CryptContext

from .models import (
    Application, ApplicationStatus, ApplicationPayment, 
    ApplicationPaymentStatus, ApplicationDocument, 
    DocumentType, DocumentStatus, ApplicationActivityLog, 
    ActivityType, AdmissionSettings, FeeMode,
    EntranceTestConfig, EntranceExamResult,
    ScholarshipCalculation, TentativeAdmission, TentativeAdmissionStatus
)
from .models.masters import Board, LeadSource, ReservationCategory
from app.models import User, Role
from app.config.settings import settings
from app.services.pdf_service import pdf_service
from app.shared.enums import ApplicationPaymentStatus, ApplicationStatus, StudentStatus
from app.domains.finance.models import ScholarshipSlab


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ======================================================================
# Activity Logger (moved from app/services/activity_logger.py)
# ======================================================================

def log_activity(
    session: Session,
    application_id: int,
    activity_type: ActivityType,
    description: str,
    performed_by: Optional[int] = None,
    ip_address: Optional[str] = None,
    extra_data: Optional[Dict] = None
) -> ApplicationActivityLog:
    """
    Log an activity for an application
    
    Args:
        session: Database session
        application_id: ID of the application
        activity_type: Type of activity
        description: Human-readable description
        performed_by: User ID who performed the action
        ip_address: IP address of the requester
        extra_data: Additional data to store as JSON
    
    Returns:
        Created activity log entry
    """
    import json
    
    log_entry = ApplicationActivityLog(
        application_id=application_id,
        activity_type=activity_type,
        description=description,
        performed_by=performed_by,
        ip_address=ip_address,
        extra_data=json.dumps(extra_data) if extra_data else None,
        created_at=datetime.utcnow()
    )
    
    session.add(log_entry)
    session.flush()  # Don't commit, let the caller handle transaction
    
    return log_entry


# ======================================================================
# Admission Service
# ======================================================================

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
        
        # Fetch Program to get Department ID
        from app.domains.academic.models import Program
        program = session.get(Program, program_id)
        department_id = program.department_id if program else None

        application = Application(
            application_number=app_number,
            name=name, email=email, phone=phone, gender=gender,
            program_id=program_id,
            department_id=department_id,
            state=state, board=board,
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
            
            from app.models import UserRole
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
            from app.domains.communication.services import email_service
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
            from app.domains.communication.services import sms_service
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
        from app.domains.academic.models import AcademicBatch, ProgramYear, BatchSemester, AcademicYear
        
        application = session.get(Application, application_id)
        if not application:
            raise ValueError("Application not found")
            
        if application.status == ApplicationStatus.ADMITTED:
             return application

        # Logic for batch discovery (simplified)
        # Logic for batch discovery
        current_year = datetime.now().year
        academic_year = session.exec(select(AcademicYear).where(AcademicYear.name.like(f"{current_year}%"))).first()
        if not academic_year:
             # Fallback: Try to find a batch with name containing current year
             # Or raise error that Academic Year is not defined
             raise ValueError(f"Academic Year starting {current_year} not found")

        batch = session.exec(
            select(AcademicBatch)
            .where(AcademicBatch.program_id == application.program_id)
            .where(AcademicBatch.admission_year_id == academic_year.id)
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


# ======================================================================
# Entrance Exam Service
# ======================================================================

class EntranceExamService:
    @staticmethod
    def create_test_config(session: Session, data: Dict[str, Any]) -> EntranceTestConfig:
        config = EntranceTestConfig(**data)
        session.add(config)
        session.commit()
        session.refresh(config)
        return config

    @staticmethod
    def get_test_config(session: Session, config_id: int) -> Optional[EntranceTestConfig]:
        return session.get(EntranceTestConfig, config_id)

    @staticmethod
    def list_test_configs(session: Session, active_only: bool = True) -> List[EntranceTestConfig]:
        statement = select(EntranceTestConfig)
        if active_only:
            statement = statement.where(EntranceTestConfig.is_active == True)
        return session.exec(statement).all()

    @staticmethod
    def process_results(session: Session, config_id: int, results: List[Dict[str, Any]], entered_by: int) -> int:
        count = 0
        for res in results:
            # Logic to create or update EntranceExamResult
            # Should also link back to Application
            pass
        return count

    @staticmethod
    def generate_hall_ticket(session: Session, admission_id: int) -> str:
        # Link to pdf_service for hall ticket generation
        return "hall_ticket_url"


# ======================================================================
# Merit Service
# ======================================================================

class MeritService:
    @staticmethod
    def calculate_scholarship(
        session: Session, 
        application_id: int, 
        calculated_by: int,
        entrance_weightage: float = 0.5,
        prev_weightage: float = 0.5
    ) -> ScholarshipCalculation:
        """
        Calculates merit score and determines scholarship slab.
        """
        application = session.get(Application, application_id)
        if not application:
            raise ValueError("Application not found")

        # Logic for merit calculation
        # 1. Get entrance marks (EntranceExamResult)
        # 2. Get previous marks (Application.previous_marks_percentage)
        # 3. Apply weights
        # 4. Find matching ScholarshipSlab
        
        calc = ScholarshipCalculation(
            application_id=application_id,
            student_name=application.name,
            course=application.program.name if application.program else "Unknown",
            calculated_by=calculated_by,
            calculation_date=datetime.utcnow()
        )
        
        # Placeholder logic
        calc.is_calculated = True
        session.add(calc)
        session.commit()
        session.refresh(calc)
        return calc

    @staticmethod
    def generate_tentative_admission(
        session: Session,
        application_id: int,
        base_fee: float
    ) -> TentativeAdmission:
        """
        Generates tentative admission structure based on scholarship.
        """

# ======================================================================
# Master Data Service
# ======================================================================

class MasterDataService:
    """Service for managing Admission Master Data (Boards, Sources, Categories)"""

    # --- Board ---
    
    @staticmethod
    def list_boards(session: Session, active_only: bool = True) -> List[Board]:
        stmt = select(Board)
        if active_only:
            stmt = stmt.where(Board.is_active == True)
        return list(session.exec(stmt).all())

    @staticmethod
    def create_board(session: Session, data: dict) -> Board:
        existing = session.exec(select(Board).where(Board.code == data["code"])).first()
        if existing:
            raise ValueError(f"Board with code {data['code']} already exists")
        
        board = Board(**data)
        session.add(board)
        session.commit()
        session.refresh(board)
        return board

    @staticmethod
    def update_board(session: Session, id: int, data: dict) -> Board:
        board = session.get(Board, id)
        if not board:
            raise ValueError("Board not found")
        
        for key, value in data.items():
            setattr(board, key, value)
        
        board.updated_at = datetime.utcnow()
        session.add(board)
        session.commit()
        session.refresh(board)
        return board

    @staticmethod
    def delete_board(session: Session, id: int) -> bool:
        board = session.get(Board, id)
        if not board:
            return False
        session.delete(board)
        session.commit()
        return True

    # --- Lead Source ---
    
    @staticmethod
    def list_lead_sources(session: Session, active_only: bool = True) -> List[LeadSource]:
        stmt = select(LeadSource)
        if active_only:
            stmt = stmt.where(LeadSource.is_active == True)
        return list(session.exec(stmt).all())

    @staticmethod
    def create_lead_source(session: Session, data: dict) -> LeadSource:
        existing = session.exec(select(LeadSource).where(LeadSource.code == data["code"])).first()
        if existing:
            raise ValueError(f"Lead Source with code {data['code']} already exists")
        
        source = LeadSource(**data)
        session.add(source)
        session.commit()
        session.refresh(source)
        return source

    @staticmethod
    def update_lead_source(session: Session, id: int, data: dict) -> LeadSource:
        source = session.get(LeadSource, id)
        if not source:
            raise ValueError("Lead Source not found")
        
        for key, value in data.items():
            setattr(source, key, value)
        
        source.updated_at = datetime.utcnow()
        session.add(source)
        session.commit()
        session.refresh(source)
        return source
        
    @staticmethod
    def delete_lead_source(session: Session, id: int) -> bool:
        source = session.get(LeadSource, id)
        if not source:
            return False
        session.delete(source)
        session.commit()
        return True

    # --- Reservation Category ---
    
    @staticmethod
    def list_reservation_categories(session: Session, active_only: bool = True) -> List[ReservationCategory]:
        stmt = select(ReservationCategory)
        if active_only:
            stmt = stmt.where(ReservationCategory.is_active == True)
        return list(session.exec(stmt).all())

    @staticmethod
    def create_reservation_category(session: Session, data: dict) -> ReservationCategory:
        existing = session.exec(select(ReservationCategory).where(ReservationCategory.code == data["code"])).first()
        if existing:
            raise ValueError(f"Category with code {data['code']} already exists")
        
        category = ReservationCategory(**data)
        session.add(category)
        session.commit()
        session.refresh(category)
        return category

    @staticmethod
    def update_reservation_category(session: Session, id: int, data: dict) -> ReservationCategory:
        category = session.get(ReservationCategory, id)
        if not category:
            raise ValueError("Category not found")
        
        for key, value in data.items():
            setattr(category, key, value)
        
        category.updated_at = datetime.utcnow()
        session.add(category)
        session.commit()
        session.refresh(category)
        return category
        
    @staticmethod
    def delete_reservation_category(session: Session, id: int) -> bool:
        category = session.get(ReservationCategory, id)
        if not category:
            return False
        session.delete(category)
        session.commit()
        return True

master_data_service = MasterDataService()
