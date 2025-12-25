from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .program import Program
    from .student import Student

class ApplicationStatus(str, Enum):
    PENDING_PAYMENT = "PENDING_PAYMENT"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    PAID = "PAID"
    FORM_COMPLETED = "FORM_COMPLETED"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    ADMITTED = "ADMITTED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"

class ApplicationPaymentStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class Application(SQLModel, table=True):
    """Student admission application model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    application_number: str = Field(index=True, unique=True, nullable=False)
    
    # Stage 1: Quick Apply Fields
    name: str
    email: str = Field(index=True)
    phone: str = Field(index=True)
    gender: str
    program_id: int = Field(foreign_key="program.id", index=True)
    state: str
    board: str
    group_of_study: str # MPC, BiPC, etc.
    
    # Stage 2: Full Form Fields
    aadhaar_number: Optional[str] = Field(default=None, index=True)
    father_name: Optional[str] = None
    father_phone: Optional[str] = None
    address: Optional[str] = None
    previous_marks_percentage: Optional[float] = None
    applied_for_scholarship: bool = Field(default=False)
    hostel_required: bool = Field(default=False)
    
    status: ApplicationStatus = Field(default=ApplicationStatus.PENDING_PAYMENT, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Links
    student_id: Optional[int] = Field(default=None, foreign_key="student.id", index=True)
    
    # Relationships
    program: "Program" = Relationship()
    payments: List["ApplicationPayment"] = Relationship(back_populates="application")
    entrance_exam_score: Optional["EntranceExamScore"] = Relationship(back_populates="application")

class ApplicationPayment(SQLModel, table=True):
    """Tracks application fee payments via Easebuzz or other gateways"""
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id", index=True)
    transaction_id: str = Field(unique=True, index=True)
    amount: float
    status: ApplicationPaymentStatus = Field(default=ApplicationPaymentStatus.PENDING)
    payment_method: Optional[str] = None # Easebuzz, Card, UPI
    paid_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    application: Application = Relationship(back_populates="payments")

class EntranceExamScore(SQLModel, table=True):
    """Manual entrance exam marks entry linked to application for scholarship calculation"""
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id", unique=True, index=True)
    marks_obtained: float
    total_marks: float = Field(default=100.0)
    exam_date: datetime = Field(default_factory=datetime.utcnow)
    verified_by: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Relationships
    application: Application = Relationship(back_populates="entrance_exam_score")
