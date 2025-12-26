"""Password setup and reset service"""
import secrets
from datetime import datetime, timedelta
from typing import Optional
from sqlmodel import Session, select
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class PasswordToken:
    """In-memory token storage (use Redis in production)"""
    _tokens = {}  # {token: {user_id, email, expires_at}}
    
    @classmethod
    def create_token(cls, user_id: int, email: str, expires_hours: int = 24) -> str:
        """Create a password setup/reset token"""
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(hours=expires_hours)
        
        cls._tokens[token] = {
            "user_id": user_id,
            "email": email,
            "expires_at": expires_at
        }
        
        return token
    
    @classmethod
    def verify_token(cls, token: str) -> Optional[dict]:
        """Verify and return token data if valid"""
        token_data = cls._tokens.get(token)
        
        if not token_data:
            return None
        
        if datetime.utcnow() > token_data["expires_at"]:
            # Token expired
            del cls._tokens[token]
            return None
        
        return token_data
    
    @classmethod
    def invalidate_token(cls, token: str):
        """Invalidate a token after use"""
        if token in cls._tokens:
            del cls._tokens[token]

def hash_password(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)

def generate_password_setup_link(base_url: str, token: str) -> str:
    """Generate password setup link"""
    return f"{base_url}/auth/setup-password?token={token}"
