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
