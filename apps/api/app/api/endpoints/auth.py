from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordRequestForm

from app.api import deps
from app.core import security
from app.config.settings import settings
from app.db.session import get_session
from app.models.user import User
from app.models.role import Role
# from app.models.user_role import UserRole
from app.schemas.auth import Token, UserCreate, LoginRequest, UserResponse as UserRead

router = APIRouter()

@router.post("/login", response_model=Token)
def login(
    login_data: LoginRequest,
    session: Session = Depends(get_session)
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = session.exec(
        select(User).where(User.email == login_data.email)
    ).first()
    
    if not user or not security.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Format roles for response
    user_roles = [role.name for role in user.roles]
    # Create simple response user object due to circular dependency in types if not careful
    user_read = UserRead(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        username=user.username,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        roles=user_roles
    )

    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "refresh_token": security.create_refresh_token(user.id),
        "token_type": "bearer",
        "user": user_read
    }

@router.post("/register", response_model=UserRead)
def register(
    user_in: UserCreate,
    session: Session = Depends(get_session)
) -> Any:
    """
    Create new user without the need to be logged in
    """
    user = session.exec(
        select(User).where(User.email == user_in.email)
    ).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
        
    # Create roles if they don't exist
    db_roles = []
    for role_name in user_in.roles:
        role = session.exec(select(Role).where(Role.name == role_name)).first()
        if not role:
            role = Role(name=role_name)
            session.add(role)
        db_roles.append(role)
        
    user = User(
        email=user_in.email,
        hashed_password=security.get_password_hash(user_in.password),
        full_name=user_in.full_name,
        username=user_in.username,
        is_active=user_in.is_active,
        roles=db_roles
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    
    user_roles = [role.name for role in user.roles]
    return UserRead(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        username=user.username,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        roles=user_roles
    )
