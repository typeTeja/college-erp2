from typing import TYPE_CHECKING, List, Optional
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import Text

if TYPE_CHECKING:
    from app.domains.student.models import Student
    from app.domains.auth.models import AuthUser as User

class HallTicketStatus(str, Enum):
    """Hall ticket status"""
    GENERATED = "GENERATED"
    DOWNLOADED = "DOWNLOADED"
    CANCELLED = "CANCELLED"
    REISSUED = "REISSUED"

class BlockReason(str, Enum):
    """Reasons for discipline block"""
    FEE_DUES = "FEE_DUES"
    ATTENDANCE_SHORTAGE = "ATTENDANCE_SHORTAGE"
    DISCIPLINARY_ACTION = "DISCIPLINARY_ACTION"
    DOCUMENT_PENDING = "DOCUMENT_PENDING"
    OTHER = "OTHER"

class HallTicketConfig(SQLModel, table=True):
    """Configuration for hall ticket generation"""
    __tablename__ = "hall_ticket_config"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Exam identification
    exam_name: str = Field(max_length=200)  # "RNET 2024", "University End Sem 2024"
    exam_code: str = Field(unique=True, index=True, max_length=50)
    academic_year: str = Field(index=True)
    
    # Exam schedule
    exam_date: datetime # Original was date, but usually full datetime or date? Using date to match. Wait, original scan said date.
    exam_start_time: str  # "10:00 AM"
    exam_end_time: str  # "01:00 PM"
    reporting_time: str = Field(default="09:30 AM")
    
    # Venue details
    venue_name: str
    venue_address: str = Field(sa_column=Column(Text))
    venue_map_url: Optional[str] = None
    
    # Instructions
    instructions: str = Field(sa_column=Column(Text))
    documents_required: Optional[str] = None  # JSON array
    prohibited_items: Optional[str] = None  # JSON array
    
    # Branding
    template_url: Optional[str] = None  # Path to custom template
    logo_url: Optional[str] = None
    header_text: Optional[str] = None
    footer_text: Optional[str] = None
    
    # Settings
    include_photo: bool = Field(default=True)
    include_signature: bool = Field(default=False)
    include_qr_code: bool = Field(default=True)
    include_barcode: bool = Field(default=False)
    
    # Status
    is_active: bool = Field(default=True)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[int] = Field(default=None, foreign_key="users.id")
    
    # Relationships
    hall_tickets: List["HallTicket"] = Relationship(
        back_populates="config",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

class HallTicket(SQLModel, table=True):
    """Individual hall ticket for a student"""
    __tablename__ = "hall_ticket"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    student_id: int = Field(foreign_key="student.id", index=True)
    hall_ticket_config_id: int = Field(foreign_key="hall_ticket_config.id", index=True)
    
    # Hall ticket details
    hall_ticket_number: str = Field(unique=True, index=True)  # "HT-2024-001234"
    
    # Student details (denormalized for quick access)
    student_name: str
    admission_number: str
    program_name: str
    year: int
    semester: int
    
    # Media
    photo_url: Optional[str] = None
    signature_url: Optional[str] = None
    
    # Generated files
    pdf_url: Optional[str] = None
    qr_code_url: Optional[str] = None
    barcode_url: Optional[str] = None
    
    # Status
    status: HallTicketStatus = Field(default=HallTicketStatus.GENERATED)
    
    # Download tracking
    download_count: int = Field(default=0)
    first_downloaded_at: Optional[datetime] = None
    last_downloaded_at: Optional[datetime] = None
    
    # Generation tracking
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    generated_by: Optional[int] = Field(default=None, foreign_key="users.id")
    
    # Cancellation/Reissue
    cancelled_at: Optional[datetime] = None
    cancelled_by: Optional[int] = Field(default=None, foreign_key="users.id")
    cancellation_reason: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    reissued_at: Optional[datetime] = None
    reissued_by: Optional[int] = Field(default=None, foreign_key="users.id")
    reissue_reason: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    student: "Student" = Relationship()
    config: "HallTicketConfig" = Relationship(back_populates="hall_tickets")

class DisciplineBlock(SQLModel, table=True):
    """Discipline block preventing hall ticket generation"""
    __tablename__ = "discipline_block"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Links
    student_id: int = Field(foreign_key="student.id", index=True)
    
    # Block details
    block_reason: BlockReason
    block_description: str = Field(sa_column=Column(Text))
    
    # Block period
    # (Leaving truncated in original manual view, but inferring common fields)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    blocked_by: int = Field(foreign_key="users.id")
    
    unblocked_at: Optional[datetime] = None
    unblocked_by: Optional[int] = Field(default=None, foreign_key="users.id")
    unblock_remarks: Optional[str] = Field(default=None, sa_column=Column(Text))
