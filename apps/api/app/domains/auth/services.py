"""
Auth Domain Services

Business logic for authentication and authorization.
ONLY Auth domain can assign roles and permissions.
"""

from typing import Optional, List
from sqlmodel import Session, select
from datetime import datetime, timedelta
import secrets

from .models import AuthUser, Role, Permission, UserRole, RolePermission
from .security import verify_password, get_password_hash, create_access_token, create_refresh_token
from .exceptions import (
    AuthenticationError,
    UserNotFoundError,
    InvalidCredentialsError,
    InactiveUserError,
    PasswordResetError
)


class AuthService:
    """
    Authentication service - Auth Domain
    
    Responsibilities:
    - Authentication (login, token management)
    - Password management (reset, change)
    - Role assignment (ONLY Auth can do this)
    - Permission assignment (ONLY Auth can do this)
    
    Does NOT handle:
    - User creation (happens in business domains: Admission, HR, Admin)
    - Business logic (student, faculty, fee, exam, etc.)
    """
    
    def __init__(self, session: Session):
        self.session = session
    
    # ==================================================================
    # Authentication
    # ==================================================================
    
    def authenticate(self, email: str, password: str) -> Optional[AuthUser]:
        """
        Authenticate user by email and password
        
        Args:
            email: User email
            password: Plain text password
        
        Returns:
            AuthUser if authentication successful, None otherwise
        
        Raises:
            InvalidCredentialsError: If credentials are incorrect
            InactiveUserError: If user account is inactive
        """
        user = self.session.exec(
            select(AuthUser).where(AuthUser.email == email)
        ).first()
        
        if not user:
            raise InvalidCredentialsError("Incorrect email or password")
        
        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Incorrect email or password")
        
        if not user.is_active:
            raise InactiveUserError("User account is inactive")
        
        # Update last login
        user.last_login = datetime.utcnow()
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[AuthUser]:
        """Get user by ID"""
        return self.session.get(AuthUser, user_id)
    
    def get_user_by_email(self, email: str) -> Optional[AuthUser]:
        """Get user by email"""
        return self.session.exec(
            select(AuthUser).where(AuthUser.email == email)
        ).first()
    
    # ==================================================================
    # Password Management
    # ==================================================================
    
    def create_password_reset_token(self, email: str) -> Optional[str]:
        """
        Create password reset token
        
        Args:
            email: User email
        
        Returns:
            Reset token if user found, None otherwise
        """
        user = self.get_user_by_email(email)
        if not user:
            # Don't reveal if user exists
            return None
        
        token = secrets.token_urlsafe(32)
        user.password_reset_token = token
        user.password_reset_expires = datetime.utcnow() + timedelta(hours=24)
        
        self.session.add(user)
        self.session.commit()
        
        return token
    
    def reset_password(self, token: str, new_password: str) -> bool:
        """
        Reset password with token
        
        Args:
            token: Password reset token
            new_password: New password
        
        Returns:
            True if successful, False otherwise
        
        Raises:
            PasswordResetError: If token is invalid or expired
        """
        user = self.session.exec(
            select(AuthUser).where(AuthUser.password_reset_token == token)
        ).first()
        
        if not user:
            raise PasswordResetError("Invalid or expired reset token")
        
        if not user.password_reset_expires or user.password_reset_expires < datetime.utcnow():
            raise PasswordResetError("Reset token has expired")
        
        user.hashed_password = get_password_hash(new_password)
        user.password_reset_token = None
        user.password_reset_expires = None
        user.updated_at = datetime.utcnow()
        
        self.session.add(user)
        self.session.commit()
        
        return True
    
    def change_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        """
        Change password for authenticated user
        
        Args:
            user_id: User ID
            current_password: Current password
            new_password: New password
        
        Returns:
            True if successful
        
        Raises:
            UserNotFoundError: If user not found
            InvalidCredentialsError: If current password is incorrect
        """
        user = self.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")
        
        if not verify_password(current_password, user.hashed_password):
            raise InvalidCredentialsError("Current password is incorrect")
        
        user.hashed_password = get_password_hash(new_password)
        user.updated_at = datetime.utcnow()
        
        self.session.add(user)
        self.session.commit()
        
        return True
    
    # ==================================================================
    # Role & Permission Management (Auth Domain Write Authority)
    # ==================================================================
    
    def assign_role(self, user_id: int, role_id: int) -> None:
        """
        Assign role to user
        
        ONLY Auth domain can assign roles.
        
        Args:
            user_id: User ID
            role_id: Role ID
        """
        # Check if already assigned
        existing = self.session.exec(
            select(UserRole).where(
                UserRole.user_id == user_id,
                UserRole.role_id == role_id
            )
        ).first()
        
        if existing:
            return  # Already assigned
        
        user_role = UserRole(user_id=user_id, role_id=role_id)
        self.session.add(user_role)
        self.session.commit()
    
    def remove_role(self, user_id: int, role_id: int) -> None:
        """
        Remove role from user
        
        ONLY Auth domain can remove roles.
        
        Args:
            user_id: User ID
            role_id: Role ID
        """
        user_role = self.session.exec(
            select(UserRole).where(
                UserRole.user_id == user_id,
                UserRole.role_id == role_id
            )
        ).first()
        
        if user_role:
            self.session.delete(user_role)
            self.session.commit()
    
    def assign_permission(self, role_id: int, permission_id: int) -> None:
        """
        Assign permission to role
        
        ONLY Auth domain can assign permissions.
        
        Args:
            role_id: Role ID
            permission_id: Permission ID
        """
        # Check if already assigned
        existing = self.session.exec(
            select(RolePermission).where(
                RolePermission.role_id == role_id,
                RolePermission.permission_id == permission_id
            )
        ).first()
        
        if existing:
            return  # Already assigned
        
        role_perm = RolePermission(role_id=role_id, permission_id=permission_id)
        self.session.add(role_perm)
        self.session.commit()
    
    def remove_permission(self, role_id: int, permission_id: int) -> None:
        """
        Remove permission from role
        
        ONLY Auth domain can remove permissions.
        
        Args:
            role_id: Role ID
            permission_id: Permission ID
        """
        role_perm = self.session.exec(
            select(RolePermission).where(
                RolePermission.role_id == role_id,
                RolePermission.permission_id == permission_id
            )
        ).first()
        
        if role_perm:
            self.session.delete(role_perm)
            self.session.commit()
    
    def get_user_roles(self, user_id: int) -> List[str]:
        """Get user role names"""
        user = self.get_user_by_id(user_id)
        if not user:
            return []
        
        return [role.name for role in user.roles]
    
    def get_user_permissions(self, user_id: int) -> List[str]:
        """Get all permissions for user (via roles)"""
        user = self.get_user_by_id(user_id)
        if not user:
            return []
        
        permissions = set()
        for role in user.roles:
            for perm in role.permissions:
                permissions.add(perm.name)
        
        return list(permissions)
