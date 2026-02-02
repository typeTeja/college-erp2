from typing import List, Optional
from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, select

from app.api.deps import get_session, get_current_active_superuser
from app.models import User
from ..models.gateway import (
    PaymentGatewayConfig, OnlinePayment, PaymentReceipt
)
from ..services.gateway import gateway_service

router = APIRouter()

@router.get("/gateways")
def list_gateways(
    *,
    session: Session = Depends(get_session)
):
    """List payment gateways"""
    stmt = select(PaymentGatewayConfig).where(PaymentGatewayConfig.is_active == True)
    return session.exec(stmt).all()

@router.post("/initiate")
def initiate_payment(
    *,
    session: Session = Depends(get_session),
    request: Request,
    payment_data: dict
):
    """Initiate online payment"""
    return gateway_service.initiate_payment(
        session,
        payment_data["student_id"],
        payment_data["student_fee_id"],
        payment_data["amount"],
        payment_data.get("payment_mode")
    )
