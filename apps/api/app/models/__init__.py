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

# Academic Domain Models - Import only what exists
from app.domains.academic.models import (
    AcademicYear,
    Section,
    PracticalBatch,
    SubjectConfig,
    Regulation,
    RegulationSubject,
    RegulationSemester,
    RegulationPromotionRule,
    ProgramYear,
    AcademicBatch,
    BatchSemester,
    BatchSubject,
    StudentSectionAssignment,
    StudentLabAssignment,
    StudentPracticalBatchAllocation,
    StudentSemesterHistory,
    StudentPromotionLog,
    StudentRegulationMigration,
)

# Student Domain Models
from app.domains.student.models import (
    Student,
    Parent,
    Enrollment,
    DocumentCategory,
    StudentDocument,
    DocumentVerification,
    ODCHotel,
    ODCRequest,
    StudentODCApplication,
    ODCBilling,
    ODCPayout,
    StudentPortalAccess,
    StudentActivity,
    StudentNotification,
)

# Admission Domain Models
from app.domains.admission.models import (
    Application,
    ApplicationPayment,
    EntranceExamScore,
    ApplicationDocument,
    ApplicationActivityLog,
    AdmissionSettings,
    TentativeAdmission,
    ScholarshipCalculation,
    EntranceTestConfig,
    EntranceExamResult,
)

# Finance Domain Models
from app.domains.finance.models import (
    FeeHead,
    InstallmentPlan,
    ScholarshipSlab,
    FeeStructure,
    FeeComponent,
    FeeInstallment,
    StudentFee,
    FeePayment,
    FeeConcession,
    FeeFine,
    StudentFeeInstallment,
    PaymentGatewayConfig,
    OnlinePayment,
    PaymentReceipt,
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

# Import models from legacy models subdirectories
try:
    from app.models.program import Program
    from app.models.subject import Subject
except ImportError:
    # These might not exist yet, create placeholders
    Program = None
    Subject = None

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
    "AcademicYear",
    "Section",
    "PracticalBatch",
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
    "StudentLabAssignment",
    "StudentPracticalBatchAllocation",
    "StudentSemesterHistory",
    "StudentPromotionLog",
    "StudentRegulationMigration",
    # Student
    "Student",
    "Parent",
    "Enrollment",
    "DocumentCategory",
    "StudentDocument",
    "DocumentVerification",
    "ODCHotel",
    "ODCRequest",
    "StudentODCApplication",
    "ODCBilling",
    "ODCPayout",
    "StudentPortalAccess",
    "StudentActivity",
    "StudentNotification",
    # Admission
    "Application",
    "ApplicationPayment",
    "EntranceExamScore",
    "ApplicationDocument",
    "ApplicationActivityLog",
    "AdmissionSettings",
    "TentativeAdmission",
    "ScholarshipCalculation",
    "EntranceTestConfig",
    "EntranceExamResult",
    # Finance
    "FeeHead",
    "InstallmentPlan",
    "ScholarshipSlab",
    "FeeStructure",
    "FeeComponent",
    "FeeInstallment",
    "StudentFee",
    "FeePayment",
    "FeeConcession",
    "FeeFine",
    "StudentFeeInstallment",
    "PaymentGatewayConfig",
    "OnlinePayment",
    "PaymentReceipt",
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
    # Legacy models (if they exist)
    "Program",
    "Subject",
]
