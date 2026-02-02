from typing import Optional
from sqlmodel import SQLModel, Field

class Parent(SQLModel, table=True):
    """Parent/Guardian information model"""
    id: Optional[int] = Field(default=None, primary_key=True)
    linked_student_id: int = Field(foreign_key="student.id", index=True)
    father_name: str
    father_mobile: str = Field(index=True)
    mother_name: Optional[str] = None
    guardian_mobile: Optional[str] = None
