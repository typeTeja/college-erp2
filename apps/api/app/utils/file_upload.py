"""File upload utility for handling document uploads"""
import os
import uuid
from datetime import datetime
from typing import Optional
from fastapi import UploadFile, HTTPException
from pathlib import Path

# Configuration
UPLOAD_DIR = Path("uploads/applications")
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {".pdf", ".jpg", ".jpeg", ".png", ".doc", ".docx"}

def ensure_upload_dir():
    """Create upload directory if it doesn't exist"""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def validate_file(file: UploadFile) -> None:
    """
    Validate uploaded file
    
    Args:
        file: Uploaded file
        
    Raises:
        HTTPException: If file is invalid
    """
    # Check file extension
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )

async def save_upload_file(
    file: UploadFile,
    application_id: int,
    document_type: str
) -> tuple[str, int]:
    """
    Save uploaded file to disk
    
    Args:
        file: Uploaded file
        application_id: Application ID
        document_type: Type of document
        
    Returns:
        Tuple of (file_url, file_size)
        
    Raises:
        HTTPException: If file is too large or invalid
    """
    ensure_upload_dir()
    validate_file(file)
    
    # Generate unique filename
    file_ext = Path(file.filename).suffix.lower()
    unique_filename = f"{document_type}_{uuid.uuid4().hex}{file_ext}"
    
    # Create application-specific directory
    app_dir = UPLOAD_DIR / str(application_id)
    app_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = app_dir / unique_filename
    
    # Read and save file
    contents = await file.read()
    file_size = len(contents)
    
    # Check file size
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {MAX_FILE_SIZE / 1024 / 1024}MB"
        )
    
    # Write file
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Return relative URL
    file_url = f"/uploads/applications/{application_id}/{unique_filename}"
    
    return file_url, file_size

def delete_file(file_url: str) -> bool:
    """
    Delete a file from disk
    
    Args:
        file_url: Relative file URL
        
    Returns:
        True if deleted, False if file not found
    """
    try:
        # Convert URL to file path
        file_path = Path(file_url.lstrip("/"))
        if file_path.exists():
            file_path.unlink()
            return True
        return False
    except Exception:
        return False

def get_file_path(file_url: str) -> Optional[Path]:
    """
    Get absolute file path from URL
    
    Args:
        file_url: Relative file URL
        
    Returns:
        Absolute file path or None if not found
    """
    file_path = Path(file_url.lstrip("/"))
    if file_path.exists():
        return file_path.absolute()
    return None
