"""
Auth Schemas

Shared authentication schemas for JWT token handling.
"""
from pydantic import BaseModel
from typing import Optional

class TokenPayload(BaseModel):
    """JWT token payload schema"""
    sub: int  # User ID
    exp: Optional[int] = None  # Expiration timestamp

class UserCreate(BaseModel):
    """User creation schema"""
    username: str
    email: str
    password: str
    full_name: str

class UserUpdate(BaseModel):
    """User update schema"""
    username: Optional[str] = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class LoginRequest(BaseModel):
    """Login request schema"""
    username: str
    password: str
