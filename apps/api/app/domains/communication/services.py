"""
Communication Domain Services

Business logic for communication domain including:
- Email service
- SMS service
"""



# ======================================================================
# Email Service
# ======================================================================

from typing import Optional, Dict
from datetime import datetime
from pydantic_settings import BaseSettings, SettingsConfigDict
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlmodel import Session, select

from app.db.session import engine
from app.domains.system.models.system import SystemSetting

class EmailSettings(BaseSettings):
    """Email configuration"""
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"
    )
    
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    FROM_EMAIL: str = ""
    FROM_NAME: str = "College ERP"

email_settings = EmailSettings()

class EmailService:
    """Service for sending emails - Communication Domain"""
    
    def _get_settings(self):
        """Fetch email settings from DB, fallback to env"""
        try:
            with Session(engine) as session:
                settings_map = {
                    "smtp.host": email_settings.SMTP_HOST,
                    "smtp.port": email_settings.SMTP_PORT,
                    "smtp.user": email_settings.SMTP_USER,
                    "smtp.password": email_settings.SMTP_PASSWORD,
                    "email.from_email": email_settings.FROM_EMAIL,
                    "email.from_name": email_settings.FROM_NAME
                }
                
                db_settings = session.exec(select(SystemSetting).where(
                    SystemSetting.key.in_(settings_map.keys())
                )).all()
                
                for s in db_settings:
                    if s.value:
                        settings_map[s.key] = s.value
                        
                return settings_map
        except Exception as e:
            print(f"Error fetching email settings from DB: {e}")
            return {
                "smtp.host": email_settings.SMTP_HOST,
                "smtp.port": email_settings.SMTP_PORT,
                "smtp.user": email_settings.SMTP_USER,
                "smtp.password": email_settings.SMTP_PASSWORD,
                "email.from_email": email_settings.FROM_EMAIL,
                "email.from_name": email_settings.FROM_NAME
            }
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        config = self._get_settings()
        if not config["smtp.host"] or not config["smtp.port"]:
            return False
            
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{config['email.from_name']} <{config['email.from_email']}>"
            msg['To'] = to_email
            
            if text_content:
                msg.attach(MIMEText(text_content, 'plain'))
            msg.attach(MIMEText(html_content, 'html'))
            
            if not config["smtp.user"] or not config["smtp.password"]:
                # Console logging for dev
                print(f"DEBUG: Email to {to_email} | Subject: {subject}")
                return True
            
            with smtplib.SMTP(config["smtp.host"], int(config["smtp.port"])) as server:
                server.starttls()
                server.login(config["smtp.user"], config["smtp.password"])
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False

email_service = EmailService()


# ======================================================================
# Sms Service
# ======================================================================

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
