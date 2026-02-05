"""
System Domain Schemas

All Pydantic schemas for the system domain including:
- Authentication (login, tokens, password reset)
- User management (create, update, response)
- Role and permission management
- System settings
- Audit logging
- File management
- Data imports
"""

from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, List, Any
from datetime import datetime, date

from app.shared.enums import AuditLogAction, SettingGroup, ImportRowStatus
from app.domains.system.models import FileModule


# ----------------------------------------------------------------------
# Authentication Schemas
# ----------------------------------------------------------------------

class Token(BaseModel):
    """JWT token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """JWT token payload"""
    sub: Optional[int] = None  # user_id
    exp: Optional[int] = None
    type: Optional[str] = "access"


class LoginRequest(BaseModel):
    """Login request schema"""
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    """Login response schema"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: "UserResponse"


class PasswordResetRequest(BaseModel):
    """Request password reset"""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Confirm password reset with token"""
    token: str
    new_password: str
    
    @validator('new_password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


class PasswordChange(BaseModel):
    """Change password (authenticated user)"""
    current_password: str
    new_password: str
    
    @validator('new_password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


# ----------------------------------------------------------------------
# User Schemas
# ----------------------------------------------------------------------

class UserBase(BaseModel):
    """Base user schema"""
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None
    preferences: Optional[dict] = {}


class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str
    role_ids: List[int] = []
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    phone: Optional[str] = None
    preferences: Optional[dict] = None
    is_active: Optional[bool] = None
    role_ids: Optional[List[int]] = None


class UserResponse(UserBase):
    """Schema for user API response"""
    id: int
    is_active: bool
    is_superuser: bool
    preferences: dict = {}
    roles: List[str] = []  # Role names
    
    @validator("roles", pre=True)
    def extract_role_names(cls, v):
        """Extract role names from Role objects if necessary"""
        if not v:
            return []
        roles_list = []
        for role in v:
            if isinstance(role, str):
                roles_list.append(role)
            elif hasattr(role, "name"):
                roles_list.append(role.name)
            elif isinstance(role, dict) and "name" in role:
                roles_list.append(role["name"])
        return roles_list
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Role & Permission Schemas
# ----------------------------------------------------------------------

class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None
    module: str


class PermissionCreate(PermissionBase):
    pass


class PermissionRead(PermissionBase):
    id: int
    
    class Config:
        from_attributes = True


class PermissionGroup(BaseModel):
    module: str
    permissions: List[PermissionRead]


class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_system: bool = False
    is_active: bool = True


class RoleCreate(RoleBase):
    permission_ids: List[int] = []


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    permission_ids: Optional[List[int]] = None


class RoleRead(RoleBase):
    id: int
    permissions: List[PermissionRead] = []
    
    class Config:
        from_attributes = True


class PermissionAuditLogRead(BaseModel):
    id: int
    actor_id: int
    role_id: int
    action: str
    permission_name: str
    timestamp: str
    actor_name: Optional[str] = None
    role_name: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# System Settings Schemas
# ----------------------------------------------------------------------

class SystemSettingBase(BaseModel):
    key: str
    value: Any
    group: SettingGroup
    is_secret: bool = False
    description: Optional[str] = None


class SystemSettingCreate(SystemSettingBase):
    pass


class SystemSettingUpdate(BaseModel):
    value: Optional[Any] = None
    description: Optional[str] = None


class SystemSettingRead(SystemSettingBase):
    id: int
    updated_at: datetime
    updated_by: Optional[int] = None
    
    class Config:
        from_attributes = True


class InstituteInfoBase(BaseModel):
    name: str
    short_code: Optional[str] = None
    address: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    logo_url: Optional[str] = None


class InstituteInfoUpdate(BaseModel):
    name: Optional[str] = None
    short_code: Optional[str] = None
    address: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    logo_url: Optional[str] = None


class InstituteInfoRead(InstituteInfoBase):
    id: int
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Audit Log Schemas
# ----------------------------------------------------------------------

class AuditLogBase(BaseModel):
    user_id: Optional[int] = None
    action: AuditLogAction
    module: str
    description: str
    target_id: Optional[str] = None
    from_value: Optional[Any] = None
    to_value: Optional[Any] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class AuditLogCreate(AuditLogBase):
    pass


class AuditLogRead(AuditLogBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# File Management Schemas
# ----------------------------------------------------------------------

class FileUploadResponse(BaseModel):
    """Response after successful file upload"""
    id: int
    file_key: str
    original_filename: str
    file_size: int
    mime_type: Optional[str]
    download_url: str
    uploaded_at: datetime


class FileDownloadResponse(BaseModel):
    """Response with file download URL"""
    id: int
    file_key: str
    original_filename: str
    file_size: int
    mime_type: Optional[str]
    download_url: str
    expires_in: int  # Seconds until URL expires


class PresignedUploadUrlRequest(BaseModel):
    """Request for presigned upload URL"""
    filename: str
    content_type: str
    module: FileModule
    entity_type: Optional[str] = None
    entity_id: Optional[int] = None


class PresignedUploadUrlResponse(BaseModel):
    """Response with presigned upload URL"""
    upload_url: str
    file_key: str
    bucket_name: str
    expires_in: int  # Seconds until URL expires


class FileListResponse(BaseModel):
    """Response with list of files"""
    files: List[FileUploadResponse]
    total: int
    skip: int
    limit: int


# ----------------------------------------------------------------------
# Data Import Schemas
# ----------------------------------------------------------------------

class ImportErrorDetail(BaseModel):
    field: str
    message: str


class ImportPreviewRow(BaseModel):
    row_number: int
    data: dict  # Generic dict for any import type
    status: ImportRowStatus
    errors: List[ImportErrorDetail] = []


class ImportPreviewResponse(BaseModel):
    total_rows: int
    valid_count: int
    invalid_count: int
    duplicate_count: int
    rows: List[ImportPreviewRow]


class ImportExecuteRequest(BaseModel):
    file_token: str  # Token referencing uploaded temporary file


class ImportLogRead(BaseModel):
    id: int
    file_name: str
    uploaded_by_id: int
    timestamp: datetime
    total_rows: int
    imported_count: int
    failed_count: int
    duplicate_count: int
    status: str
    
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Core Master Schemas
# ----------------------------------------------------------------------

class DepartmentBase(BaseModel):
    department_name: str
    department_code: str
    description: Optional[str] = None
    hod_faculty_id: Optional[int] = None
    is_active: bool = True

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    department_name: Optional[str] = None
    department_code: Optional[str] = None
    description: Optional[str] = None
    hod_faculty_id: Optional[int] = None
    is_active: Optional[bool] = None

class DepartmentRead(DepartmentBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
