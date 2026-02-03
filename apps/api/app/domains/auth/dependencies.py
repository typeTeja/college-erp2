"""
Auth Domain Dependencies

FastAPI dependencies for authentication and authorization.
Provides auth guards: get_current_user, require_role, require_permission.
"""

from typing import List, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlmodel import Session, select

from app.db.session import get_session
from app.core.rbac import RBACService
from .models import AuthUser, Permission
from .security import decode_token
from .exceptions import AuthenticationError, AuthorizationError

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> AuthUser:
    """
    Get current authenticated user from JWT token
    
    Args:
        token: JWT access token from Authorization header
        session: Database session
    
    Returns:
        Authenticated AuthUser
    
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type", "access")
        
        if user_id is None:
            raise credentials_exception
        
        if token_type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type. Expected access token."
            )
        
    except JWTError:
        raise credentials_exception
    
    # Get user from database
    user = session.get(AuthUser, int(user_id))
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    return user


def get_current_active_user(
    current_user: AuthUser = Depends(get_current_user)
) -> AuthUser:
    """
    Get current active user (alias for get_current_user)
    
    Args:
        current_user: Current authenticated user
    
    Returns:
        Active AuthUser
    """
    return current_user


def get_current_superuser(
    current_user: AuthUser = Depends(get_current_user)
) -> AuthUser:
    """
    Require current user to be a superuser
    
    Args:
        current_user: Current authenticated user
    
    Returns:
        Superuser AuthUser
    
    Raises:
        HTTPException: If user is not a superuser
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Superuser required."
        )
    return current_user


def require_role(*role_names: str):
    """
    Require user to have one of the specified roles
    
    Usage:
        @router.get("/admin")
        def admin_endpoint(
            current_user: AuthUser = Depends(require_role("ADMIN", "PRINCIPAL"))
        ):
            ...
    
    Args:
        *role_names: One or more role names (user must have at least one)
    
    Returns:
        FastAPI dependency function
    """
    def dependency(current_user: AuthUser = Depends(get_current_user)) -> AuthUser:
        user_roles = [role.name for role in current_user.roles]
        
        if not any(role in user_roles for role in role_names):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required role: {', '.join(role_names)}"
            )
        
        return current_user
    
    return dependency


def require_permission(*permission_names: str):
    """
    Require user to have one of the specified permissions
    Uses RBACService for caching.
    """
    def dependency(
        current_user: AuthUser = Depends(get_current_user),
        session: Session = Depends(get_session)
    ) -> AuthUser:
        # Superusers have all permissions
        if current_user.is_superuser:
            return current_user

        # Get permissions via Cached Service
        user_permissions = RBACService.get_user_permissions(session, current_user.id)
        
        if not any(perm in user_permissions for perm in permission_names):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Required permission: {', '.join(permission_names)}"
            )
        
        return current_user
    
    return dependency


def require_any_permission(*permission_names: str):
    """
    Alias for require_permission (for clarity)
    Require user to have ANY of the specified permissions
    """
    return require_permission(*permission_names)


def require_all_permissions(*permission_names: str):
    """
    Require user to have ALL of the specified permissions
    Uses RBACService for caching.
    """
    def dependency(
        current_user: AuthUser = Depends(get_current_user),
        session: Session = Depends(get_session)
    ) -> AuthUser:
        # Superusers have all permissions
        if current_user.is_superuser:
            return current_user
            
        # Get permissions via Cached Service
        user_permissions = RBACService.get_user_permissions(session, current_user.id)
        
        if not all(perm in user_permissions for perm in permission_names):
            missing = set(permission_names) - user_permissions
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required permissions: {', '.join(missing)}"
            )
        
        return current_user
    
    return dependency
