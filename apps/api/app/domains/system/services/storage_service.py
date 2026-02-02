import os
import uuid
from typing import Optional, BinaryIO, Tuple
from datetime import datetime
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from fastapi import UploadFile, HTTPException
from pathlib import Path

from app.config.settings import settings

class StorageService:
    """Service for handling file storage operations - System Domain"""
    
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=settings.S3_ENDPOINT or None,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            region_name=settings.S3_REGION,
            config=Config(
                signature_version='s3v4',
                s3={'addressing_style': 'path'} if settings.S3_FORCE_PATH_STYLE else {}
            ),
            use_ssl=settings.S3_ENDPOINT.startswith('https://') if settings.S3_ENDPOINT else True,
        )
        self.bucket_documents = settings.S3_BUCKET
    
    def _generate_unique_key(self, prefix: str, filename: str) -> str:
        file_ext = Path(filename).suffix.lower()
        unique_id = uuid.uuid4().hex
        timestamp = datetime.utcnow().strftime('%Y%m%d')
        return f"{prefix}/{timestamp}_{unique_id}_{file_ext}"

    async def upload_file(self, file: UploadFile, prefix: str) -> Tuple[str, int, str]:
        s3_key = self._generate_unique_key(prefix, file.filename)
        contents = await file.read()
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_documents,
                Key=s3_key,
                Body=contents,
                ContentType=file.content_type
            )
            return s3_key, len(contents), file.content_type
        except ClientError as e:
            raise HTTPException(status_code=500, detail=str(e))

storage_service = StorageService()
