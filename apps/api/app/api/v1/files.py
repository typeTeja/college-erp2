"""File upload and management API endpoints"""
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from sqlmodel import Session, select
from datetime import datetime

from app.db.session import get_session
from app.api.deps import get_current_user
from app.models.user import User
from app.models.file_metadata import FileMetadata, FileModule
from app.services.storage_service import storage_service
from app.schemas.file_schema import (
    FileUploadResponse,
    FileDownloadResponse,
    FileListResponse,
    PresignedUploadUrlRequest,
    PresignedUploadUrlResponse
)

router = APIRouter()


@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    module: FileModule = Query(...),
    entity_type: Optional[str] = Query(None),
    entity_id: Optional[int] = Query(None),
    description: Optional[str] = Query(None),
    is_public: bool = Query(False),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a file to S3/MinIO storage
    
    - **file**: File to upload
    - **module**: Module uploading the file (ADMISSIONS, STUDENTS, etc.)
    - **entity_type**: Optional entity type (e.g., 'Application', 'Student')
    - **entity_id**: Optional entity ID
    - **description**: Optional file description
    - **is_public**: Whether file should be publicly accessible
    """
    # Determine bucket based on file type and module
    if file.content_type and file.content_type.startswith('image/'):
        bucket = storage_service.bucket_images
    else:
        bucket = storage_service.bucket_documents
    
    # Generate prefix based on module and entity
    prefix = f"{module.value.lower()}"
    if entity_type and entity_id:
        prefix = f"{prefix}/{entity_type.lower()}/{entity_id}"
    
    # Upload file
    try:
        file_key, file_size, mime_type = await storage_service.upload_file(
            file=file,
            prefix=prefix,
            bucket=bucket
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    
    # Create file metadata record
    file_metadata = FileMetadata(
        file_key=file_key,
        bucket_name=bucket,
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
    
    # Generate download URL
    download_url = storage_service.generate_presigned_download_url(
        key=file_key,
        bucket=bucket,
        expiration=300 if not is_public else 86400  # 5 min for private, 24h for public
    )
    
    return FileUploadResponse(
        id=file_metadata.id,
        file_key=file_key,
        original_filename=file.filename,
        file_size=file_size,
        mime_type=mime_type,
        download_url=download_url,
        uploaded_at=file_metadata.uploaded_at
    )


@router.post("/presigned-upload-url", response_model=PresignedUploadUrlResponse)
async def get_presigned_upload_url(
    request: PresignedUploadUrlRequest,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Generate a presigned URL for direct browser upload to S3/MinIO
    
    This allows the frontend to upload files directly to S3 without going through the backend,
    which is more efficient for large files.
    """
    # Determine bucket
    if request.content_type and request.content_type.startswith('image/'):
        bucket = storage_service.bucket_images
    else:
        bucket = storage_service.bucket_documents
    
    # Generate file key
    prefix = f"{request.module.value.lower()}"
    if request.entity_type and request.entity_id:
        prefix = f"{prefix}/{request.entity_type.lower()}/{request.entity_id}"
    
    file_key = storage_service._generate_unique_key(prefix, request.filename)
    
    # Generate presigned upload URL
    upload_url = storage_service.generate_presigned_upload_url(
        key=file_key,
        bucket=bucket,
        content_type=request.content_type,
        expiration=900  # 15 minutes
    )
    
    return PresignedUploadUrlResponse(
        upload_url=upload_url,
        file_key=file_key,
        bucket_name=bucket,
        expires_in=900
    )


@router.post("/confirm-upload/{file_key:path}", response_model=FileUploadResponse)
async def confirm_upload(
    file_key: str,
    module: FileModule = Query(...),
    original_filename: str = Query(...),
    file_size: int = Query(...),
    mime_type: str = Query(...),
    entity_type: Optional[str] = Query(None),
    entity_id: Optional[int] = Query(None),
    description: Optional[str] = Query(None),
    is_public: bool = Query(False),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Confirm a file upload after direct browser upload via presigned URL
    
    After the frontend uploads directly to S3, it should call this endpoint
    to create the metadata record in the database.
    """
    # Determine bucket from file_key or mime_type
    if mime_type and mime_type.startswith('image/'):
        bucket = storage_service.bucket_images
    else:
        bucket = storage_service.bucket_documents
    
    # Verify file exists in S3
    if not storage_service.file_exists(file_key, bucket):
        raise HTTPException(status_code=404, detail="File not found in storage")
    
    # Create file metadata record
    file_metadata = FileMetadata(
        file_key=file_key,
        bucket_name=bucket,
        original_filename=original_filename,
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
    
    # Generate download URL
    download_url = storage_service.generate_presigned_download_url(
        key=file_key,
        bucket=bucket,
        expiration=300 if not is_public else 86400
    )
    
    return FileUploadResponse(
        id=file_metadata.id,
        file_key=file_key,
        original_filename=original_filename,
        file_size=file_size,
        mime_type=mime_type,
        download_url=download_url,
        uploaded_at=file_metadata.uploaded_at
    )


@router.get("/{file_id}/download", response_model=FileDownloadResponse)
async def get_download_url(
    file_id: int,
    expiration: int = Query(300, ge=60, le=86400),  # 1 min to 24 hours
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get a presigned download URL for a file
    
    - **file_id**: ID of the file metadata record
    - **expiration**: URL expiration time in seconds (default: 300 = 5 minutes)
    """
    file_metadata = session.get(FileMetadata, file_id)
    if not file_metadata:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Check if file is deleted
    if file_metadata.deleted_at:
        raise HTTPException(status_code=410, detail="File has been deleted")
    
    # Generate download URL
    download_url = storage_service.generate_presigned_download_url(
        key=file_metadata.file_key,
        bucket=file_metadata.bucket_name,
        filename=file_metadata.original_filename,
        expiration=expiration
    )
    
    return FileDownloadResponse(
        id=file_metadata.id,
        file_key=file_metadata.file_key,
        original_filename=file_metadata.original_filename,
        file_size=file_metadata.file_size,
        mime_type=file_metadata.mime_type,
        download_url=download_url,
        expires_in=expiration
    )


@router.get("/", response_model=FileListResponse)
async def list_files(
    module: Optional[FileModule] = Query(None),
    entity_type: Optional[str] = Query(None),
    entity_id: Optional[int] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    List files with optional filtering
    
    - **module**: Filter by module
    - **entity_type**: Filter by entity type
    - **entity_id**: Filter by entity ID
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return
    """
    # Build query
    statement = select(FileMetadata).where(FileMetadata.deleted_at == None)
    
    if module:
        statement = statement.where(FileMetadata.module == module)
    if entity_type:
        statement = statement.where(FileMetadata.entity_type == entity_type)
    if entity_id:
        statement = statement.where(FileMetadata.entity_id == entity_id)
    
    # Get total count
    count_statement = statement
    total = len(session.exec(count_statement).all())
    
    # Apply pagination
    statement = statement.offset(skip).limit(limit).order_by(FileMetadata.uploaded_at.desc())
    
    files = session.exec(statement).all()
    
    # Generate download URLs for each file
    file_responses = []
    for file_meta in files:
        download_url = storage_service.generate_presigned_download_url(
            key=file_meta.file_key,
            bucket=file_meta.bucket_name,
            expiration=300
        )
        file_responses.append(FileUploadResponse(
            id=file_meta.id,
            file_key=file_meta.file_key,
            original_filename=file_meta.original_filename,
            file_size=file_meta.file_size,
            mime_type=file_meta.mime_type,
            download_url=download_url,
            uploaded_at=file_meta.uploaded_at
        ))
    
    return FileListResponse(
        files=file_responses,
        total=total,
        skip=skip,
        limit=limit
    )


@router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Soft delete a file (marks as deleted but doesn't remove from storage)
    
    To permanently delete, use /files/{file_id}/permanent-delete
    """
    file_metadata = session.get(FileMetadata, file_id)
    if not file_metadata:
        raise HTTPException(status_code=404, detail="File not found")
    
    if file_metadata.deleted_at:
        raise HTTPException(status_code=410, detail="File already deleted")
    
    # Soft delete
    file_metadata.deleted_at = datetime.utcnow()
    session.add(file_metadata)
    session.commit()
    
    return {"message": "File deleted successfully", "file_id": file_id}


@router.delete("/{file_id}/permanent")
async def permanent_delete_file(
    file_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Permanently delete a file from storage and database
    
    WARNING: This action cannot be undone!
    """
    file_metadata = session.get(FileMetadata, file_id)
    if not file_metadata:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Delete from S3
    storage_service.delete_file(file_metadata.file_key, file_metadata.bucket_name)
    
    # Delete from database
    session.delete(file_metadata)
    session.commit()
    
    return {"message": "File permanently deleted", "file_id": file_id}
