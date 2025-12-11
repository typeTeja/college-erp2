from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.db.session import get_session
from app.api.deps import get_current_user
from app.models.user import User
from typing import List, Dict, Any
from datetime import datetime

router = APIRouter()

@router.get("/recent")
async def get_recent_admissions(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    limit: int = 10
) -> List[Dict[str, Any]]:
    """Get recent admission applications"""
    
    # For now, return mock data
    # TODO: Implement actual queries when Admission model is ready
    return [
        {
            "id": 1,
            "fullName": "Rahul Sharma",
            "email": "rahul.sharma@example.com",
            "course": {"id": 1, "name": "Computer Science Engineering"},
            "status": "PENDING",
            "createdAt": datetime.now().isoformat()
        },
        {
            "id": 2,
            "fullName": "Priya Patel",
            "email": "priya.patel@example.com",
            "course": {"id": 2, "name": "Electronics Engineering"},
            "status": "APPROVED",
            "createdAt": datetime.now().isoformat()
        },
        {
            "id": 3,
            "fullName": "Amit Kumar",
            "email": "amit.kumar@example.com",
            "course": {"id": 1, "name": "Computer Science Engineering"},
            "status": "PENDING",
            "createdAt": datetime.now().isoformat()
        }
    ]
