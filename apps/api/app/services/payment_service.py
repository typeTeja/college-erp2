"""Payment service for handling Easebuzz payment gateway integration"""
import hashlib
import hmac
from typing import Dict, Optional
from datetime import datetime
from pydantic import BaseSettings

class PaymentSettings(BaseSettings):
    """Payment gateway configuration"""
    EASEBUZZ_MERCHANT_KEY: str = ""
    EASEBUZZ_SALT: str = ""
    EASEBUZZ_ENV: str = "test"  # test or prod
    EASEBUZZ_BASE_URL: str = "https://testpay.easebuzz.in"
    
    class Config:
        env_file = ".env"

payment_settings = PaymentSettings()

class EasebuzzService:
    """Service for Easebuzz payment gateway integration"""
    
    def __init__(self):
        self.merchant_key = payment_settings.EASEBUZZ_MERCHANT_KEY
        self.salt = payment_settings.EASEBUZZ_SALT
        self.base_url = payment_settings.EASEBUZZ_BASE_URL
        self.env = payment_settings.EASEBUZZ_ENV
    
    def generate_hash(self, data: Dict[str, str]) -> str:
        """
        Generate hash for Easebuzz payment request
        
        Hash format: key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5||||||salt
        """
        hash_string = (
            f"{self.merchant_key}|{data['txnid']}|{data['amount']}|"
            f"{data['productinfo']}|{data['firstname']}|{data['email']}|"
            f"{data.get('udf1', '')}|{data.get('udf2', '')}|{data.get('udf3', '')}|"
            f"{data.get('udf4', '')}|{data.get('udf5', '')}||||||{self.salt}"
        )
        
        hash_value = hashlib.sha512(hash_string.encode('utf-8')).hexdigest()
        return hash_value
    
    def verify_hash(self, response_data: Dict[str, str]) -> bool:
        """
        Verify hash from Easebuzz response
        
        Response hash format: salt|status||||||udf5|udf4|udf3|udf2|udf1|email|firstname|productinfo|amount|txnid|key
        """
        received_hash = response_data.get('hash', '')
        
        hash_string = (
            f"{self.salt}|{response_data.get('status', '')}||||||"
            f"{response_data.get('udf5', '')}|{response_data.get('udf4', '')}|"
            f"{response_data.get('udf3', '')}|{response_data.get('udf2', '')}|"
            f"{response_data.get('udf1', '')}|{response_data.get('email', '')}|"
            f"{response_data.get('firstname', '')}|{response_data.get('productinfo', '')}|"
            f"{response_data.get('amount', '')}|{response_data.get('txnid', '')}|{self.merchant_key}"
        )
        
        calculated_hash = hashlib.sha512(hash_string.encode('utf-8')).hexdigest()
        
        return calculated_hash == received_hash
    
    def initiate_payment(
        self,
        application_id: int,
        amount: float,
        name: str,
        email: str,
        phone: str,
        return_url: str,
        webhook_url: str
    ) -> Dict[str, str]:
        """
        Initiate payment and return payment form data
        
        Args:
            application_id: Application ID
            amount: Payment amount
            name: Applicant name
            email: Applicant email
            phone: Applicant phone
            return_url: URL to redirect after payment
            webhook_url: URL for payment webhook
            
        Returns:
            Dictionary with payment form data
        """
        # Generate unique transaction ID
        txnid = f"APP{application_id}_{int(datetime.now().timestamp())}"
        
        payment_data = {
            "key": self.merchant_key,
            "txnid": txnid,
            "amount": str(amount),
            "productinfo": f"Application Fee - {application_id}",
            "firstname": name,
            "email": email,
            "phone": phone,
            "surl": return_url,  # Success URL
            "furl": return_url,  # Failure URL
            "udf1": str(application_id),  # Store application ID
            "udf2": "",
            "udf3": "",
            "udf4": "",
            "udf5": "",
        }
        
        # Generate hash
        payment_data["hash"] = self.generate_hash(payment_data)
        
        # Add payment URL
        payment_data["action_url"] = f"{self.base_url}/pay/{self.merchant_key}"
        
        return payment_data
    
    def process_webhook(self, webhook_data: Dict[str, str]) -> Dict[str, any]:
        """
        Process payment webhook from Easebuzz
        
        Args:
            webhook_data: Webhook payload from Easebuzz
            
        Returns:
            Processed payment information
        """
        # Verify hash
        if not self.verify_hash(webhook_data):
            raise ValueError("Invalid hash in webhook data")
        
        status = webhook_data.get('status', '')
        
        return {
            "transaction_id": webhook_data.get('txnid', ''),
            "application_id": int(webhook_data.get('udf1', 0)),
            "amount": float(webhook_data.get('amount', 0)),
            "status": "SUCCESS" if status == "success" else "FAILED",
            "payment_method": webhook_data.get('mode', ''),
            "easebuzz_id": webhook_data.get('easepayid', ''),
            "bank_ref_num": webhook_data.get('bank_ref_num', ''),
            "error_message": webhook_data.get('error_Message', ''),
            "paid_at": datetime.now() if status == "success" else None
        }

# Singleton instance
easebuzz_service = EasebuzzService()
