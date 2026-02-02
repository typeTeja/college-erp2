from typing import TYPE_CHECKING, List, Optional
from enum import Enum
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship, Column, JSON
from sqlalchemy import Text

if TYPE_CHECKING:
    from .enrollment import Enrollment
    from app.models.program import Program
    from .parent import Parent
    from app.domains.academic.models.student_history import StudentSemesterHistory, StudentPromotionLog

from app.schemas.json_fields import StudentDocuments
from app.shared.enums import BloodGroup, CreatedFrom, Gender, ScholarshipCategory, StudentStatus


class Student(SQLModel, table=True):
    """Student information model with comprehensive details"""
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Basic Information
    admission_number: str = Field(index=True, unique=True)
    name: str
    middle_name: Optional[str] = None
    dob: Optional[str] = None
    
    # Contact Information
    phone: Optional[str] = Field(default=None, index=True)
    email: Optional[str] = Field(default=None, index=True)
    alternate_mobile: Optional[str] = None
    
    # Address Information
    current_address: Optional[str] = Field(default=None, sa_column=Column(Text))
    permanent_address: Optional[str] = Field(default=None, sa_column=Column(Text))
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    
    # Demographics
    gender: Gender = Field(default=Gender.MALE)
    blood_group: Optional[BloodGroup] = None
    aadhaar_number: Optional[str] = Field(default=None, unique=True, index=True)
    nationality: str = Field(default="Indian")
    religion: Optional[str] = None
    caste_category: Optional[str] = None  # Can also use ScholarshipCategory enum
    
    # Parent Details
    father_name: Optional[str] = None
    father_mobile: Optional[str] = None
    father_email: Optional[str] = None
    father_occupation: Optional[str] = None
    
    mother_name: Optional[str] = None
    mother_mobile: Optional[str] = None
    mother_email: Optional[str] = None
    mother_occupation: Optional[str] = None
    
    # Guardian Details
    guardian_name: Optional[str] = None
    guardian_mobile: Optional[str] = None
    guardian_relation: Optional[str] = None
    
    # Emergency Contact
    emergency_contact_name: Optional[str] = None
    emergency_contact_mobile: Optional[str] = None
    emergency_contact_relation: Optional[str] = None
    
    # Previous Education
    previous_qualification: Optional[str] = None
    previous_institution: Optional[str] = None
    previous_institution_city: Optional[str] = None
    previous_institution_district: Optional[str] = None
    previous_board: Optional[str] = None
    previous_marks: Optional[float] = None
    previous_percentage: Optional[float] = None
    previous_year_of_passing: Optional[int] = None
    
    # Documents (JSON field to store document URLs)
    documents: Optional[StudentDocuments] = Field(default_factory=StudentDocuments, sa_column=Column(JSON))
    # Example: {"photo": "url", "10th_certificate": "url", "12th_certificate": "url"}
    
    # Portal Access
    portal_user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    portal_password_hash: Optional[str] = None
    portal_last_login: Optional[datetime] = None
    
    # Fee Tracking
    fee_structure_id: Optional[int] = Field(default=None, foreign_key="fee_structure.id")
    total_fee: Optional[float] = None
    paid_amount: Optional[float] = Field(default=0.0)
    pending_amount: Optional[float] = None
    
    # Academic Links
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True)
    program_id: int = Field(foreign_key="program.id", index=True)
    
    # Strict Academic Structure (Foreign Keys)
    batch_id: int = Field(foreign_key="academic_batches.id", index=True)
    program_year_id: int = Field(foreign_key="program_years.id", index=True)
    batch_semester_id: int = Field(foreign_key="batch_semesters.id", index=True)
    section_id: Optional[int] = Field(default=None, foreign_key="section.id", index=True)
    practical_batch_id: Optional[int] = Field(default=None, foreign_key="practical_batch.id", index=True)
    
    # Flags relative to admission
    hostel_required: bool = Field(default=False)
    transport_required: bool = Field(default=False)
    scholarship_category: ScholarshipCategory = Field(default=ScholarshipCategory.GENERAL)
    lateral_entry: bool = Field(default=False)
    
    # Status
    status: StudentStatus = Field(default=StudentStatus.IMPORTED_PENDING_VERIFICATION)
    
    # Deactivation Tracking
    deactivated_at: Optional[datetime] = None
    deactivated_by: Optional[int] = Field(default=None, foreign_key="user.id")
    deactivation_reason: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # Metadata
    created_from: CreatedFrom = Field(default=CreatedFrom.MANUAL)  # manual, admission, bulk_upload
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    program: "Program" = Relationship(back_populates="students")
    enrollments: List["Enrollment"] = Relationship(back_populates="student")
    parent: Optional["Parent"] = Relationship(sa_relationship_kwargs={"uselist": False, "foreign_keys": "Parent.linked_student_id"})
    
    # Academic foundation relationships
    semester_history: List["StudentSemesterHistory"] = Relationship(back_populates="student")
    promotion_logs: List["StudentPromotionLog"] = Relationship(back_populates="student")
