import sys
import os
from pathlib import Path

# Add parent directory to path to allow importing app modules
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from sqlmodel import Session, select
from app.db.session import engine
from app.models.settings import SystemSetting, SettingGroup

def init_settings():
    """Initialize system settings from environment variables if not already present"""
    print("Initializing system settings...")
    
    with Session(engine) as session:
        # Define settings to migrate
        integrations = [
            # Easebuzz
            {
                "key": "easebuzz.merchant_key",
                "value": os.getenv("EASEBUZZ_MERCHANT_KEY", ""),
                "group": SettingGroup.INTEGRATION,
                "is_secret": True,
                "description": "Easebuzz Merchant Key"
            },
            {
                "key": "easebuzz.salt",
                "value": os.getenv("EASEBUZZ_SALT", ""),
                "group": SettingGroup.INTEGRATION,
                "is_secret": True,
                "description": "Easebuzz Salt"
            },
            {
                "key": "easebuzz.env",
                "value": os.getenv("EASEBUZZ_ENV", "test"),
                "group": SettingGroup.INTEGRATION,
                "is_secret": False,
                "description": "Easebuzz Environment (test/prod)"
            },
            # SMTP Email
            {
                "key": "smtp.host",
                "value": os.getenv("SMTP_HOST", "smtp.gmail.com"),
                "group": SettingGroup.INTEGRATION,
                "is_secret": False,
                "description": "SMTP Host"
            },
            {
                "key": "smtp.port",
                "value": os.getenv("SMTP_PORT", "587"),
                "group": SettingGroup.INTEGRATION,
                "is_secret": False,
                "description": "SMTP Port"
            },
            {
                "key": "smtp.user",
                "value": os.getenv("SMTP_USER", ""),
                "group": SettingGroup.INTEGRATION,
                "is_secret": False, # Usually visible, but maybe treat as secret? Standard practice is visible. The password is secret.
                "description": "SMTP Username"
            },
            {
                "key": "smtp.password",
                "value": os.getenv("SMTP_PASSWORD", ""),
                "group": SettingGroup.INTEGRATION,
                "is_secret": True,
                "description": "SMTP Password"
            },
            {
                "key": "email.from_name",
                "value": os.getenv("FROM_NAME", "College ERP"),
                "group": SettingGroup.INTEGRATION,
                "is_secret": False,
                "description": "Email Sender Name"
            },
            {
                "key": "email.from_email",
                "value": os.getenv("FROM_EMAIL", ""),
                "group": SettingGroup.INTEGRATION,
                "is_secret": False,
                "description": "Email Sender Address"
            },
            # Msg91 (Placeholder as per UI)
            {
                "key": "msg91.auth_key",
                "value": os.getenv("MSG91_AUTH_KEY", ""),
                "group": SettingGroup.INTEGRATION,
                "is_secret": True,
                "description": "Msg91 Auth Key"
            }
        ]

        for item in integrations:
            # Check if exists
            existing = session.exec(select(SystemSetting).where(SystemSetting.key == item["key"])).first()
            if not existing:
                print(f"Creating setting: {item['key']}")
                setting = SystemSetting(
                    key=item["key"],
                    value=item["value"],
                    group=item["group"],
                    is_secret=item["is_secret"],
                    description=item["description"]
                )
                session.add(setting)
            else:
                print(f"Setting already exists: {item['key']}")
        
        session.commit()
        print("Settings initialization complete.")

if __name__ == "__main__":
    init_settings()
