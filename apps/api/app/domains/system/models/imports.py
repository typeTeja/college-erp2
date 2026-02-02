from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class ImportLog(SQLModel, table=True):
    __tablename__ = "system_import_log"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    file_name: str
    uploaded_by_id: int = Field(foreign_key="user.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    total_rows: int = 0
    imported_count: int = 0
    failed_count: int = 0
    duplicate_count: int = 0
    status: str = "PENDING"  # PREVIEW, SUCCESS, PARTIAL, FAILED
