from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
import requests

class SMSSettings(BaseSettings):
    """SMS configuration for MSG91"""
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"
    )
    
    MSG91_AUTH_KEY: str = ""
    MSG91_SENDER_ID: str = "COLEGE"
    MSG91_ROUTE: str = "4"
    MSG91_COUNTRY_CODE: str = "91"

sms_settings = SMSSettings()

class SMSService:
    """Service for sending SMS - Communication Domain"""
    
    def __init__(self):
        self.auth_key = sms_settings.MSG91_AUTH_KEY
        self.sender_id = sms_settings.MSG91_SENDER_ID
        self.route = sms_settings.MSG91_ROUTE
        self.country_code = sms_settings.MSG91_COUNTRY_CODE
    
    def send_sms(self, mobile: str, message: str) -> bool:
        try:
            mobile = ''.join(filter(str.isdigit, mobile))
            if mobile.startswith(self.country_code):
                mobile = mobile[len(self.country_code):]
            
            url = "https://api.msg91.com/api/sendhttp.php"
            params = {
                'authkey': self.auth_key,
                'mobiles': mobile,
                'message': message,
                'sender': self.sender_id,
                'route': self.route,
                'country': self.country_code
            }
            
            response = requests.get(url, params=params, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"Failed to send SMS: {str(e)}")
            return False

sms_service = SMSService()
