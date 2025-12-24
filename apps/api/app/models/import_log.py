from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class ImportLog(SQLModel, table=True):
    """Audit log for bulk data imports"""
    __tablename__ = "import_log"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    file_name: str
    uploaded_by_id: int = Field(foreign_key="user.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    total_rows: int = Field(default=0)
    imported_count: int = Field(default=0)
    failed_count: int = Field(default=0)
    duplicate_count: int = Field(default=0)
    ip_address: Optional[str] = None
    status: str = Field(default="PENDING") # PENDING, SUCCESS, PARTIAL, FAILED
    
    # Metadata
    module: str = Field(default="STUDENT") # STUDENT, FACULTY, etc.
    error_report_path: Optional[str] = None
