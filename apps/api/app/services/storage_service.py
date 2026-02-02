"""
Storage Service - S3/MinIO Cloud Storage

Production-ready cloud storage implementation using MinIO (S3-compatible).
Supports file upload, download, deletion, and presigned URLs.
"""
from typing import Tuple, Optional
from fastapi import UploadFile, HTTPException
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
import uuid
from datetime import datetime, timedelta
from pathlib import Path
import logging

from app.config.settings import settings

logger = logging.getLogger(__name__)


class StorageService:
    """S3/MinIO cloud storage service"""
    
    def __init__(self):
        """Initialize S3/MinIO client"""
        self.storage_backend = settings.STORAGE_BACKEND
        
        if self.storage_backend == "s3":
            # S3/MinIO configuration
            self.s3_client = boto3.client(
                's3',
                endpoint_url=settings.S3_ENDPOINT,
                aws_access_key_id=settings.S3_ACCESS_KEY,
                aws_secret_access_key=settings.S3_SECRET_KEY,
                region_name=settings.S3_REGION,
                config=Config(
                    signature_version='s3v4',
                    s3={'addressing_style': 'path'} if settings.S3_FORCE_PATH_STYLE else {}
                )
            )
            
            # Bucket names
            self.bucket_documents = settings.S3_BUCKET
            self.bucket_images = settings.S3_BUCKET_IMAGES
            self.bucket_temp = settings.S3_BUCKET_TEMP
            
            # Ensure buckets exist
            self._ensure_buckets_exist()
        else:
            # Fallback to local filesystem
            self.bucket_documents = "documents"
            self.bucket_images = "images"
            self.bucket_temp = "temp"
            self.upload_dir = Path("uploads")
            self.upload_dir.mkdir(exist_ok=True)
            logger.warning("Using local filesystem storage (not recommended for production)")
    
    def _ensure_buckets_exist(self):
        """Ensure S3 buckets exist, create if they don't"""
        if self.storage_backend != "s3":
            return
        
        buckets = [self.bucket_documents, self.bucket_images, self.bucket_temp]
        
        try:
            existing_buckets = [b['Name'] for b in self.s3_client.list_buckets()['Buckets']]
            
            for bucket in buckets:
                if bucket not in existing_buckets:
                    try:
                        self.s3_client.create_bucket(Bucket=bucket)
                        logger.info(f"Created S3 bucket: {bucket}")
                    except ClientError as e:
                        if e.response['Error']['Code'] != 'BucketAlreadyOwnedByYou':
                            logger.error(f"Error creating bucket {bucket}: {e}")
        except Exception as e:
            logger.error(f"Error checking/creating buckets: {e}")
    
    async def upload_file(
        self, 
        file: UploadFile, 
        prefix: str = "", 
        bucket: str = None
    ) -> Tuple[str, int, str]:
        """
        Upload file to S3/MinIO or local storage
        
        Args:
            file: FastAPI UploadFile object
            prefix: Optional prefix for file path (e.g., "admission/2024")
            bucket: Bucket name (defaults to documents bucket)
        
        Returns:
            Tuple of (file_key, file_size, mime_type)
        """
        if bucket is None:
            bucket = self.bucket_documents
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_ext = Path(file.filename).suffix
        unique_id = str(uuid.uuid4())[:8]
        
        # Construct file key
        if prefix:
            file_key = f"{prefix}/{timestamp}_{unique_id}{file_ext}"
        else:
            file_key = f"{timestamp}_{unique_id}{file_ext}"
        
        # Read file content
        content = await file.read()
        file_size = len(content)
        mime_type = file.content_type or "application/octet-stream"
        
        # Check file size
        if file_size > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size: {settings.MAX_UPLOAD_SIZE / 1024 / 1024}MB"
            )
        
        if self.storage_backend == "s3":
            # Upload to S3/MinIO
            try:
                self.s3_client.put_object(
                    Bucket=bucket,
                    Key=file_key,
                    Body=content,
                    ContentType=mime_type,
                    Metadata={
                        'original_filename': file.filename,
                        'upload_timestamp': timestamp
                    }
                )
                logger.info(f"Uploaded file to S3: {bucket}/{file_key}")
            except ClientError as e:
                logger.error(f"S3 upload error: {e}")
                raise HTTPException(status_code=500, detail="File upload failed")
        else:
            # Fallback to local filesystem
            file_path = self.upload_dir / bucket / file_key
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, "wb") as f:
                f.write(content)
            
            logger.info(f"Uploaded file locally: {file_path}")
        
        return file_key, file_size, mime_type
    
    def upload_bytes(
        self, 
        content: bytes, 
        filename: str, 
        bucket: str = None,
        content_type: str = "application/octet-stream"
    ) -> str:
        """
        Upload bytes to S3/MinIO or local storage
        
        Args:
            content: File content as bytes
            filename: Desired filename/key
            bucket: Bucket name (defaults to documents bucket)
            content_type: MIME type
        
        Returns:
            File URL or key
        """
        if bucket is None:
            bucket = self.bucket_documents
        
        if self.storage_backend == "s3":
            # Upload to S3/MinIO
            try:
                self.s3_client.put_object(
                    Bucket=bucket,
                    Key=filename,
                    Body=content,
                    ContentType=content_type
                )
                
                # Return CDN URL if configured, otherwise S3 URL
                if settings.CDN_BASE_URL:
                    return f"{settings.CDN_BASE_URL}/{bucket}/{filename}"
                else:
                    return f"{settings.S3_ENDPOINT}/{bucket}/{filename}"
            except ClientError as e:
                logger.error(f"S3 upload error: {e}")
                raise HTTPException(status_code=500, detail="File upload failed")
        else:
            # Fallback to local filesystem
            file_path = self.upload_dir / bucket / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, "wb") as f:
                f.write(content)
            
            return f"/uploads/{bucket}/{filename}"
    
    def get_presigned_url(
        self, 
        file_key: str, 
        bucket: str = None,
        expiration: int = 3600
    ) -> str:
        """
        Generate presigned URL for temporary file access
        
        Args:
            file_key: File key in S3
            bucket: Bucket name (defaults to documents bucket)
            expiration: URL expiration in seconds (default: 1 hour)
        
        Returns:
            Presigned URL
        """
        if bucket is None:
            bucket = self.bucket_documents
        
        if self.storage_backend == "s3":
            try:
                url = self.s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': bucket, 'Key': file_key},
                    ExpiresIn=expiration
                )
                return url
            except ClientError as e:
                logger.error(f"Error generating presigned URL: {e}")
                raise HTTPException(status_code=500, detail="Failed to generate download URL")
        else:
            # Local filesystem - return direct path
            return f"/uploads/{bucket}/{file_key}"
    
    def file_exists(self, file_key: str, bucket: str = None) -> bool:
        """Check if file exists in S3/MinIO or local storage"""
        if bucket is None:
            bucket = self.bucket_documents
        
        if self.storage_backend == "s3":
            try:
                self.s3_client.head_object(Bucket=bucket, Key=file_key)
                return True
            except ClientError:
                return False
        else:
            file_path = self.upload_dir / bucket / file_key
            return file_path.exists()
    
    def delete_file(self, file_key: str, bucket: str = None) -> bool:
        """Delete file from S3/MinIO or local storage"""
        if bucket is None:
            bucket = self.bucket_documents
        
        if self.storage_backend == "s3":
            try:
                self.s3_client.delete_object(Bucket=bucket, Key=file_key)
                logger.info(f"Deleted file from S3: {bucket}/{file_key}")
                return True
            except ClientError as e:
                logger.error(f"Error deleting file: {e}")
                return False
        else:
            file_path = self.upload_dir / bucket / file_key
            if file_path.exists():
                file_path.unlink()
                return True
            return False
    
    def get_file_metadata(self, file_key: str, bucket: str = None) -> dict:
        """Get file metadata from S3/MinIO"""
        if bucket is None:
            bucket = self.bucket_documents
        
        if self.storage_backend == "s3":
            try:
                response = self.s3_client.head_object(Bucket=bucket, Key=file_key)
                return {
                    'size': response['ContentLength'],
                    'content_type': response.get('ContentType'),
                    'last_modified': response['LastModified'],
                    'metadata': response.get('Metadata', {})
                }
            except ClientError as e:
                logger.error(f"Error getting file metadata: {e}")
                return {}
        else:
            file_path = self.upload_dir / bucket / file_key
            if file_path.exists():
                stat = file_path.stat()
                return {
                    'size': stat.st_size,
                    'last_modified': datetime.fromtimestamp(stat.st_mtime)
                }
            return {}


# Singleton instance
storage_service = StorageService()
