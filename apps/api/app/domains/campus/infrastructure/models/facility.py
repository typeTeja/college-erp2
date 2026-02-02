from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, Text
from app.shared.enums import RoomType


if TYPE_CHECKING:
    from app.models.department import Department

class MasterClassroom(SQLModel, table=True):
    """Classroom Management - Facility Structure"""
    __tablename__ = "master_classroom"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)  # e.g., "Room 101", "Computer Lab 1"
    code: str = Field(unique=True, index=True)
    
    room_type: RoomType = Field(default=RoomType.CLASSROOM)
    building: Optional[str] = None
    floor: Optional[int] = None
    
    capacity: int = Field(default=40)
    
    has_projector: bool = Field(default=False)
    has_ac: bool = Field(default=False)
    has_smart_board: bool = Field(default=False)
    has_computer: bool = Field(default=False)
    
    department_id: Optional[int] = Field(default=None, foreign_key="department.id")
    
    is_active: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
