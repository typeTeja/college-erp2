"""
Student Domain Exceptions

Custom exceptions for the student domain.
"""


class StudentDomainError(Exception):
    """Base exception for student domain"""
    pass


class StudentNotFoundError(StudentDomainError):
    """Raised when a student is not found"""
    pass


class ParentNotFoundError(StudentDomainError):
    """Raised when a parent is not found"""
    pass


class EnrollmentNotFoundError(StudentDomainError):
    """Raised when an enrollment is not found"""
    pass


class DocumentNotFoundError(StudentDomainError):
    """Raised when a document is not found"""
    pass


class ODCRequestNotFoundError(StudentDomainError):
    """Raised when an ODC request is not found"""
    pass


class DuplicateEnrollmentError(StudentDomainError):
    """Raised when trying to create a duplicate enrollment"""
    pass


class InvalidDocumentError(StudentDomainError):
    """Raised when document validation fails"""
    pass
