"""
Auth Domain Router

API endpoints for authentication.
NO /register endpoint - user creation happens in business domains.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from datetime import timedelta

from app.db.session import get_session
from .schemas import (
    LoginRequest,
    Token,
    PasswordResetRequest,
    PasswordResetConfirm,
    PasswordChange,
    AuthUserInfo,
    RefreshTokenRequest
)
from .services import AuthService
from .security import create_access_token, create_refresh_token, decode_token
from .dependencies import get_current_user
from app.core.rbac import RBACService
from .models import AuthUser
from .exceptions import (
    InvalidCredentialsError,
    InactiveUserError,
    PasswordResetError,
    InvalidTokenError
)

router = APIRouter()


# ======================================================================
# Authentication Endpoints
# ======================================================================

@router.post("/login", response_model=Token)
def login(
    login_data: LoginRequest,
    session: Session = Depends(get_session)
):
    """
    Login endpoint - returns JWT tokens
    
    Args:
        login_data: Email and password
        session: Database session
    
    Returns:
        Access token, refresh token, and user info
    """
    service = AuthService(session)
    
    try:
        user = service.authenticate(login_data.email, login_data.password)
    except (InvalidCredentialsError, InactiveUserError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    
    # Create tokens
    access_token = create_access_token(
        user.id,
        expires_delta=timedelta(minutes=30)
    )
    refresh_token = create_refresh_token(user.id)
    
    # Get user roles
    user_roles = [role.name for role in user.roles]
    user_permissions = list(RBACService.get_user_permissions(session, user.id))
    
    # Create user info
    user_info = AuthUserInfo(
        id=user.id,
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        roles=user_roles,
        permissions=user_permissions
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user_info
    )


@router.post("/refresh", response_model=Token)
def refresh_token(
    refresh_data: RefreshTokenRequest,
    session: Session = Depends(get_session)
):
    """
    Refresh access token using refresh token
    
    Args:
        refresh_data: Refresh token
        session: Database session
    
    Returns:
        New access token and refresh token
    """
    try:
        payload = decode_token(refresh_data.refresh_token)
        token_type = payload.get("type")
        
        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        user_id = int(payload.get("sub"))
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Get user
    service = AuthService(session)
    user = service.get_user_by_id(user_id)
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Create new tokens
    access_token = create_access_token(
        user.id,
        expires_delta=timedelta(minutes=30)
    )
    new_refresh_token = create_refresh_token(user.id)
    
    # Get user roles
    user_roles = [role.name for role in user.roles]
    
    # Create user info
    user_info = AuthUserInfo(
        id=user.id,
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        roles=user_roles,
        permissions=user_permissions
    )
    
    return Token(
        access_token=access_token,
        refresh_token=new_refresh_token,
        user=user_info
    )


@router.get("/me", response_model=AuthUserInfo)
def get_current_user_info(
    current_user: AuthUser = Depends(get_current_user)
):
    """
    Get current user info
    
    Args:
        current_user: Current authenticated user
    
    Returns:
        User info
    """
    user_roles = [role.name for role in current_user.roles]
    
    # Use standard access but we need session for RBACService
    from app.db.session import get_session
    session = next(get_session())
    user_permissions = list(RBACService.get_user_permissions(session, current_user.id))
    
    return AuthUserInfo(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
        roles=user_roles,
        permissions=user_permissions
    )


# ======================================================================
# Password Management Endpoints
# ======================================================================

@router.post("/password-reset/request")
def request_password_reset(
    data: PasswordResetRequest,
    session: Session = Depends(get_session)
):
    """
    Request password reset - sends email with token
    
    Args:
        data: Email address
        session: Database session
    
    Returns:
        Success message
    
    Note:
        Always returns success to prevent email enumeration
    """
    service = AuthService(session)
    token = service.create_password_reset_token(data.email)
    
    # TODO: Send email with token via communication domain
    # For now, just return success (in production, send email)
    
    return {
        "message": "If the email exists, a password reset link has been sent",
        "token": token  # TODO: Remove in production, only for development
    }


@router.post("/password-reset/confirm")
def confirm_password_reset(
    data: PasswordResetConfirm,
    session: Session = Depends(get_session)
):
    """
    Confirm password reset with token
    
    Args:
        data: Reset token and new password
        session: Database session
    
    Returns:
        Success message
    """
    service = AuthService(session)
    
    try:
        service.reset_password(data.token, data.new_password)
    except PasswordResetError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    return {"message": "Password reset successful"}


@router.post("/password-change")
def change_password(
    data: PasswordChange,
    current_user: AuthUser = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Change password for authenticated user
    
    Args:
        data: Current and new password
        current_user: Current authenticated user
        session: Database session
    
    Returns:
        Success message
    """
    service = AuthService(session)
    
    try:
        service.change_password(
            current_user.id,
            data.current_password,
            data.new_password
        )
    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    return {"message": "Password changed successfully"}
