from typing import List, Optional, Dict
from datetime import date, datetime, timedelta
from decimal import Decimal
from sqlmodel import Session, select
from fastapi import HTTPException

from ..models.fee import (
    FeeStructure, StudentFee, StudentFeeInstallment,
    FeePayment, FeeConcession, FeeFine, PaymentStatus
)
from app.domains.student.models.student import Student

class FeeService:
    """Service for fee management operations"""
    
    @staticmethod
    def create_fee_structure(
        session: Session,
        fee_structure_data: dict
    ) -> FeeStructure:
        """Create a new fee structure"""
        # Logic from fee_service.py
        total = sum([
            fee_structure_data.get(k, Decimal("0.00")) 
            for k in ["tuition_fee", "library_fee", "lab_fee", "uniform_fee", "caution_deposit", "digital_fee", "miscellaneous_fee"]
        ])
        
        num_installments = fee_structure_data.get("number_of_installments", 4)
        installment_amount = total / num_installments
        
        fee_structure = FeeStructure(
            **fee_structure_data,
            total_annual_fee=total,
            total_amount=total,
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
        fee_structure = session.get(FeeStructure, fee_structure_id)
        if not fee_structure:
            raise HTTPException(status_code=404, detail="Fee structure not found")
        
        concession_amount = fee_structure.total_annual_fee * Decimal(str(concession_percentage / 100))
        net_annual_fee = fee_structure.total_annual_fee - concession_amount
        installment_amount = net_annual_fee / fee_structure.number_of_installments
        
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
            total_fee=fee_structure.total_annual_fee,
            paid_amount=Decimal("0.00")
        )
        session.add(student_fee)
        session.commit()
        session.refresh(student_fee)
        
        # In actual project, this should call generate_installments
        return student_fee

fee_service = FeeService()
