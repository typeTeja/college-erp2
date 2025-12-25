from fastapi import APIRouter
from app.api.v1 import auth, odc, dashboard, admissions, import_api, fees

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
api_router.include_router(import_api.router, prefix="/import", tags=["import"])

# Include fees routes
api_router.include_router(fees.router, prefix="/fees", tags=["fees"])
