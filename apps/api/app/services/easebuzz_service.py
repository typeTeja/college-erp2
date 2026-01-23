import hashlib
import httpx
import logging
from typing import Dict, Any, Optional
from app.config.settings import settings

# Configure logging
logger = logging.getLogger(__name__)

class EasebuzzService:
    """
    Service for Easebuzz Payment Gateway Integration
    Handles hash generation, verification, and API calls.
    Ref: https://docs.easebuzz.in/docs/payment-gateway/jl5acj6genz7q-python
    """
    
    BASE_URL_TEST = "https://testpay.easebuzz.in"
    BASE_URL_PROD = "https://pay.easebuzz.in"
    
    def __init__(self):
        self.key = settings.EASEBUZZ_MERCHANT_KEY
        self.salt = settings.EASEBUZZ_SALT
        self.env = settings.EASEBUZZ_ENV.lower()
        self.base_url = self.BASE_URL_TEST if self.env == "test" else self.BASE_URL_PROD

    def generate_hash(self, data: Dict[str, Any]) -> str:
        """
        Generate hash for payment request
        Sequence: key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5||||||salt
        """
        hash_sequence = [
            self.key,
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
        
        # Add empty strings for udf6 to udf10
        hash_sequence.extend([''] * 5)
        
        # Add salt at the end
        hash_sequence.append(self.salt)
        
        hash_string = "|".join(hash_sequence)
        return hashlib.sha512(hash_string.encode('utf-8')).hexdigest()

    def verify_response_hash(self, data: Dict[str, Any]) -> bool:
        """
        Verify hash from Easebuzz response
        Sequence: salt|status||||||udf5|udf4|udf3|udf2|udf1|email|firstname|productinfo|amount|txnid|key
        """
        try:
            received_hash = data.get('hash')
            if not received_hash:
                return False
                
            hash_sequence = [self.salt, str(data.get('status', ''))]
            
            # Add empty strings for udf10 to udf6 (reverse order)
            hash_sequence.extend([''] * 5)
            
            # Add udf5 to udf1 (reverse order)
            hash_sequence.extend([
                str(data.get('udf5', '')),
                str(data.get('udf4', '')),
                str(data.get('udf3', '')),
                str(data.get('udf2', '')),
                str(data.get('udf1', ''))
            ])
            
            hash_sequence.extend([
                str(data.get('email', '')),
                str(data.get('firstname', '')),
                str(data.get('productinfo', '')),
                str(data.get('amount', '')),
                str(data.get('txnid', '')),
                self.key
            ])
            
            hash_string = "|".join(hash_sequence)
            calculated_hash = hashlib.sha512(hash_string.encode('utf-8')).hexdigest()
            
            return calculated_hash == received_hash
            
        except Exception as e:
            logger.error(f"Error verifying hash: {str(e)}")
            return False

    async def initiate_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call Easebuzz Initiate API
        """
        url = f"{self.base_url}/payment/initiateLink"
        
        # Ensure mandatory fields
        hash_value = self.generate_hash(payment_data)
        
        payload = {
            "key": self.key,
            "txnid": payment_data['txnid'],
            "amount": payment_data['amount'],
            "productinfo": payment_data['productinfo'],
            "firstname": payment_data['firstname'],
            "phone": payment_data['phone'],
            "email": payment_data['email'],
            "surl": payment_data.get('surl', 'http://localhost:8000/api/v1/payment/response'), # Default to backend for API test
            "furl": payment_data.get('furl', 'http://localhost:8000/api/v1/payment/response'), # Default to backend for API test
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
        
        return {"status": 0, "error": f"HTTP Error: {response.status_code}", "raw": response.text}

easebuzz_service = EasebuzzService()
