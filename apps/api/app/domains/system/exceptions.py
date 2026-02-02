"""
System Domain Exceptions

Custom exceptions for the system domain.
"""


class SystemDomainError(Exception):
    """Base exception for system domain"""
    pass


class UserNotFoundError(SystemDomainError):
    """Raised when a user is not found"""
    pass


class RoleNotFoundError(SystemDomainError):
    """Raised when a role is not found"""
    pass


class PermissionNotFoundError(SystemDomainError):
    """Raised when a permission is not found"""
    pass


class PermissionDeniedError(SystemDomainError):
    """Raised when user lacks required permissions"""
    pass


class InvalidCredentialsError(SystemDomainError):
    """Raised when login credentials are invalid"""
    pass


class UserAlreadyExistsError(SystemDomainError):
    """Raised when trying to create a user that already exists"""
    pass


class SettingNotFoundError(SystemDomainError):
    """Raised when a system setting is not found"""
    pass


class FileNotFoundError(SystemDomainError):
    """Raised when a file is not found"""
    pass


class ImportError(SystemDomainError):
    """Raised when data import fails"""
    pass
