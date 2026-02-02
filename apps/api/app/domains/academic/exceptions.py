"""
Academic Domain Exceptions

Custom exceptions for the academic domain.
"""


class AcademicDomainError(Exception):
    """Base exception for academic domain"""
    pass


class AcademicYearNotFoundError(AcademicDomainError):
    """Raised when an academic year is not found"""
    pass


class BatchNotFoundError(AcademicDomainError):
    """Raised when a batch is not found"""
    pass


class RegulationNotFoundError(AcademicDomainError):
    """Raised when a regulation is not found"""
    pass


class SectionNotFoundError(AcademicDomainError):
    """Raised when a section is not found"""
    pass


class ExamNotFoundError(AcademicDomainError):
    """Raised when an exam is not found"""
    pass


class AttendanceNotFoundError(AcademicDomainError):
    """Raised when attendance record is not found"""
    pass


class TimetableNotFoundError(AcademicDomainError):
    """Raised when timetable is not found"""
    pass


class HallTicketNotFoundError(AcademicDomainError):
    """Raised when hall ticket is not found"""
    pass


class RegulationLockedError(AcademicDomainError):
    """Raised when trying to modify a locked regulation"""
    pass


class BatchAlreadyExistsError(AcademicDomainError):
    """Raised when trying to create a duplicate batch"""
    pass


class InvalidPromotionError(AcademicDomainError):
    """Raised when student promotion is invalid"""
    pass
