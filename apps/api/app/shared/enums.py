"""
Consolidated Enums

Single source of truth for all enum definitions across the ERP system.
Organized by domain for clarity.
"""

from enum import Enum


# ----------------------------------------------------------------------
# Generic Enums
# ----------------------------------------------------------------------

class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class BloodGroup(str, Enum):
    A_POS = "A+"
    A_NEG = "A-"
    B_POS = "B+"
    B_NEG = "B-"
    AB_POS = "AB+"
    AB_NEG = "AB-"
    O_POS = "O+"
    O_NEG = "O-"


class RoomType(str, Enum):
    # Classroom/facility types
    CLASSROOM = "CLASSROOM"
    LAB = "LAB"
    SEMINAR_HALL = "SEMINAR_HALL"
    AUDITORIUM = "AUDITORIUM"
    LIBRARY = "LIBRARY"
    STAFF_ROOM = "STAFF_ROOM"
    OFFICE = "OFFICE"
    OTHER = "OTHER"
    # Hostel room types
    NON_AC = "NON_AC"
    AC = "AC"
    DELUXE = "DELUXE"


class TopicStatus(str, Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


class QuestionType(str, Enum):
    MCQ = "MCQ"
    THEORETICAL = "THEORETICAL"
    PRACTICAL = "PRACTICAL"


class TicketStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class ProgramType(str, Enum):
    UG = "UG"
    PG = "PG"
    DIPLOMA = "DIPLOMA"
    CERTIFICATE = "CERTIFICATE"
    PHD = "PHD"


class ProgramStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"


# ----------------------------------------------------------------------
# System Domain
# ----------------------------------------------------------------------

class SettingGroup(str, Enum):
    PERSONAL = "PERSONAL"
    INSTITUTE = "INSTITUTE"
    ACADEMIC = "ACADEMIC"
    INTEGRATION = "INTEGRATION"
    SECURITY = "SECURITY"


class AuditLogAction(str, Enum):
    LOGIN = "LOGIN"
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    PERMISSION_CHANGE = "PERMISSION_CHANGE"
    SETTING_CHANGE = "SETTING_CHANGE"
    SECURITY_ALERT = "SECURITY_ALERT"


class ImportRowStatus(str, Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    WARNING = "WARNING"
    DUPLICATE = "DUPLICATE"


# ----------------------------------------------------------------------
# Academic Domain
# ----------------------------------------------------------------------

class AttendanceStatus(str, Enum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    LATE = "LATE"
    ON_DUTY = "ON_DUTY"


class SessionStatus(str, Enum):
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class ExamType(str, Enum):
    MID_TERM = "MID_TERM"
    FINAL = "FINAL"
    INTERNAL = "INTERNAL"
    PRACTICAL = "PRACTICAL"
    BOTH = "BOTH"  # For subjects with both theory and practical


class ExamStatus(str, Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    COMPLETED = "COMPLETED"


class ExamResultStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    ABSENT = "ABSENT"
    DETAINED = "DETAINED"
    WITHHELD = "WITHHELD"


class DayOfWeek(str, Enum):
    MONDAY = "MONDAY"
    TUESDAY = "TUESDAY"
    WEDNESDAY = "WEDNESDAY"
    THURSDAY = "THURSDAY"
    FRIDAY = "FRIDAY"
    SATURDAY = "SATURDAY"
    SUNDAY = "SUNDAY"


class SlotType(str, Enum):
    THEORY = "THEORY"
    PRACTICAL = "PRACTICAL"
    BREAK = "BREAK"
    ASSEMBLY = "ASSEMBLY"


class AdjustmentStatus(str, Enum):
    REQUESTED = "REQUESTED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    COMPLETED = "COMPLETED"


class AcademicYearStatus(str, Enum):
    UPCOMING = "UPCOMING"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"


class SubjectType(str, Enum):
    THEORY = "THEORY"
    PRACTICAL = "PRACTICAL"
    PROJECT = "PROJECT"
    ELECTIVE = "ELECTIVE"
    AUDIT = "AUDIT"


class EvaluationType(str, Enum):
    THEORY_ONLY = "THEORY_ONLY"
    PRACTICAL_ONLY = "PRACTICAL_ONLY"
    THEORY_AND_PRACTICAL = "THEORY_AND_PRACTICAL"
    PROJECT = "PROJECT"


class PromotionRuleType(str, Enum):
    CREDIT_PERCENTAGE = "CREDIT_PERCENTAGE"
    CREDIT_COUNT = "CREDIT_COUNT"
    BACKLOG_COUNT = "BACKLOG_COUNT"


class RegulationStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"


class BatchStatus(str, Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"


class SemesterStatus(str, Enum):
    UPCOMING = "UPCOMING"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"


# ----------------------------------------------------------------------
# Student Domain
# ----------------------------------------------------------------------

class GenderPreference(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    ANY = "ANY"


class ODCStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class PayoutStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"


class BillingStatus(str, Enum):
    DRAFT = "DRAFT"
    SENT = "SENT"
    PAID = "PAID"
    CANCELLED = "CANCELLED"


class StudentStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    ON_LEAVE = "ON_LEAVE"
    WITHDRAWN = "WITHDRAWN"
    DETAINED = "DETAINED"
    SUSPENDED = "SUSPENDED"
    GRADUATED = "GRADUATED"
    ALUMNI = "ALUMNI"
    IMPORTED_PENDING_VERIFICATION = "IMPORTED_PENDING_VERIFICATION"


# ----------------------------------------------------------------------
# Admission Domain
# ----------------------------------------------------------------------

class ApplicationPaymentStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class ApplicationStatus(str, Enum):
    """Application workflow statuses"""
    # Legacy Statuses (DB Support)
    APPLIED = "APPLIED"
    
    # Enhanced Workflow Statuses
    QUICK_APPLY_SUBMITTED = "QUICK_APPLY_SUBMITTED"  # Stage 1 complete, account created
    LOGGED_IN = "LOGGED_IN"  # Student logged in but form incomplete
    FORM_IN_PROGRESS = "FORM_IN_PROGRESS"  # Student started full form
    
    # Payment Statuses
    PENDING_PAYMENT = "PENDING_PAYMENT"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    PAID = "PAID"
    
    # Application Processing Statuses
    FORM_COMPLETED = "FORM_COMPLETED"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    ADMITTED = "ADMITTED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"


class FeeMode(str, Enum):
    """Payment mode for application fee"""
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"


class DocumentType(str, Enum):
    """Types of documents that can be uploaded"""
    PHOTO = "PHOTO"
    AADHAAR = "AADHAAR"
    TENTH_MARKSHEET = "TENTH_MARKSHEET"
    TWELFTH_MARKSHEET = "TWELFTH_MARKSHEET"
    MIGRATION_CERTIFICATE = "MIGRATION_CERTIFICATE"
    TRANSFER_CERTIFICATE = "TRANSFER_CERTIFICATE"
    CASTE_CERTIFICATE = "CASTE_CERTIFICATE"
    INCOME_CERTIFICATE = "INCOME_CERTIFICATE"
    CONDUCT_CERTIFICATE = "CONDUCT_CERTIFICATE"
    BONAFIDE_CERTIFICATE = "BONAFIDE_CERTIFICATE"
    EQUIVALENCY_CERTIFICATE = "EQUIVALENCY_CERTIFICATE"
    MEDICAL_FITNESS_CERTIFICATE = "MEDICAL_FITNESS_CERTIFICATE"
    STUDENT_SIGNATURE = "STUDENT_SIGNATURE"
    PARENT_SIGNATURE = "PARENT_SIGNATURE"
    ADDRESS_PROOF = "ADDRESS_PROOF"
    SPORTS_CERTIFICATE = "SPORTS_CERTIFICATE"
    NCC_CERTIFICATE = "NCC_CERTIFICATE"
    OTHER = "OTHER"


class DocumentStatus(str, Enum):
    """Document verification status"""
    UPLOADED = "UPLOADED"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"


class ActivityType(str, Enum):
    """Types of activities that can be logged"""
    APPLICATION_CREATED = "APPLICATION_CREATED"
    PAYMENT_INITIATED = "PAYMENT_INITIATED"
    PAYMENT_SUCCESS = "PAYMENT_SUCCESS"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    OFFLINE_PAYMENT_VERIFIED = "OFFLINE_PAYMENT_VERIFIED"
    FORM_COMPLETED = "FORM_COMPLETED"
    DOCUMENT_UPLOADED = "DOCUMENT_UPLOADED"
    DOCUMENT_VERIFIED = "DOCUMENT_VERIFIED"
    DOCUMENT_REJECTED = "DOCUMENT_REJECTED"
    STATUS_CHANGED = "STATUS_CHANGED"
    ADMISSION_CONFIRMED = "ADMISSION_CONFIRMED"
    ADMISSION_REJECTED = "ADMISSION_REJECTED"
    APPLICATION_DELETED = "APPLICATION_DELETED"
    APPLICATION_RESTORED = "APPLICATION_RESTORED"
    TEST_DATA_CLEANUP = "TEST_DATA_CLEANUP"


class TentativeAdmissionStatus(str, Enum):
    """Tentative admission status"""
    PENDING_PAYMENT = "PENDING_PAYMENT"
    PAYMENT_RECEIVED = "PAYMENT_RECEIVED"
    EXPIRED = "EXPIRED"



class ScholarshipCategory(str, Enum):
    GENERAL = "GENERAL"
    SC = "SC"
    ST = "ST"
    OBC = "OBC"
    EWS = "EWS"


class Religion(str, Enum):
    """Religious affiliations"""
    HINDU = "HINDU"
    MUSLIM = "MUSLIM"
    CHRISTIAN = "CHRISTIAN"
    SIKH = "SIKH"
    BUDDHIST = "BUDDHIST"
    JAIN = "JAIN"
    PARSI = "PARSI"
    OTHER = "OTHER"
    PREFER_NOT_TO_SAY = "PREFER_NOT_TO_SAY"


class CasteCategory(str, Enum):
    """Caste categories for reservations"""
    GENERAL = "GENERAL"
    OC = "OC"  # Open Category
    BC_A = "BC_A"
    BC_B = "BC_B"
    BC_C = "BC_C"
    BC_D = "BC_D"
    BC_E = "BC_E"
    SC = "SC"  # Scheduled Caste
    ST = "ST"  # Scheduled Tribe
    EWS = "EWS"  # Economically Weaker Section


class ParentRelation(str, Enum):
    """Parent/Guardian relationship types"""
    FATHER = "FATHER"
    MOTHER = "MOTHER"
    GUARDIAN = "GUARDIAN"
    GRANDFATHER = "GRANDFATHER"
    GRANDMOTHER = "GRANDMOTHER"
    UNCLE = "UNCLE"
    AUNT = "AUNT"
    SIBLING = "SIBLING"
    OTHER = "OTHER"


class EducationLevel(str, Enum):
    """Education qualification levels"""
    SSC = "SSC"  # 10th
    INTERMEDIATE = "INTERMEDIATE"  # 10+2
    DIPLOMA = "DIPLOMA"
    DEGREE = "DEGREE"
    POST_GRADUATE = "POST_GRADUATE"


class EducationBoard(str, Enum):
    """Education boards/universities"""
    CBSE = "CBSE"
    ICSE = "ICSE"
    STATE_BOARD = "STATE_BOARD"
    IB = "IB"
    NIOS = "NIOS"
    UNIVERSITY = "UNIVERSITY"
    OTHER = "OTHER"


class ActivityLevel(str, Enum):
    """Extra-curricular activity participation level"""
    COLLEGE = "COLLEGE"
    DISTRICT = "DISTRICT"
    STATE = "STATE"
    NATIONAL = "NATIONAL"
    INTERNATIONAL = "INTERNATIONAL"


class AddressType(str, Enum):
    """Address types"""
    PRESENT = "PRESENT"
    PERMANENT = "PERMANENT"
    COMMUNICATION = "COMMUNICATION"



# ----------------------------------------------------------------------
# Finance Domain
# ----------------------------------------------------------------------

class FeeCategory(str, Enum):
    GENERAL = "GENERAL"
    MANAGEMENT = "MANAGEMENT"
    NRI = "NRI"
    SCHOLARSHIP = "SCHOLARSHIP"


class PaymentMode(str, Enum):
    ONLINE = "ONLINE"
    CASH = "CASH"
    CHEQUE = "CHEQUE"
    DD = "DD"
    UPI = "UPI"


class PaymentStatus(str, Enum):
    INITIATED = "INITIATED"
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"


class PaymentMethod(str, Enum):
    CASH = "CASH"
    BANK_TRANSFER = "BANK_TRANSFER"
    UPI = "UPI"
    CHEQUE = "CHEQUE"


# ----------------------------------------------------------------------
# Communication Domain
# ----------------------------------------------------------------------

class CircularTarget(str, Enum):
    ALL = "ALL"
    STAFF = "STAFF"
    STUDENTS = "STUDENTS"
    PARENTS = "PARENTS"
    SPECIFIC_ROLES = "SPECIFIC_ROLES"
    SPECIFIC_DEPARTMENTS = "SPECIFIC_DEPARTMENTS"


class NotificationType(str, Enum):
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"


class NotificationChannel(str, Enum):
    SMS = "SMS"
    EMAIL = "EMAIL"
    WHATSAPP = "WHATSAPP"
    PUSH = "PUSH"


# ----------------------------------------------------------------------
# Campus Domain
# ----------------------------------------------------------------------

class HostelType(str, Enum):
    BOYS = "BOYS"
    GIRLS = "GIRLS"
    STAFF = "STAFF"
    GUEST = "GUEST"


class GatePassType(str, Enum):
    LOCAL = "LOCAL"
    HOME = "HOME"
    EMERGENCY = "EMERGENCY"


class GatePassStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    OUT = "OUT"
    RETURNED = "RETURNED"
    EXPIRED = "EXPIRED"


class ComplaintStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class AssetCategory(str, Enum):
    UNIFORM = "UNIFORM"
    IT_EQUIPMENT = "IT_EQUIPMENT"
    LAB_EQUIPMENT = "LAB_EQUIPMENT"
    FURNITURE = "FURNITURE"
    STATIONERY = "STATIONERY"
    OTHERS = "OTHERS"


class AllocationStatus(str, Enum):
    ISSUED = "ISSUED"
    RETURNED = "RETURNED"
    DAMAGED = "DAMAGED"
    LOST = "LOST"


class UniformSize(str, Enum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"
    CUSTOM = "CUSTOM"


class IssueStatus(str, Enum):
    ISSUED = "ISSUED"
    RETURNED = "RETURNED"
    OVERDUE = "OVERDUE"
    LOST = "LOST"


class BookStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    ISSUED = "ISSUED"
    LOST = "LOST"
    DAMAGED = "DAMAGED"


class MemberType(str, Enum):
    STUDENT = "STUDENT"
    FACULTY = "FACULTY"
    STAFF = "STAFF"


# ----------------------------------------------------------------------
# Other / Uncategorized
# ----------------------------------------------------------------------

class CreatedFrom(str, Enum):
    MANUAL = "manual"
    ADMISSION = "admission"
    BULK_UPLOAD = "bulk_upload"


class DifficultyLevel(str, Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class TicketPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

