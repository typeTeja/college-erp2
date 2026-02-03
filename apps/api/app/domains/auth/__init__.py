"""
Auth Domain

Authentication and Authorization domain following DDD principles.

Key principles:
- AuthUser model (not generic User) - table name remains 'users'
- No public registration - user creation happens in business domains
- Action-based permissions (e.g., EXAM_MARK_ENTRY)
- Security utilities in auth domain (JWT, password hashing)
- Strict domain boundaries - only Auth assigns roles/permissions
"""

from .models import AuthUser, Role, Permission, UserRole, RolePermission
from .schemas import (
    LoginRequest,
    Token,
    PasswordResetRequest,
    PasswordResetConfirm,
    PasswordChange,
    AuthUserInfo,
    RoleRead,
    PermissionRead
)
from .services import AuthService

from .exceptions import (
    AuthDomainError,
    AuthenticationError,
    AuthorizationError,
    UserNotFoundError,
    InvalidTokenError,
    PasswordResetError
)

__all__ = [
    # Models
    "AuthUser",
    "Role",
    "Permission",
    "UserRole",
    "RolePermission",
    # Schemas
    "LoginRequest",
    "Token",
    "PasswordResetRequest",
    "PasswordResetConfirm",
    "PasswordChange",
    "AuthUserInfo",
    "RoleRead",
    "PermissionRead",
    # Services
    "AuthService",
    # Dependencies

    # Exceptions
    "AuthDomainError",
    "AuthenticationError",
    "AuthorizationError",
    "UserNotFoundError",
    "InvalidTokenError",
    "PasswordResetError",
]
