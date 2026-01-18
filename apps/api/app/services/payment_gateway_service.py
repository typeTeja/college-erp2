"""
Payment Gateway Service Layer

Handles business logic for online payments including:
- Payment initiation
- Gateway integration (Razorpay/Easebuzz)
- Payment verification
- Receipt generation
- Refund processing
"""
from typing import Dict, Optional
from datetime import datetime
from sqlmodel import Session, select
from fastapi import HTTPException
import secrets
import hashlib
import hmac

from app.models.payment_gateway import (
    PaymentGatewayConfig, OnlinePayment, PaymentReceipt,
    PaymentStatus, PaymentMode
)
from app.models.student import Student
from app.models.fee import StudentFee


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
    def generate_order_id(student_id: int, fee_id: int) -> str:
        """Generate unique order ID"""
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        random_suffix = secrets.token_hex(4)
        return f"ORD-{student_id}-{fee_id}-{timestamp}-{random_suffix}"
    
    @staticmethod
    def calculate_transaction_fee(
        amount: float,
        gateway: PaymentGatewayConfig
    ) -> float:
        """Calculate transaction fee"""
        percentage_fee = amount * (gateway.transaction_fee_percentage / 100)
        total_fee = percentage_fee + gateway.transaction_fee_fixed
        return round(total_fee, 2)
    
    @staticmethod
    def initiate_payment(
        session: Session,
        student_id: int,
        student_fee_id: int,
        amount: float,
        payment_mode: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> OnlinePayment:
        """Initiate online payment"""
        # Validate student
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Validate fee
        fee = session.get(StudentFee, student_fee_id)
        if not fee:
            raise HTTPException(status_code=404, detail="Student fee not found")
        
        # Get active gateway
        gateway = PaymentGatewayService.get_active_gateway(session)
        
        # Validate amount
        if amount < gateway.min_transaction_amount:
            raise HTTPException(
                status_code=400,
                detail=f"Amount must be at least ₹{gateway.min_transaction_amount}"
            )
        
        if amount > gateway.max_transaction_amount:
            raise HTTPException(
                status_code=400,
                detail=f"Amount cannot exceed ₹{gateway.max_transaction_amount}"
            )
        
        # Calculate fees
        transaction_fee = PaymentGatewayService.calculate_transaction_fee(amount, gateway)
        net_amount = amount - transaction_fee
        
        # Generate order ID
        order_id = PaymentGatewayService.generate_order_id(student_id, student_fee_id)
        
        # Create payment record
        payment = OnlinePayment(
            student_id=student_id,
            student_fee_id=student_fee_id,
            payment_gateway_config_id=gateway.id,
            amount=amount,
            payment_mode=PaymentMode(payment_mode) if payment_mode else None,
            gateway_order_id=order_id,
            customer_name=student.name,
            customer_email=student.email or "",
            customer_phone=student.phone or "",
            transaction_fee=transaction_fee,
            net_amount=net_amount,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        session.add(payment)
        session.commit()
        session.refresh(payment)
        
        # In production, integrate with actual gateway API
        # For Razorpay:
        # import razorpay
        # client = razorpay.Client(auth=(gateway.api_key, gateway.api_secret))
        # order = client.order.create({
        #     "amount": int(amount * 100),  # Convert to paise
        #     "currency": "INR",
        #     "receipt": order_id
        # })
        # payment.gateway_transaction_id = order['id']
        
        return payment
    
    @staticmethod
    def verify_payment_signature(
        order_id: str,
        payment_id: str,
        signature: str,
        secret: str
    ) -> bool:
        """Verify payment signature (Razorpay)"""
        message = f"{order_id}|{payment_id}"
        generated_signature = hmac.new(
            secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(generated_signature, signature)
    
    @staticmethod
    def process_payment_callback(
        session: Session,
        payment_id: int,
        gateway_payment_id: str,
        gateway_signature: str,
        gateway_response: Dict
    ) -> OnlinePayment:
        """Process payment callback from gateway"""
        payment = session.get(OnlinePayment, payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        # Get gateway config
        gateway = session.get(PaymentGatewayConfig, payment.payment_gateway_config_id)
        
        # Verify signature
        is_valid = PaymentGatewayService.verify_payment_signature(
            payment.gateway_order_id,
            gateway_payment_id,
            gateway_signature,
            gateway.webhook_secret or gateway.api_secret
        )
        
        if is_valid:
            payment.payment_status = PaymentStatus.SUCCESS
            payment.gateway_payment_id = gateway_payment_id
            payment.gateway_signature = gateway_signature
            payment.gateway_response = str(gateway_response)
            payment.completed_at = datetime.utcnow()
            
            # Generate receipt
            receipt = PaymentGatewayService.generate_receipt(session, payment)
            payment.receipt_number = receipt.receipt_number
            payment.receipt_generated = True
        else:
            payment.payment_status = PaymentStatus.FAILED
            payment.gateway_error_message = "Invalid signature"
            payment.failed_at = datetime.utcnow()
        
        session.commit()
        session.refresh(payment)
        return payment
    
    @staticmethod
    def generate_receipt(
        session: Session,
        payment: OnlinePayment
    ) -> PaymentReceipt:
        """Generate payment receipt"""
        # Generate receipt number
        count = len(session.exec(select(PaymentReceipt)).all())
        receipt_number = f"REC-{datetime.utcnow().strftime('%Y%m')}-{str(count + 1).zfill(6)}"
        
        receipt = PaymentReceipt(
            online_payment_id=payment.id,
            receipt_number=receipt_number,
            amount=payment.amount,
            transaction_fee=payment.transaction_fee,
            net_amount=payment.net_amount
        )
        
        session.add(receipt)
        session.commit()
        session.refresh(receipt)
        
        # TODO: Generate PDF receipt
        # receipt.pdf_url = generate_pdf(receipt)
        # receipt.pdf_generated = True
        
        return receipt
    
    @staticmethod
    def get_payment_status(
        session: Session,
        payment_id: int
    ) -> Dict:
        """Get payment status"""
        payment = session.get(OnlinePayment, payment_id)
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        return {
            "payment_id": payment.id,
            "order_id": payment.gateway_order_id,
            "status": payment.payment_status,
            "amount": payment.amount,
            "transaction_fee": payment.transaction_fee,
            "net_amount": payment.net_amount,
            "initiated_at": payment.initiated_at.isoformat(),
            "completed_at": payment.completed_at.isoformat() if payment.completed_at else None
        }
