"""
Communication Domain Exceptions

Custom exceptions for the communication domain.
"""


class CommunicationDomainError(Exception):
    """Base exception for communication domain"""
    pass


class CircularNotFoundError(CommunicationDomainError):
    """Raised when a circular is not found"""
    pass


class NotificationNotFoundError(CommunicationDomainError):
    """Raised when a notification is not found"""
    pass


class EmailSendError(CommunicationDomainError):
    """Raised when email sending fails"""
    pass


class SMSSendError(CommunicationDomainError):
    """Raised when SMS sending fails"""
    pass


class InvalidRecipientError(CommunicationDomainError):
    """Raised when recipient is invalid"""
    pass
