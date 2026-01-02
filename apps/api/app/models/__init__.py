# Central registry for Alembic autogenerate
# Import all models here so Alembic can discover them

from .user import User
from .odc import ODCHotel, ODCRequest, StudentODCApplication
from .role import Role
from .user_role import UserRole
from .permission import Permission, RolePermission, PermissionAuditLog
from .department import Department
from .program import Program
from .program_year import ProgramYear
from .semester import Semester
from .subject import Subject
from .student import Student
from .faculty import Faculty
from .enrollment import Enrollment
from .parent import Parent
from .staff import Staff
from .operations import Shift, MaintenanceTicket
from .exam import Exam, ExamSchedule, ExamResult
from .timetable import (
    TimeSlot,
    Classroom,
    TimetableTemplate,
    ClassSchedule,
    ClassAdjustment,
)
from .fee import (
    FeeStructure,
    FeeComponent,
    FeeInstallment,
    StudentFee,
    FeePayment,
    FeeConcession,
    FeeFine,
)
from .attendance import AttendanceSession, AttendanceRecord
from .admissions import Application, ApplicationPayment, EntranceExamScore, ApplicationDocument, ApplicationActivityLog
from .library import Book, BookIssue, LibraryFine
from .hostel import HostelBlock, HostelRoom, BedAllocation, GatePass, HostelComplaint
from .lesson import LessonPlan, SyllabusTopic, QuestionBank, Question
from .inventory import Asset, AssetAllocation, AssetMaintenance, AssetAudit, UniformAllocation
from .communication import Circular, Notification, NotificationLog
from .settings import SystemSetting, AuditLog

__all__ = [
    "User",
    "Role",
    "UserRole",
    "Department",
    "Program",
    "ProgramYear",
    "Semester",
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
    "EntranceExamScore",
    "ApplicationDocument",
    "ApplicationActivityLog",
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
    "AuditLog",
]
