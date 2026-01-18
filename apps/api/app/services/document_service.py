"""
Document Management Service Layer

Handles business logic for document management including:
- File upload and storage
- Document verification
- File validation
- Version management
"""
from typing import List, Optional, Dict
from datetime import datetime, date, timedelta
import os
import hashlib
from pathlib import Path
from sqlmodel import Session, select
from fastapi import HTTPException, UploadFile
import aiofiles

from app.models.documents import (
    DocumentCategory, StudentDocument, DocumentVerification,
    VerificationStatus
)
from app.models.student import Student


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
        
        # Check file type
        file_ext = file.filename.split('.')[-1].lower()
        allowed_types = category.allowed_file_types
        
        if isinstance(allowed_types, str):
            import json
            allowed_types = json.loads(allowed_types)
        
        if file_ext not in allowed_types:
            errors.append(f"File type .{file_ext} not allowed. Allowed: {', '.join(allowed_types)}")
        
        # Check file size
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
        # Get category
        category = session.get(DocumentCategory, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Document category not found")
        
        # Validate student
        student = session.get(Student, student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        # Validate file
        validation = DocumentService.validate_file(file, category)
        if not validation["is_valid"]:
            raise HTTPException(status_code=400, detail=validation["errors"])
        
        # Check existing documents count
        stmt = select(StudentDocument).where(
            StudentDocument.student_id == student_id,
            StudentDocument.document_category_id == category_id,
            StudentDocument.is_latest == True
        )
        existing_docs = session.exec(stmt).all()
        
        if len(existing_docs) >= category.max_files:
            raise HTTPException(
                status_code=400,
                detail=f"Maximum {category.max_files} file(s) allowed for this category"
            )
        
        # Read file content
        content = await file.read()
        file_hash = DocumentService.calculate_file_hash(content)
        
        # Check for duplicates
        stmt = select(StudentDocument).where(
            StudentDocument.student_id == student_id,
            StudentDocument.file_hash == file_hash
        )
        duplicate = session.exec(stmt).first()
        if duplicate:
            raise HTTPException(status_code=400, detail="This file has already been uploaded")
        
        # Generate file path
        file_ext = file.filename.split('.')[-1].lower()
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{student_id}_{category.code}_{timestamp}.{file_ext}"
        
        # Create directory structure
        upload_path = Path(DocumentService.UPLOAD_DIR) / str(student_id) / category.code
        upload_path.mkdir(parents=True, exist_ok=True)
        
        file_path = upload_path / filename
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        # Mark previous versions as not latest
        for doc in existing_docs:
            doc.is_latest = False
        
        # Calculate expiry date
        expiry_date = None
        if category.valid_for_days:
            expiry_date = date.today() + timedelta(days=category.valid_for_days)
        
        # Create document record
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
        
        # Update document status
        document.verification_status = status
        document.verified_by = verified_by
        document.verified_at = datetime.utcnow()
        
        if status == VerificationStatus.REJECTED:
            document.rejection_reason = rejection_reason
        
        # Create verification record
        verification = DocumentVerification(
            student_document_id=document_id,
            verified_by=verified_by,
            verification_status=status,
            checklist_items=str(checklist_items) if checklist_items else None,
            remarks=remarks,
            rejection_reason=rejection_reason
        )
        
        session.add(verification)
        session.commit()
        session.refresh(document)
        
        return document
    
    @staticmethod
    def get_student_documents(
        session: Session,
        student_id: int,
        category_id: Optional[int] = None,
        verification_status: Optional[VerificationStatus] = None,
        latest_only: bool = True
    ) -> List[StudentDocument]:
        """Get documents for a student"""
        stmt = select(StudentDocument).where(StudentDocument.student_id == student_id)
        
        if category_id:
            stmt = stmt.where(StudentDocument.document_category_id == category_id)
        
        if verification_status:
            stmt = stmt.where(StudentDocument.verification_status == verification_status)
        
        if latest_only:
            stmt = stmt.where(StudentDocument.is_latest == True)
        
        return session.exec(stmt).all()
    
    @staticmethod
    def check_document_expiry(session: Session):
        """Check and mark expired documents"""
        today = date.today()
        
        stmt = select(StudentDocument).where(
            StudentDocument.expiry_date.isnot(None),
            StudentDocument.expiry_date < today,
            StudentDocument.is_expired == False
        )
        
        expired_docs = session.exec(stmt).all()
        
        for doc in expired_docs:
            doc.is_expired = True
            doc.verification_status = VerificationStatus.EXPIRED
        
        session.commit()
        return len(expired_docs)
    
    @staticmethod
    def get_verification_statistics(
        session: Session,
        category_id: Optional[int] = None
    ) -> Dict:
        """Get document verification statistics"""
        stmt = select(StudentDocument)
        
        if category_id:
            stmt = stmt.where(StudentDocument.document_category_id == category_id)
        
        documents = session.exec(stmt).all()
        
        total = len(documents)
        pending = sum(1 for d in documents if d.verification_status == VerificationStatus.PENDING)
        verified = sum(1 for d in documents if d.verification_status == VerificationStatus.VERIFIED)
        rejected = sum(1 for d in documents if d.verification_status == VerificationStatus.REJECTED)
        expired = sum(1 for d in documents if d.verification_status == VerificationStatus.EXPIRED)
        
        return {
            "total": total,
            "pending": pending,
            "verified": verified,
            "rejected": rejected,
            "expired": expired,
            "verification_rate": round((verified / total * 100) if total > 0 else 0, 2)
        }
