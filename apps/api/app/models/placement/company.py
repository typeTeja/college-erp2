from typing import Optional
from datetime import datetime, date
from decimal import Decimal
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import DECIMAL, Text

class PlacementCompany(SQLModel, table=True):
    """Hotels/Companies for Placements"""
    __tablename__ = "placement_company"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)  # e.g., "Taj Hotels", "ITC Hotels"
    code: str = Field(unique=True, index=True)
    
    company_type: str = Field(default="HOTEL")  # HOTEL, RESTAURANT, CRUISE, OTHER
    
    # Contact Information
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    
    address: Optional[str] = Field(default=None, sa_column=Column(Text))
    city: Optional[str] = None
    state: Optional[str] = None
    country: str = Field(default="India")
    
    website: Optional[str] = None
    
    # Partnership details
    is_partner: bool = Field(default=False)
    partnership_start_date: Optional[date] = None
    mou_document_url: Optional[str] = None
    
    # Placement stats
    avg_package_lpa: Optional[Decimal] = Field(default=None, sa_column=Column(DECIMAL(10, 2)))
    students_placed: int = Field(default=0)
    
    is_active: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
