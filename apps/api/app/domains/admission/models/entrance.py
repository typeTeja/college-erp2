from typing import TYPE_CHECKING, Optional, List
from datetime import datetime, date
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import JSON, Text

if TYPE_CHECKING:
    from app.domains.auth.models import AuthUser
    from app.domains.finance.models import ScholarshipSlab
    from .application import Application
    from ....schemas.json_fields import EntranceTestSubject, SubjectMarksEntry

class EntranceExamScore(SQLModel, table=True):
    """Manual entrance exam marks entry linked to application for scholarship calculation"""
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id", unique=True, index=True)
    marks_obtained: float
    total_marks: float = Field(default=100.0)
    exam_date: datetime = Field(default_factory=datetime.utcnow)
    verified_by: Optional[int] = Field(default=None, foreign_key="users.id")
    
    # Relationships
    application: "Application" = Relationship(back_populates="entrance_exam_score")

class EntranceTestConfig(SQLModel, table=True):
    """Configuration for entrance exams (RNET)"""
    __tablename__ = "entrance_test_config"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    test_name: str = Field(max_length=200)
    test_code: str = Field(unique=True, index=True, max_length=50)
    academic_year: str = Field(index=True)
    
    program_ids: List[int] = Field(default=[], sa_column=Column(JSON))
    
    test_date: date
    test_time: str
    test_duration_minutes: int = Field(default=120)
    reporting_time: str = Field(default="09:30 AM")
    
    venue_name: str
    venue_address: str = Field(sa_column=Column(Text))
    venue_instructions: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    guidelines: Optional[str] = Field(default=None, sa_column=Column(Text))
    documents_required: List[str] = Field(default=[], sa_column=Column(JSON))
    
    total_marks: float = Field(default=100.0)
    subjects: List["EntranceTestSubject"] = Field(default=[], sa_column=Column(JSON))
    
    is_active: bool = Field(default=True)
    registration_open: bool = Field(default=True)
    registration_deadline: Optional[date] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[int] = Field(default=None, foreign_key="users.id")
    
    results: List["EntranceExamResult"] = Relationship(back_populates="test_config")

class EntranceExamResult(SQLModel, table=True):
    """Entrance exam results and scholarship calculation"""
    __tablename__ = "entrance_exam_result"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    admission_id: int = Field(foreign_key="application.id", index=True)
    test_config_id: int = Field(foreign_key="entrance_test_config.id", index=True)
    scholarship_slab_id: Optional[int] = Field(default=None, foreign_key="scholarship_slab.id", index=True)
    
    hall_ticket_number: str = Field(unique=True, index=True)
    student_name: str
    program_code: str = Field(index=True)
    
    total_max_marks: float
    total_secured_marks: float
    entrance_percentage: float = Field(ge=0, le=100)
    
    subject_marks: List["SubjectMarksEntry"] = Field(default=[], sa_column=Column(JSON))
    
    previous_percentage: float = Field(ge=0, le=100)
    
    entrance_points: float = Field(ge=0, le=100)
    previous_points: float = Field(ge=0, le=100)
    total_points: float = Field(ge=0, le=100)
    average_points: float = Field(ge=0, le=100)
    
    entrance_weightage: float = Field(default=0.5)
    previous_weightage: float = Field(default=0.5)
    
    scholarship_amount: Optional[float] = None
    scholarship_percentage: Optional[float] = None
    
    result_status: str = Field(default="pending")
    remarks: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    omr_sheet_number: Optional[str] = None
    omr_sheet_url: Optional[str] = None
    
    entered_by: Optional[int] = Field(default=None, foreign_key="users.id")
    entered_at: Optional[datetime] = None
    verified_by: Optional[int] = Field(default=None, foreign_key="users.id")
    verified_at: Optional[datetime] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    admission: "Application" = Relationship(back_populates="entrance_result")
    test_config: EntranceTestConfig = Relationship(back_populates="results")
    scholarship_slab: Optional["ScholarshipSlab"] = Relationship(back_populates="results")
    
    # Explicit User Relationships
    entry_user: Optional["AuthUser"] = Relationship(sa_relationship_kwargs={"foreign_keys": "EntranceExamResult.entered_by"})
    verifier: Optional["AuthUser"] = Relationship(sa_relationship_kwargs={"foreign_keys": "EntranceExamResult.verified_by"})
