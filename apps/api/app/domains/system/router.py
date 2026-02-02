from .routers.settings import router as settings_router
from .routers.institute import router as institute_router
from .routers.files import router as files_router
from .routers.audit import router as audit_router
from .routers.imports import router as imports_router

router = APIRouter()
router.include_router(settings_router, prefix="/settings")
router.include_router(institute_router, prefix="/institute")
router.include_router(files_router, prefix="/files")
router.include_router(audit_router, prefix="/audit")
router.include_router(imports_router, prefix="/imports")
