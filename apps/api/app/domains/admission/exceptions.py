"""
Admission Domain Exceptions

Custom exceptions for the admission domain.
"""


class AdmissionDomainError(Exception):
    """Base exception for admission domain"""
    pass


class ApplicationNotFoundError(AdmissionDomainError):
    """Raised when an application is not found"""
    pass


class InvalidApplicationStatusError(AdmissionDomainError):
    """Raised when application status transition is invalid"""
    pass


class DuplicateApplicationError(AdmissionDomainError):
    """Raised when trying to create a duplicate application"""
    pass


class MeritListNotFoundError(AdmissionDomainError):
    """Raised when merit list is not found"""
    pass


class EntranceExamNotFoundError(AdmissionDomainError):
    """Raised when entrance exam is not found"""
    pass


class AdmissionClosedError(AdmissionDomainError):
    """Raised when trying to apply after admission deadline"""
    pass
