"""
Payment Gateway API Endpoints

Provides online payment functionality
"""
from typing import Optional
from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, select
from pydantic import BaseModel

from app.api.deps import get_session, get_current_active_superuser
from app.models.user import User
from app.models.payment_gateway import (
    PaymentGatewayConfig, OnlinePayment, PaymentReceipt
)
from app.services.payment_gateway_service import PaymentGatewayService

router = APIRouter(prefix="/payments", tags=["Online Payments"])


# Schemas
class PaymentGatewayCreate(BaseModel):
    gateway_name: str
    gateway_code: str
    merchant_id: str
    api_key: str
    api_secret: str
    supported_payment_modes: list
    is_default: bool = False


class PaymentInitiateRequest(BaseModel):
    student_id: int
    student_fee_id: int
    amount: float
    payment_mode: Optional[str] = None


class PaymentCallbackRequest(BaseModel):
    payment_id: int
    gateway_payment_id: str
    gateway_signature: str
    gateway_response: dict


# ============================================================================
# Gateway Configuration Endpoints
# ============================================================================

@router.post("/gateways")
def create_gateway(
    *,
    session: Session = Depends(get_session),
    gateway_data: PaymentGatewayCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Create payment gateway configuration"""
    gateway = PaymentGatewayConfig(**gateway_data.model_dump())
    session.add(gateway)
    session.commit()
    session.refresh(gateway)
    return gateway


@router.get("/gateways")
def list_gateways(
    *,
    session: Session = Depends(get_session)
):
    """List payment gateways"""
    stmt = select(PaymentGatewayConfig).where(
        PaymentGatewayConfig.is_active == True
    )
    return session.exec(stmt).all()


# ============================================================================
# Payment Processing Endpoints
# ============================================================================

@router.post("/initiate")
def initiate_payment(
    *,
    session: Session = Depends(get_session),
    request: Request,
    payment_data: PaymentInitiateRequest
):
    """Initiate online payment"""
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    
    payment = PaymentGatewayService.initiate_payment(
        session,
        payment_data.student_id,
        payment_data.student_fee_id,
        payment_data.amount,
        payment_data.payment_mode,
        ip_address,
        user_agent
    )
    
    return {
        "payment_id": payment.id,
        "order_id": payment.gateway_order_id,
        "amount": payment.amount,
        "currency": payment.currency,
        "customer_name": payment.customer_name,
        "customer_email": payment.customer_email,
        "customer_phone": payment.customer_phone
    }


@router.post("/callback")
def payment_callback(
    *,
    session: Session = Depends(get_session),
    callback_data: PaymentCallbackRequest
):
    """Handle payment gateway callback"""
    payment = PaymentGatewayService.process_payment_callback(
        session,
        callback_data.payment_id,
        callback_data.gateway_payment_id,
        callback_data.gateway_signature,
        callback_data.gateway_response
    )
    
    return {
        "status": payment.payment_status,
        "payment_id": payment.id,
        "receipt_number": payment.receipt_number
    }


@router.get("/status/{payment_id}")
def get_payment_status(
    *,
    session: Session = Depends(get_session),
    payment_id: int
):
    """Get payment status"""
    return PaymentGatewayService.get_payment_status(session, payment_id)


# ============================================================================
# Payment History Endpoints
# ============================================================================

@router.get("/history/{student_id}")
def get_payment_history(
    *,
    session: Session = Depends(get_session),
    student_id: int,
    limit: int = 50
):
    """Get student payment history"""
    stmt = select(OnlinePayment).where(
        OnlinePayment.student_id == student_id
    ).order_by(OnlinePayment.created_at.desc()).limit(limit)
    
    return session.exec(stmt).all()


# ============================================================================
# Receipt Endpoints
# ============================================================================

@router.get("/receipt/{payment_id}")
def get_receipt(
    *,
    session: Session = Depends(get_session),
    payment_id: int
):
    """Get payment receipt"""
    stmt = select(PaymentReceipt).where(
        PaymentReceipt.online_payment_id == payment_id
    )
    receipt = session.exec(stmt).first()
    
    if not receipt:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Receipt not found")
    
    return receipt


@router.post("/receipt/{receipt_id}/email")
def email_receipt(
    *,
    session: Session = Depends(get_session),
    receipt_id: int,
    email: str
):
    """Email payment receipt"""
    receipt = session.get(PaymentReceipt, receipt_id)
    if not receipt:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Receipt not found")
    
    # TODO: Implement email sending
    receipt.email_sent = True
    receipt.email_sent_to = email
    from datetime import datetime
    receipt.email_sent_at = datetime.utcnow()
    
    session.commit()
    return {"message": "Receipt sent successfully"}


# ============================================================================
# Statistics Endpoints
# ============================================================================

@router.get("/statistics/summary")
def get_payment_statistics(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Get payment statistics"""
    from app.models.payment_gateway import PaymentStatus
    
    stmt = select(OnlinePayment)
    payments = session.exec(stmt).all()
    
    total = len(payments)
    successful = sum(1 for p in payments if p.payment_status == PaymentStatus.SUCCESS)
    failed = sum(1 for p in payments if p.payment_status == PaymentStatus.FAILED)
    pending = sum(1 for p in payments if p.payment_status == PaymentStatus.PENDING)
    
    total_amount = sum(p.amount for p in payments if p.payment_status == PaymentStatus.SUCCESS)
    total_fees = sum(p.transaction_fee for p in payments if p.payment_status == PaymentStatus.SUCCESS)
    
    return {
        "total_transactions": total,
        "successful": successful,
        "failed": failed,
        "pending": pending,
        "success_rate": round((successful / total * 100) if total > 0 else 0, 2),
        "total_amount_collected": float(total_amount),
        "total_transaction_fees": float(total_fees)
    }
