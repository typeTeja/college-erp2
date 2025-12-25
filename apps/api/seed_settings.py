from sqlmodel import Session, select
from app.db.session import engine
from app.models.settings import SystemSetting, SettingGroup

def seed_settings():
    initial_settings = [
        # Institute Identity
        {"key": "institute.name", "value": "Regency College of Hotel Management", "group": SettingGroup.INSTITUTE},
        {"key": "institute.short_code", "value": "RCHM", "group": SettingGroup.INSTITUTE},
        {"key": "institute.address", "value": "Hyderabad, Telangana", "group": SettingGroup.INSTITUTE},
        
        # Academic Config
        {"key": "academic.current_year", "value": "2024-2025", "group": SettingGroup.ACADEMIC},
        {"key": "academic.working_days", "value": ["MON", "TUE", "WED", "THU", "FRI", "SAT"], "group": SettingGroup.ACADEMIC},
        
        # Attendance Rules
        {"key": "attendance.grace_time", "value": 15, "group": SettingGroup.ACADEMIC},
        
        # Integration (Secrets)
        {"key": "integration.msg91_key", "value": "", "group": SettingGroup.INTEGRATION, "is_secret": True},
        {"key": "integration.easebuzz_key", "value": "", "group": SettingGroup.INTEGRATION, "is_secret": True},
    ]

    with Session(engine) as session:
        for setting_data in initial_settings:
            # Check if exists
            existing = session.exec(select(SystemSetting).where(SystemSetting.key == setting_data["key"])).first()
            if not existing:
                setting = SystemSetting(**setting_data)
                session.add(setting)
        
        session.commit()
        print("Success: Initial settings seeded.")

if __name__ == "__main__":
    seed_settings()
