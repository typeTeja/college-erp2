"""
Fee Management Service Layer

Handles all fee-related business logic including:
- Fee structure management
- Student fee assignment
- Installment generation
- Fine calculation
- Payment processing
"""
from typing import List, Optional, Dict
from datetime import date, datetime, timedelta
from decimal import Decimal
from sqlmodel import Session, select
from fastapi import HTTPException

from app.models.fee import (
    FeeStructure, StudentFee, StudentFeeInstallment,
    FeePayment, FeeConcession, FeeFine, PaymentStatus
)
from app.models.student import Student
from app.schemas.fee import (
    FeeStructureCreate, StudentFeeCreate, FeePaymentCreate,
    FeeConcessionCreate, FineCalculationRequest
)


class FeeService:
    """Service for fee management operations"""
    
    @staticmethod
    def create_fee_structure(
        session: Session,
        fee_structure_data: FeeStructureCreate
    ) -> FeeStructure:
        """Create a new fee structure"""
        # Calculate total annual fee from components
        total = (
            fee_structure_data.tuition_fee +
            fee_structure_data.library_fee +
            fee_structure_data.lab_fee +
            fee_structure_data.uniform_fee +
            fee_structure_data.caution_deposit +
            fee_structure_data.digital_fee +
            fee_structure_data.miscellaneous_fee
        )
        
        # Calculate installment amount
        installment_amount = total / fee_structure_data.number_of_installments
        
        fee_structure = FeeStructure(
            **fee_structure_data.model_dump(),
            total_annual_fee=total,
            total_amount=total,  # Legacy field
            installment_amount=installment_amount
        )
        
        session.add(fee_structure)
        session.commit()
        session.refresh(fee_structure)
        return fee_structure
    
    @staticmethod
    def assign_fee_to_student(
        session: Session,
        student_id: int,
        fee_structure_id: int,
        academic_year: str,
        concession_percentage: float = 0.0,
        old_dues: Decimal = Decimal("0.00")
    ) -> StudentFee:
        """Assign a fee structure to a student"""
        # Get fee structure
        fee_structure = session.get(FeeStructure, fee_structure_id)
        if not fee_structure:
            raise HTTPException(status_code=404, detail="Fee structure not found")
        
        # Get student
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Calculate concession
        concession_amount = fee_structure.total_annual_fee * Decimal(str(concession_percentage / 100))
        net_annual_fee = fee_structure.total_annual_fee - concession_amount
        
        # Calculate installment amount
        installment_amount = net_annual_fee / fee_structure.number_of_installments
        
        # Create student fee
        student_fee = StudentFee(
            student_id=student_id,
            fee_structure_id=fee_structure_id,
            academic_year=academic_year,
            total_annual_fee=fee_structure.total_annual_fee,
            concession_amount=concession_amount,
            net_annual_fee=net_annual_fee,
            number_of_installments=fee_structure.number_of_installments,
            installment_amount=installment_amount,
            old_dues=old_dues,
            total_paid=Decimal("0.00"),
            total_pending=net_annual_fee + old_dues,
            total_fee=fee_structure.total_annual_fee,  # Legacy
            paid_amount=Decimal("0.00")  # Legacy
        )
        
        session.add(student_fee)
        session.commit()
        session.refresh(student_fee)
        
        # Generate installments
        FeeService.generate_installments(session, student_fee.id)
        
        return student_fee
    
    @staticmethod
    def generate_installments(
        session: Session,
        student_fee_id: int,
        start_date: Optional[date] = None
    ) -> List[StudentFeeInstallment]:
        """Generate installments for a student fee"""
        student_fee = session.get(StudentFee, student_fee_id)
        if not student_fee:
            raise HTTPException(status_code=404, detail="Student fee not found")
        
        # Default start date to today
        if not start_date:
            start_date = date.today()
        
        installments = []
        installment_amount = student_fee.installment_amount
        
        # Distribute old dues in first installment
        first_installment_total = installment_amount + student_fee.old_dues
        
        for i in range(1, student_fee.number_of_installments + 1):
            # Calculate due date (every 3 months)
            due_date = start_date + timedelta(days=90 * (i - 1))
            
            # First installment includes old dues
            total_amount = first_installment_total if i == 1 else installment_amount
            old_dues_included = student_fee.old_dues if i == 1 else Decimal("0.00")
            
            installment = StudentFeeInstallment(
                student_fee_id=student_fee_id,
                student_id=student_fee.student_id,
                installment_number=i,
                amount=installment_amount,
                due_date=due_date,
                old_dues_included=old_dues_included,
                total_amount=total_amount,
                paid_amount=Decimal("0.00"),
                payment_status="pending"
            )
            
            session.add(installment)
            installments.append(installment)
        
        session.commit()
        return installments
    
    @staticmethod
    def record_payment(
        session: Session,
        payment_data: FeePaymentCreate,
        user_id: Optional[int] = None
    ) -> FeePayment:
        """Record a fee payment"""
        student_fee = session.get(StudentFee, payment_data.student_fee_id)
        if not student_fee:
            raise HTTPException(status_code=404, detail="Student fee not found")
        
        # Create payment record
        payment = FeePayment(
            **payment_data.model_dump(),
            payment_date=datetime.utcnow()
        )
        
        session.add(payment)
        
        # Update student fee totals
        if payment.payment_status == PaymentStatus.SUCCESS:
            student_fee.total_paid += payment.amount
            student_fee.total_pending -= payment.amount
            student_fee.paid_amount = student_fee.total_paid  # Legacy
            
            # Update installments
            FeeService._allocate_payment_to_installments(
                session, student_fee.id, payment.amount
            )
        
        session.commit()
        session.refresh(payment)
        return payment
    
    @staticmethod
    def _allocate_payment_to_installments(
        session: Session,
        student_fee_id: int,
        amount: Decimal
    ):
        """Allocate payment amount to pending installments"""
        # Get pending installments ordered by due date
        stmt = select(StudentFeeInstallment).where(
            StudentFeeInstallment.student_fee_id == student_fee_id,
            StudentFeeInstallment.payment_status.in_(["pending", "partial"])
        ).order_by(StudentFeeInstallment.due_date)
        
        installments = session.exec(stmt).all()
        
        remaining_amount = amount
        
        for installment in installments:
            if remaining_amount <= 0:
                break
            
            pending = installment.total_amount - installment.paid_amount
            
            if remaining_amount >= pending:
                # Fully pay this installment
                installment.paid_amount = installment.total_amount
                installment.payment_status = "paid"
                installment.payment_date = date.today()
                remaining_amount -= pending
            else:
                # Partially pay this installment
                installment.paid_amount += remaining_amount
                installment.payment_status = "partial"
                remaining_amount = Decimal("0.00")
        
        session.commit()
    
    @staticmethod
    def calculate_fine(
        session: Session,
        installment_id: int,
        fine_per_day: Decimal = Decimal("10.00")
    ) -> Decimal:
        """Calculate fine for overdue installment"""
        installment = session.get(StudentFeeInstallment, installment_id)
        if not installment:
            raise HTTPException(status_code=404, detail="Installment not found")
        
        # Check if overdue
        if installment.payment_status == "paid":
            return Decimal("0.00")
        
        today = date.today()
        if today <= installment.due_date:
            return Decimal("0.00")
        
        # Calculate days overdue
        days_overdue = (today - installment.due_date).days
        fine_amount = fine_per_day * days_overdue
        
        # Update installment fine
        installment.fine_amount = fine_amount
        session.commit()
        
        return fine_amount
    
    @staticmethod
    def apply_concession(
        session: Session,
        concession_data: FeeConcessionCreate,
        approved_by: Optional[int] = None
    ) -> FeeConcession:
        """Apply a fee concession"""
        student_fee = session.get(StudentFee, concession_data.student_fee_id)
        if not student_fee:
            raise HTTPException(status_code=404, detail="Student fee not found")
        
        concession = FeeConcession(
            **concession_data.model_dump(),
            approved_by=str(approved_by) if approved_by else None,
            approved_at=datetime.utcnow(),
            status="approved"
        )
        
        session.add(concession)
        
        # Update student fee
        student_fee.concession_amount += concession.amount
        student_fee.net_annual_fee = student_fee.total_annual_fee - student_fee.concession_amount
        student_fee.total_pending = student_fee.net_annual_fee - student_fee.total_paid
        
        session.commit()
        session.refresh(concession)
        return concession
    
    @staticmethod
    def waive_fine(
        session: Session,
        installment_id: int,
        waiver_reason: str,
        waived_by: int
    ) -> StudentFeeInstallment:
        """Waive fine for an installment"""
        installment = session.get(StudentFeeInstallment, installment_id)
        if not installment:
            raise HTTPException(status_code=404, detail="Installment not found")
        
        installment.fine_waived = True
        installment.fine_waived_by = waived_by
        installment.fine_waived_date = datetime.utcnow()
        installment.fine_waiver_reason = waiver_reason
        installment.fine_amount = Decimal("0.00")
        
        session.commit()
        session.refresh(installment)
        return installment
    
    @staticmethod
    def get_student_fee_summary(
        session: Session,
        student_id: int,
        academic_year: Optional[str] = None
    ) -> Dict:
        """Get fee summary for a student"""
        stmt = select(StudentFee).where(StudentFee.student_id == student_id)
        
        if academic_year:
            stmt = stmt.where(StudentFee.academic_year == academic_year)
        
        student_fees = session.exec(stmt).all()
        
        total_fee = sum(sf.total_annual_fee for sf in student_fees)
        total_paid = sum(sf.total_paid for sf in student_fees)
        total_pending = sum(sf.total_pending for sf in student_fees)
        total_concession = sum(sf.concession_amount for sf in student_fees)
        
        return {
            "student_id": student_id,
            "academic_year": academic_year,
            "total_fee": float(total_fee),
            "total_paid": float(total_paid),
            "total_pending": float(total_pending),
            "total_concession": float(total_concession),
            "fee_records": len(student_fees)
        }
