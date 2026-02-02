from typing import Optional, List
from datetime import time, date
from pydantic import BaseModel
from app.domains.academic.models import DayOfWeek, SlotType, AdjustmentStatus

# --- TimeSlot ---
class TimeSlotBase(BaseModel):
    name: str # e.g. "Period 1"
    start_time: time
    end_time: time
    type: SlotType = SlotType.THEORY
    is_active: bool = True

class TimeSlotCreate(TimeSlotBase):
    pass

class TimeSlotRead(TimeSlotBase):
    id: int

# --- Classroom ---
class ClassroomBase(BaseModel):
    room_number: str
    capacity: int
    type: str = "LECTURE"
    is_active: bool = True

class ClassroomCreate(ClassroomBase):
    pass

class ClassroomRead(ClassroomBase):
    id: int

# --- Timetable Template ---
class TimetableTemplateBase(BaseModel):
    name: str
    description: Optional[str] = None

class TimetableTemplateCreate(TimetableTemplateBase):
    pass

class TimetableTemplateRead(TimetableTemplateBase):
    id: int

# --- Class Schedule (Timetable Entry) ---
class ClassScheduleBase(BaseModel):
    academic_year_id: int
    semester_id: int
    section_id: Optional[int] = None
    day_of_week: DayOfWeek
    period_id: int
    subject_id: Optional[int] = None
    faculty_id: Optional[int] = None
    room_id: Optional[int] = None

class ClassScheduleCreate(ClassScheduleBase):
    pass

class ClassScheduleRead(ClassScheduleBase):
    id: int
    period: Optional[TimeSlotRead] = None
    # Add other nested reads (Subject, Faculty) if needed

# --- Class Adjustment (Substitution) ---
class ClassAdjustmentBase(BaseModel):
    timetable_entry_id: int
    date: date
    original_faculty_id: int
    substitute_faculty_id: Optional[int] = None
    reason: Optional[str] = None

class ClassAdjustmentCreate(ClassAdjustmentBase):
    pass

class ClassAdjustmentUpdate(BaseModel):
    substitute_faculty_id: Optional[int] = None
    status: AdjustmentStatus

class ClassAdjustmentRead(ClassAdjustmentBase):
    id: int
    status: AdjustmentStatus
    created_at: date
