from fastapi import APIRouter
from .routers.students import router as students_router
from .routers.odc import router as odc_router
from .routers.document import router as document_router
from .routers.portal import router as portal_router

router = APIRouter()

router.include_router(students_router, tags=["Students"])
router.include_router(portal_router, prefix="/portal", tags=["Student Portal"])
router.include_router(odc_router, prefix="/odc", tags=["ODC"])
router.include_router(document_router, prefix="/documents", tags=["Documents"])
