"""
Entrance Exam Models - RNET/Entrance Test Management

Manages entrance exams, results, and scholarship allocation
"""
from typing import TYPE_CHECKING, List, Optional
from datetime import datetime, date
from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from sqlalchemy import Text

if TYPE_CHECKING:
    from ..admissions import Application


class EntranceTestConfig(SQLModel, table=True):
    """Configuration for entrance exams (RNET)"""
    __tablename__ = "entrance_test_config"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Test identification
    test_name: str = Field(max_length=200)  # e.g., "Regency National Entrance Test 2024-25"
    test_code: str = Field(unique=True, index=True, max_length=50)  # e.g., "RNET-2024"
    academic_year: str = Field(index=True)  # e.g., "2024-2025"
    
    # Applicable programs (JSON array of program_ids)
    program_ids: Optional[str] = Field(default=None, sa_column=Column(JSON))
    
    # Schedule
    test_date: date
    test_time: str  # e.g., "10:00 AM"
    test_duration_minutes: int = Field(default=120)  # 2 hours
    reporting_time: str = Field(default="09:30 AM")
    
    # Venue
    venue_name: str
    venue_address: str = Field(sa_column=Column(Text))
    venue_instructions: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Guidelines
    guidelines: Optional[str] = Field(default=None, sa_column=Column(Text))  # Rich text/HTML
    documents_required: Optional[str] = Field(default=None, sa_column=Column(JSON))  # ["Hall Ticket", "Photo ID"]
    
    # Exam details
    total_marks: float = Field(default=100.0)
    subjects: Optional[str] = Field(default=None, sa_column=Column(JSON))  # [{"name": "English", "marks": 25}]
    
    # Status
    is_active: bool = Field(default=True)
    registration_open: bool = Field(default=True)
    registration_deadline: Optional[date] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[int] = Field(default=None, foreign_key="user.id")
    
    # Relationships
    results: List["EntranceExamResult"] = Relationship(back_populates="test_config")


class EntranceExamResult(SQLModel, table=True):
    """Entrance exam results and scholarship calculation"""
    __tablename__ = "entrance_exam_result"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    admission_id: int = Field(foreign_key="application.id", index=True)
    test_config_id: int = Field(foreign_key="entrance_test_config.id", index=True)
    scholarship_slab_id: Optional[int] = Field(default=None, foreign_key="scholarship_slab.id", index=True)
    
    # Student info (denormalized for quick access)
    hall_ticket_number: str = Field(unique=True, index=True)
    student_name: str
    program_code: str = Field(index=True)
    
    # Entrance exam marks
    total_max_marks: float
    total_secured_marks: float
    entrance_percentage: float = Field(ge=0, le=100)
    
    # Subject-wise marks (JSON)
    subject_marks: Optional[str] = Field(default=None, sa_column=Column(JSON))
    # Example: [{"subject": "English", "max": 25, "secured": 20}]
    
    # Previous qualification marks (from admission)
    previous_percentage: float = Field(ge=0, le=100)
    
    # Points calculation (weighted average)
    entrance_points: float = Field(ge=0, le=100)  # Entrance percentage * weightage
    previous_points: float = Field(ge=0, le=100)  # Previous percentage * weightage
    total_points: float = Field(ge=0, le=100)  # Sum of both
    average_points: float = Field(ge=0, le=100)  # Average of both
    
    # Weightage used (for reference)
    entrance_weightage: float = Field(default=0.5)  # 50%
    previous_weightage: float = Field(default=0.5)  # 50%
    
    # Scholarship details
    scholarship_amount: Optional[float] = None
    scholarship_percentage: Optional[float] = None
    
    # Status
    result_status: str = Field(default="pending")  # pending, approved, rejected
    remarks: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # OMR details (optional)
    omr_sheet_number: Optional[str] = None
    omr_sheet_url: Optional[str] = None
    
    # Entry tracking
    entered_by: Optional[int] = Field(default=None, foreign_key="user.id")
    entered_at: Optional[datetime] = None
    verified_by: Optional[int] = Field(default=None, foreign_key="user.id")
    verified_at: Optional[datetime] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    admission: "Application" = Relationship(back_populates="entrance_result")
    test_config: "EntranceTestConfig" = Relationship(back_populates="results")
    scholarship_slab: Optional["ScholarshipSlab"] = Relationship(back_populates="results")



