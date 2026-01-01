"""Storage service for S3/MinIO file operations"""
import os
import uuid
from typing import Optional, BinaryIO, Tuple
from datetime import datetime, timedelta
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from fastapi import UploadFile, HTTPException

# Make python-magic optional (requires libmagic system library)
try:
    import magic
    HAS_MAGIC = True
except (ImportError, OSError):
    HAS_MAGIC = False

from pathlib import Path

from app.config.settings import settings


class StorageService:
    """Service for handling file storage operations with S3/MinIO"""
    
    def __init__(self):
        """Initialize S3 client with configuration from settings"""
        self.s3_client = boto3.client(
            's3',
            endpoint_url=settings.S3_ENDPOINT,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name=settings.S3_REGION,
            config=Config(
                signature_version='s3v4',
                s3={'addressing_style': 'path'} if settings.S3_FORCE_PATH_STYLE else {}
            ),
            use_ssl=settings.S3_ENDPOINT.startswith('https://') if settings.S3_ENDPOINT else True,
        )
        
        # Bucket names
        self.bucket_documents = settings.S3_BUCKET
        self.bucket_images = settings.S3_BUCKET_IMAGES
        self.bucket_temp = settings.S3_BUCKET_TEMP
    
    def _generate_unique_key(self, prefix: str, filename: str) -> str:
        """
        Generate unique S3 key with prefix and UUID
        
        Args:
            prefix: Folder prefix (e.g., 'admissions/123')
            filename: Original filename
            
        Returns:
            Unique S3 key
        """
        file_ext = Path(filename).suffix.lower()
        unique_id = uuid.uuid4().hex
        timestamp = datetime.utcnow().strftime('%Y%m%d')
        
        # Clean filename - remove extension and special chars
        clean_name = Path(filename).stem[:50]  # Limit length
        clean_name = "".join(c for c in clean_name if c.isalnum() or c in ('-', '_'))
        
        return f"{prefix}/{timestamp}_{unique_id}_{clean_name}{file_ext}"
    
    def _detect_mime_type(self, file_content: bytes, filename: str) -> str:
        """
        Detect MIME type from file content
        
        Args:
            file_content: File binary content
            filename: Original filename
            
        Returns:
            MIME type string
        """
        if HAS_MAGIC:
            try:
                mime = magic.Magic(mime=True)
                return mime.from_buffer(file_content)
            except Exception:
                pass
        
        # Fallback to extension-based detection
        ext = Path(filename).suffix.lower()
        mime_map = {
            '.pdf': 'application/pdf',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.doc': 'application/msword',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.xls': 'application/vnd.ms-excel',
            '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            '.csv': 'text/csv',
        }
        return mime_map.get(ext, 'application/octet-stream')
    
    async def upload_file(
        self,
        file: UploadFile,
        prefix: str,
        bucket: Optional[str] = None,
        allowed_extensions: Optional[set] = None,
        max_size: Optional[int] = None
    ) -> Tuple[str, int, str]:
        """
        Upload file to S3/MinIO
        
        Args:
            file: FastAPI UploadFile object
            prefix: S3 key prefix (folder path)
            bucket: Bucket name (defaults to documents bucket)
            allowed_extensions: Set of allowed file extensions
            max_size: Maximum file size in bytes
            
        Returns:
            Tuple of (s3_key, file_size, mime_type)
            
        Raises:
            HTTPException: If validation fails or upload fails
        """
        # Use default bucket if not specified
        if bucket is None:
            bucket = self.bucket_documents
        
        # Validate file extension
        file_ext = Path(file.filename).suffix.lower()
        if allowed_extensions and file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
            )
        
        # Read file content
        contents = await file.read()
        file_size = len(contents)
        
        # Validate file size
        max_upload_size = max_size or settings.MAX_UPLOAD_SIZE
        if file_size > max_upload_size:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {max_upload_size / 1024 / 1024}MB"
            )
        
        # Detect MIME type
        mime_type = self._detect_mime_type(contents, file.filename)
        
        # Generate unique key
        s3_key = self._generate_unique_key(prefix, file.filename)
        
        try:
            # Upload to S3
            self.s3_client.put_object(
                Bucket=bucket,
                Key=s3_key,
                Body=contents,
                ContentType=mime_type,
                Metadata={
                    'original_filename': file.filename,
                    'uploaded_at': datetime.utcnow().isoformat()
                }
            )
            
            return s3_key, file_size, mime_type
            
        except ClientError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload file: {str(e)}"
            )
    
    def generate_presigned_upload_url(
        self,
        key: str,
        bucket: Optional[str] = None,
        expiration: int = 900,  # 15 minutes
        content_type: Optional[str] = None
    ) -> str:
        """
        Generate presigned URL for direct upload from client
        
        Args:
            key: S3 key for the file
            bucket: Bucket name
            expiration: URL expiration time in seconds
            content_type: Expected content type
            
        Returns:
            Presigned upload URL
        """
        if bucket is None:
            bucket = self.bucket_documents
        
        params = {
            'Bucket': bucket,
            'Key': key
        }
        
        if content_type:
            params['ContentType'] = content_type
        
        try:
            url = self.s3_client.generate_presigned_url(
                'put_object',
                Params=params,
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate upload URL: {str(e)}"
            )
    
    def generate_presigned_download_url(
        self,
        key: str,
        bucket: Optional[str] = None,
        expiration: int = 300,  # 5 minutes
        filename: Optional[str] = None
    ) -> str:
        """
        Generate presigned URL for file download
        
        Args:
            key: S3 key of the file
            bucket: Bucket name
            expiration: URL expiration time in seconds
            filename: Optional filename for Content-Disposition header
            
        Returns:
            Presigned download URL
        """
        if bucket is None:
            bucket = self.bucket_documents
        
        params = {
            'Bucket': bucket,
            'Key': key
        }
        
        if filename:
            params['ResponseContentDisposition'] = f'attachment; filename="{filename}"'
        
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params=params,
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate download URL: {str(e)}"
            )
    
    def delete_file(self, key: str, bucket: Optional[str] = None) -> bool:
        """
        Delete file from S3
        
        Args:
            key: S3 key of the file
            bucket: Bucket name
            
        Returns:
            True if deleted successfully
        """
        if bucket is None:
            bucket = self.bucket_documents
        
        try:
            self.s3_client.delete_object(Bucket=bucket, Key=key)
            return True
        except ClientError:
            return False
    
    def file_exists(self, key: str, bucket: Optional[str] = None) -> bool:
        """
        Check if file exists in S3
        
        Args:
            key: S3 key of the file
            bucket: Bucket name
            
        Returns:
            True if file exists
        """
        if bucket is None:
            bucket = self.bucket_documents
        
        try:
            self.s3_client.head_object(Bucket=bucket, Key=key)
            return True
        except ClientError:
            return False
    
    def get_file_metadata(self, key: str, bucket: Optional[str] = None) -> dict:
        """
        Get file metadata from S3
        
        Args:
            key: S3 key of the file
            bucket: Bucket name
            
        Returns:
            Dictionary with file metadata
        """
        if bucket is None:
            bucket = self.bucket_documents
        
        try:
            response = self.s3_client.head_object(Bucket=bucket, Key=key)
            return {
                'size': response.get('ContentLength'),
                'content_type': response.get('ContentType'),
                'last_modified': response.get('LastModified'),
                'metadata': response.get('Metadata', {})
            }
        except ClientError as e:
            raise HTTPException(
                status_code=404,
                detail=f"File not found: {str(e)}"
            )
    
    def copy_file(
        self,
        source_key: str,
        dest_key: str,
        source_bucket: Optional[str] = None,
        dest_bucket: Optional[str] = None
    ) -> bool:
        """
        Copy file within S3 or between buckets
        
        Args:
            source_key: Source S3 key
            dest_key: Destination S3 key
            source_bucket: Source bucket name
            dest_bucket: Destination bucket name
            
        Returns:
            True if copied successfully
        """
        if source_bucket is None:
            source_bucket = self.bucket_documents
        if dest_bucket is None:
            dest_bucket = self.bucket_documents
        
        try:
            copy_source = {'Bucket': source_bucket, 'Key': source_key}
            self.s3_client.copy_object(
                CopySource=copy_source,
                Bucket=dest_bucket,
                Key=dest_key
            )
            return True
        except ClientError:
            return False
    
    def list_files(
        self,
        prefix: str,
        bucket: Optional[str] = None,
        max_keys: int = 100
    ) -> list:
        """
        List files in S3 with given prefix
        
        Args:
            prefix: S3 key prefix to filter
            bucket: Bucket name
            max_keys: Maximum number of keys to return
            
        Returns:
            List of file keys
        """
        if bucket is None:
            bucket = self.bucket_documents
        
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=bucket,
                Prefix=prefix,
                MaxKeys=max_keys
            )
            
            if 'Contents' not in response:
                return []
            
            return [obj['Key'] for obj in response['Contents']]
        except ClientError:
            return []


# Singleton instance
storage_service = StorageService()
