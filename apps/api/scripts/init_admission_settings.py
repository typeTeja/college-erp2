"""
Script to initialize default admission settings
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select
from app.db.session import engine
from app.models.admission_settings import AdmissionSettings

def init_admission_settings():
    """Initialize admission settings with default values"""
    with Session(engine) as session:
        # Check if settings already exist
        existing = session.exec(select(AdmissionSettings)).first()
        
        if existing:
            print(f"✅ Admission settings already exist (ID: {existing.id})")
            print(f"   - Application Fee Enabled: {existing.application_fee_enabled}")
            print(f"   - Application Fee Amount: ₹{existing.application_fee_amount}")
            print(f"   - Online Payment Enabled: {existing.online_payment_enabled}")
            print(f"   - Offline Payment Enabled: {existing.offline_payment_enabled}")
            print(f"   - Auto Create Student Account: {existing.auto_create_student_account}")
            print(f"   - Send Credentials Email: {existing.send_credentials_email}")
            print(f"   - Send Credentials SMS: {existing.send_credentials_sms}")
            return existing
        
        # Create default settings
        settings = AdmissionSettings(
            application_fee_enabled=True,
            application_fee_amount=500.0,
            online_payment_enabled=True,
            offline_payment_enabled=True,
            payment_gateway="razorpay",
            auto_create_student_account=True,
            send_credentials_email=True,
            send_credentials_sms=True,
            portal_base_url="http://localhost:3000"
        )
        
        session.add(settings)
        session.commit()
        session.refresh(settings)
        
        print("✅ Created default admission settings:")
        print(f"   - Application Fee: ₹{settings.application_fee_amount}")
        print(f"   - Online Payment: Enabled")
        print(f"   - Offline Payment: Enabled")
        print(f"   - Auto Create Accounts: Enabled")
        print(f"   - Email Notifications: Enabled")
        print(f"   - SMS Notifications: Enabled")
        
        return settings

if __name__ == "__main__":
    print("Initializing Admission Settings...")
    init_admission_settings()
    print("\n✅ Done!")
