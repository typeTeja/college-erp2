from typing import Dict, Optional
from datetime import datetime
from sqlmodel import Session, select
from fastapi import HTTPException
import secrets
import hashlib
import hmac

from ..models.gateway import (
    PaymentGatewayConfig, OnlinePayment, PaymentReceipt,
    PaymentStatus, OnlinePaymentMode
)
from app.domains.student.models.student import Student
from ..models.fee import StudentFee

class PaymentGatewayService:
    """Service for payment gateway operations"""
    
    @staticmethod
    def get_active_gateway(session: Session) -> PaymentGatewayConfig:
        """Get active payment gateway"""
        stmt = select(PaymentGatewayConfig).where(
            PaymentGatewayConfig.is_active == True,
            PaymentGatewayConfig.is_default == True
        )
        gateway = session.exec(stmt).first()
        if not gateway:
            raise HTTPException(status_code=404, detail="No active payment gateway configured")
        return gateway
    
    @staticmethod
    def initiate_payment(
        session: Session,
        student_id: int,
        student_fee_id: int,
        amount: float,
        payment_mode: Optional[str] = None
    ) -> OnlinePayment:
        """Initiate online payment"""
        student = session.get(Student, student_id)
        gateway = PaymentGatewayService.get_active_gateway(session)
        
        payment = OnlinePayment(
            student_id=student_id,
            student_fee_id=student_fee_id,
            payment_gateway_config_id=gateway.id,
            amount=amount,
            customer_name=student.name,
            customer_email=student.email or "",
            customer_phone=student.phone or ""
        )
        session.add(payment)
        session.commit()
        session.refresh(payment)
        return payment

gateway_service = PaymentGatewayService()
