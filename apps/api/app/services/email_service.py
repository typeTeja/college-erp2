"""Email notification service for sending application-related emails"""
from typing import Optional, Dict
from datetime import datetime
from pydantic import BaseSettings, EmailStr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSettings(BaseSettings):
    """Email configuration"""
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    FROM_EMAIL: str = ""
    FROM_NAME: str = "College ERP - Admissions"
    
    class Config:
        env_file = ".env"

email_settings = EmailSettings()

class EmailService:
    """Service for sending emails"""
    
    def __init__(self):
        self.smtp_host = email_settings.SMTP_HOST
        self.smtp_port = email_settings.SMTP_PORT
        self.smtp_user = email_settings.SMTP_USER
        self.smtp_password = email_settings.SMTP_PASSWORD
        self.from_email = email_settings.FROM_EMAIL
        self.from_name = email_settings.FROM_NAME
    
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
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            
            # Add text and HTML parts
            if text_content:
                part1 = MIMEText(text_content, 'plain')
                msg.attach(part1)
            
            part2 = MIMEText(html_content, 'html')
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
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

# Singleton instance
email_service = EmailService()
