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
    ) -> tuple[str, str, bool]:
        """
        Create student portal account AFTER payment completion
        If user exists, links application to existing user.
        
        Returns: (portal_username, portal_password, is_new_account)
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
        
        # Check if user with email already exists
        existing_user = session.exec(select(User).where(User.email == application.email)).first()
        
        if existing_user:
            # Link to existing user
            portal_user = existing_user
            portal_username = existing_user.username
            # We don't know the password
            portal_password = None 
            is_new_account = False
            print(f"Linking application {application.id} to existing user {portal_user.id}")
        else:
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
            
            # Assign student role upon creation
            from app.models.user_role import UserRole
            user_role = UserRole(user_id=portal_user.id, role_id=student_role.id)
            session.add(user_role)
            is_new_account = True
        
        # Link user to application
        application.portal_user_id = portal_user.id
        if portal_password:
             application.portal_password_hash = AdmissionService.hash_password(portal_password)
        
        # Ensure student role exists for linked user
        student_role = session.exec(select(Role).where(Role.name == "STUDENT")).first()
        # Check if user has student role
        # (This check is a bit complex with sqlmodel relationships, maybe just try to add and ignore duplicate or check user.roles)
        # Simplified: If we created the user, we added the role. If existing, we assume/add it.
        # Let's simple skip if existing for now to avoid complexity, or just leave as is since we removed the adding logic from above for existing users?
        # Re-adding logic for existing users:
        if existing_user and student_role:
             # Check if already has role
             # Assuming we can't easily check link table directly without query?
             # Let's iterate user.roles if loaded, or query link table
             from app.models.user_role import UserRole
             existing_link = session.exec(select(UserRole).where(UserRole.user_id == portal_user.id, UserRole.role_id == student_role.id)).first()
             if not existing_link:
                 user_role = UserRole(user_id=portal_user.id, role_id=student_role.id)
                 session.add(user_role)
        
        # Log activity
        activity_log = ApplicationActivityLog(
            application_id=application.id,
            activity_type=ActivityType.PAYMENT_SUCCESS,
            description="Portal account created after payment completion",
        )
        session.add(activity_log)
        
        session.add(application)
        session.commit()
        session.refresh(application)
        
        return portal_username, portal_password, is_new_account
    @staticmethod
    def generate_receipt(
        application: Application,
        payment_id: str,
        amount: float,
        payment_date: datetime,
        program_name: str = None
    ) -> str:
        """
        Generate PDF Receipt for Application Fee
        Returns: S3 URL or relative path to generated PDF
        """
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import letter
            from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from app.services.storage_service import storage_service
            import os
            
            # Create PDF in temp directory
            filename = f"Receipt_{application.application_number}_{payment_id}.pdf"
            temp_path = f"/tmp/{filename}"
            
            doc = SimpleDocTemplate(temp_path, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            
            # Title
            title_style = ParagraphStyle('Title', parent=styles['Heading1'], alignment=1, spaceAfter=20)
            elements.append(Paragraph("Payment Receipt", title_style))
            elements.append(Spacer(1, 12))
            
            # Info Table
            data = [
                ["Receipt No:", f"REC-{payment_id}"],
                ["Date:", payment_date.strftime("%d-%b-%Y %H:%M")],
                ["Application No:", application.application_number],
                ["Applicant Name:", application.name],
                ["Program:", program_name or str(application.program_id)],
                ["Payment Mode:", "Online (Easebuzz)"],
                ["Transaction ID:", payment_id],
                ["Amount Paid:", f"INR {amount:.2f}"],
                ["Status:", "SUCCESS"]
            ]
            
            table = Table(data, colWidths=[150, 300])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('BACKGROUND', (0, 0), (1, -1), colors.whitesmoke),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 20))
            
            # Footer
            footer_text = "This is a computer generated receipt and does not require a signature."
            elements.append(Paragraph(footer_text, styles['Normal']))
            
            doc.build(elements)
            
            # Upload to Storage (S3/MinIO)
            with open(temp_path, "rb") as f:
                content = f.read()
                file_url = storage_service.upload_bytes(
                    file_content=content,
                    filename=filename,
                    content_type="application/pdf",
                    prefix="receipts"
                )
            
            # Cleanup
            os.remove(temp_path)
            
            return file_url
            
        except Exception as e:
            print(f"Error generating receipt PDF: {str(e)}")
            return ""

    @staticmethod
    def process_payment_completion(
        session: Session,
        application_id: int,
        transaction_id: str,
        amount: float,
        payment_date: datetime = None,
        background_tasks = None,
        payment_method: str = "UNKNOWN"
    ) -> bool:
        """
        Process successful payment (Offline or Online)
        1. Update Status
        2. Create Portal Account
        3. Generate Receipt
        4. Send Emails
        """
        try:
            from app.services.email_service import email_service
            from app.models.admissions import ApplicationDocument, DocumentType, DocumentStatus
            
            application = session.get(Application, application_id)
            if not application:
                return False
            
            # Update Payment Status
            application.status = ApplicationStatus.PAID
            application.payment_status = 'PAID'
            application.payment_id = transaction_id
            application.payment_date = payment_date or datetime.utcnow()
            
            session.add(application)
            
            # Update ApplicationPayment Record
            from app.models.admissions import ApplicationPayment, ApplicationPaymentStatus
            payment_stmt = select(ApplicationPayment).where(
                ApplicationPayment.transaction_id == transaction_id
            )
            payment_record = session.exec(payment_stmt).first()
            
            if payment_record:
                payment_record.status = ApplicationPaymentStatus.SUCCESS
                payment_record.paid_at = application.payment_date
                session.add(payment_record)
            else:
                # Create if missing (e.g. manual payment or legacy)
                payment_record = ApplicationPayment(
                    application_id=application.id,
                    transaction_id=transaction_id,
                    amount=amount,
                    status=ApplicationPaymentStatus.SUCCESS,
                    payment_method=payment_method,
                    paid_at=application.payment_date
                )
                session.add(payment_record)

            session.flush()

            # Fetch Program Name
            from app.models.program import Program
            program_obj = session.get(Program, application.program_id)
            program_name = program_obj.name if program_obj else str(application.program_id)

            # Generate Receipt
            receipt_url = AdmissionService.generate_receipt(
                application=application,
                payment_id=transaction_id,
                amount=amount,
                payment_date=application.payment_date,
                program_name=program_name
            )
            
            # Store Receipt as Document
            if receipt_url:
                receipt_doc = ApplicationDocument(
                    application_id=application.id,
                    document_type=DocumentType.OTHER, # Using OTHER to avoid enum migration issues
                    file_url=receipt_url,
                    file_name="Payment Receipt",
                    file_size=0, # Unknown size
                    status=DocumentStatus.VERIFIED,
                    verified_by=None, # System verified
                    verified_at=datetime.utcnow()
                )
                session.add(receipt_doc)
            
            # Create Portal Account
            portal_username, portal_password, is_new_account = (None, None, False)
            try:
                portal_username, portal_password, is_new_account = AdmissionService.create_portal_account_after_payment(
                    session=session,
                    application=application
                )
            except ValueError as e:
                print(f"Account creation skipped: {e}")
                
            session.commit()
            session.refresh(application)
            
            if background_tasks:
                # Send Payment Success Email (Always)
                background_tasks.add_task(
                    email_service.send_payment_success,
                    to_email=application.email,
                    name=application.name,
                    application_number=application.application_number,
                    amount=amount,
                    transaction_id=transaction_id,
                    receipt_url=receipt_url
                )
                
                # Send Credentials OR Account Link Email
                if is_new_account and portal_username and portal_password:
                     # New User -> Send Credentials
                     background_tasks.add_task(
                        email_service.send_portal_credentials,
                        to_email=application.email,
                        name=application.name,
                        application_number=application.application_number,
                        username=portal_username,
                        password=portal_password,
                        portal_url=f"{settings.PORTAL_BASE_URL}/login"
                    )
                elif not is_new_account and portal_username:
                     # Existing User -> Send "Linked" notification
                     background_tasks.add_task(
                        email_service.send_existing_user_linked,
                        to_email=application.email,
                        name=application.name,
                        application_number=application.application_number,
                        portal_url=f"{settings.PORTAL_BASE_URL}"
                     )
            
            return True
        except Exception as e:
            print(f"Error processing payment completion: {str(e)}")
            return False

    @staticmethod
    def soft_delete_application(
        session: Session,
        application_id: int,
        deleted_by: int,
        reason: str
    ) -> Application:
        """
        Soft delete an application.
        Strictly prevents deletion of PAID applications.
        """
        application = session.get(Application, application_id)
        if not application:
            raise ValueError("Application not found")
            
        # Safety Check: Cannot delete PAID applications
        if application.status == ApplicationStatus.PAID or application.payment_status in ['PAID', 'SUCCESS']:
             raise ValueError("Cannot delete a PAID application. This action is restricted for data integrity.")
             
        # Perform Soft Delete
        application.is_deleted = True
        application.deleted_at = datetime.utcnow()
        application.deleted_by = deleted_by
        application.delete_reason = reason
        
        session.add(application)
        
        # Log Activity
        log = ApplicationActivityLog(
            application_id=application.id,
            activity_type=ActivityType.APPLICATION_DELETED,
            description=f"Application soft-deleted by user {deleted_by}. Reason: {reason}",
            performed_by=deleted_by
        )
        session.add(log)
        session.commit()
        session.refresh(application)
        return application

    @staticmethod
    def restore_application(
        session: Session,
        application_id: int,
        restored_by: int
    ) -> Application:
        """
        Restore a soft-deleted application
        """
        application = session.get(Application, application_id)
        if not application:
            raise ValueError("Application not found")
            
        if not application.is_deleted:
            return application
            
        # Restore
        application.is_deleted = False
        application.deleted_at = None
        application.deleted_by = None
        application.delete_reason = None
        
        session.add(application)
        
        # Log Activity
        log = ApplicationActivityLog(
            application_id=application.id,
            activity_type=ActivityType.APPLICATION_RESTORED,
            description=f"Application restored by user {restored_by}",
            performed_by=restored_by
        )
        session.add(log)
        session.commit()
        session.refresh(application)
        return application

    @staticmethod
    def cleanup_test_applications(
        session: Session,
        performed_by: int
    ) -> int:
        """
        Bulk cleanup of 'Test' applications
        Target: Unpaid applications with 'test' in name or email
        """
        from sqlmodel import or_, col
        
        # Find candidates
        # Not PAID, Not Deleted, Name/Email contains 'test' (case insensitive)
        statement = select(Application).where(
            Application.is_deleted == False,
            or_(
                Application.status != ApplicationStatus.PAID,
                Application.payment_status.notin_(['PAID', 'SUCCESS'])
            ),
            or_(
                col(Application.name).ilike('%test%'),
                col(Application.email).ilike('%test%')
            )
        )
        
        applications = session.exec(statement).all()
        count = 0
        
        for app in applications:
            # Double check payment status to be absolutely safe
            if app.status == ApplicationStatus.PAID or app.payment_status in ['PAID', 'SUCCESS']:
                continue
                
            app.is_deleted = True
            app.deleted_at = datetime.utcnow()
            app.deleted_by = performed_by
            app.delete_reason = "Bulk Cleanup: Test Data"
            session.add(app)
            
            # Log individual activity
            log = ApplicationActivityLog(
                application_id=app.id,
                activity_type=ActivityType.APPLICATION_DELETED,
                description=f"Bulk cleanup (Test Data)",
                performed_by=performed_by
            )
            session.add(log)
            count += 1
            
        if count > 0:
            # Log bulk activity
            # We don't have a specific bulk log table, but we can log to system logs or just commit
            pass
            
        session.commit()
        return count
