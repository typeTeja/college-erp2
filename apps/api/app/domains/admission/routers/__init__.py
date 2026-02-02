from fastapi import APIRouter
from .application import router as application_router
from .enhanced import router as enhanced_router
from .admin import router as admin_router

router = APIRouter()
router.include_router(application_router, tags=["Application"])
router.include_router(enhanced_router, prefix="/enhanced", tags=["Enhanced Admission"])
router.include_router(admin_router, prefix="/admin", tags=["Admission Admin"])
