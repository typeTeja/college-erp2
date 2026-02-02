"""
Auth Domain Exceptions

Custom exceptions for authentication and authorization.
"""


class AuthDomainError(Exception):
    """Base exception for auth domain"""
    pass


class AuthenticationError(AuthDomainError):
    """Raised when authentication fails"""
    pass


class AuthorizationError(AuthDomainError):
    """Raised when user lacks required permissions"""
    pass


class UserNotFoundError(AuthDomainError):
    """Raised when user is not found"""
    pass


class InvalidTokenError(AuthDomainError):
    """Raised when JWT token is invalid or expired"""
    pass


class PasswordResetError(AuthDomainError):
    """Raised when password reset fails"""
    pass


class InactiveUserError(AuthDomainError):
    """Raised when user account is inactive"""
    pass


class InvalidCredentialsError(AuthDomainError):
    """Raised when login credentials are incorrect"""
    pass
