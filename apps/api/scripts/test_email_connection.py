import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load .env from parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

print(f"Testing SMTP connection to {SMTP_HOST}:{SMTP_PORT}...")
print(f"User: {SMTP_USER}")
# Mask password for display
masked_pwd = SMTP_PASSWORD[:4] + "***" if SMTP_PASSWORD else "None"
print(f"Password: {masked_pwd}")

try:
    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    server.starttls()
    print("TLS started. Logging in...")
    server.login(SMTP_USER, SMTP_PASSWORD)
    print("Login successful!")
    
    # Send a test email to self
    msg = MIMEText("This is a test email from College ERP debug script.")
    msg['Subject'] = "College ERP SMTP Test"
    msg['From'] = SMTP_USER
    msg['To'] = SMTP_USER
    
    server.send_message(msg)
    print("Test email sent successfully!")
    server.quit()
except Exception as e:
    print(f"SMTP Error: {e}")
