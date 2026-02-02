# Central registry for Alembic autogenerate
# Import all models here so Alembic can discover them

from .user import User
from .role import Role
from .user_role import UserRole
from .permission import Permission, RolePermission, PermissionAuditLog
from .department import Department
from .program import Program
from .subject import Subject
# HR Domain
from app.domains.hr.models import Staff, Faculty, Designation
# Student Domain
from app.domains.student.models import (
    Student, Parent, Enrollment,
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
# System Domain
from app.domains.system.models import SystemSetting, AuditLog as SettingsAuditLog, InstituteInfo, FileMetadata, ImportLog

__all__ = [
    "User",
    "Role",
    "UserRole",
    "Department",
    "Program",
    "Subject",
    "Student",
    "Parent",
    "Faculty",
    "Staff",
    "Shift",
    "MaintenanceTicket",
    "Exam",
    "ExamSchedule",
    "ExamResult",
    "Enrollment",
    "ODCHotel",
    "ODCRequest",
    "StudentODCApplication",
    "TimeSlot",
    "Classroom",
    "TimetableTemplate",
    "ClassSchedule",
    "ClassAdjustment",
    "FeeStructure",
    "FeeComponent",
    "FeeInstallment",
    "StudentFee",
    "FeePayment",
    "FeeConcession",
    "FeeFine",
    "Application",
    "ApplicationPayment",
    "ApplicationDocument",
    "ApplicationActivityLog",
    "AdmissionSettings",
    "Book",
    "BookIssue",
    "LibraryFine",
    "HostelBlock",
    "HostelRoom",
    "BedAllocation",
    "GatePass",
    "HostelComplaint",
    "Permission",
    "RolePermission",
    "PermissionAuditLog",
    "LessonPlan",
    "SyllabusTopic",
    "QuestionBank",
    "Question",
    "Asset",
    "AssetAllocation",
    "AssetMaintenance",
    "AssetAudit",
    "UniformAllocation",
    "Circular",
    "Notification",
    "NotificationLog",
    "SystemSetting",
    "SettingsAuditLog",
    "AuditLog",
    "InstituteInfo",
    "AttendanceSession",
    "AttendanceRecord",
    "AcademicYear",
    "AcademicBatch",
    "Section",
    "PracticalBatch",
    "SubjectConfig",
    "FeeHead",
    "InstallmentPlan",
    "ScholarshipSlab",
    "PaymentGatewayConfig",
    "OnlinePayment",
    "PaymentReceipt",
    "StudentFeeInstallment",
    "Board",
    "PreviousQualification",
    "StudyGroup",
    "ReservationCategory",
    "StudentPracticalBatchAllocation",
    "LeadSource",
    "Designation",
    "MasterClassroom",
    "PlacementCompany",
    "EmailTemplate",
    "SMSTemplate",
    "FileMetadata",
    "ImportLog",
    "EntranceTestConfig",
    "EntranceExamResult",
    "TentativeAdmission",
    "ScholarshipCalculation"
]
