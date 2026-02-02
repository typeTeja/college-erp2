from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from sqlmodel import Session, select
from datetime import datetime

from app.api.deps import get_session, get_current_user
from ..models.files import FileMetadata, FileModule
from ..services.storage_service import storage_service
from ..schemas.files import FileUploadResponse, FileDownloadResponse, FileListResponse, PresignedUploadUrlRequest, PresignedUploadUrlResponse

router = APIRouter()

@router.post("/upload", response_model=FileUploadResponse, tags=["System - Files"])
async def upload_file(
    file: UploadFile = File(...),
    module: FileModule = Query(...),
    entity_type: Optional[str] = Query(None),
    entity_id: Optional[int] = Query(None),
    description: Optional[str] = Query(None),
    is_public: bool = Query(False),
    session: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    """Upload a file to storage"""
    prefix = f"{module.value.lower()}"
    if entity_type and entity_id:
        prefix = f"{prefix}/{entity_type.lower()}/{entity_id}"
    
    file_key, file_size, mime_type = await storage_service.upload_file(file=file, prefix=prefix)
    
    file_metadata = FileMetadata(
        file_key=file_key,
        bucket_name=storage_service.bucket_documents,
        original_filename=file.filename,
        file_size=file_size,
        mime_type=mime_type,
        is_public=is_public,
        module=module,
        entity_type=entity_type,
        entity_id=entity_id,
        uploaded_by=current_user.id,
        description=description
    )
    
    session.add(file_metadata)
    session.commit()
    session.refresh(file_metadata)
    
    return FileUploadResponse(
        id=file_metadata.id,
        file_key=file_key,
        original_filename=file.filename,
        file_size=file_size,
        mime_type=mime_type,
        download_url="", # Simplified
        uploaded_at=file_metadata.uploaded_at
    )
