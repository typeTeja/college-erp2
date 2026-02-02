"""
Student Assignment Schemas
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class StudentAssignmentBase(BaseModel):
    """Base schema for student assignments"""
    student_id: int
    section_id: int
    batch_id: int
    semester_no: int


class StudentSectionAssignmentCreate(StudentAssignmentBase):
    """Schema for creating section assignment"""
    assignment_type: str = "MANUAL"


class StudentSectionAssignmentRead(StudentAssignmentBase):
    """Schema for reading section assignment"""
    id: int
    assignment_type: str
    assigned_at: datetime
    assigned_by: Optional[int]
    is_active: bool
    
    class Config:
        from_attributes = True


class AutoAssignRequest(BaseModel):
    """Request schema for auto-assignment"""
    batch_id: int = Field(..., description="Batch ID")
    semester_no: int = Field(..., ge=1, le=10, description="Semester number")


class AutoAssignResponse(BaseModel):
    """Response schema for auto-assignment"""
    assigned_count: int
    unassigned_count: int
    message: str


class ReassignRequest(BaseModel):
    """Request schema for reassignment"""
    new_section_id: int = Field(..., description="New section ID")


class SectionRosterStudent(BaseModel):
    """Student in section roster"""
    assignment_id: int
    student_id: int
    student_name: str
    admission_number: str
    assignment_type: str
    assigned_at: datetime


class SectionRosterResponse(BaseModel):
    """Response schema for section roster"""
    section_id: int
    section_name: str
    section_code: str
    current_strength: int
    max_strength: int
    students: List[SectionRosterStudent]


class UnassignedStudentsResponse(BaseModel):
    """Response schema for unassigned students"""
    batch_id: int
    semester_no: int
    count: int
    students: List[dict]  # Student details
