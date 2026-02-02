"""
Auth Domain Schemas

Pydantic schemas for authentication and authorization.
NO UserCreate schema - user creation happens in business domains.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# ======================================================================
# Authentication Schemas
# ======================================================================

class LoginRequest(BaseModel):
    """Login request with email and password"""
    email: EmailStr
    password: str


class Token(BaseModel):
    """JWT token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: Optional["AuthUserInfo"] = None


class TokenData(BaseModel):
    """Decoded token data"""
    user_id: Optional[int] = None
    type: Optional[str] = None  # "access" or "refresh"


class RefreshTokenRequest(BaseModel):
    """Refresh token request"""
    refresh_token: str


# ======================================================================
# Password Management Schemas
# ======================================================================

class PasswordResetRequest(BaseModel):
    """Request password reset via email"""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Confirm password reset with token"""
    token: str
    new_password: str = Field(min_length=8)


class PasswordChange(BaseModel):
    """Change password for authenticated user"""
    current_password: str
    new_password: str = Field(min_length=8)


# ======================================================================
# User Info Schemas (Read-only)
# ======================================================================

class AuthUserInfo(BaseModel):
    """
    Read-only user info for token response.
    This is NOT for user creation - just for returning user data.
    """
    id: int
    email: str
    username: str
    full_name: Optional[str] = None
    is_active: bool
    is_superuser: bool
    roles: List[str] = []
    
    class Config:
        from_attributes = True


# ======================================================================
# Role & Permission Schemas
# ======================================================================

class RoleBase(BaseModel):
    """Base role schema"""
    name: str
    description: Optional[str] = None


class RoleCreate(RoleBase):
    """Create role schema"""
    pass


class RoleRead(RoleBase):
    """Read role schema"""
    id: int
    is_system: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class PermissionBase(BaseModel):
    """Base permission schema"""
    name: str
    description: Optional[str] = None
    category: Optional[str] = None


class PermissionCreate(PermissionBase):
    """Create permission schema"""
    pass


class PermissionRead(PermissionBase):
    """Read permission schema"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ======================================================================
# Role/Permission Assignment Schemas
# ======================================================================

class AssignRoleRequest(BaseModel):
    """Assign role to user"""
    user_id: int
    role_id: int


class AssignPermissionRequest(BaseModel):
    """Assign permission to role"""
    role_id: int
    permission_id: int
