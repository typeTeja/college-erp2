"""
Finance Domain Services

Business logic for finance domain including:
- Fee management
- Payment gateway integration
- Easebuzz payment processing
"""



# ======================================================================
# Fee
# ======================================================================

from typing import List, Optional, Dict
from datetime import date, datetime, timedelta
from decimal import Decimal
from sqlmodel import Session, select
from fastapi import HTTPException

from ..models.fee import (
    FeeStructure, StudentFee, StudentFeeInstallment,
    FeePayment, FeeConcession, FeeFine, PaymentStatus
)
from app.models import Student

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


# ======================================================================
# Gateway
# ======================================================================

from typing import Dict, Optional
from datetime import datetime
from sqlmodel import Session, select
from fastapi import HTTPException
import secrets
import hashlib
import hmac

from ..models.gateway import (
    PaymentGatewayConfig, OnlinePayment, PaymentReceipt,
    PaymentStatus, PaymentMode
)
from app.models import Student
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


# ======================================================================
# Easebuzz
# ======================================================================

import hashlib
import httpx
import logging
from typing import Dict, Any, Optional
from app.config.settings import settings
from sqlmodel import Session, select
from app.models.settings.system import SystemSetting

logger = logging.getLogger(__name__)

class EasebuzzService:
    """
    Service for Easebuzz Payment Gateway Integration
    """
    BASE_URL_TEST = "https://testpay.easebuzz.in"
    BASE_URL_PROD = "https://pay.easebuzz.in"
    
    def _get_config(self, session: Session):
        """Fetch Easebuzz config from DB, fallback to env"""
        config = {
            "key": settings.EASEBUZZ_MERCHANT_KEY,
            "salt": settings.EASEBUZZ_SALT,
            "env": settings.EASEBUZZ_ENV
        }
        
        db_settings = session.exec(select(SystemSetting).where(
            SystemSetting.key.in_(["easebuzz.merchant_key", "easebuzz.salt", "easebuzz.env"])
        )).all()
        
        for s in db_settings:
            if s.key == "easebuzz.merchant_key" and s.value:
                config["key"] = s.value
            elif s.key == "easebuzz.salt" and s.value:
                config["salt"] = s.value
            elif s.key == "easebuzz.env" and s.value:
                config["env"] = s.value
        
        return config

    def generate_hash(self, session: Session, data: Dict[str, Any]) -> str:
        config = self._get_config(session)
        key = config["key"]
        salt = config["salt"]
        
        hash_sequence = [
            key,
            str(data.get('txnid', '')),
            str(data.get('amount', '')),
            str(data.get('productinfo', '')),
            str(data.get('firstname', '')),
            str(data.get('email', '')),
            str(data.get('udf1', '')),
            str(data.get('udf2', '')),
            str(data.get('udf3', '')),
            str(data.get('udf4', '')),
            str(data.get('udf5', ''))
        ]
        hash_sequence.extend([''] * 5)
        hash_sequence.append(salt)
        
        hash_string = "|".join(hash_sequence)
        return hashlib.sha512(hash_string.encode('utf-8')).hexdigest()

    async def initiate_payment(self, session: Session, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        config = self._get_config(session)
        base_url = self.BASE_URL_TEST if config["env"].lower() == "test" else self.BASE_URL_PROD
        url = f"{base_url}/payment/initiateLink"
        
        amount_str = "{:.2f}".format(float(payment_data['amount']))
        payment_data['amount'] = amount_str
        
        hash_value = self.generate_hash(session, payment_data)
        
        payload = {
            "key": config["key"],
            "txnid": payment_data['txnid'],
            "amount": amount_str,
            "productinfo": payment_data['productinfo'],
            "firstname": payment_data['firstname'],
            "phone": payment_data['phone'],
            "email": payment_data['email'],
            "surl": payment_data.get('surl'),
            "furl": payment_data.get('furl'),
            "hash": hash_value,
            "udf1": payment_data.get('udf1', ''),
            "udf2": payment_data.get('udf2', ''),
            "udf3": payment_data.get('udf3', ''),
            "udf4": payment_data.get('udf4', ''),
            "udf5": payment_data.get('udf5', '')
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=payload)
        
        if response.status_code == 200:
            return response.json()
        return {"status": 0, "error": f"HTTP Error: {response.status_code}"}

easebuzz_service = EasebuzzService()
