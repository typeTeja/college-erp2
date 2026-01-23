import hashlib
import httpx
import logging
from typing import Dict, Any, Optional
from app.config.settings import settings

# Configure logging
logger = logging.getLogger(__name__)

from sqlmodel import Session, select
from app.db.session import engine
from app.models.settings import SystemSetting

class EasebuzzService:
    """
    Service for Easebuzz Payment Gateway Integration
    Handles hash generation, verification, and API calls.
    Ref: https://docs.easebuzz.in/docs/payment-gateway/jl5acj6genz7q-python
    """
    
    BASE_URL_TEST = "https://testpay.easebuzz.in"
    BASE_URL_PROD = "https://pay.easebuzz.in"
    
    def __init__(self):
        # We fetch settings dynamically now
        pass

    def _get_config(self):
        """Fetch Easebuzz config from DB, fallback to env"""
        try:
            with Session(engine) as session:
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
        except Exception as e:
            logger.error(f"Error fetching Easebuzz settings: {e}")
            return {
                "key": settings.EASEBUZZ_MERCHANT_KEY,
                "salt": settings.EASEBUZZ_SALT,
                "env": settings.EASEBUZZ_ENV
            }

    def generate_hash(self, data: Dict[str, Any]) -> str:
        """
        Generate hash for payment request
        Sequence: key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5||||||salt
        """
        config = self._get_config()
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
        
        # Add empty strings for udf6 to udf10
        hash_sequence.extend([''] * 5)
        
        # Add salt at the end
        hash_sequence.append(salt)
        
        hash_string = "|".join(hash_sequence)
        generated_hash = hashlib.sha512(hash_string.encode('utf-8')).hexdigest()
        # print(f"DEBUG Hash Sequence: {hash_string}")
        return generated_hash

    def verify_response_hash(self, data: Dict[str, Any]) -> bool:
        """
        Verify hash from Easebuzz response
        Sequence: salt|status||||||udf5|udf4|udf3|udf2|udf1|email|firstname|productinfo|amount|txnid|key
        """
        try:
            received_hash = data.get('hash')
            if not received_hash:
                return False
                
            config = self._get_config()
            key = config["key"]
            salt = config["salt"]
            
            hash_sequence = [salt, str(data.get('status', ''))]
            
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
                key
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
        config = self._get_config()
        base_url = self.BASE_URL_TEST if config["env"].lower() == "test" else self.BASE_URL_PROD
        url = f"{base_url}/payment/initiateLink"
        
        # Ensure mandatory fields
        # Ensure amount is strictly formatted to 2 decimal places
        amount_str = "{:.2f}".format(float(payment_data['amount']))
        
        # Update payment_data for hash generation
        payment_data['amount'] = amount_str
        
        hash_value = self.generate_hash(payment_data)
        
        payload = {
            "key": config["key"],
            "txnid": payment_data['txnid'],
            "amount": amount_str,
            "productinfo": payment_data['productinfo'],
            "firstname": payment_data['firstname'],
            "phone": payment_data['phone'],
            "email": payment_data['email'],
            "surl": payment_data.get('surl') or 'http://localhost:8000/api/v1/payment/response',
            "furl": payment_data.get('furl') or 'http://localhost:8000/api/v1/payment/response',
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
