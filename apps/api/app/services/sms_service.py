"""SMS notification service using MSG91 for sending application-related SMS"""
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
import requests
import json

class SMSSettings(BaseSettings):
    """SMS configuration for MSG91"""
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"
    )
    
    MSG91_AUTH_KEY: str = ""
    MSG91_SENDER_ID: str = "COLEGE"  # 6 characters sender ID
    MSG91_ROUTE: str = "4"  # 4 for transactional SMS
    MSG91_COUNTRY_CODE: str = "91"  # India country code

sms_settings = SMSSettings()

class SMSService:
    """Service for sending SMS via MSG91"""
    
    def __init__(self):
        self.auth_key = sms_settings.MSG91_AUTH_KEY
        self.sender_id = sms_settings.MSG91_SENDER_ID
        self.route = sms_settings.MSG91_ROUTE
        self.country_code = sms_settings.MSG91_COUNTRY_CODE
        self.api_url = "https://api.msg91.com/api/v5/flow/"
    
    def send_sms(
        self,
        mobile: str,
        message: str
    ) -> bool:
        """
        Send SMS using MSG91 API
        
        Args:
            mobile: Mobile number (without country code)
            message: SMS message content
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            # Remove any non-numeric characters
            mobile = ''.join(filter(str.isdigit, mobile))
            
            # Remove country code if present
            if mobile.startswith(self.country_code):
                mobile = mobile[len(self.country_code):]
            
            # MSG91 API endpoint for sending SMS
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
            
            if response.status_code == 200:
                result = response.json() if response.text else {}
                # MSG91 returns success message in different formats
                if response.text and ('success' in response.text.lower() or response.status_code == 200):
                    return True
            
            print(f"MSG91 SMS API Error: {response.status_code} - {response.text}")
            return False
            
        except Exception as e:
            print(f"Failed to send SMS: {str(e)}")
            return False
    
    def send_portal_credentials(
        self,
        mobile: str,
        name: str,
        username: str,
        password: str,
        application_number: str
    ) -> bool:
        """Send student portal login credentials via SMS"""
        
        # SMS message (160 characters limit for single SMS)
        message = f"""Dear {name},
Your Portal Login:
Username: {username}
Password: {password}
App No: {application_number}
Login at portal.college.edu
-Admissions Team"""
        
        return self.send_sms(mobile, message)
    
    def send_otp(
        self,
        mobile: str,
        otp: str
    ) -> bool:
        """Send OTP via SMS"""
        message = f"Your OTP for College ERP is: {otp}. Valid for 10 minutes. Do not share with anyone."
        return self.send_sms(mobile, message)
    
    def send_application_status(
        self,
        mobile: str,
        name: str,
        application_number: str,
        status: str
    ) -> bool:
        """Send application status update via SMS"""
        message = f"Dear {name}, Your application {application_number} status: {status}. Check portal for details."
        return self.send_sms(mobile, message)

# Singleton instance
sms_service = SMSService()
