"""
Communication Domain Router

All API endpoints for the communication domain.
Re-exports router from subdirectory for backward compatibility.
"""

from fastapi import APIRouter
from .routers.communication import router as communication_router

router = APIRouter()

# Include communication router
router.include_router(communication_router, tags=["Communication"])
