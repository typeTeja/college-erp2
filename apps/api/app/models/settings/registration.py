from typing import Optional, Any
from datetime import datetime
from decimal import Decimal
from sqlmodel import SQLModel, Field, Column, JSON
from sqlalchemy import DECIMAL

class Board(SQLModel, table=True):
    """Boards/Universities Master - CBSE, State Boards, etc."""
    __tablename__ = "board"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)  # e.g., "CBSE", "Telangana State Board"
    code: str = Field(unique=True, index=True)  # e.g., "CBSE", "TSBIE"
    full_name: Optional[str] = None
    state: Optional[str] = None
    country: str = Field(default="India")
    
    is_active: bool = Field(default=True)
    display_order: int = Field(default=0)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PreviousQualification(SQLModel, table=True):
    """Previous Qualifications - 10th, 12th, Diploma, etc."""
    __tablename__ = "previous_qualification"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)  # e.g., "10th Standard", "12th Science"
    code: str = Field(unique=True, index=True)  # e.g., "10TH", "12TH_SCI"
    level: int = Field(default=1)  # 1=10th, 2=12th, 3=UG, 4=PG
    
    is_mandatory_for_admission: bool = Field(default=True)
    required_documents: Any = Field(default=[], sa_column=Column(JSON))  # List of required doc types
    
    is_active: bool = Field(default=True)
    display_order: int = Field(default=0)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)

class StudyGroup(SQLModel, table=True):
    """Groups of Study - MPC, BiPC, Commerce, etc."""
    __tablename__ = "study_group"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)  # e.g., "MPC", "BiPC", "Commerce"
    code: str = Field(unique=True, index=True)
    full_name: Optional[str] = None  # e.g., "Mathematics, Physics, Chemistry"
    
    qualification_id: Optional[int] = Field(default=None, foreign_key="previous_qualification.id")
    
    subjects: Any = Field(default=[], sa_column=Column(JSON))  # List of subjects
    
    is_active: bool = Field(default=True)
    display_order: int = Field(default=0)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ReservationCategory(SQLModel, table=True):
    """Reservation Categories - SC, ST, OBC, etc."""
    __tablename__ = "reservation_category"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)  # e.g., "SC", "ST", "OBC"
    code: str = Field(unique=True, index=True)
    full_name: Optional[str] = None  # e.g., "Scheduled Caste"
    
    reservation_percentage: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(5, 2)))
    fee_concession_percentage: Decimal = Field(default=Decimal("0.00"), sa_column=Column(DECIMAL(5, 2)))
    
    requires_certificate: bool = Field(default=True)
    certificate_issuing_authority: Optional[str] = None
    
    is_active: bool = Field(default=True)
    display_order: int = Field(default=0)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)

class LeadSource(SQLModel, table=True):
    """Lead Sources - Marketing channels"""
    __tablename__ = "lead_source"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)  # e.g., "Website", "Social Media", "Campus Visit"
    code: str = Field(unique=True, index=True)
    description: Optional[str] = None
    
    category: str = Field(default="DIGITAL")  # DIGITAL, OFFLINE, REFERRAL, OTHER
    
    is_active: bool = Field(default=True)
    display_order: int = Field(default=0)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
