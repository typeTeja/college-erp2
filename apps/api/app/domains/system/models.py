"""
System Domain Models

Database models for the system domain including:
- System configuration (SystemSetting, InstituteInfo)
- Audit logging (AuditLog, PermissionAuditLog)
- File management (FileMetadata)
- Data imports (ImportLog)

Note: User, Role, Permission models moved to domains/auth/
"""

from typing import TYPE_CHECKING, List, Optional, Any
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, Column, JSON

from app.shared.enums import AuditLogAction, SettingGroup


# ----------------------------------------------------------------------
# Enums
# ----------------------------------------------------------------------

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


# ----------------------------------------------------------------------
# System Configuration
# ----------------------------------------------------------------------

class SystemSetting(SQLModel, table=True):
    """General key-value store for all ERP configurations"""
    __tablename__ = "system_setting"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    key: str = Field(index=True, unique=True, description="Unique key like 'institute.name'")
    value: Any = Field(sa_column=Column(JSON))
    group: SettingGroup = Field(index=True)
    is_secret: bool = Field(default=False, description="If true, encrypt at rest and mask in UI")
    description: Optional[str] = None
    
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    updated_by: Optional[int] = Field(default=None, foreign_key="users.id")


class InstituteInfo(SQLModel, table=True):
    """Stores basic institute identity information"""
    __tablename__ = "institute_info"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., description="Institute full name")
    short_code: Optional[str] = Field(None, description="Short code or abbreviation")
    address: Optional[str] = Field(None)
    contact_email: Optional[str] = Field(None)
    contact_phone: Optional[str] = Field(None)
    logo_url: Optional[str] = Field(None, description="URL to stored logo image")


# ----------------------------------------------------------------------
# Audit & Logging
# ----------------------------------------------------------------------

class AuditLog(SQLModel, table=True):
    """System-wide audit trail"""
    __tablename__ = "audit_log"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    
    user_id: Optional[int] = Field(default=None, foreign_key="users.id", index=True)
    action: AuditLogAction = Field(index=True)
    module: str = Field(index=True)  # e.g., 'SETTINGS', 'ADMISSIONS', 'FEES'
    
    description: str
    target_id: Optional[str] = None  # ID of the record changed
    
    from_value: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    to_value: Optional[Any] = Field(default=None, sa_column=Column(JSON))
    
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class PermissionAuditLog(SQLModel, table=True):
    """Logs changes to role permissions for compliance"""
    __tablename__ = "permission_audit_log"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    actor_id: int = Field(foreign_key="users.id", index=True)
    role_id: int = Field(foreign_key="role.id", index=True)
    action: str  # "ADD_PERMISSION", "REMOVE_PERMISSION"
    permission_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ----------------------------------------------------------------------
# File Management
# ----------------------------------------------------------------------

class FileMetadata(SQLModel, table=True):
    """Tracks all files uploaded to storage"""
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
    
    uploaded_by: Optional[int] = Field(default=None, foreign_key="users.id")
    uploaded_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    deleted_at: Optional[datetime] = None
    
    description: Optional[str] = None
    tags: Optional[str] = None


# ----------------------------------------------------------------------
# Data Import
# ----------------------------------------------------------------------

class ImportLog(SQLModel, table=True):
    """Tracks bulk data import operations"""
    __tablename__ = "system_import_log"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    file_name: str
    uploaded_by_id: int = Field(foreign_key="users.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    total_rows: int = 0
    imported_count: int = 0
    duplicate_count: int = 0
    status: str = "PENDING"  # PREVIEW, SUCCESS, PARTIAL, FAILED


# ----------------------------------------------------------------------
# Core Masters
# ----------------------------------------------------------------------

class Department(SQLModel, table=True):
    """
    Department Management (Core System Master)
    Represents academic & operational ownership, independent of HR.
    """
    __tablename__ = "department"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    department_name: str = Field(unique=True, index=True, description="Official name of the department")
    department_code: str = Field(unique=True, index=True, description="Short code e.g., CSE, MECH")
    description: Optional[str] = None
    hod_faculty_id: Optional[int] = Field(default=None, index=True, description="Head of Department (Faculty ID)")
    
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
