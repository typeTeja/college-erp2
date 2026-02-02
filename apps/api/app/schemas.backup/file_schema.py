"""Pydantic schemas for file upload/download operations"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.file_metadata import FileModule


class FileUploadResponse(BaseModel):
    """Response after successful file upload"""
    id: int
    file_key: str
    original_filename: str
    file_size: int
    mime_type: Optional[str]
    download_url: str
    uploaded_at: datetime


class FileDownloadResponse(BaseModel):
    """Response with file download URL"""
    id: int
    file_key: str
    original_filename: str
    file_size: int
    mime_type: Optional[str]
    download_url: str
    expires_in: int  # Seconds until URL expires


class PresignedUploadUrlRequest(BaseModel):
    """Request for presigned upload URL"""
    filename: str
    content_type: str
    module: FileModule
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None


class PresignedUploadUrlResponse(BaseModel):
    """Response with presigned upload URL"""
    upload_url: str
    file_key: str
    bucket_name: str
    expires_in: int  # Seconds until URL expires


class FileListResponse(BaseModel):
    """Response with list of files"""
    files: List[FileUploadResponse]
    total: int
    skip: int
    limit: int
