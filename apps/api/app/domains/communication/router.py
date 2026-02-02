from fastapi import APIRouter
from .routers.communication import router as comm_router

router = APIRouter()
router.include_router(comm_router)
