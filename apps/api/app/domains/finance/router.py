from fastapi import APIRouter
from .routers.fees import router as fees_router
from .routers.gateway import router as gateway_router
from .easebuzz import router as easebuzz_router

router = APIRouter()

router.include_router(fees_router, tags=["Fees"])
router.include_router(gateway_router, prefix="/payments", tags=["Payments"])
router.include_router(easebuzz_router, prefix="/easebuzz", tags=["Easebuzz"])
