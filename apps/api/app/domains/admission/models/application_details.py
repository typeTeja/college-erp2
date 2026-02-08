"""
Application Detail Models

Normalized tables for comprehensive admission application data.
These models store detailed information that will be migrated to 
the Student domain upon admission confirmation.

Design Philosophy:
- Normalized structure prevents data duplication
- Supports multiple parents and education records
- Clean separation from Student domain
- Easy data migration upon admission
"""

from typing import TYPE_CHECKING, Optional
from datetime import date, datetime
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import Text
from app.shared.enums import (
    ParentRelation, Gender, EducationLevel, EducationBoard,
    ActivityLevel, AddressType
)

if TYPE_CHECKING:
    from .application import Application
    from app.domains.auth.models import AuthUser


# ======================================================================
# Parent/Guardian Information
# ======================================================================

class ApplicationParent(SQLModel, table=True):
    """Parent or Guardian information for application"""
    __tablename__ = "application_parent"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id", index=True)
    
    # Basic Information
    relation: ParentRelation
    name: str = Field(max_length=200)
    gender: Optional[Gender] = None
    
    # Contact
    mobile: str = Field(max_length=15)
    email: Optional[str] = None
    
    # Professional
    qualification: Optional[str] = Field(default=None, max_length=200)
    occupation: Optional[str] = Field(default=None, max_length=200)
    annual_income: Optional[float] = None
    
    # Bank Details (Optional)
    bank_account_number: Optional[str] = None
    bank_name: Optional[str] = None
    bank_ifsc: Optional[str] = None
    
    # Metadata
    is_primary_contact: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    application: "Application" = Relationship(back_populates="parents")


# ======================================================================
# Previous Education
# ======================================================================

class ApplicationEducation(SQLModel, table=True):
    """Previous education details for application"""
    __tablename__ = "application_education"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id", index=True)
    
    # Education Level
    level: EducationLevel  # SSC, INTERMEDIATE, DEGREE
    
    # Institution Details
    institution_name: str = Field(max_length=300)
    institution_address: Optional[str] = Field(default=None, sa_column=Column(Text))
    institution_code: Optional[str] = Field(default=None, max_length=50)
    
    # Board/University
    board: EducationBoard
    board_other: Optional[str] = Field(default=None, max_length=200)  # If board is OTHER
    
    # Academic Performance
    hall_ticket_number: Optional[str] = Field(default=None, max_length=100)
    year_of_passing: Optional[int] = None
    secured_marks: Optional[float] = None
    total_marks: Optional[float] = None
    percentage: Optional[float] = Field(default=None, ge=0, le=100)
    cgpa: Optional[float] = Field(default=None, ge=0, le=10)
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    application: "Application" = Relationship(back_populates="education_history")


# ======================================================================
# Address Information
# ======================================================================

class ApplicationAddress(SQLModel, table=True):
    """Address details for application"""
    __tablename__ = "application_address"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id", index=True)
    
    # Address Type
    address_type: AddressType  # PRESENT or PERMANENT
    
    # Address Components
    address_line: str = Field(sa_column=Column(Text))
    village_city: str = Field(max_length=200)
    district: Optional[str] = Field(default=None, max_length=200)
    state: str = Field(max_length=100)
    country: str = Field(default="India", max_length=100)
    pincode: str = Field(max_length=10)
    
    # Contact Numbers
    telephone_residence: Optional[str] = None
    telephone_office: Optional[str] = None
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    application: "Application" = Relationship(back_populates="addresses")


# ======================================================================
# Bank Details
# ======================================================================

class ApplicationBankDetails(SQLModel, table=True):
    """Student bank account details for application"""
    __tablename__ = "application_bank_details"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id", unique=True, index=True)
    
    # Bank Information
    account_number: str = Field(max_length=50)
    account_holder_name: Optional[str] = Field(default=None, max_length=200)
    bank_name: str = Field(max_length=200)
    branch_name: Optional[str] = Field(default=None, max_length=200)
    ifsc_code: str = Field(max_length=11)
    
    # Verification
    is_verified: bool = Field(default=False)
    verified_at: Optional[datetime] = None
    verified_by: Optional[int] = Field(default=None, foreign_key="users.id")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    application: "Application" = Relationship(back_populates="bank_details")
    verifier: Optional["AuthUser"] = Relationship(sa_relationship_kwargs={"foreign_keys": "ApplicationBankDetails.verified_by"})


# ======================================================================
# Medical Fitness
# ======================================================================

class ApplicationHealth(SQLModel, table=True):
    """Medical fitness declaration for application"""
    __tablename__ = "application_health"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id", unique=True, index=True)
    
    # Medical Fitness
    is_medically_fit: bool = Field(default=False)
    
    # Biometrics
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    
    # Medical Details
    allergies: Optional[str] = Field(default=None, sa_column=Column(Text))
    chronic_illness_details: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Emergency Contact / Family Doctor
    doctor_name: Optional[str] = Field(default=None, max_length=200)
    doctor_phone: Optional[str] = Field(default=None, max_length=15)
    
    # Practitioner Details (for official certificate)
    practitioner_name: Optional[str] = Field(default=None, max_length=200)
    practitioner_registration_number: Optional[str] = Field(default=None, max_length=100)
    certificate_date: Optional[date] = None
    certificate_place: Optional[str] = Field(default=None, max_length=200)
    
    # Certificate Reference
    certificate_document_id: Optional[int] = Field(default=None, foreign_key="application_document.id")
    
    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    application: "Application" = Relationship(back_populates="health_info")
