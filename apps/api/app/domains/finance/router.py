"""
Finance Domain Router

All API endpoints for the finance domain.
Re-exports routers from subdirectory for backward compatibility.
"""

from fastapi import APIRouter
from .routers.fees import router as fees_router
from .routers.gateway import router as gateway_router
from .routers.easebuzz import router as easebuzz_router

router = APIRouter()

# Include all sub-routers
router.include_router(fees_router, prefix="/fees", tags=["Fees"])
router.include_router(gateway_router, prefix="/gateway", tags=["Payment Gateway"])
router.include_router(easebuzz_router, prefix="/easebuzz", tags=["Easebuzz"])
