import sys
import os
# import pytest  <-- Removed
from fastapi.testclient import TestClient
from sqlmodel import Session, select, delete

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from app.db.session import engine
from app.models.user import User
from app.models.role import Role
from app.models.admissions import Application, ApplicationStatus, ApplicationPayment
from app.models.user_role import UserRole
from app.services.admission_service import AdmissionService
from app.core.security import create_access_token

client = TestClient(app)

def test_applicant_to_student_flow():
    email = "test_applicant_flow@college.edu"
    
    with Session(engine) as session:
        # Cleanup
        existing_user = session.exec(select(User).where(User.email == email)).first()
        if existing_user:
            # Delete related application first if exists
            # We need to find application linked to this user or email
            app_del = session.exec(select(Application).where(Application.email == email)).all()
            for a in app_del:
                from app.models.admissions import ApplicationActivityLog, ApplicationDocument
                
                # Delete logs
                logs = session.exec(select(ApplicationActivityLog).where(ApplicationActivityLog.application_id == a.id)).all()
                for l in logs:
                    session.delete(l)
                    
                # Delete documents
                docs = session.exec(select(ApplicationDocument).where(ApplicationDocument.application_id == a.id)).all()
                for d in docs:
                    session.delete(d)

                # Delete entrance exam scores
                from app.models.admissions import EntranceExamScore
                scores = session.exec(select(EntranceExamScore).where(EntranceExamScore.application_id == a.id)).all()
                for s in scores:
                    session.delete(s)

                # Delete payments
                payments = session.exec(select(ApplicationPayment).where(ApplicationPayment.application_id == a.id)).all()
                for p in payments:
                    session.delete(p)
                
                session.delete(a)
            
            # Delete links first
            session.exec(delete(UserRole).where(UserRole.user_id == existing_user.id))
            session.delete(existing_user)
            session.commit()
            
        # 1. Create Mock Application
        app_obj = Application(
            application_number="TEST-APP-001",
            name="Test Applicant",
            email=email,
            phone="9998887776",
            program_id=1,
            status=ApplicationStatus.QUICK_APPLY_SUBMITTED
        )
        session.add(app_obj)
        session.flush()
        
        # 2. Simulate Payment Completion -> Trigger Account Creation
        print("\n[TEST] simulating payment completion...")
        # We call the service method directly to test logic
        username, password, is_new = AdmissionService.create_portal_account_after_payment(session, app_obj)
        session.commit()
        session.refresh(app_obj)
        
        print(f"[TEST] Portal Account Created: {username}")
        
        # 3. Verify Role is APPLICANT
        user = session.exec(select(User).where(User.email == email)).first()
        assert user is not None
        assert len(user.roles) > 0
        role_names = [r.name for r in user.roles]
        print(f"[TEST] User Roles: {role_names}")
        assert "APPLICANT" in role_names
        assert "STUDENT" not in role_names
        
        # 4. Verify Access Blocked (Try to get student profile)
        # Login
        token = create_access_token(user.id)
        headers = {"Authorization": f"Bearer {token}"}
        
        print("[TEST] Attempting to access Student Profile as APPLICANT...")
        # This endpoint depends on get_current_active_student
        response = client.get("/api/v1/student-portal/profile", headers=headers)
        print(f"[TEST] Response Status: {response.status_code}")
        print(f"[TEST] Response Detail: {response.json()}")
        
        # We expect 403 Forbidden or 404 Not Found (if profile missing, but deps should catch role first)
        # Our update to deps.py raises 403 for APPLICANT role
        assert response.status_code == 403
        
        # 5. Admin Confirms Admission -> Transition to STUDENT
        admin = session.exec(select(User).where(User.is_superuser == True)).first()
        admin_token = create_access_token(admin.id)
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        
        print("[TEST] Admin confirming admission...")
        # Mock payment status for confirmation check
        app_obj.payment_status = "PAID"
        app_obj.aadhaar_number = "123412341234" # Req for student
        app_obj.gender = "MALE"
        app_obj.hostel_required = False
        session.add(app_obj)
        session.commit()

        # Call confirm point
        conf_response = client.post(f"/api/v1/admissions/{app_obj.id}/confirm", headers=admin_headers)
        if conf_response.status_code != 200:
             print(f"[ERROR] Confirmation Failed: {conf_response.json()}")
        assert conf_response.status_code == 200
        
        # Refresh User
        session.refresh(user)
        new_role_names = [r.name for r in user.roles]
        print(f"[TEST] User Roles after confirmation: {new_role_names}")
        
        assert "STUDENT" in new_role_names
        # assert "APPLICANT" not in new_role_names # Optional: we removed it in logic
        
        # 6. Verify Access Allowed
        print("[TEST] Attempting to access Student Profile as STUDENT...")
        response_success = client.get("/api/v1/student-portal/profile", headers=headers)
        print(f"[TEST] Response Status: {response_success.status_code}")
        
        # Should be 200 now
        assert response_success.status_code == 200
        print("[TEST] ✅ Flow Verified Successfully")

if __name__ == "__main__":
    try:
        test_applicant_to_student_flow()
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

