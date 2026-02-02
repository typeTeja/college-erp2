from pydantic import BaseModel
from typing import Optional

class SubjectBase(BaseModel):
    name: str
    code: str
    credits: int = 3
    description: Optional[str] = None

class SubjectRead(SubjectBase):
    id: int
    class Config:
        from_attributes = True
