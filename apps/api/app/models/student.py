from typing import TYPE_CHECKING, List, Optional
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .enrollment import Enrollment
    from .program import Program
    from .parent import Parent

class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

class BloodGroup(str, Enum):
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    AB_POS = "AB+"
    AB_NEG = "AB-"
    O_POS = "O+"
    O_NEG = "O-"

class ScholarshipCategory(str, Enum):
    GENERAL = "GENERAL"
    SC = "SC"
    ST = "ST"
    OBC = "OBC"
    EWS = "EWS"

class StudentStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ALUMNI = "ALUMNI"
    IMPORTED_PENDING_VERIFICATION = "IMPORTED_PENDING_VERIFICATION"

class Student(SQLModel, table=True):
    """Student information model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    admission_number: str = Field(index=True, unique=True)
    name: str
    dob: Optional[str] = None
    phone: Optional[str] = Field(default=None, index=True)
    email: Optional[str] = Field(default=None, index=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", index=True)
    program_id: int = Field(foreign_key="program.id", index=True)
    current_year: int = Field(default=1)  # Current academic year (1, 2, 3, 4)
    current_semester: int = Field(default=1) # Mutable semester
    section: str = Field(default="A")
    batch: str = Field(default="2024-2028") # e.g. 2024-2028
    
    # Demographics
    gender: Gender = Field(default=Gender.MALE)
    aadhaar_number: Optional[str] = Field(default=None, unique=True, index=True)
    blood_group: Optional[BloodGroup] = None
    
    # Flags relative to admission
    hostel_required: bool = Field(default=False)
    transport_required: bool = Field(default=False)
    scholarship_category: ScholarshipCategory = Field(default=ScholarshipCategory.GENERAL)
    lateral_entry: bool = Field(default=False)
    
    status: StudentStatus = Field(default=StudentStatus.IMPORTED_PENDING_VERIFICATION)
    
    # Relationships
    program: "Program" = Relationship(back_populates="students")
    enrollments: List["Enrollment"] = Relationship(back_populates="student")
    parent: Optional["Parent"] = Relationship(sa_relationship_kwargs={"uselist": False, "foreign_keys": "Parent.linked_student_id"})
