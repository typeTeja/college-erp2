from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List

# Token Schemas
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

# Login Schemas
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

# User Schemas
class UserBase(BaseModel):
    """Base user schema"""
    username: str
    email: EmailStr
    full_name: Optional[str] = None
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
        # If v is a list of Role objects or similar dicts
        # Pydantic v2 usually handles this if we use model_validator or field_validator
        # But for ORM objects, we need manual extraction
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

# Password Reset Schemas
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
