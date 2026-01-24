import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import Session, select
from app.db.session import engine
from app.models.user import User
from app.models.role import Role
from app.models.admissions import Application, ApplicationStatus
from app.services.admission_service import AdmissionService

def test_reapplication_flow():
    with Session(engine) as session:
        print("🚀 Starting Re-application Flow Test...")
        
        # 1. Ensure Student Role Exists
        student_role = session.exec(select(Role).where(Role.name == "STUDENT")).first()
        if not student_role:
            print("❌ Student role not found. Creating temporary role...")
            student_role = Role(name="STUDENT", description="Student Role")
            session.add(student_role)
            session.commit()
            session.refresh(student_role)
        
        # 2. Create/Get Existing User
        test_email = "test_reapply@example.com"
        existing_user = session.exec(select(User).where(User.email == test_email)).first()
        
        if not existing_user:
            print(f"Creating foundational user: {test_email}")
            existing_user = User(
                username="testuser99",
                email=test_email,
                hashed_password="hashed_secret",
                full_name="Test User Original",
                is_active=True
            )
            session.add(existing_user)
            session.commit()
            session.refresh(existing_user)
        else:
            print(f"Using existing user: {existing_user.id}")

        # 3. Create NEW Application with SAME Email
        print("Creating new application with same email...")
        new_app = Application(
            application_number=f"APP-TEST-{datetime.utcnow().timestamp()}",
            name="Test User New App",
            email=test_email, # SAME EMAIL
            phone="9999999999",
            gender="Male",
            program_id=1, # Assuming program 1 exists or FK not strict in partial logic
            state="TestState",
            board="CBSE",
            group_of_study="MPC",
            status=ApplicationStatus.PENDING_PAYMENT,
            application_fee=500.0,
            fee_mode="ONLINE"
        )
        session.add(new_app)
        session.commit()
        session.refresh(new_app)
        print(f"Created Application ID: {new_app.id}")

        # 4. Run Logic: Create Portal Account (Simulation)
        print(">>> Executing AdmissionService.create_portal_account_after_payment...")
        try:
            username, password, is_new = AdmissionService.create_portal_account_after_payment(
                session=session,
                application=new_app
            )
            
            print(f"Result: username={username}, password={password}, is_new={is_new}")
            
            # 5. Verification
            if is_new:
                 print("❌ FAILED: Should not be marked as new account.")
            else:
                 print("✅ SUCCESS: Correctly identified as existing account.")
                 
            if new_app.portal_user_id == existing_user.id:
                 print(f"✅ SUCCESS: Application linked to User ID {existing_user.id}")
            else:
                 print(f"❌ FAILED: Linked to wrong user ID: {new_app.portal_user_id}")
                 
            if password is None:
                 print("✅ SUCCESS: No password returned (security safe).")
            else:
                 print("❌ FAILED: Password returned for existing user.")

        except Exception as e:
            print(f"❌ EXCEPTION during execution: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_reapplication_flow()
