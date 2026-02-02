from pydantic import BaseModel
from typing import Optional, List

class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None
    module: str

class PermissionCreate(PermissionBase):
    pass

class PermissionRead(PermissionBase):
    id: int
    
    class Config:
        from_attributes = True

class PermissionGroup(BaseModel):
    module: str
    permissions: List[PermissionRead]
