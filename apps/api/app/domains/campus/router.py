from fastapi import APIRouter
from .hostel.router import router as hostel_router
from .library.router import router as library_router
from .inventory.router import router as inventory_router
from .transport.router import router as transport_router

router = APIRouter()

router.include_router(hostel_router, prefix="/hostels", tags=["Campus - Hostel"])
router.include_router(library_router, prefix="/library", tags=["Campus - Library"])
router.include_router(inventory_router, prefix="/inventory", tags=["Campus - Inventory"])
router.include_router(transport_router, prefix="/transport", tags=["Campus - Transport"])
