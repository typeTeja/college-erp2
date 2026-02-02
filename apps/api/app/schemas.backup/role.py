from pydantic import BaseModel
from typing import Optional, List
from .permission import PermissionRead

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_system: bool = False
    is_active: bool = True

class RoleCreate(RoleBase):
    permission_ids: List[int] = []

class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    permission_ids: Optional[List[int]] = None

class RoleRead(RoleBase):
    id: int
    permissions: List[PermissionRead] = []
    
    class Config:
        from_attributes = True

class PermissionAuditLogRead(BaseModel):
    id: int
    actor_id: int
    role_id: int
    action: str
    permission_name: str
    timestamp: str
    actor_name: Optional[str] = None
    role_name: Optional[str] = None

    class Config:
        from_attributes = True
