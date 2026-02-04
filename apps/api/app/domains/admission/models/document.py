from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from app.shared.enums import DocumentType, DocumentStatus

if TYPE_CHECKING:
    from .application import Application

class ApplicationDocument(SQLModel, table=True):
    """Documents uploaded by applicants for verification"""
    __tablename__ = "application_document"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    application_id: int = Field(foreign_key="application.id", index=True)
    document_type: DocumentType
    file_url: str
    file_name: str
    file_size: int  # in bytes
    status: DocumentStatus = Field(default=DocumentStatus.UPLOADED)
    rejection_reason: Optional[str] = None
    verified_by: Optional[int] = Field(default=None, foreign_key="users.id")
    verified_at: Optional[datetime] = None
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    application: "Application" = Relationship(back_populates="documents")
