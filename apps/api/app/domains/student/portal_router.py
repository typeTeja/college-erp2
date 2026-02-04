from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, func
from typing import List, Optional
from datetime import datetime

from app.api.deps import get_session, get_current_user
from app.domains.auth.models import AuthUser as User
from app.domains.student.models import Student, StudentPortalAccess, StudentActivity, StudentNotification
from app.domains.student.schemas import StudentRead

router = APIRouter()

@router.get("/dashboard")
def get_dashboard(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    student = session.exec(select(Student).where(Student.user_id == current_user.id)).first()
    if not student:
         raise HTTPException(status_code=404, detail="Student profile not found")
    
    # Placeholder for actual dashboard stats (attendance, fees, etc)
    return {
        "student": student,
        "stats": {
            "attendance": 85.5,
            "pending_fees": 15000,
            "notifications": 3
        }
    }

@router.get("/profile", response_model=StudentRead)
def get_profile(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    student = session.exec(select(Student).where(Student.user_id == current_user.id)).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student profile not found")
    return student

@router.get("/notifications", response_model=List[dict]) # Replace with proper schema if needed
def get_notifications(unread: bool = False, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    student = session.exec(select(Student).where(Student.user_id == current_user.id)).first()
    if not student:
         return []
    
    statement = select(StudentNotification).where(StudentNotification.student_id == student.id)
    if unread:
        statement = statement.where(StudentNotification.is_read == False)
    
    return session.exec(statement).all()

@router.post("/notifications/{id}/read")
def mark_read(id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    notif = session.get(StudentNotification, id)
    if notif:
        notif.is_read = True
        notif.read_at = datetime.utcnow()
        session.add(notif)
        session.commit()
    return {"status": "success"}

@router.get("/activity")
def get_activity(limit: int = 10, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    student = session.exec(select(Student).where(Student.user_id == current_user.id)).first()
    if not student:
        return []
    statement = select(StudentActivity).where(StudentActivity.student_id == student.id).order_by(StudentActivity.created_at.desc()).limit(limit)
    return session.exec(statement).all()
