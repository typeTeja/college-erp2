import sys
import os
from dotenv import load_dotenv

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load env variables from apps/api/.env
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(env_path)

print(f"Loading env from: {env_path}")
print(f"SMTP_HOST from env: {os.getenv('SMTP_HOST')}")
print(f"SMTP_USER from env: {os.getenv('SMTP_USER')}")

try:
    from app.services.email_service import email_service
    
    print("\n--- Testing Email Service ---")
    # Settings are now fetched dynamically from DB/Env
    
    to_email = os.getenv('SMTP_USER') # Send to self for testing
    
    to_email = os.getenv('SMTP_USER') # Send to self for testing
    subject = "Test Email from College ERP"
    html_content = "<h1>Test Email</h1><p>This is a test email from the College ERP system.</p>"
    text_content = "This is a test email from the College ERP system."
    
    print(f"\nSending test email to: {to_email}")
    
    success = email_service.send_email(to_email, subject, html_content, text_content)
    
    if success:
        print("\n✅ Email sent successfully!")
    else:
        print("\n❌ Failed to send email.")

except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
