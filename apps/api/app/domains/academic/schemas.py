"""
Academic Domain Schemas

Pydantic schemas for the academic domain.
Note: This is a simplified version. Full schemas can be added as needed.
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date


from app.shared.enums import ProgramType, ProgramStatus

# ----------------------------------------------------------------------
# Program Schemas
# ----------------------------------------------------------------------

class ProgramBase(BaseModel):
    name: str
    code: str
    alias: Optional[str] = None
    program_type: ProgramType = ProgramType.UG
    department_id: Optional[int] = None
    
    # Duration Rules
    duration_years: int
    number_of_semesters: Optional[int] = 0
    
    # Logic Toggles (Strict spec)
    semester_system: bool = True
    rnet_required: bool = True
    allow_installments: bool = True
    
    # Status
    status: ProgramStatus = ProgramStatus.ACTIVE
    is_active: bool = True

class ProgramCreate(ProgramBase):
    pass

class ProgramRead(ProgramBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Academic Year Schemas
# ----------------------------------------------------------------------

class AcademicYearBase(BaseModel):
    year: str
    start_date: date
    end_date: date
    is_current: bool = False


class AcademicYearCreate(AcademicYearBase):
    pass


class AcademicYearRead(AcademicYearBase):
    id: int
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Batch Schemas
# ----------------------------------------------------------------------

class BatchBase(BaseModel):
    batch_code: str
    batch_name: str
    program_id: int
    regulation_id: int
    joining_year: int
    start_year: int
    end_year: int
    regulation_code: Optional[str] = None


class BatchCreate(BatchBase):
    pass


class BatchRead(BatchBase):
    id: int
    current_year: int
    total_students: int
    status: str
    is_active: bool
    frozen_at: Optional[datetime] = None
    freeze_checksum: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class BatchSemesterBase(BaseModel):
    batch_id: int
    semester_number: int
    academic_year_id: int
    start_date: datetime
    end_date: datetime


class BatchSemesterCreate(BatchSemesterBase):
    pass


class BatchSemesterRead(BatchSemesterBase):
    id: int
    status: str
    is_current: bool
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Subject Schemas
# ----------------------------------------------------------------------

from app.shared.enums import SubjectType, EvaluationType

class SubjectBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    department_id: Optional[int] = None
    faculty_id: Optional[int] = None
    is_active: bool = True

class SubjectCreate(SubjectBase):
    pass

class SubjectRead(SubjectBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class SubjectConfigBase(BaseModel):
    subject_id: int
    has_theory: bool = True
    has_practical: bool = False
    theory_credits: float = 3.0
    practical_credits: float = 0.0
    internal_marks: int = 40
    external_marks: int = 60

class SubjectConfigCreate(SubjectConfigBase):
    pass

class SubjectConfigRead(SubjectConfigBase):
    id: int
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Regulation Schemas
# ----------------------------------------------------------------------

from app.shared.enums import RegulationStatus, ProgramType, PromotionRuleType

class RegulationSemesterBase(BaseModel):
    semester: int
    total_credits: float
    min_credits: float

class RegulationSemesterCreate(RegulationSemesterBase):
    pass

class RegulationSemesterRead(RegulationSemesterBase):
    id: int

class RegulationPromotionRuleBase(BaseModel):
    from_year: int
    to_year: int
    rule_type: PromotionRuleType
    min_credits_required: Optional[float] = None
    min_credit_percentage_required: Optional[float] = None
    max_backlogs_allowed: Optional[int] = None

class RegulationPromotionRuleCreate(RegulationPromotionRuleBase):
    pass

class RegulationPromotionRuleRead(RegulationPromotionRuleBase):
    id: int

class RegulationSubjectBase(BaseModel):
    subject_id: int
    semester: int
    credits: float
    subject_type: SubjectType = SubjectType.THEORY
    evaluation_type: EvaluationType = EvaluationType.THEORY_ONLY
    is_elective: bool = False
    elective_group: Optional[str] = None
    max_marks: int = 100
    internal_max: int = 40
    external_max: int = 60
    counts_for_hall_ticket: bool = True
    counts_for_promotion: bool = True

class RegulationSubjectCreate(RegulationSubjectBase):
    pass

class RegulationSubjectRead(RegulationSubjectBase):
    id: int

class RegulationBase(BaseModel):
    name: str
    program_id: int
    program_type: ProgramType = ProgramType.UG
    total_credits: int
    duration_years: int
    has_credit_based_detention: bool = True
    min_sgpa: float = 5.0
    min_cgpa: float = 5.0
    internal_pass_percentage: float = 0.0
    external_pass_percentage: float = 35.0
    total_pass_percentage: float = 40.0
    regulation_version: str = "v1"
    effective_from_year: Optional[int] = None

class RegulationCreate(RegulationBase):
    pass

# ----------------------------------------------------------------------
# Timetable & Operations Schemas
# ----------------------------------------------------------------------

from app.shared.enums import DayOfWeek, SlotType, AdjustmentStatus

class TimeSlotBase(BaseModel):
    name: str
    start_time: str # "HH:MM"
    end_time: str # "HH:MM"
    type: SlotType = SlotType.THEORY
    is_active: bool = True

class TimeSlotCreate(TimeSlotBase):
    pass

class TimeSlotRead(TimeSlotBase):
    id: int
    
    class Config:
        from_attributes = True

class ClassroomBase(BaseModel):
    room_number: str
    capacity: int
    type: str = "LECTURE"
    is_active: bool = True

class ClassroomCreate(ClassroomBase):
    pass

class ClassroomRead(ClassroomBase):
    id: int
    
    class Config:
        from_attributes = True

class ClassScheduleBase(BaseModel):
    academic_year_id: int
    batch_semester_id: int
    section_id: Optional[int] = None
    practical_batch_id: Optional[int] = None
    day_of_week: DayOfWeek
    period_id: int
    subject_id: Optional[int] = None
    faculty_id: Optional[int] = None
    room_id: Optional[int] = None

class ClassScheduleCreate(ClassScheduleBase):
    pass

class ClassScheduleRead(ClassScheduleBase):
    id: int
    
    class Config:
        from_attributes = True

class StudentSectionAssignmentBase(BaseModel):
    student_id: int
    section_id: int
    assignment_type: str = "AUTO"
    is_active: bool = True

class StudentSectionAssignmentCreate(StudentSectionAssignmentBase):
    pass

class StudentSectionAssignmentRead(StudentSectionAssignmentBase):
    id: int
    
    class Config:
        from_attributes = True

# ----------------------------------------------------------------------
# University Examination Schemas
# ----------------------------------------------------------------------

from app.shared.enums import ExamResultStatus

class UniversityExamBase(BaseModel):
    exam_name: str
    exam_code: str
    academic_year: str
    semester: int
    registration_start: date
    registration_end: date
    late_registration_end: Optional[date] = None
    exam_start_date: date
    exam_end_date: date
    exam_fee: float
    late_fee: float = 0.0
    min_attendance_percentage: float = 75.0
    allow_detained_students: bool = False
    instructions: Optional[str] = None

class UniversityExamCreate(UniversityExamBase):
    pass

class UniversityExamRead(UniversityExamBase):
    id: int
    is_active: bool
    is_registration_open: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UniversityExamRegistrationBase(BaseModel):
    student_id: int
    university_exam_id: int
    batch_semester_id: int
    subjects_registered: List[dict] # Will be serialized to JSON
    exam_fee: float
    late_fee: float = 0.0
    total_fee: float

class UniversityExamRegistrationCreate(UniversityExamRegistrationBase):
    pass

class UniversityExamRegistrationRead(UniversityExamRegistrationBase):
    id: int
    registration_number: str
    registration_date: date
    fee_paid: bool
    is_eligible: bool
    hall_ticket_number: Optional[str] = None
    hall_ticket_generated: bool
    
    class Config:
        from_attributes = True

class UniversityExamResultBase(BaseModel):
    student_id: int
    university_exam_id: int
    batch_subject_id: int
    theory_marks: Optional[float] = None
    practical_marks: Optional[float] = None
    internal_marks: Optional[float] = None
    total_marks: float
    percentage: float
    grade: Optional[str] = None
    grade_points: Optional[float] = None
    credits_earned: int
    result_status: ExamResultStatus = ExamResultStatus.PASS

class UniversityExamResultCreate(UniversityExamResultBase):
    pass

class UniversityExamResultRead(UniversityExamResultBase):
    id: int
    
    class Config:
        from_attributes = True

class RegulationRead(RegulationBase):
    id: int
    is_locked: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Section Schemas
# ----------------------------------------------------------------------

class SectionBase(BaseModel):
    name: str
    batch_id: int
    semester_no: int
    capacity: int = 60


class SectionCreate(SectionBase):
    pass


class SectionRead(SectionBase):
    id: int
    current_strength: int
    
    class Config:
        from_attributes = True


class PracticalBatchBase(BaseModel):
    name: str
    batch_id: int
    batch_semester_id: int
    capacity: int = 30
    code: str


class PracticalBatchCreate(PracticalBatchBase):
    pass


class PracticalBatchRead(PracticalBatchBase):
    id: int
    current_strength: int
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Exam Schemas
# ----------------------------------------------------------------------

from app.shared.enums import ExamType, ExamStatus, ExamResultStatus

class ExamBase(BaseModel):
    name: str
    exam_type: ExamType
    academic_year: str
    batch_semester_id: int
    start_date: date
    end_date: date
    description: Optional[str] = None

class ExamCreate(ExamBase):
    pass

class ExamRead(ExamBase):
    id: int
    status: ExamStatus
    
    class Config:
        from_attributes = True

class InternalExamBase(BaseModel):
    name: str
    exam_code: str
    academic_year: str
    batch_id: int
    batch_semester_id: int
    exam_type: ExamType = ExamType.MID_TERM
    start_date: date
    end_date: date
    total_marks: int = 100
    passing_marks: int = 40
    weightage: float = 0.3

class InternalExamCreate(InternalExamBase):
    pass

class InternalExamRead(InternalExamBase):
    id: int
    is_published: bool
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class StudentInternalMarksBase(BaseModel):
    student_id: int
    internal_exam_subject_id: int
    marks_obtained: Optional[float] = None
    is_absent: bool = False
    remarks: Optional[str] = None

class StudentInternalMarksCreate(StudentInternalMarksBase):
    pass

class StudentInternalMarksRead(StudentInternalMarksBase):
    id: int
    is_verified: bool
    
    class Config:
        from_attributes = True


# ----------------------------------------------------------------------
# Attendance Schemas
# ----------------------------------------------------------------------

from app.shared.enums import SessionStatus, AttendanceStatus

class AttendanceSessionBase(BaseModel):
    subject_id: int
    faculty_id: int
    program_id: int
    program_year_id: int
    semester: int
    section: Optional[str] = None
    practical_batch_id: Optional[int] = None
    session_date: date
    start_time: str # Format "HH:MM"
    end_time: str # Format "HH:MM"
    status: SessionStatus = SessionStatus.SCHEDULED

class AttendanceSessionCreate(AttendanceSessionBase):
    pass

class AttendanceSessionRead(AttendanceSessionBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class AttendanceRecordBase(BaseModel):
    student_id: int
    session_id: int
    status: AttendanceStatus
    remarks: Optional[str] = None

class AttendanceRecordCreate(AttendanceRecordBase):
    pass

class AttendanceRecordRead(AttendanceRecordBase):
    id: int
    
    class Config:
        from_attributes = True

class BulkAttendanceMark(BaseModel):
    session_id: int
    attendance_data: List[AttendanceRecordCreate]

# ----------------------------------------------------------------------
# Timetable Schemas
# ----------------------------------------------------------------------

from app.shared.enums import DayOfWeek, SlotType

class TimetableSlotBase(BaseModel):
    day_of_week: DayOfWeek
    start_time: str
    end_time: str
    slot_type: SlotType = SlotType.THEORY
    batch_semester_id: int
    subject_id: Optional[int] = None
    faculty_id: Optional[int] = None
    room_id: Optional[int] = None
    section: Optional[str] = None

class TimetableSlotCreate(TimetableSlotBase):
    pass

class TimetableSlotRead(TimetableSlotBase):
    id: int
    
    class Config:
        from_attributes = True

# ----------------------------------------------------------------------
# Audit & Override Schemas
# ----------------------------------------------------------------------

class BatchRuleOverrideBase(BaseModel):
    batch_id: int
    rule_type: str
    old_value: str
    new_value: str
    reason: str
    document_ref: Optional[str] = None

class BatchRuleOverrideCreate(BatchRuleOverrideBase):
    approved_by_id: int

class BatchRuleOverrideRead(BatchRuleOverrideBase):
    id: int
    approved_by_id: int
    approved_at: datetime

    class Config:
        from_attributes = True
