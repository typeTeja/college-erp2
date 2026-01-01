"""File metadata model for tracking uploaded files"""
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum


class FileModule(str, Enum):
    """Modules that can upload files"""
    ADMISSIONS = "ADMISSIONS"
    STUDENTS = "STUDENTS"
    FACULTY = "FACULTY"
    EXAMS = "EXAMS"
    LIBRARY = "LIBRARY"
    HOSTEL = "HOSTEL"
    FEES = "FEES"
    COMMUNICATION = "COMMUNICATION"
    INSTITUTE = "INSTITUTE"
    OTHER = "OTHER"


class FileMetadata(SQLModel, table=True):
    """Tracks all files uploaded to S3/MinIO storage"""
    __tablename__ = "file_metadata"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # S3 Information
    file_key: str = Field(index=True, unique=True, max_length=500)  # S3 object key
    bucket_name: str = Field(max_length=100)  # Bucket where file is stored
    
    # File Information
    original_filename: str = Field(max_length=255)
    file_size: int  # Size in bytes
    mime_type: Optional[str] = Field(default=None, max_length=100)
    checksum: Optional[str] = Field(default=None, max_length=64)  # MD5 or SHA256
    
    # Access Control
    is_public: bool = Field(default=False)  # Whether file is publicly accessible
    
    # Metadata
    module: FileModule = Field(index=True)  # Which module uploaded this
    entity_type: Optional[str] = Field(default=None, max_length=50, index=True)  # e.g., 'Application', 'Student'
    entity_id: Optional[int] = Field(default=None, index=True)  # ID of the related entity
    
    # Audit
    uploaded_by: Optional[int] = Field(default=None, foreign_key="user.id")
    uploaded_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    deleted_at: Optional[datetime] = None  # Soft delete
    
    # Additional metadata (JSON-like storage)
    description: Optional[str] = None
    tags: Optional[str] = None  # Comma-separated tags
