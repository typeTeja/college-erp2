"""Email notification service for sending application-related emails"""
from typing import Optional, Dict
from datetime import datetime
from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSettings(BaseSettings):
    """Email configuration"""
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"  # Allow extra fields from .env
    )
    
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    FROM_EMAIL: str = ""
    FROM_NAME: str = "College ERP - Admissions"

email_settings = EmailSettings()

from sqlmodel import Session, select
from app.db.session import engine
from app.models.settings import SystemSetting

class EmailService:
    """Service for sending emails"""
    
    def __init__(self):
        # We no longer load settings at init to support runtime changes
        pass
    
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
                
                # Fetch all relevant settings
                db_settings = session.exec(select(SystemSetting).where(
                    SystemSetting.key.in_(settings_map.keys())
                )).all()
                
                # Update map with DB values
                for s in db_settings:
                    if s.value:
                        settings_map[s.key] = s.value
                        
                return settings_map
        except Exception as e:
            print(f"Error fetching email settings from DB: {e}")
            # Fallback to env default
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
        """
        Send an email
        
        Args:
            to_email: Recipient email
            subject: Email subject
            html_content: HTML email body
            text_content: Plain text email body (optional)
            
        Returns:
            True if sent successfully, False otherwise
        """
        config = self._get_settings()
        
        # Validate critical config
        if not config["smtp.host"] or not config["smtp.port"]:
            print("SMTP configuration missing")
            return False
            
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{config['email.from_name']} <{config['email.from_email']}>"
            msg['To'] = to_email
            
            # Add text and HTML parts
            if text_content:
                part1 = MIMEText(text_content, 'plain')
                msg.attach(part1)
            
            part2 = MIMEText(html_content, 'html')
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(config["smtp.host"], int(config["smtp.port"])) as server:
                server.starttls()
                if config["smtp.user"] and config["smtp.password"]:
                    server.login(config["smtp.user"], config["smtp.password"])
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False
    
    def send_application_confirmation(
        self,
        to_email: str,
        name: str,
        application_number: str,
        fee_mode: str,
        amount: float
    ) -> bool:
        """Send application confirmation email"""
        subject = f"Application Received - {application_number}"
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2563eb;">Application Received Successfully!</h2>
                    
                    <p>Dear {name},</p>
                    
                    <p>Thank you for applying to our college. Your application has been received and is being processed.</p>
                    
                    <div style="background-color: #f3f4f6; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <strong>Application Details:</strong><br>
                        Application Number: <strong>{application_number}</strong><br>
                        Payment Mode: <strong>{fee_mode}</strong><br>
                        Application Fee: <strong>₹{amount:.2f}</strong>
                    </div>
                    
                    {'<p><strong>Next Steps:</strong><br>Please proceed with the online payment to continue your application process.</p>' if fee_mode == 'ONLINE' else '<p><strong>Next Steps:</strong><br>Please visit the college office to pay the application fee and upload the payment proof.</p>'}
                    
                    <p>You can track your application status by logging in to the portal.</p>
                    
                    <p>If you have any questions, please contact our admissions office.</p>
                    
                    <p>Best regards,<br>
                    Admissions Team</p>
                </div>
            </body>
        </html>
        """
        
        text_content = f"""
        Application Received Successfully!
        
        Dear {name},
        
        Thank you for applying to our college. Your application has been received and is being processed.
        
        Application Details:
        Application Number: {application_number}
        Payment Mode: {fee_mode}
        Application Fee: ₹{amount:.2f}
        
        {'Next Steps: Please proceed with the online payment to continue your application process.' if fee_mode == 'ONLINE' else 'Next Steps: Please visit the college office to pay the application fee and upload the payment proof.'}
        
        You can track your application status by logging in to the portal.
        
        If you have any questions, please contact our admissions office.
        
        Best regards,
        Admissions Team
        """
        
        return self.send_email(to_email, subject, html_content, text_content)
    
    def send_payment_success(
        self,
        to_email: str,
        name: str,
        application_number: str,
        amount: float,
        transaction_id: str
    ) -> bool:
        """Send payment success confirmation email"""
        subject = f"Payment Successful - {application_number}"
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #16a34a;">Payment Received Successfully!</h2>
                    
                    <p>Dear {name},</p>
                    
                    <p>We have received your payment for the application fee.</p>
                    
                    <div style="background-color: #f0fdf4; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #16a34a;">
                        <strong>Payment Details:</strong><br>
                        Application Number: <strong>{application_number}</strong><br>
                        Amount Paid: <strong>₹{amount:.2f}</strong><br>
                        Transaction ID: <strong>{transaction_id}</strong><br>
                        Date: <strong>{datetime.now().strftime('%d %B %Y, %I:%M %p')}</strong>
                    </div>
                    
                    <p><strong>Next Steps:</strong><br>
                    Please complete the full application form by logging in to the portal. You will need to provide additional details and upload required documents.</p>
                    
                    <p>Best regards,<br>
                    Admissions Team</p>
                </div>
            </body>
        </html>
        """
        
        return self.send_email(to_email, subject, html_content)
    
    def send_admission_confirmation(
        self,
        to_email: str,
        name: str,
        admission_number: str,
        program_name: str,
        password_setup_link: str
    ) -> bool:
        """Send admission confirmation email with password setup link"""
        subject = f"Admission Confirmed - {admission_number}"
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #16a34a;">🎉 Congratulations! Admission Confirmed</h2>
                    
                    <p>Dear {name},</p>
                    
                    <p>We are pleased to inform you that your admission has been confirmed!</p>
                    
                    <div style="background-color: #f0fdf4; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #16a34a;">
                        <strong>Admission Details:</strong><br>
                        Admission Number: <strong>{admission_number}</strong><br>
                        Program: <strong>{program_name}</strong><br>
                        Status: <strong>CONFIRMED</strong>
                    </div>
                    
                    <div style="background-color: #fef3c7; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #f59e0b;">
                        <strong>⚠️ Important: Set Up Your Account</strong><br>
                        <p>Please set up your password to access the student portal:</p>
                        <a href="{password_setup_link}" style="display: inline-block; background-color: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-top: 10px;">Set Up Password</a>
                        <p style="margin-top: 10px; font-size: 12px; color: #666;">This link will expire in 24 hours.</p>
                    </div>
                    
                    <p><strong>Next Steps:</strong></p>
                    <ol>
                        <li>Set up your password using the link above</li>
                        <li>Login to the student portal</li>
                        <li>Complete your profile</li>
                        <li>Check your fee schedule</li>
                        <li>Download your admission letter</li>
                    </ol>
                    
                    <p>Welcome to our college family!</p>
                    
                    <p>Best regards,<br>
                    Admissions Team</p>
                </div>
            </body>
        </html>
        """
        
        return self.send_email(to_email, subject, html_content)
    
    def send_document_verification_status(
        self,
        to_email: str,
        name: str,
        document_type: str,
        status: str,
        rejection_reason: Optional[str] = None
    ) -> bool:
        """Send document verification status email"""
        subject = f"Document {status.title()} - {document_type}"
        
        if status == "VERIFIED":
            color = "#16a34a"
            bg_color = "#f0fdf4"
            message = f"Your {document_type} has been verified successfully."
        else:
            color = "#dc2626"
            bg_color = "#fef2f2"
            message = f"Your {document_type} has been rejected."
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: {color};">Document {status.title()}</h2>
                    
                    <p>Dear {name},</p>
                    
                    <p>{message}</p>
                    
                    <div style="background-color: {bg_color}; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid {color};">
                        <strong>Document:</strong> {document_type}<br>
                        <strong>Status:</strong> {status}
                        {f'<br><strong>Reason:</strong> {rejection_reason}' if rejection_reason else ''}
                    </div>
                    
                    {f'<p>Please re-upload the correct document to proceed with your application.</p>' if status == 'REJECTED' else '<p>Thank you for submitting the required documents.</p>'}
                    
                    <p>Best regards,<br>
                    Admissions Team</p>
                </div>
            </body>
        </html>
        """
        
        return self.send_email(to_email, subject, html_content)
    
    def send_portal_credentials(
        self,
        to_email: str,
        name: str,
        application_number: str,
        username: str,
        password: str,
        portal_url: str = "https://portal.college.edu"
    ) -> bool:
        """Send student portal login credentials email"""
        subject = f"Your Student Portal Login Credentials - {application_number}"
        
        html_content = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2563eb;">🎓 Welcome to Our Student Portal!</h2>
                    
                    <p>Dear {name},</p>
                    
                    <p>Thank you for submitting your application. Your student portal account has been created successfully.</p>
                    
                    <div style="background-color: #eff6ff; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #2563eb;">
                        <strong>Application Number:</strong> <strong>{application_number}</strong>
                    </div>
                    
                    <div style="background-color: #f0fdf4; padding: 20px; border-radius: 8px; margin: 20px 0; border: 2px solid #16a34a;">
                        <h3 style="color: #16a34a; margin-top: 0;">🔐 Your Login Credentials</h3>
                        <div style="background-color: white; padding: 15px; border-radius: 5px; margin: 10px 0;">
                            <strong>Username:</strong> <code style="background-color: #f3f4f6; padding: 4px 8px; border-radius: 3px; font-size: 14px;">{username}</code><br><br>
                            <strong>Password:</strong> <code style="background-color: #f3f4f6; padding: 4px 8px; border-radius: 3px; font-size: 14px;">{password}</code>
                        </div>
                        <p style="margin-bottom: 0; font-size: 12px; color: #666;">
                            ⚠️ <strong>Important:</strong> Please save these credentials securely. You can change your password after logging in.
                        </p>
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{portal_url}" style="display: inline-block; background-color: #2563eb; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-weight: bold;">Login to Portal</a>
                    </div>
                    
                    <div style="background-color: #fef3c7; padding: 15px; border-radius: 5px; margin: 20px 0; border-left: 4px solid #f59e0b;">
                        <strong>📋 Next Steps:</strong>
                        <ol style="margin: 10px 0;">
                            <li>Login to the student portal using the credentials above</li>
                            <li>Complete the remaining application form</li>
                            <li>Upload required documents</li>
                            <li>Complete payment (if applicable)</li>
                        </ol>
                    </div>
                    
                    <p>If you have any questions or face any issues logging in, please contact our admissions office.</p>
                    
                    <p>Best regards,<br>
                    Admissions Team</p>
                </div>
            </body>
        </html>
        """
        
        text_content = f"""
        Welcome to Our Student Portal!
        
        Dear {name},
        
        Thank you for submitting your application. Your student portal account has been created successfully.
        
        Application Number: {application_number}
        
        Your Login Credentials:
        Username: {username}
        Password: {password}
        
        Portal URL: {portal_url}
        
        Next Steps:
        1. Login to the student portal using the credentials above
        2. Complete the remaining application form
        3. Upload required documents
        4. Complete payment (if applicable)
        
        Important: Please save these credentials securely. You can change your password after logging in.
        
        If you have any questions or face any issues logging in, please contact our admissions office.
        
        Best regards,
        Admissions Team
        """
        
        return self.send_email(to_email, subject, html_content, text_content)

# Singleton instance
email_service = EmailService()
