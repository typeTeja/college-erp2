from fastapi import APIRouter
from app.api.v1 import auth

api_router = APIRouter()

# Include auth routes
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])

from app.api.v1 import odc
api_router.include_router(odc.router, prefix="/odc", tags=["odc"])

