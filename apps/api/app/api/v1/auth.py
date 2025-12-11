from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.db.session import get_session
from app.services.auth_service import AuthService
from app.schemas.auth import (
    LoginResponse,
    UserCreate,
    UserResponse,
    UserUpdate,
    PasswordResetRequest,
    PasswordResetConfirm,
    PasswordChange,
    Token
)
from app.core.security import create_access_token, create_refresh_token
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    """Login with username and password"""
    auth_service = AuthService(session)
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create tokens
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)
    
    # Get user roles
    roles = auth_service.get_user_roles(user.id)
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            roles=roles
        )
    )

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    """Register a new user"""
    auth_service = AuthService(session)
    
    try:
        user = auth_service.create_user(user_data)
        roles = auth_service.get_user_roles(user.id)
        
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            roles=roles
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get current user information"""
    auth_service = AuthService(session)
    roles = auth_service.get_user_roles(current_user.id)
    
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
        roles=roles
    )

@router.put("/me", response_model=UserResponse)
def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update current user information"""
    auth_service = AuthService(session)
    user = auth_service.update_user(current_user.id, user_data)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    roles = auth_service.get_user_roles(user.id)
    
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        roles=roles
    )

@router.post("/password-reset/request")
def request_password_reset(
    data: PasswordResetRequest,
    session: Session = Depends(get_session)
):
    """Request password reset token"""
    auth_service = AuthService(session)
    token = auth_service.create_password_reset_token(data.email)
    
    # Always return success to prevent email enumeration
    return {"message": "If the email exists, a password reset link has been sent"}

@router.post("/password-reset/confirm")
def confirm_password_reset(
    data: PasswordResetConfirm,
    session: Session = Depends(get_session)
):
    """Confirm password reset with token"""
    auth_service = AuthService(session)
    success = auth_service.reset_password(data.token, data.new_password)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    return {"message": "Password reset successful"}

@router.post("/password/change")
def change_password(
    data: PasswordChange,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Change password for authenticated user"""
    auth_service = AuthService(session)
    success = auth_service.change_password(
        current_user.id,
        data.current_password,
        data.new_password
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    return {"message": "Password changed successfully"}
