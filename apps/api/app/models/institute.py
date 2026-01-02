from typing import Optional
from sqlmodel import SQLModel, Field

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
