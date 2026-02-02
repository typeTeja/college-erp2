from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
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
    """Tracks all files uploaded to storage - System Domain"""
    __tablename__ = "file_metadata"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    file_key: str = Field(index=True, unique=True, max_length=500)
    bucket_name: str = Field(max_length=100)
    
    original_filename: str = Field(max_length=255)
    file_size: int
    mime_type: Optional[str] = Field(default=None, max_length=100)
    checksum: Optional[str] = Field(default=None, max_length=64)
    
    is_public: bool = Field(default=False)
    
    module: FileModule = Field(index=True)
    entity_type: Optional[str] = Field(default=None, max_length=50, index=True)
    entity_id: Optional[int] = Field(default=None, index=True)
    
    uploaded_by: Optional[int] = Field(default=None, foreign_key="user.id")
    uploaded_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    deleted_at: Optional[datetime] = None
    
    description: Optional[str] = None
    tags: Optional[str] = None
