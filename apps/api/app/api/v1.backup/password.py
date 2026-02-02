"""Password setup and reset endpoints"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session, select
from pydantic import BaseModel, EmailStr
from app.db.session import get_session
from app.models import User
from app.services.password_service import (
    PasswordToken, hash_password, verify_password, generate_password_setup_link
)
from app.services.email_service import email_service

router = APIRouter()

class PasswordSetupRequest(BaseModel):
    token: str
    password: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

@router.post("/setup-password")
async def setup_password(
    data: PasswordSetupRequest,
    session: Session = Depends(get_session)
):
    """
    Set up password for a new user account
    
    This endpoint is used after admission confirmation
    """
    # Verify token
    token_data = PasswordToken.verify_token(data.token)
    if not token_data:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    # Get user
    user = session.get(User, token_data["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Validate password
    if len(data.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    
    # Update password and activate account
    user.hashed_password = hash_password(data.password)
    user.is_active = True
    
    session.add(user)
    session.commit()
    
    # Invalidate token
    PasswordToken.invalidate_token(data.token)
    
    return {
        "message": "Password set successfully. You can now login.",
        "email": user.email
    }

@router.post("/request-password-reset")
async def request_password_reset(
    data: PasswordResetRequest,
    request: Request,
    session: Session = Depends(get_session)
):
    """Request a password reset link"""
    # Find user
    statement = select(User).where(User.email == data.email)
    user = session.exec(statement).first()
    
    if not user:
        # Don't reveal if email exists
        return {"message": "If the email exists, a reset link has been sent"}
    
    # Generate token
    token = PasswordToken.create_token(user.id, user.email, expires_hours=2)
    
    # Generate reset link using PORTAL_BASE_URL (HTTPS-aware)
    from app.config.settings import settings
    reset_link = f"{settings.PORTAL_BASE_URL}/auth/reset-password?token={token}"
    
    # Send email (TODO: Create password reset email template)
    try:
        email_service.send_email(
            to_email=user.email,
            subject="Password Reset Request",
            html_content=f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <h2>Password Reset Request</h2>
                    <p>Click the link below to reset your password:</p>
                    <a href="{reset_link}" style="display: inline-block; background-color: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Reset Password</a>
                    <p style="margin-top: 20px; font-size: 12px; color: #666;">This link will expire in 2 hours.</p>
                    <p style="font-size: 12px; color: #666;">If you didn't request this, please ignore this email.</p>
                </body>
            </html>
            """
        )
    except Exception as e:
        print(f"Failed to send password reset email: {str(e)}")
    
    return {"message": "If the email exists, a reset link has been sent"}

@router.post("/reset-password")
async def reset_password(
    data: PasswordSetupRequest,
    session: Session = Depends(get_session)
):
    """Reset password using token"""
    # Verify token
    token_data = PasswordToken.verify_token(data.token)
    if not token_data:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    # Get user
    user = session.get(User, token_data["user_id"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Validate password
    if len(data.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    
    # Update password
    user.hashed_password = hash_password(data.password)
    
    session.add(user)
    session.commit()
    
    # Invalidate token
    PasswordToken.invalidate_token(data.token)
    
    return {"message": "Password reset successfully"}

@router.get("/verify-token/{token}")
async def verify_token(token: str):
    """Verify if a password setup/reset token is valid"""
    token_data = PasswordToken.verify_token(token)
    
    if not token_data:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    return {
        "valid": True,
        "email": token_data["email"],
        "expires_at": token_data["expires_at"]
    }
