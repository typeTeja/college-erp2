from enum import Enum
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import date, time

if TYPE_CHECKING:
    from .faculty import Faculty
    from .subject import Subject
    from .student import Semester
    # from .academic_year import AcademicYear # Assuming exists or using ID directly

class DayOfWeek(str, Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"

class SlotType(str, Enum):
    THEORY = "THEORY"
    PRACTICAL = "PRACTICAL"
    BREAK = "BREAK"
    ASSEMBLY = "ASSEMBLY"

class AdjustmentStatus(str, Enum):
    REQUESTED = "REQUESTED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    COMPLETED = "COMPLETED"

# --- Master Data ---

class TimeSlot(SQLModel, table=True):
    """Defines a period (e.g., 09:00 - 10:00)"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str  # e.g., "Period 1", "Morning Break"
    start_time: time
    end_time: time
    type: SlotType = Field(default=SlotType.THEORY)
    is_active: bool = Field(default=True)

class Classroom(SQLModel, table=True):
    """Physical rooms/labs"""
    id: Optional[int] = Field(default=None, primary_key=True)
    room_number: str = Field(index=True, unique=True)
    capacity: int
    type: str = Field(default="LECTURE") # LECTURE, LAB, SEMINAR_HALL
    is_active: bool = Field(default=True)

# --- Timetable Structure ---

class TimetableTemplate(SQLModel, table=True):
    """Named templates for schedule structures (e.g. 'Regular 9-4', 'Half Day')"""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    description: Optional[str] = None

class ClassSchedule(SQLModel, table=True):
    """The actual Timetable entries"""
    __tablename__ = "timetable_entry"

    id: Optional[int] = Field(default=None, primary_key=True)
    academic_year_id: int
    semester_id: int = Field(foreign_key="semester.id")
    section_id: Optional[int] = None # Or link to a Section model if it exists
    
    day_of_week: DayOfWeek
    period_id: int = Field(foreign_key="timeslot.id")
    subject_id: Optional[int] = Field(default=None, foreign_key="subject.id")
    faculty_id: Optional[int] = Field(default=None, foreign_key="faculty.id")
    room_id: Optional[int] = Field(default=None, foreign_key="classroom.id")
    
    # Relationships
    period: Optional[TimeSlot] = Relationship()
    # subject: Optional["Subject"] = Relationship()
    # faculty: Optional["Faculty"] = Relationship()
    # room: Optional[Classroom] = Relationship()

class ClassAdjustment(SQLModel, table=True):
    """Substitution/Adjustment Ledger"""
    id: Optional[int] = Field(default=None, primary_key=True)
    timetable_entry_id: int = Field(foreign_key="timetable_entry.id")
    date: date
    
    original_faculty_id: int = Field(foreign_key="faculty.id")
    substitute_faculty_id: Optional[int] = Field(default=None, foreign_key="faculty.id")
    
    status: AdjustmentStatus = Field(default=AdjustmentStatus.REQUESTED)
    reason: Optional[str] = None
    
    created_at: date = Field(default_factory=date.today)
