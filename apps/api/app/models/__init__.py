# Central registry for Alembic autogenerate
# Import all models here so Alembic can discover them

from .user import User
from .odc import ODCHotel, ODCRequest, StudentODCApplication
from .role import Role
from .user_role import UserRole
from .department import Department
from .program import Program
from .program_year import ProgramYear
from .semester import Semester
from .subject import Subject
from .student import Student
from .faculty import Faculty
from .enrollment import Enrollment
from .parent import Parent
from .import_log import ImportLog

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
    "Faculty",
    "Enrollment",
    "ODCHotel",
    "ODCRequest",
    "StudentODCApplication",
    "Parent",
    "ImportLog",
]
