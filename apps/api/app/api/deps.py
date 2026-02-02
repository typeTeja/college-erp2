from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlmodel import Session, select

from app.core import security
from app.config.settings import settings
from app.db.session import get_session
from app.models.user import User
from app.models.role import Role
from app.models.student import Student
from app.schemas.auth import TokenPayload

# OAuth2 scheme for Swagger UI auth
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError) as e:
        print(f"DEBUG AUTH: JWT Validation Failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = session.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user

def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    # Check is_superuser field or role
    if current_user.is_superuser:
        return current_user
        
    is_admin_role = any(role.name in ["SUPER_ADMIN", "ADMIN"] for role in current_user.roles)
    if not is_admin_role:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user

def get_current_active_student(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> Student:
    """Get the student record associated with the current user"""
    # STRICT CHECK: User must have STUDENT role
    is_student_role = any(role.name == "STUDENT" for role in current_user.roles)
    if not is_student_role:
        # Check if they are just an applicant
        is_applicant = any(role.name == "APPLICANT" for role in current_user.roles)
        if is_applicant:
             raise HTTPException(
                status_code=403, 
                detail="Admission not confirmed. Please complete the admission process to access this feature."
            )
        
        # Fallback for other roles
        raise HTTPException(
            status_code=403,
            detail="User does not have STUDENT privileges"
        )
        
    statement = select(Student).where(Student.user_id == current_user.id)
    student = session.exec(statement).first()
    
    if not student:
        raise HTTPException(
            status_code=404, 
            detail="Student profile not found for this user"
        )
    return student
