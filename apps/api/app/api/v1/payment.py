"""Payment and webhook endpoints for admissions"""
from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlmodel import Session
from app.db.session import get_session
from app.api.deps import get_current_user
from app.models.user import User
from app.models.admissions import (
    Application, ApplicationStatus, ApplicationPayment, ApplicationPaymentStatus,
    ActivityType
)
from app.services.payment_service import easebuzz_service
from app.services.email_service import email_service
from app.services.activity_logger import log_activity
from typing import Dict

payment_router = APIRouter()

def get_client_ip(request: Request) -> str:
    """Extract client IP address from request"""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0]
    return request.client.host if request.client else "unknown"

@payment_router.post("/{id}/payment/initiate")
async def initiate_payment(
    id: int,
    return_url: str,
    request: Request,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Initiate online payment for an application
    
    Returns payment form data to be submitted to Easebuzz
    """
    application = session.get(Application, id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Check permission
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN"] for role in current_user.roles)
    is_owner = current_user.email == application.email
    
    if not (is_admin or is_owner):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Check if already paid
    if application.status not in [ApplicationStatus.PENDING_PAYMENT, ApplicationStatus.PAYMENT_FAILED]:
        raise HTTPException(status_code=400, detail="Application fee already paid or not applicable")
    
    # Application fee amount (TODO: Make this configurable)
    amount = 500.0  # ₹500
    
    # Generate webhook URL using BACKEND_BASE_URL (HTTPS-aware)
    from app.config.settings import settings
    webhook_url = f"{settings.BACKEND_BASE_URL}/api/v1/admissions/payment/webhook"
    
    # Initiate payment
    payment_data = easebuzz_service.initiate_payment(
        application_id=id,
        amount=amount,
        name=application.name,
        email=application.email,
        phone=application.phone,
        return_url=return_url,
        webhook_url=webhook_url
    )
    
    # Create payment record
    payment = ApplicationPayment(
        application_id=id,
        transaction_id=payment_data["txnid"],
        amount=amount,
        status=ApplicationPaymentStatus.PENDING,
        payment_method="Easebuzz"
    )
    
    session.add(payment)
    session.flush()
    
    # Log activity
    log_activity(
        session=session,
        application_id=id,
        activity_type=ActivityType.PAYMENT_INITIATED,
        description=f"Payment initiated: ₹{amount}",
        performed_by=current_user.id,
        ip_address=get_client_ip(request),
        extra_data={"amount": amount, "transaction_id": payment_data["txnid"]}
    )
    
    session.commit()
    
    return {
        "payment_data": payment_data,
        "message": "Payment initiated successfully. Submit this data to Easebuzz."
    }

@payment_router.post("/payment/webhook")
async def payment_webhook(
    request: Request,
    session: Session = Depends(get_session)
):
    """
    Webhook endpoint for Easebuzz payment notifications
    
    This endpoint is called by Easebuzz after payment completion
    """
    # Get form data from webhook
    form_data = await request.form()
    webhook_data = dict(form_data)
    
    try:
        # Process webhook
        payment_info = easebuzz_service.process_webhook(webhook_data)
        
        # Find application
        application = session.get(Application, payment_info["application_id"])
        if not application:
            raise HTTPException(status_code=404, detail="Application not found")
        
        # Find payment record
        from sqlmodel import select
        statement = select(ApplicationPayment).where(
            ApplicationPayment.transaction_id == payment_info["transaction_id"]
        )
        payment = session.exec(statement).first()
        
        if not payment:
            # Create new payment record if not exists
            payment = ApplicationPayment(
                application_id=payment_info["application_id"],
                transaction_id=payment_info["transaction_id"],
                amount=payment_info["amount"],
                status=ApplicationPaymentStatus.PENDING
            )
            session.add(payment)
        
        # Update payment status
        if payment_info["status"] == "SUCCESS":
            payment.status = ApplicationPaymentStatus.SUCCESS
            payment.paid_at = payment_info["paid_at"]
            payment.payment_method = payment_info["payment_method"]
            
            # Update application status
            application.status = ApplicationStatus.PAID
            
            # Log activity
            log_activity(
                session=session,
                application_id=application.id,
                activity_type=ActivityType.PAYMENT_SUCCESS,
                description=f"Payment successful: ₹{payment_info['amount']}",
                ip_address=get_client_ip(request),
                extra_data={
                    "transaction_id": payment_info["transaction_id"],
                    "amount": payment_info["amount"],
                    "easebuzz_id": payment_info["easebuzz_id"]
                }
            )
            
            # Send payment success email
            try:
                email_service.send_payment_success(
                    to_email=application.email,
                    name=application.name,
                    application_number=application.application_number,
                    amount=payment_info["amount"],
                    transaction_id=payment_info["transaction_id"]
                )
            except Exception as e:
                print(f"Failed to send payment success email: {str(e)}")
        
        else:
            payment.status = ApplicationPaymentStatus.FAILED
            application.status = ApplicationStatus.PAYMENT_FAILED
            
            # Log activity
            log_activity(
                session=session,
                application_id=application.id,
                activity_type=ActivityType.PAYMENT_FAILED,
                description=f"Payment failed: {payment_info.get('error_message', 'Unknown error')}",
                ip_address=get_client_ip(request),
                extra_data={
                    "transaction_id": payment_info["transaction_id"],
                    "error": payment_info.get("error_message")
                }
            )
        
        session.add(payment)
        session.add(application)
        session.commit()
        
        return {"status": "success", "message": "Webhook processed successfully"}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {str(e)}")

@payment_router.get("/{id}/payment/status")
async def get_payment_status(
    id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get payment status for an application"""
    application = session.get(Application, id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Check permission
    is_admin = any(role.name in ["SUPER_ADMIN", "ADMIN"] for role in current_user.roles)
    is_owner = current_user.email == application.email
    
    if not (is_admin or is_owner):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return {
        "application_id": id,
        "application_status": application.status,
        "payments": [
            {
                "transaction_id": p.transaction_id,
                "amount": p.amount,
                "status": p.status,
                "payment_method": p.payment_method,
                "paid_at": p.paid_at,
                "created_at": p.created_at
            }
            for p in application.payments
        ]
    }
