from fastapi import APIRouter
from .hostel.routers.hostel import router as hostel_router
from .library.routers.library import router as library_router
from .inventory.routers.inventory import router as inventory_router
from .transport.routers.transport import router as transport_router

router = APIRouter()

router.include_router(hostel_router, prefix="/hostels", tags=["Campus - Hostel"])
router.include_router(library_router, prefix="/library", tags=["Campus - Library"])
router.include_router(inventory_router, prefix="/inventory", tags=["Campus - Inventory"])
router.include_router(transport_router, prefix="/transport", tags=["Campus - Transport"])
