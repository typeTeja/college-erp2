"""
Academic Domain Router

API endpoints for the academic domain.
Note: This is a simplified version. Full endpoints can be added as needed.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List, Optional

from app.api.deps import get_session, get_current_user
from app.domains.auth.models import AuthUser as User
from app.domains.system.schemas import DepartmentRead
from app.domains.academic.exceptions import (
    AcademicYearNotFoundError, BatchNotFoundError,
    RegulationNotFoundError, SectionNotFoundError
)
from app.domains.hr.services import HRService
from app.domains.academic.services import ProgramService, AcademicService
from app.domains.academic.setup_service import academic_setup_service
from app.domains.academic.operations_service import academic_operations_service
from app.domains.academic.university_exam_service import university_exam_service
from app.domains.academic.attendance_service import attendance_service
from app.domains.academic.exam_service import exam_service
from app.domains.academic.schemas import (
    AcademicYearCreate, AcademicYearRead,
    BatchCreate, BatchRead,
    RegulationCreate, RegulationRead,
    SectionCreate, SectionRead,
    BatchSemesterCreate, BatchSemesterRead,
    PracticalBatchCreate, PracticalBatchRead,
    ProgramRead,
    AttendanceSessionCreate, AttendanceSessionRead,
    AttendanceRecordRead, BulkAttendanceMark,
    InternalExamCreate, InternalExamRead,
    StudentInternalMarksCreate, StudentInternalMarksRead,
    SubjectCreate, SubjectRead,
    SubjectConfigCreate, SubjectConfigRead,
    RegulationSubjectCreate, RegulationSubjectRead,
    RegulationSemesterCreate, RegulationSemesterRead,
    RegulationPromotionRuleCreate, RegulationPromotionRuleRead,
    TimeSlotCreate, TimeSlotRead,
    ClassroomCreate, ClassroomRead,
    ClassScheduleCreate, ClassScheduleRead,
    StudentSectionAssignmentCreate, StudentSectionAssignmentRead,
    UniversityExamCreate, UniversityExamRead,
    UniversityExamRegistrationCreate, UniversityExamRegistrationRead,
    UniversityExamResultCreate, UniversityExamResultRead
)


router = APIRouter()


# ----------------------------------------------------------------------
# Program & Department Master Data
# ----------------------------------------------------------------------

@router.get("/programs", response_model=List[ProgramRead])
def list_programs(
    session: Session = Depends(get_session),
):
    """List all academic programs"""
    return ProgramService.get_programs(session)


@router.get("/departments", response_model=List[DepartmentRead])
def list_departments(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List all functional departments (HR/Academic)"""
    hr_service = HRService(session)
    return hr_service.list_departments()


# ----------------------------------------------------------------------
# Academic Year Endpoints
# ----------------------------------------------------------------------

@router.get("/academic-years", response_model=List[AcademicYearRead])
def list_academic_years(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List all academic years"""
    service = AcademicService(session)
    years = service.list_academic_years()
    return years


@router.post("/academic-years", response_model=AcademicYearRead, status_code=status.HTTP_201_CREATED)
def create_academic_year(
    year_data: AcademicYearCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new academic year"""
    service = AcademicService(session)
    year = service.create_academic_year(year_data)
    return year


# ----------------------------------------------------------------------
# Batch Endpoints
# ----------------------------------------------------------------------

@router.get("/batches", response_model=List[BatchRead])
def list_batches(
    program_id: Optional[int] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List all batches"""
    service = AcademicService(session)
    batches = service.list_batches(program_id=program_id)
    return batches


@router.post("/batches", response_model=BatchRead, status_code=status.HTTP_201_CREATED)
def create_batch(
    data: BatchCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new academic batch"""
    service = AcademicService(session)
    return service.create_batch(data)


@router.get("/batches/{batch_id}", response_model=BatchRead)
def get_batch(
    batch_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get batch by ID"""
    service = AcademicService(session)
    try:
        batch = service.get_batch(batch_id)
        return batch
    except BatchNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/batches/{batch_id}/semesters", response_model=List[dict])
def get_batch_semesters(
    batch_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get semesters for a batch"""
    service = AcademicService(session)
    try:
        return service.get_batch_semesters(batch_id)
    except BatchNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/batches/{batch_id}/program-years", response_model=List[dict])
def get_program_years(
    batch_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get academic years (program years) for a batch"""
    from app.domains.academic.models.batch import ProgramYear
    return session.exec(select(ProgramYear)).all()


@router.post("/batch-semesters", response_model=BatchSemesterRead, status_code=status.HTTP_201_CREATED)
def create_batch_semester(
    data: BatchSemesterCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new semester for a batch"""
    service = AcademicService(session)
    return service.create_batch_semester(data)


@router.get("/batches/{batch_id}/subjects", response_model=List[dict])
def get_batch_subjects(
    batch_id: int,
    semester_no: Optional[int] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get subjects for a batch, optionally filtered by semester"""
    service = AcademicService(session)
    try:
        return service.get_batch_subjects(batch_id, semester_no)
    except (BatchNotFoundError, HierarchyValidationError) as e:
        raise HTTPException(status_code=404, detail=str(e))


# ----------------------------------------------------------------------
# Regulation Endpoints
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# Regulation Endpoints
# ----------------------------------------------------------------------

@router.get("/regulations", response_model=List[RegulationRead])
def list_regulations(
    program_id: Optional[int] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List all regulations"""
    return academic_setup_service.list_regulations(session, program_id=program_id)


@router.get("/regulations/{regulation_id}", response_model=RegulationRead)
def get_regulation(
    regulation_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get regulation details"""
    try:
        return academic_setup_service.get_regulation(session, regulation_id)
    except RegulationNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ----------------------------------------------------------------------
# Section Endpoints
# ----------------------------------------------------------------------

@router.get("/sections", response_model=List[SectionRead])
def list_sections(
    batch_id: Optional[int] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List all sections"""
    service = AcademicService(session)
    sections = service.list_sections(batch_id=batch_id)
    return sections


@router.post("/sections", response_model=SectionRead, status_code=status.HTTP_201_CREATED)
def create_section(
    data: SectionCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new section"""
    service = AcademicService(session)
    return service.create_section(data)


@router.post("/practical-batches", response_model=PracticalBatchRead, status_code=status.HTTP_201_CREATED)
def create_practical_batch(
    data: PracticalBatchCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new practical laboratory batch"""
    service = AcademicService(session)
    return service.create_practical_batch(data)


# ----------------------------------------------------------------------
# Attendance Endpoints
# ----------------------------------------------------------------------

@router.post("/attendance/sessions", response_model=AttendanceSessionRead, status_code=status.HTTP_201_CREATED)
def create_attendance_session(
    data: AttendanceSessionCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new attendance session"""
    return attendance_service.create_session(session, data)


@router.post("/attendance/mark", response_model=List[AttendanceRecordRead])
def mark_attendance(
    data: BulkAttendanceMark,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Mark bulk attendance for a session"""
    return attendance_service.mark_bulk_attendance(session, data)


@router.get("/attendance/sessions/{session_id}/records", response_model=List[AttendanceRecordRead])
def get_session_attendance(
    session_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get all attendance records for a session"""
    return attendance_service.get_session_attendance(session, session_id)


@router.get("/attendance/student/{student_id}/summary")
def get_student_attendance(
    student_id: int,
    subject_id: Optional[int] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get attendance summary for a student"""
    return attendance_service.get_student_attendance_summary(session, student_id, subject_id)


# ----------------------------------------------------------------------
# Internal Exam Endpoints
# ----------------------------------------------------------------------

@router.post("/exams/internal", response_model=InternalExamRead, status_code=status.HTTP_201_CREATED)
def create_internal_exam(
    data: InternalExamCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new internal exam cycle"""
    return exam_service.create_internal_exam(session, data)


@router.post("/exams/internal/marks", response_model=StudentInternalMarksRead)
def mark_exam_marks(
    data: StudentInternalMarksCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Record marks for a student in an internal exam subject"""
    return exam_service.mark_student_marks(session, data)


@router.get("/exams/internal/{exam_id}")
def get_internal_exam(
    exam_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get full details of an internal exam"""
    return exam_service.get_internal_exam_details(session, exam_id)


# ----------------------------------------------------------------------
# Academic Setup (Subjects & Regulations)
# ----------------------------------------------------------------------

@router.get("/subjects", response_model=List[SubjectRead])
def list_subjects(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List all academic subjects"""
    return academic_setup_service.list_subjects(session)


@router.get("/subjects/{subject_id}", response_model=SubjectRead)
def get_subject(
    subject_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get subject by ID"""
    return academic_setup_service.get_subject(session, subject_id)


@router.post("/subjects", response_model=SubjectRead, status_code=status.HTTP_201_CREATED)
def create_subject(
    data: SubjectCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new academic subject"""
    return academic_setup_service.create_subject(session, data)


@router.post("/subjects/config", response_model=SubjectConfigRead, status_code=status.HTTP_201_CREATED)
def configure_subject(
    data: SubjectConfigCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Configure evaluation and credits for a subject"""
    return academic_setup_service.configure_subject(session, data)


@router.post("/regulations", response_model=RegulationRead, status_code=status.HTTP_201_CREATED)
def create_regulation(
    data: RegulationCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new academic regulation"""
    return academic_setup_service.create_regulation(session, data, user_id=current_user.id)


@router.post("/regulations/{regulation_id}/subjects", response_model=RegulationSubjectRead)
def add_subject_to_regulation(
    regulation_id: int,
    data: RegulationSubjectCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Map a subject to a regulation"""
    try:
        return academic_setup_service.add_subject_to_regulation(session, regulation_id, data)
    except (RegulationNotFoundError, RegulationLockedError) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/regulations/{regulation_id}/semesters", response_model=RegulationSemesterRead)
def add_regulation_semester_rules(
    regulation_id: int,
    data: RegulationSemesterCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Add credit rules for a semester in a regulation"""
    return academic_setup_service.add_semester_rules(session, regulation_id, data)


@router.post("/regulations/{regulation_id}/promotion-rules", response_model=RegulationPromotionRuleRead)
def add_regulation_promotion_rule(
    regulation_id: int,
    data: RegulationPromotionRuleCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Add a promotion rule (e.g., Year 1 to Year 2) for a regulation"""
    return academic_setup_service.add_promotion_rule(session, regulation_id, data)


@router.post("/regulations/{regulation_id}/lock", response_model=RegulationRead)
def lock_regulation(
    regulation_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Lock a regulation to prevent further modification"""
    try:
        return academic_setup_service.lock_regulation(session, regulation_id, user_id=current_user.id)
    except RegulationNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ----------------------------------------------------------------------
# Academic Operations (Timetable & Assignments)
# ----------------------------------------------------------------------

@router.get("/timeslots", response_model=List[TimeSlotRead])
def list_timeslots(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List all defined periods/timeslots"""
    return academic_operations_service.list_timeslots(session)


@router.get("/classrooms", response_model=List[ClassroomRead])
def list_classrooms(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List all registered classrooms"""
    return academic_operations_service.list_classrooms(session)


@router.get("/timetable", response_model=List[ClassScheduleRead])
def list_timetable_entries(
    academic_year_id: int,
    batch_semester_id: Optional[int] = None,
    section_id: Optional[int] = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Fetch timetable with filters"""
    return academic_operations_service.list_timetable_entries(
        session, academic_year_id, batch_semester_id, section_id
    )


@router.post("/timeslots", response_model=TimeSlotRead, status_code=status.HTTP_201_CREATED)
def create_timeslot(
    data: TimeSlotCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Define a new academic period/timeslot"""
    return academic_operations_service.create_timeslot(session, data)


@router.post("/classrooms", response_model=ClassroomRead, status_code=status.HTTP_201_CREATED)
def create_classroom(
    data: ClassroomCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Register a new classroom"""
    return academic_operations_service.create_classroom(session, data)


@router.post("/timetable", response_model=ClassScheduleRead, status_code=status.HTTP_201_CREATED)
def create_timetable_entry(
    data: ClassScheduleCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new timetable entry with conflict checks"""
    return academic_operations_service.create_timetable_entry(session, data)


@router.post("/assignments/section", response_model=StudentSectionAssignmentRead, status_code=status.HTTP_201_CREATED)
def assign_student_to_section(
    data: StudentSectionAssignmentCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Assign a student to a section"""
    return academic_operations_service.assign_student_to_section(session, data, user_id=current_user.id)


# ----------------------------------------------------------------------
# University Examinations
# ----------------------------------------------------------------------

@router.post("/exams/university", response_model=UniversityExamRead, status_code=status.HTTP_201_CREATED)
def create_university_exam(
    data: UniversityExamCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Create a new university examination cycle"""
    return university_exam_service.create_exam(session, data, user_id=current_user.id)


@router.post("/exams/university/register", response_model=UniversityExamRegistrationRead, status_code=status.HTTP_201_CREATED)
def register_for_university_exam(
    data: UniversityExamRegistrationCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Register a student for a university exam"""
    return university_exam_service.register_student(session, data)


@router.post("/exams/university/{exam_id}/generate-hall-tickets", response_model=List[UniversityExamRegistrationRead])
def generate_hall_tickets(
    exam_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Generate hall tickets for eligible students in an exam cycle"""
    return university_exam_service.generate_hall_tickets(session, exam_id)


@router.post("/exams/university/results", response_model=UniversityExamResultRead, status_code=status.HTTP_201_CREATED)
def record_university_result(
    data: UniversityExamResultCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Record university exam result for a student subject"""
    return university_exam_service.record_result(session, data)
