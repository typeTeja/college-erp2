from typing import List, Optional
from datetime import datetime, date
from sqlmodel import Session, select, desc, func
from app.models.odc import (
    ODCHotel, ODCRequest, StudentODCApplication, 
    ODCStatus, ApplicationStatus, ODCBilling, ODCPayout,
    BillingStatus, PaymentMethod
)
from app.schemas.odc import (
    ODCHotelCreate, ODCRequestCreate, ApplicationCreate, SelectionUpdate,
    StudentFeedbackSubmit, HotelFeedbackSubmit, BillingCreate, BillingMarkPaid,
    PayoutBatchProcess
)
from app.models.student import Student

class ODCService:
    def __init__(self, session: Session):
        self.session = session

    # Hotel Management
    def create_hotel(self, hotel_data: ODCHotelCreate) -> ODCHotel:
        hotel = ODCHotel(**hotel_data.model_dump())
        self.session.add(hotel)
        self.session.commit()
        self.session.refresh(hotel)
        return hotel

    def get_hotels(self, skip: int = 0, limit: int = 100) -> List[ODCHotel]:
        return self.session.exec(
            select(ODCHotel).where(ODCHotel.is_active == True).offset(skip).limit(limit)
        ).all()

    # Request Management
    def create_request(self, request_data: ODCRequestCreate, user_id: int) -> ODCRequest:
        request = ODCRequest(
            **request_data.model_dump(),
            created_by_id=user_id,
            status=ODCStatus.OPEN
        )
        self.session.add(request)
        self.session.commit()
        self.session.refresh(request)
        return request

    def get_requests(self, status: Optional[ODCStatus] = None) -> List[ODCRequest]:
        query = select(ODCRequest)
        if status:
            query = query.where(ODCRequest.status == status)
        query = query.order_by(desc(ODCRequest.event_date))
        return self.session.exec(query).all()

    def get_request_by_id(self, request_id: int) -> Optional[ODCRequest]:
        return self.session.get(ODCRequest, request_id)

    # Application Management
    def apply_for_odc(self, student_id: int, request_id: int) -> StudentODCApplication:
        # Check if already applied
        existing = self.session.exec(
            select(StudentODCApplication).where(
                StudentODCApplication.student_id == student_id,
                StudentODCApplication.request_id == request_id
            )
        ).first()
        
        if existing:
            raise ValueError("Student has already applied for this ODC")
            
        # Check vacancies
        request = self.get_request_by_id(request_id)
        if not request or request.status != ODCStatus.OPEN:
            raise ValueError("ODC Request is closed or invalid")

        application = StudentODCApplication(
            request_id=request_id,
            student_id=student_id,
            status=ApplicationStatus.APPLIED
        )
        self.session.add(application)
        self.session.commit()
        self.session.refresh(application)
        return application

    def update_selections(self, update_data: SelectionUpdate) -> List[StudentODCApplication]:
        updated_apps = []
        for app_id in update_data.application_ids:
            app = self.session.get(StudentODCApplication, app_id)
            if app:
                app.status = update_data.status
                if update_data.remarks:
                    app.admin_remarks = update_data.remarks
                self.session.add(app)
                updated_apps.append(app)
        
        self.session.commit()
        return updated_apps
    
    def get_student_applications(self, student_id: int) -> List[StudentODCApplication]:
        return self.session.exec(
            select(StudentODCApplication)
            .where(StudentODCApplication.student_id == student_id)
            .order_by(desc(StudentODCApplication.applied_at))
        ).all()
    
    # Feedback Management
    def submit_student_feedback(
        self, 
        application_id: int, 
        student_id: int, 
        feedback_data: StudentFeedbackSubmit
    ) -> StudentODCApplication:
        """Submit student feedback for an attended ODC event"""
        app = self.session.get(StudentODCApplication, application_id)
        
        if not app or app.student_id != student_id:
            raise ValueError("Application not found or unauthorized")
        
        if app.status != ApplicationStatus.ATTENDED:
            raise ValueError("Can only submit feedback for attended events")
        
        app.student_feedback = feedback_data.student_feedback
        app.student_rating = feedback_data.student_rating
        
        self.session.add(app)
        self.session.commit()
        self.session.refresh(app)
        return app
    
    def submit_hotel_feedback(
        self, 
        application_id: int, 
        feedback_data: HotelFeedbackSubmit
    ) -> StudentODCApplication:
        """Submit hotel/admin feedback for a student"""
        app = self.session.get(StudentODCApplication, application_id)
        
        if not app:
            raise ValueError("Application not found")
        
        app.hotel_feedback = feedback_data.hotel_feedback
        app.hotel_rating = feedback_data.hotel_rating
        
        self.session.add(app)
        self.session.commit()
        self.session.refresh(app)
        return app
    
    # Billing Management
    def generate_billing(
        self, 
        request_id: int, 
        user_id: int,
        billing_data: BillingCreate
    ) -> ODCBilling:
        """Generate billing/invoice for a completed ODC event"""
        request = self.get_request_by_id(request_id)
        
        if not request:
            raise ValueError("Request not found")
        
        if request.status != ODCStatus.COMPLETED:
            raise ValueError("Can only generate billing for completed events")
        
        # Check if billing already exists
        existing = self.session.exec(
            select(ODCBilling).where(ODCBilling.request_id == request_id)
        ).first()
        
        if existing:
            raise ValueError("Billing already exists for this request")
        
        # Count attended students
        attended_count = self.session.exec(
            select(func.count(StudentODCApplication.id))
            .where(
                StudentODCApplication.request_id == request_id,
                StudentODCApplication.status == ApplicationStatus.ATTENDED
            )
        ).one()
        
        if attended_count == 0:
            raise ValueError("No students attended this event")
        
        # Generate invoice number
        invoice_number = f"ODC-{request_id}-{datetime.now().strftime('%Y%m%d')}"
        
        total_amount = attended_count * request.pay_amount
        
        billing = ODCBilling(
            request_id=request_id,
            invoice_number=invoice_number,
            total_students=attended_count,
            amount_per_student=request.pay_amount,
            total_amount=total_amount,
            invoice_date=billing_data.invoice_date,
            due_date=billing_data.due_date,
            notes=billing_data.notes,
            created_by_id=user_id,
            status=BillingStatus.DRAFT
        )
        
        self.session.add(billing)
        self.session.commit()
        self.session.refresh(billing)
        return billing
    
    def get_billings(self, status: Optional[BillingStatus] = None) -> List[ODCBilling]:
        """Get all billings, optionally filtered by status"""
        query = select(ODCBilling)
        if status:
            query = query.where(ODCBilling.status == status)
        query = query.order_by(desc(ODCBilling.created_at))
        return self.session.exec(query).all()
    
    def mark_billing_paid(
        self, 
        billing_id: int, 
        payment_data: BillingMarkPaid
    ) -> ODCBilling:
        """Mark a billing as paid"""
        billing = self.session.get(ODCBilling, billing_id)
        
        if not billing:
            raise ValueError("Billing not found")
        
        if billing.status == BillingStatus.PAID:
            raise ValueError("Billing already marked as paid")
        
        billing.status = BillingStatus.PAID
        billing.payment_method = payment_data.payment_method
        billing.payment_reference = payment_data.payment_reference
        billing.paid_date = payment_data.paid_date
        if payment_data.notes:
            billing.notes = f"{billing.notes or ''}\n{payment_data.notes}".strip()
        billing.updated_at = datetime.utcnow()
        
        self.session.add(billing)
        self.session.commit()
        self.session.refresh(billing)
        return billing
    
    # Payout Management
    def get_pending_payouts(self) -> List[StudentODCApplication]:
        """Get all applications eligible for payout (ATTENDED but not paid)"""
        return self.session.exec(
            select(StudentODCApplication)
            .where(
                StudentODCApplication.status == ApplicationStatus.ATTENDED,
                StudentODCApplication.payout_status == "PENDING"
            )
            .order_by(StudentODCApplication.applied_at)
        ).all()
    
    def process_payouts(
        self, 
        user_id: int,
        payout_data: PayoutBatchProcess
    ) -> List[ODCPayout]:
        """Process batch payouts for multiple applications"""
        payouts = []
        
        for app_id in payout_data.application_ids:
            app = self.session.get(StudentODCApplication, app_id)
            
            if not app:
                continue
            
            if app.status != ApplicationStatus.ATTENDED:
                continue
            
            if app.payout_status == "PAID":
                continue
            
            # Check if payout already exists
            existing_payout = self.session.exec(
                select(ODCPayout).where(ODCPayout.application_id == app_id)
            ).first()
            
            if existing_payout:
                continue
            
            # Get request to determine payout amount
            request = self.get_request_by_id(app.request_id)
            if not request:
                continue
            
            # Create payout
            payout = ODCPayout(
                application_id=app_id,
                amount=request.pay_amount,
                payment_method=payout_data.payment_method,
                payout_date=payout_data.payout_date,
                notes=payout_data.notes,
                processed_by_id=user_id
            )
            
            # Update application
            app.payout_status = "PAID"
            app.payout_amount = request.pay_amount
            
            self.session.add(payout)
            self.session.add(app)
            payouts.append(payout)
        
        self.session.commit()
        return payouts

