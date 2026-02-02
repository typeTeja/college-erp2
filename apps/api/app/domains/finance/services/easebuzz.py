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
