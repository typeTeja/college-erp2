from typing import Optional
from datetime import datetime
from enum import Enum as PyEnum
from sqlmodel import SQLModel, Field

class Designation(SQLModel, table=True):
    """Designation Management"""
    __tablename__ = "designation"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)  # e.g., "Professor", "Assistant Professor"
    code: str = Field(unique=True, index=True)
    
    level: int = Field(default=1)  # Hierarchy level
    department_id: Optional[int] = Field(default=None, foreign_key="department.id")
    
    min_experience_years: int = Field(default=0)
    min_qualification: Optional[str] = None
    
    is_teaching: bool = Field(default=True)
    is_active: bool = Field(default=True)
    display_order: int = Field(default=0)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)

from ..enums import RoomType


class MasterClassroom(SQLModel, table=True):
    """Classroom Management"""
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
