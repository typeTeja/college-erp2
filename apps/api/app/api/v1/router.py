from fastapi import APIRouter
from app.api.v1 import auth, odc, dashboard, admissions, import_api, students

api_router = APIRouter()

# Include auth routes
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

# Include ODC routes
api_router.include_router(odc.router, prefix="/odc", tags=["odc"])

# Include dashboard routes
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])

# Include admissions routes
api_router.include_router(admissions.router, prefix="/admissions", tags=["admissions"])

# Include import routes
# Include import routes
api_router.include_router(import_api.router, prefix="/import", tags=["import"])

# Include students routes
api_router.include_router(students.router, prefix="/students", tags=["students"])
