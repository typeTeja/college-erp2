from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ..models.files import FileModule

class FileUploadResponse(BaseModel):
    id: int
    file_key: str
    original_filename: str
    file_size: int
    mime_type: Optional[str]
    download_url: str
    uploaded_at: datetime

class FileDownloadResponse(BaseModel):
    id: int
    file_key: str
    original_filename: str
    file_size: int
    mime_type: Optional[str]
    download_url: str
    expires_in: int 

class PresignedUploadUrlRequest(BaseModel):
    filename: str
    content_type: str
    module: FileModule
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None

class PresignedUploadUrlResponse(BaseModel):
    upload_url: str
    file_key: str
    bucket_name: str
    expires_in: int 

class FileListResponse(BaseModel):
    files: List[FileUploadResponse]
    total: int
    skip: int
    limit: int
