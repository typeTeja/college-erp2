"""
Campus Domain Schemas

Pydantic schemas for the campus domain.
Note: This is a simplified version covering all subdomains.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
from decimal import Decimal


# ----------------------------------------------------------------------
# Hostel Schemas
# ----------------------------------------------------------------------

class HostelBlockBase(BaseModel):
    name: str
    type: str
    total_floors: int


class HostelBlockRead(HostelBlockBase):
    id: int
    
    class Config:
        from_attributes = True


class BedAllocationBase(BaseModel):
    room_id: int
    bed_number: str
    student_id: Optional[int] = None


class BedAllocationRead(BedAllocationBase):
    id: int
    allocation_date: datetime
    is_active: bool
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Library Schemas
# ----------------------------------------------------------------------

class BookBase(BaseModel):
    title: str
    author: str
    isbn: Optional[str] = None
    total_copies: int


class BookRead(BookBase):
    id: int
    available_copies: int
    
    class Config:
        from_attributes = True


class BookIssueBase(BaseModel):
    book_id: int
    user_id: int
    issue_date: date
    due_date: date


class BookIssueRead(BookIssueBase):
    id: int
    return_date: Optional[date] = None
    status: str
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Transport Schemas
# ----------------------------------------------------------------------

class RouteBase(BaseModel):
    name: str
    start_point: str
    end_point: str


class RouteRead(RouteBase):
    id: int
    
    class Config:
        from_attributes = True


class VehicleBase(BaseModel):
    vehicle_number: str
    vehicle_type: str
    capacity: int


class VehicleRead(VehicleBase):
    id: int
    is_active: bool
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Inventory Schemas
# ----------------------------------------------------------------------

class AssetBase(BaseModel):
    name: str
    asset_code: str
    category: str
    purchase_date: date
    purchase_cost: Decimal


class AssetRead(AssetBase):
    id: int
    status: str
    
    class Config:
        from_attributes = True
