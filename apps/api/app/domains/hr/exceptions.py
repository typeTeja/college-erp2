"""
HR Domain Exceptions

Custom exceptions for the HR domain.
"""


class HRDomainError(Exception):
    """Base exception for HR domain"""
    pass


class DesignationNotFoundError(HRDomainError):
    """Raised when a designation is not found"""
    pass


class StaffNotFoundError(HRDomainError):
    """Raised when a staff member is not found"""
    pass


class FacultyNotFoundError(HRDomainError):
    """Raised when a faculty member is not found"""
    pass


class DuplicateEmailError(HRDomainError):
    """Raised when trying to create staff/faculty with duplicate email"""
    pass


class DuplicateMobileError(HRDomainError):
    """Raised when trying to create staff with duplicate mobile"""
    pass
