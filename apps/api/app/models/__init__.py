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

# Admission Domain Models
from app.domains.admission.models import (
    Application,
    ApplicationDocument,
    LeadSource,
)

# Finance Domain Models
from app.domains.finance.models import (
    FeeConfiguration,
    FeePayment,
    FeeHead,
    InstallmentPlan,
    ScholarshipSlab,
    PaymentGatewayConfig,
    OnlinePayment,
    PaymentReceipt,
    StudentFeeInstallment,
)

# Communication Domain Models
from app.domains.communication.models import (
    Circular,
    Notification,
    NotificationLog,
)

# Campus Domain Models
from app.domains.campus.hostel.models import (
    HostelBlock,
    HostelRoom,
    BedAllocation,
    GatePass,
    HostelComplaint,
)

from app.domains.campus.library.models import (
    Book,
    LibraryMember,
    DigitalResource,
    BookIssue,
    LibraryFine,
)

from app.domains.campus.inventory.models import (
    Asset,
    AssetAllocation,
    AssetMaintenance,
    AssetAudit,
    UniformAllocation,
)

from app.domains.campus.transport.models import (
    Vehicle,
    TransportRoute,
    TransportAllocation,
    VehicleGPSLog,
)

from app.domains.campus.infrastructure.models import (
    MasterClassroom,
    MaintenanceTicket,
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
