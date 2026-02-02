from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from typing import List, Optional, Any
from sqlmodel import Session
from app.api.deps import get_session, get_current_user
from ..services.import_service import ImportService
from ..schemas.system import ImportExecuteRequest

router = APIRouter()

@router.post("/preview", tags=["System - Imports"])
def preview_import(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    service = ImportService(session)
    return service.preview_import(file, current_user.id)

@router.post("/execute", tags=["System - Imports"])
def execute_import(
    preview_data: Any,
    file_name: str,
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    service = ImportService(session)
    return service.execute_import(preview_data.rows, current_user.id, file_name)
