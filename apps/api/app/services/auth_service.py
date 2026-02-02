from typing import Optional
from datetime import datetime, timedelta
from sqlmodel import Session, select, or_
from app.models import User
from app.models import Role
from app.models import UserRole
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from app.schemas.auth import UserCreate, UserUpdate, LoginRequest
import secrets

class AuthService:
    """Authentication service layer"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password"""
        # Allow login validation by username OR email
        statement = select(User).where(
            or_(
                User.username == username,
                User.email == username
            )
        )
        user = self.session.exec(statement).first()
        
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            return None
        
        # Update last login
        user.last_login = datetime.utcnow()
        self.session.add(user)
        self.session.commit()
        
        return user
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user"""
        # Check if username exists
        existing = self.session.exec(
            select(User).where(User.username == user_data.username)
        ).first()
        if existing:
            raise ValueError("Username already exists")
        
        # Check if email exists
        existing = self.session.exec(
            select(User).where(User.email == user_data.email)
        ).first()
        if existing:
            raise ValueError("Email already exists")
        
        # Create user
        user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=get_password_hash(user_data.password)
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        
        # Assign roles
        if user_data.role_ids:
            for role_id in user_data.role_ids:
                user_role = UserRole(user_id=user.id, role_id=role_id)
                self.session.add(user_role)
            self.session.commit()
        
        return user
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update user"""
        user = self.session.get(User, user_id)
        if not user:
            return None
        
        update_data = user_data.model_dump(exclude_unset=True)
        
        # Handle role updates separately
        role_ids = update_data.pop('role_ids', None)
        
        for field, value in update_data.items():
            setattr(user, field, value)
        
        user.updated_at = datetime.utcnow()
        
        # Update roles if provided
        if role_ids is not None:
            # Remove existing roles
            self.session.exec(
                select(UserRole).where(UserRole.user_id == user_id)
            ).all()
            for ur in self.session.exec(select(UserRole).where(UserRole.user_id == user_id)).all():
                self.session.delete(ur)
            
            # Add new roles
            for role_id in role_ids:
                user_role = UserRole(user_id=user.id, role_id=role_id)
                self.session.add(user_role)
        
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.session.get(User, user_id)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()
    
    def create_password_reset_token(self, email: str) -> Optional[str]:
        """Create password reset token"""
        user = self.get_user_by_email(email)
        if not user:
            return None
        
        token = secrets.token_urlsafe(32)
        user.password_reset_token = token
        user.password_reset_expires = datetime.utcnow() + timedelta(hours=24)
        
        self.session.add(user)
        self.session.commit()
        
        return token
    
    def reset_password(self, token: str, new_password: str) -> bool:
        """Reset password with token"""
        statement = select(User).where(User.password_reset_token == token)
        user = self.session.exec(statement).first()
        
        if not user:
            return False
        
        if not user.password_reset_expires or user.password_reset_expires < datetime.utcnow():
            return False
        
        user.hashed_password = get_password_hash(new_password)
        user.password_reset_token = None
        user.password_reset_expires = None
        user.updated_at = datetime.utcnow()
        
        self.session.add(user)
        self.session.commit()
        
        return True
    
    def change_password(self, user_id: int, current_password: str, new_password: str) -> bool:
        """Change password for authenticated user"""
        user = self.session.get(User, user_id)
        if not user:
            return False
        
        if not verify_password(current_password, user.hashed_password):
            return False
        
        user.hashed_password = get_password_hash(new_password)
        user.updated_at = datetime.utcnow()
        
        self.session.add(user)
        self.session.commit()
        
        return True
    
    def get_user_roles(self, user_id: int) -> list[str]:
        """Get user role names"""
        user = self.session.get(User, user_id)
        if not user:
            return []
        
        # Get roles through link table
        statement = (
            select(Role)
            .join(UserRole, UserRole.role_id == Role.id)
            .where(UserRole.user_id == user_id)
        )
        roles = self.session.exec(statement).all()
        
        return [role.name for role in roles]
