import sys
import os

# Add apps/api to path
sys.path.append(os.path.abspath('apps/api'))

# Mock env vars for settings validation if needed
os.environ['DATABASE_URL'] = 'sqlite:///test.db'
os.environ['SECRET_KEY'] = 'test-secret-key'
os.environ['BACKEND_BASE_URL'] = 'http://localhost:8000'
os.environ['PORTAL_BASE_URL'] = 'http://localhost:3000'

try:
    print("Verifying Admissions Domain Imports...")
    
    from app.domains.admission.models import Application, AdmissionSettings
    print("✅ Models imported")
    
    from app.domains.admission.schemas import ApplicationCreate, ApplicationRead
    print("✅ Schemas imported")
    
    from app.domains.admission.service import AdmissionService
    print("✅ Service imported")
    
    from app.domains.admission.router import router
    print("✅ Router imported")
    
    from app.api.v1.router import api_router
    print("✅ Main API Router updated and imported")
    
    print("\nAdmissions Domain Migration Verified Successfully!")
except Exception as e:
    print(f"\n❌ Verification Failed: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
