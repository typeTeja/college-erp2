# Central registry for Alembic autogenerate
# Import all models here so Alembic can discover them

# System models now in domains/system/models.py
# from .user import User
# from .role import Role
# from .user_role import UserRole
# from .permission import Permission, RolePermission, PermissionAuditLog
from .department import Department
from .program import Program
from .subject import Subject
from .lesson import LessonPlan, SyllabusTopic, QuestionBank, Question
from .master_data import Board, PreviousQualification, StudyGroup, ReservationCategory, LeadSource
from .placement.company import PlacementCompany
from .settings.notifications import EmailTemplate, SMSTemplate
"""
Central Models Import

This file serves as a central import point for all models.
All models are now organized in domain-specific modules under app/domains/.

Legacy model files have been deleted and replaced with domain-specific models.
"""

# Auth Domain Models (moved from system)
from app.domains.auth.models import (
    AuthUser as User,  # Alias for backward compatibility
    Role,
    Permission,
    UserRole,
    RolePermission,
)

# System Domain Models
from app.domains.system.models import (
    SystemSetting,
    InstituteInfo,
    AuditLog,
    PermissionAuditLog,
    FileMetadata,
    ImportLog,
)

# HR Domain Models
from app.domains.hr.models import (
    Designation,
    Staff,
    Faculty,
)

# Academic Domain Models
from app.domains.academic.models import (
    Department,
    Program,
    Subject,
    AcademicYear,
    AcademicBatch,
    Section,
    PracticalBatch,
    SubjectConfig,
    Regulation,
    Semester,
    Shift,
    Exam,
    ExamSchedule,
    ExamResult,
    Question,
    Timetable,
    TimeSlot,
    Classroom,
    TimetableTemplate,
    ClassSchedule,
    ClassAdjustment,
    AttendanceSession,
    AttendanceRecord,
    InternalExam,
    InternalExamSchedule,
    InternalExamResult,
    EntranceExam,
    EntranceExamSchedule,
    EntranceExamResult,
    HallTicket,
)

# Student Domain Models
from app.domains.student.models import (
    Student,
    Parent,
    Enrollment,
    StudentPracticalBatchAllocation,
    Board,
    PreviousQualification,
    StudyGroup,
    ReservationCategory,
)
from app.domains.student.models import (
    ODCHotel, ODCRequest, StudentODCApplication, ODCBilling, ODCPayout,
    DocumentCategory, StudentDocument, DocumentVerification
)
from .operations import Shift, MaintenanceTicket
# Finance Domain
from app.domains.finance.models import (
    FeeStructure, FeeComponent, FeeInstallment, StudentFee,
    FeePayment, FeeConcession, FeeFine, StudentFeeInstallment,
    PaymentGatewayConfig, OnlinePayment, PaymentReceipt,
    FeeHead, InstallmentPlan, ScholarshipSlab
)

# Admissions Domain
from app.domains.admission.models import (
    Application, ApplicationPayment, ApplicationDocument, 
    ApplicationActivityLog, AdmissionSettings,
    EntranceTestConfig, EntranceExamResult,
    TentativeAdmission, ScholarshipCalculation
)

# Academic Domain
from app.domains.academic.models import (
    AcademicBatch, ProgramYear, BatchSemester, BatchSubject,
    Regulation, RegulationSemester, RegulationSubject, RegulationPromotionRule,
    AcademicYear, Section, PracticalBatch, SubjectConfig,
    InternalExam, InternalExamSubject, StudentInternalMarks, InternalMarksConsolidated,
    UniversityExam, UniversityExamRegistration, UniversityExamResult, SemesterResult,
    HallTicket, HallTicketConfig, DisciplineBlock,
    StudentSectionAssignment, StudentLabAssignment,
    StudentPracticalBatchAllocation,
    StudentSemesterHistory, StudentPromotionLog, StudentRegulationMigration, PromotionEligibility,
    Exam, ExamSchedule, ExamResult,
    AttendanceSession, AttendanceRecord,
    TimeSlot, Classroom, TimetableTemplate, ClassSchedule, 
    ClassAdjustment, DayOfWeek, SlotType, AdjustmentStatus
)

# Campus Domain
from app.domains.campus.models import (
    HostelBlock, HostelRoom, BedAllocation, HostelType, RoomType,
    GatePass, HostelComplaint, GatePassType, GatePassStatus, ComplaintStatus,
    Book, LibraryMember, DigitalResource, BookStatus, MemberType,
    BookIssue, LibraryFine, IssueStatus,
    Asset, AssetAllocation, AssetAudit, UniformAllocation, AssetCategory, AllocationStatus, UniformSize,
    Vehicle, TransportRoute, TransportAllocation, VehicleGPSLog,
    AssetMaintenance, MasterClassroom
)
# Communication Domain
from app.domains.communication.models import Circular, Notification, NotificationLog
# Auth Domain Models (moved from system)
from app.domains.auth.models import (
    AuthUser as User,  # Alias for backward compatibility
    Role,
    Permission,
    UserRole,
    RolePermission,
)

# System Domain Models
from app.domains.system.models import (
    SystemSetting,
    InstituteInfo,
    AuditLog,
    PermissionAuditLog,
    FileMetadata,
    ImportLog,
)

# Export all models
__all__ = [
    # Auth
    "User",
    "Role",
    "Permission",
    "UserRole",
    "RolePermission",
    # System
    "SystemSetting",
    "InstituteInfo",
    "AuditLog",
    "PermissionAuditLog",
    "FileMetadata",
    "ImportLog",
    # HR
    "Designation",
    "Staff",
    "Faculty",
    # Academic
    "Department",
    "Program",
    "Subject",
    "AcademicYear",
    "AcademicBatch",
    "Section",
    "PracticalBatch",
    "SubjectConfig",
    "Regulation",
    "Semester",
    "Shift",
    "Exam",
    "ExamSchedule",
    "ExamResult",
    "Question",
    "Timetable",
    "TimeSlot",
    "Classroom",
    "TimetableTemplate",
    "ClassSchedule",
    "ClassAdjustment",
    "AttendanceSession",
    "AttendanceRecord",
    "InternalExam",
    "InternalExamSchedule",
    "InternalExamResult",
    "EntranceExam",
    "EntranceExamSchedule",
    "EntranceExamResult",
    "HallTicket",
    # Student
    "Student",
    "Parent",
    "Enrollment",
    "StudentPracticalBatchAllocation",
    "Board",
    "PreviousQualification",
    "StudyGroup",
    "ReservationCategory",
    # Admission
    "Application",
    "ApplicationDocument",
    "LeadSource",
    # Finance
    "FeeConfiguration",
    "FeePayment",
    "FeeHead",
    "InstallmentPlan",
    "ScholarshipSlab",
    "PaymentGatewayConfig",
    "OnlinePayment",
    "PaymentReceipt",
    "StudentFeeInstallment",
    # Communication
    "Circular",
    "Notification",
    "NotificationLog",
    # Campus
    "HostelBlock",
    "HostelRoom",
    "BedAllocation",
    "GatePass",
    "HostelComplaint",
    "Book",
    "LibraryMember",
    "DigitalResource",
    "BookIssue",
    "LibraryFine",
    "Asset",
    "AssetAllocation",
    "AssetMaintenance",
    "AssetAudit",
    "UniformAllocation",
    "Vehicle",
    "TransportRoute",
    "TransportAllocation",
    "VehicleGPSLog",
    "MasterClassroom",
    "MaintenanceTicket",
]
