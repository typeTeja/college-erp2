"""
Document Management Models - Document Upload & Verification

Manages student documents, categories, and verification workflow
"""
from typing import TYPE_CHECKING, List, Optional
from datetime import datetime, date
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import Text, JSON

if TYPE_CHECKING:
    from ..student import Student
    from ..user import User


class VerificationStatus(str, Enum):
    """Document verification status"""
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    EXPIRED = "EXPIRED"


class DocumentCategory(SQLModel, table=True):
    """Document category configuration"""
    __tablename__ = "document_category"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Category details
    name: str = Field(max_length=200)  # "10th Marksheet", "Aadhar Card"
    code: str = Field(unique=True, index=True, max_length=50)  # "10TH_MARKS"
    description: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Requirements
    is_required: bool = Field(default=False)  # Required for admission
    is_mandatory: bool = Field(default=False)  # Must be submitted
    
    # File constraints
    allowed_file_types: str = Field(sa_column=Column(JSON))  # ["pdf", "jpg", "png"]
    max_file_size: int = Field(default=10485760)  # 10MB in bytes
    max_files: int = Field(default=1)  # Number of files allowed
    
    # Verification
    verification_required: bool = Field(default=True)
    valid_for_days: Optional[int] = None  # Document validity period
    
    # Instructions
    upload_instructions: Optional[str] = Field(default=None, sa_column=Column(Text))
    sample_document_url: Optional[str] = None
    
    # Display
    display_order: int = Field(default=0)
    icon: Optional[str] = None
    
    # Status
    is_active: bool = Field(default=True)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    documents: List["StudentDocument"] = Relationship(
        back_populates="category",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class StudentDocument(SQLModel, table=True):
    """Student uploaded documents"""
    __tablename__ = "student_document"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    student_id: int = Field(foreign_key="student.id", index=True)
    document_category_id: int = Field(foreign_key="document_category.id", index=True)
    
    # File details
    file_name: str
    file_path: str  # Storage path
    file_size: int  # Bytes
    file_type: str  # pdf, jpg, png
    file_hash: Optional[str] = None  # For duplicate detection
    
    # Upload tracking
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    uploaded_by: Optional[int] = Field(default=None, foreign_key="user.id")
    upload_ip: Optional[str] = None
    
    # Verification
    verification_status: VerificationStatus = Field(default=VerificationStatus.PENDING)
    verified_by: Optional[int] = Field(default=None, foreign_key="user.id")
    verified_at: Optional[datetime] = None
    rejection_reason: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Validity
    expiry_date: Optional[date] = None
    is_expired: bool = Field(default=False)
    
    # Versioning
    version_number: int = Field(default=1)
    previous_document_id: Optional[int] = Field(default=None, foreign_key="student_document.id")
    is_latest: bool = Field(default=True)
    
    # Metadata
    document_number: Optional[str] = None  # For ID cards, certificates
    issue_date: Optional[date] = None
    issuing_authority: Optional[str] = None
    
    # Notes
    student_remarks: Optional[str] = Field(default=None, sa_column=Column(Text))
    admin_remarks: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship()
    category: "DocumentCategory" = Relationship(back_populates="documents")
    verifications: List["DocumentVerification"] = Relationship(
        back_populates="document",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class DocumentVerification(SQLModel, table=True):
    """Document verification audit trail"""
    __tablename__ = "document_verification"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    student_document_id: int = Field(foreign_key="student_document.id", index=True)
    
    # Verification details
    verified_by: int = Field(foreign_key="user.id")
    verified_at: datetime = Field(default_factory=datetime.utcnow)
    verification_status: VerificationStatus
    
    # Checklist
    checklist_items: Optional[str] = Field(default=None, sa_column=Column(JSON))
    # Example: [{"item": "Photo clear", "checked": true}, {"item": "Details match", "checked": true}]
    
    # Remarks
    remarks: Optional[str] = Field(default=None, sa_column=Column(Text))
    rejection_reason: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Follow-up
    requires_resubmission: bool = Field(default=False)
    resubmission_deadline: Optional[date] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    document: "StudentDocument" = Relationship(back_populates="verifications")
