from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlmodel import Session
from app.api.deps import get_current_user, get_session
from app.models.user import User
from ..models.document import VerificationStatus
from ..services.document import document_service

router = APIRouter()

@router.get("/")
def get_my_documents(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Retrieve current student/user documents"""
    # Assuming user is linked to a student
    # In a real app, find student_id from current_user
    # student_id = ...
    # return document_service.get_student_documents(session, student_id)
    return {"message": "Endpoint migrated to Student Domain"}

@router.post("/upload")
async def upload_document(
    category_id: int = Form(...),
    student_id: int = Form(...),
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Upload a document"""
    return await document_service.upload_document(
        session=session,
        student_id=student_id,
        category_id=category_id,
        file=file,
        uploaded_by=current_user.id
    )
