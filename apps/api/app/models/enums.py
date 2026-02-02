from enum import Enum

# --- Generic Enums ---
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

# --- Student Enums ---
class ScholarshipCategory(str, Enum):
    GENERAL = "GENERAL"
    SC = "SC"
    ST = "ST"
    OBC = "OBC"
    EWS = "EWS"

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

# --- Academic Enums ---
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

class ExamType(str, Enum):
    INTERNAL = "INTERNAL"
    EXTERNAL = "EXTERNAL"
    BOTH = "BOTH"

# --- Infrastructure Enums ---
class RoomType(str, Enum):
    CLASSROOM = "CLASSROOM"
    LAB = "LAB"
    SEMINAR_HALL = "SEMINAR_HALL"
    AUDITORIUM = "AUDITORIUM"
    LIBRARY = "LIBRARY"
    STAFF_ROOM = "STAFF_ROOM"
    OFFICE = "OFFICE"
    OTHER = "OTHER"

# --- Metadata Enums ---
class CreatedFrom(str, Enum):
    MANUAL = "manual"
    ADMISSION = "admission"
    BULK_UPLOAD = "bulk_upload"

