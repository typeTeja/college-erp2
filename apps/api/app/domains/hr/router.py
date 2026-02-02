from fastapi import APIRouter
from .routers.staff import router as staff_router
from .routers.faculty import router as faculty_router
from .routers.designation import router as designation_router

router = APIRouter()

router.include_router(staff_router)
router.include_router(faculty_router)
router.include_router(designation_router)
