from typing import List, Optional, Dict
from datetime import datetime, date, timedelta
import os
import hashlib
from pathlib import Path
from sqlmodel import Session, select
from fastapi import HTTPException, UploadFile
import aiofiles

from ..models.document import DocumentCategory, StudentDocument, DocumentVerification, VerificationStatus
from ..models.student import Student

class DocumentService:
    """Service for document management operations"""
    
    # File storage configuration
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/var/www/uploads/documents")
    MAX_FILE_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", 10485760))  # 10MB
    
    @staticmethod
    def calculate_file_hash(file_content: bytes) -> str:
        """Calculate SHA256 hash of file content"""
        return hashlib.sha256(file_content).hexdigest()
    
    @staticmethod
    def validate_file(
        file: UploadFile,
        category: DocumentCategory
    ) -> Dict:
        """Validate uploaded file against category constraints"""
        errors = []
        file_ext = file.filename.split('.')[-1].lower()
        allowed_types = category.allowed_file_types
        
        if file_ext not in allowed_types:
            errors.append(f"File type .{file_ext} not allowed. Allowed: {', '.join(allowed_types)}")
        
        if file.size and file.size > category.max_file_size:
            max_mb = category.max_file_size / (1024 * 1024)
            errors.append(f"File size exceeds maximum of {max_mb}MB")
        
        return {
            "is_valid": len(errors) == 0,
            "errors": errors
        }
    
    @staticmethod
    async def upload_document(
        session: Session,
        student_id: int,
        category_id: int,
        file: UploadFile,
        uploaded_by: Optional[int] = None,
        upload_ip: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> StudentDocument:
        """Upload and store a document"""
        category = session.get(DocumentCategory, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Document category not found")
        
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        validation = DocumentService.validate_file(file, category)
        if not validation["is_valid"]:
            raise HTTPException(status_code=400, detail=validation["errors"])
        
        stmt = select(StudentDocument).where(
            StudentDocument.student_id == student_id,
            StudentDocument.document_category_id == category_id,
            StudentDocument.is_latest == True
        )
        existing_docs = session.exec(stmt).all()
        
        if len(existing_docs) >= category.max_files:
            raise HTTPException(status_code=400, detail=f"Maximum {category.max_files} file(s) allowed")
        
        content = await file.read()
        file_hash = DocumentService.calculate_file_hash(content)
        
        stmt = select(StudentDocument).where(
            StudentDocument.student_id == student_id,
            StudentDocument.file_hash == file_hash
        )
        if session.exec(stmt).first():
            raise HTTPException(status_code=400, detail="This file has already been uploaded")
        
        # Save file logic...
        file_ext = file.filename.split('.')[-1].lower()
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{student_id}_{category.code}_{timestamp}.{file_ext}"
        upload_path = Path(DocumentService.UPLOAD_DIR) / str(student_id) / category.code
        upload_path.mkdir(parents=True, exist_ok=True)
        file_path = upload_path / filename
        
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        for doc in existing_docs:
            doc.is_latest = False
        
        expiry_date = None
        if category.valid_for_days:
            expiry_date = date.today() + timedelta(days=category.valid_for_days)
        
        document = StudentDocument(
            student_id=student_id,
            document_category_id=category_id,
            file_name=file.filename,
            file_path=str(file_path),
            file_size=len(content),
            file_type=file_ext,
            file_hash=file_hash,
            uploaded_by=uploaded_by,
            upload_ip=upload_ip,
            expiry_date=expiry_date,
            version_number=len(existing_docs) + 1,
            previous_document_id=existing_docs[0].id if existing_docs else None,
            document_number=metadata.get("document_number") if metadata else None,
            issue_date=metadata.get("issue_date") if metadata else None,
            issuing_authority=metadata.get("issuing_authority") if metadata else None,
            student_remarks=metadata.get("student_remarks") if metadata else None
        )
        session.add(document)
        session.commit()
        session.refresh(document)
        return document

    @staticmethod
    def verify_document(
        session: Session,
        document_id: int,
        verified_by: int,
        status: VerificationStatus,
        checklist_items: Optional[List[Dict]] = None,
        remarks: Optional[str] = None,
        rejection_reason: Optional[str] = None
    ) -> StudentDocument:
        """Verify or reject a document"""
        document = session.get(StudentDocument, document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        document.verification_status = status
        document.verified_by = verified_by
        document.verified_at = datetime.utcnow()
        if status == VerificationStatus.REJECTED:
            document.rejection_reason = rejection_reason
        
        verification = DocumentVerification(
            student_document_id=document_id,
            verified_by=verified_by,
            verification_status=status,
            checklist_items=checklist_items,
            remarks=remarks,
            rejection_reason=rejection_reason
        )
        session.add(verification)
        session.commit()
        session.refresh(document)
        return document

document_service = DocumentService()
