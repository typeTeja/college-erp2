from .program import Program
from .setup import AcademicYear, Section, PracticalBatch
from .subject import Subject, SubjectConfig
from .regulation import (
    Regulation,
    RegulationSubject,
    RegulationSemester,
    RegulationPromotionRule,
)
from .batch import (
    ProgramYear,
    AcademicBatch,
    BatchSemester,
    BatchSubject,
)
from .assignment import (
    StudentSectionAssignment,
    StudentPracticalBatchAllocation,
)
from .history import (
    PromotionEligibility,
    StudentSemesterHistory,
    StudentPromotionLog,
    StudentRegulationMigration,
)
from .attendance import (
    AttendanceSession,
    AttendanceRecord,
)
from .timetable import (
    TimeSlot,
    Classroom,
    TimetableTemplate,
    ClassSchedule,
    ClassAdjustment,
)
from .exam import (
    Exam,
    ExamSchedule,
    ExamResult,
    InternalExam,
    InternalExamSubject,
    StudentInternalMarks,
    InternalMarksConsolidated,
    UniversityExam,
    UniversityExamRegistration,
    UniversityExamResult,
    SemesterResult,
)
from .hall_ticket import (
    HallTicketConfig,
    HallTicket,
    DisciplineBlock,
)

__all__ = [
    "Program",
    "AcademicYear",
    "Section",
    "PracticalBatch",
    "Subject",
    "SubjectConfig",
    "Regulation",
    "RegulationSubject",
    "RegulationSemester",
    "RegulationPromotionRule",
    "ProgramYear",
    "AcademicBatch",
    "BatchSemester",
    "BatchSubject",
    "StudentSectionAssignment",
    "StudentPracticalBatchAllocation",
    "PromotionEligibility",
    "StudentSemesterHistory",
    "StudentPromotionLog",
    "StudentRegulationMigration",
    "AttendanceSession",
    "AttendanceRecord",
    "TimeSlot",
    "Classroom",
    "TimetableTemplate",
    "ClassSchedule",
    "ClassAdjustment",
    "Exam",
    "ExamSchedule",
    "ExamResult",
    "InternalExam",
    "InternalExamSubject",
    "StudentInternalMarks",
    "InternalMarksConsolidated",
    "UniversityExam",
    "UniversityExamRegistration",
    "UniversityExamResult",
    "SemesterResult",
    "HallTicketConfig",
    "HallTicket",
    "DisciplineBlock",
]
