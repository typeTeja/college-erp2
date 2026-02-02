"""
System Domain Models

All database models for the system domain including:
- User authentication and authorization (User, Role, Permission)
- System configuration (SystemSetting, InstituteInfo)
- Audit logging (AuditLog, PermissionAuditLog)
- File management (FileMetadata)
- Data imports (ImportLog)
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
# Link Tables (Many-to-Many)
# ----------------------------------------------------------------------

class UserRole(SQLModel, table=True):
    """Link table for User-Role many-to-many relationship"""
    __tablename__ = "user_role"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    role_id: int = Field(foreign_key="role.id", index=True)


class RolePermission(SQLModel, table=True):
    """Link table for Role-Permission many-to-many relationship"""
    __tablename__ = "role_permission"
    
    role_id: int = Field(foreign_key="role.id", primary_key=True)
    permission_id: int = Field(foreign_key="permission.id", primary_key=True)


# ----------------------------------------------------------------------
# Core Models
# ----------------------------------------------------------------------

class User(SQLModel, table=True):
    """User authentication and profile model"""
    __tablename__ = "user"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    phone: Optional[str] = Field(default=None, index=True)
    full_name: Optional[str] = None
    hashed_password: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    
    # Password reset fields
    password_reset_token: Optional[str] = None
    password_reset_expires: Optional[datetime] = None
    
    # Preferences (JSON store for notifications, theme, etc.)
    preferences: Optional[dict] = Field(default_factory=dict, sa_column=Column(JSON))
    
    # Timestamps
    last_login: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    roles: List["Role"] = Relationship(back_populates="users", link_model=UserRole)


class Role(SQLModel, table=True):
    """Role-based access control model"""
    __tablename__ = "role"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: Optional[str] = None
    is_system: bool = Field(default=False)
    is_active: bool = Field(default=True)
    
    # Relationships
    users: List["User"] = Relationship(back_populates="roles", link_model=UserRole)
    permissions: List["Permission"] = Relationship(back_populates="roles", link_model=RolePermission)


class Permission(SQLModel, table=True):
    """Granular permission model"""
    __tablename__ = "permission"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)  # e.g., "admissions:read"
    description: Optional[str] = None
    module: str = Field(index=True)  # e.g., "Admissions", "Fees" (for grouping)
    
    # Relationships
    roles: List["Role"] = Relationship(back_populates="permissions", link_model=RolePermission)


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
    updated_by: Optional[int] = Field(default=None, foreign_key="user.id")


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
    
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True)
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
    actor_id: int = Field(foreign_key="user.id", index=True)
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
    
    uploaded_by: Optional[int] = Field(default=None, foreign_key="user.id")
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
    uploaded_by_id: int = Field(foreign_key="user.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    total_rows: int = 0
    imported_count: int = 0
    failed_count: int = 0
    duplicate_count: int = 0
    status: str = "PENDING"  # PREVIEW, SUCCESS, PARTIAL, FAILED
