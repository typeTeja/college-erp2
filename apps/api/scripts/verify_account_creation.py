import asyncio
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from sqlmodel import Session, select
from app.db.session import engine
from app.services.admission_service import AdmissionService
from app.models.admissions import Application, ApplicationStatus
from app.models.role import Role
from app.models.user import User

async def verify_account_creation():
    with Session(engine) as session:
        print("1. Checking STUDENT Role...")
        role = session.exec(select(Role).where(Role.name == "STUDENT")).first()
        if role:
            print(f"   ✅ Role Found: {role.name} (ID: {role.id})")
        else:
            print("   ❌ Role STUDENT NOT Found! Verification will fail.")
            return

        print("\n2. Creating Test Application...")
        # Create a dummy application
        app = AdmissionService.create_quick_apply(
            session=session,
            name="Test Account Gen",
            email="test.account@example.com",
            phone="9988776644",
            gender="FEMALE",
            program_id=1,
            state="Test State",
            board="CBSE",
            group_of_study="MPC",
            payment_mode="ONLINE"
        )
        print(f"   Created Application: {app.application_number} (ID: {app.id})")
        
        # Ensure settings allow auto account creation
        settings = AdmissionService.get_admission_settings(session)
        settings.auto_create_student_account = True
        session.add(settings)
        session.commit()
        
        print("\n3. Testing Logic: create_portal_account_after_payment...")
        try:
            username, password = AdmissionService.create_portal_account_after_payment(
                session=session,
                application=app
            )
            
            print(f"   ✅ Account Created Successfully!")
            print(f"   Username: {username}")
            print(f"   Password: {password}")
            
            # Verify User in DB
            user = session.exec(select(User).where(User.username == username)).first()
            if user:
                print(f"   ✅ User Record Found: ID {user.id}")
                
                # Check Role Link
                from app.models.user_role import UserRole
                link = session.exec(select(UserRole).where(
                    UserRole.user_id == user.id,
                    UserRole.role_id == role.id
                )).first()
                if link:
                    print("   ✅ User has STUDENT role linked")
                else:
                     print("   ❌ User missing STUDENT role link")
            else:
                print("   ❌ User Record NOT Found")
                
            # Verify Link in Application
            session.refresh(app)
            if app.portal_user_id == user.id:
                 print("   ✅ Application linked to User")
            else:
                 print(f"   ❌ Application link mismatch: {app.portal_user_id}")
                 
        except Exception as e:
            print(f"   ❌ Error creating account: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(verify_account_creation())
