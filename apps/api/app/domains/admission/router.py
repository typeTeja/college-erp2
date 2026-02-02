"""
Admission Domain Router

All API endpoints for the admission domain.
Re-exports routers from subdirectory for backward compatibility.
"""

from fastapi import APIRouter
from .routers.application import router as application_router
from .routers.enhanced import router as enhanced_router
from .routers.admin import router as admin_router

router = APIRouter()

# Include all sub-routers
router.include_router(application_router, tags=["Application"])
router.include_router(enhanced_router, prefix="/enhanced", tags=["Enhanced Admission"])
router.include_router(admin_router, prefix="/admin", tags=["Admission Admin"])
