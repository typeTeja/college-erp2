"""
Admission Domain Models - Master Data

Models for configurable master data entities:
- Education Boards (CBSE, ICSE, SSC)
- Lead Sources (Google, Social Media, Referral)
- Reservation Categories (General, BC-A, SC, ST)
"""
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

# ======================================================================
# Education Board
# ======================================================================

class Board(SQLModel, table=True):
    """Education Board (e.g. CBSE, ICSE, SSC)"""
    __tablename__ = "admission_board"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    code: str = Field(unique=True, index=True)
    description: Optional[str] = None
    
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# ======================================================================
# Lead Source
# ======================================================================

class LeadSource(SQLModel, table=True):
    """Lead Source (e.g. Website, Walk-in, Referral)"""
    __tablename__ = "admission_lead_source"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    code: str = Field(unique=True, index=True)
    
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# ======================================================================
# Reservation Category
# ======================================================================

class ReservationCategory(SQLModel, table=True):
    """Social Category (e.g. General, OBC, SC/ST)"""
    __tablename__ = "admission_reservation_category"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    code: str = Field(unique=True, index=True)
    description: Optional[str] = None
    
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
