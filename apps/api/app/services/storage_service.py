"""
Storage Service - File Upload/Download

Minimal local filesystem implementation for file storage operations.
For production, consider upgrading to cloud storage (S3, Azure Blob, GCS).
"""
from typing import Tuple, Optional
from fastapi import UploadFile
import os
import uuid
from pathlib import Path
from datetime import datetime


class StorageService:
    """Local filesystem storage service"""
    
    def __init__(self):
        self.bucket_documents = "documents"
        self.bucket_images = "images"
        self.upload_dir = Path("uploads")
        self.upload_dir.mkdir(exist_ok=True)
    
    async def upload_file(
        self, 
        file: UploadFile, 
        prefix: str = "", 
        bucket: str = "documents"
    ) -> Tuple[str, int, str]:
        """
        Upload file to local storage
        
        Args:
            file: FastAPI UploadFile object
            prefix: Optional prefix for file path (e.g., "admission/2024")
            bucket: Bucket name (subdirectory)
        
        Returns:
            Tuple of (file_key, file_size, mime_type)
        """
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_ext = Path(file.filename).suffix
        unique_id = str(uuid.uuid4())[:8]
        
        # Construct file path
        if prefix:
            file_key = f"{bucket}/{prefix}/{timestamp}_{unique_id}{file_ext}"
        else:
            file_key = f"{bucket}/{timestamp}_{unique_id}{file_ext}"
        
        file_path = self.upload_dir / file_key
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save file
        content = await file.read()
        file_size = len(content)
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        mime_type = file.content_type or "application/octet-stream"
        
        return file_key, file_size, mime_type
    
    def upload_bytes(
        self, 
        content: bytes, 
        filename: str, 
        bucket: str = "documents"
    ) -> str:
        """
        Upload bytes to local storage
        
        Args:
            content: File content as bytes
            filename: Desired filename
            bucket: Bucket name (subdirectory)
        
        Returns:
            File URL (relative path)
        """
        file_path = self.upload_dir / bucket / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        return f"/uploads/{bucket}/{filename}"
    
    def get_file_path(self, file_key: str) -> Path:
        """Get absolute file path from file key"""
        return self.upload_dir / file_key
    
    def file_exists(self, file_key: str) -> bool:
        """Check if file exists"""
        return self.get_file_path(file_key).exists()
    
    def delete_file(self, file_key: str) -> bool:
        """Delete file from storage"""
        file_path = self.get_file_path(file_key)
        if file_path.exists():
            file_path.unlink()
            return True
        return False


# Singleton instance
storage_service = StorageService()
