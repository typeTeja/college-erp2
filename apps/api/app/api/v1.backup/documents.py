"""
Document Management API Endpoints

Provides comprehensive document management functionality
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from pydantic import BaseModel

from app.api.deps import get_session, get_current_active_superuser, get_current_user
from app.models import User
from app.models.documents import DocumentCategory, StudentDocument, VerificationStatus
from app.services.document_service import DocumentService

router = APIRouter(prefix="/documents", tags=["Document Management"])


# Schemas
class DocumentCategoryCreate(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    is_required: bool = False
    is_mandatory: bool = False
    allowed_file_types: List[str]
    max_file_size: int = 10485760
    max_files: int = 1
    verification_required: bool = True
    valid_for_days: Optional[int] = None
    upload_instructions: Optional[str] = None


class DocumentVerifyRequest(BaseModel):
    status: str  # VERIFIED, REJECTED
    checklist_items: Optional[List[dict]] = None
    remarks: Optional[str] = None
    rejection_reason: Optional[str] = None


# ============================================================================
# Document Category Endpoints
# ============================================================================

@router.post("/categories")
def create_category(
    *,
    session: Session = Depends(get_session),
    category_data: DocumentCategoryCreate,
    current_user: User = Depends(get_current_active_superuser)
):
    """Create document category"""
    category = DocumentCategory(**category_data.model_dump())
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


@router.get("/categories")
def list_categories(
    *,
    session: Session = Depends(get_session),
    is_active: Optional[bool] = Query(None),
    is_required: Optional[bool] = Query(None)
):
    """List document categories"""
    stmt = select(DocumentCategory)
    
    if is_active is not None:
        stmt = stmt.where(DocumentCategory.is_active == is_active)
    if is_required is not None:
        stmt = stmt.where(DocumentCategory.is_required == is_required)
    
    stmt = stmt.order_by(DocumentCategory.display_order)
    return session.exec(stmt).all()


@router.get("/categories/{category_id}")
def get_category(
    *,
    session: Session = Depends(get_session),
    category_id: int
):
    """Get document category"""
    category = session.get(DocumentCategory, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


# ============================================================================
# Document Upload Endpoints
# ============================================================================

@router.post("/upload")
async def upload_document(
    *,
    session: Session = Depends(get_session),
    student_id: int = Form(...),
    category_id: int = Form(...),
    file: UploadFile = File(...),
    document_number: Optional[str] = Form(None),
    issue_date: Optional[str] = Form(None),
    issuing_authority: Optional[str] = Form(None),
    student_remarks: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user)
):
    """Upload a document"""
    metadata = {
        "document_number": document_number,
        "issue_date": issue_date,
        "issuing_authority": issuing_authority,
        "student_remarks": student_remarks
    }
    
    document = await DocumentService.upload_document(
        session,
        student_id,
        category_id,
        file,
        uploaded_by=current_user.id,
        metadata=metadata
    )
    
    return document


@router.get("/student/{student_id}")
def get_student_documents(
    *,
    session: Session = Depends(get_session),
    student_id: int,
    category_id: Optional[int] = Query(None),
    verification_status: Optional[str] = Query(None),
    latest_only: bool = Query(True)
):
    """Get documents for a student"""
    status = VerificationStatus(verification_status) if verification_status else None
    
    return DocumentService.get_student_documents(
        session,
        student_id,
        category_id,
        status,
        latest_only
    )


@router.get("/{document_id}")
def get_document(
    *,
    session: Session = Depends(get_session),
    document_id: int
):
    """Get document details"""
    document = session.get(StudentDocument, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.get("/{document_id}/download")
def download_document(
    *,
    session: Session = Depends(get_session),
    document_id: int,
    current_user: User = Depends(get_current_user)
):
    """Download a document"""
    document = session.get(StudentDocument, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check file exists
    import os
    if not os.path.exists(document.file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        document.file_path,
        filename=document.file_name,
        media_type=f"application/{document.file_type}"
    )


# ============================================================================
# Document Verification Endpoints
# ============================================================================

@router.post("/{document_id}/verify")
def verify_document(
    *,
    session: Session = Depends(get_session),
    document_id: int,
    request: DocumentVerifyRequest,
    current_user: User = Depends(get_current_active_superuser)
):
    """Verify or reject a document"""
    status = VerificationStatus(request.status)
    
    return DocumentService.verify_document(
        session,
        document_id,
        current_user.id,
        status,
        request.checklist_items,
        request.remarks,
        request.rejection_reason
    )


@router.get("/pending/count")
def get_pending_count(
    *,
    session: Session = Depends(get_session),
    category_id: Optional[int] = Query(None)
):
    """Get count of pending verifications"""
    stmt = select(StudentDocument).where(
        StudentDocument.verification_status == VerificationStatus.PENDING
    )
    
    if category_id:
        stmt = stmt.where(StudentDocument.document_category_id == category_id)
    
    count = len(session.exec(stmt).all())
    return {"pending_count": count}


# ============================================================================
# Statistics Endpoints
# ============================================================================

@router.get("/statistics/verification")
def get_verification_statistics(
    *,
    session: Session = Depends(get_session),
    category_id: Optional[int] = Query(None)
):
    """Get verification statistics"""
    return DocumentService.get_verification_statistics(session, category_id)


@router.post("/maintenance/check-expiry")
def check_expired_documents(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_superuser)
):
    """Check and mark expired documents"""
    count = DocumentService.check_document_expiry(session)
    return {"expired_count": count}
