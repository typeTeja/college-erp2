from .batch import AcademicBatch, ProgramYear, BatchSemester, BatchSubject
from .regulation import Regulation, RegulationSemester, RegulationSubject, RegulationPromotionRule
from .setup import AcademicYear, Section, PracticalBatch, SubjectConfig
from .internal_exam import (
    InternalExam, InternalExamSubject, StudentInternalMarks, 
    InternalMarksConsolidated, ExamType as InternalExamType, ResultStatus as InternalResultStatus,
    ResultStatus
)
from .university_exam import (
    UniversityExam, UniversityExamRegistration, UniversityExamResult,
    SemesterResult, ExamResultStatus as UniversityExamResultStatus,
    ExamResultStatus
)
from .hall_ticket import HallTicket, HallTicketConfig, DisciplineBlock, HallTicketStatus, BlockReason
from .assignment import StudentSectionAssignment, StudentLabAssignment
from .allocation import StudentPracticalBatchAllocation
from .student_history import (
    StudentSemesterHistory, StudentPromotionLog, 
    StudentRegulationMigration, PromotionEligibility
)
from .exam import Exam, ExamSchedule, ExamResult, ExamType, ExamStatus
from .attendance import AttendanceSession, AttendanceRecord, AttendanceStatus, SessionStatus
from .timetable import (
    TimeSlot, Classroom, TimetableTemplate, ClassSchedule, 
    ClassAdjustment, DayOfWeek, SlotType, AdjustmentStatus
)
