from typing import List, Set
from fastapi import Request
from sqlmodel import select, Session
from app.models.permission import Permission, RolePermission
from app.models.role import Role

# Standard Permission Seeds
CORE_PERMISSIONS = {
    "Academics": [
        ("academics:read", "View academic structures"),
        ("academics:write", "Manage academic setups"),
        ("timetable:manage", "Manage class schedules"),
        ("attendance:manage", "Record and verify attendance"),
    ],
    "Admissions": [
        ("admissions:read", "View admission applications"),
        ("admissions:write", "Create/Update applications"),
        ("admissions:confirm", "Confirm admissions (Student creation)"),
    ],
    "Fees": [
        ("fees:read", "View fee structures and statuses"),
        ("fees:write", "Manage fee installments"),
        ("fees:approve", "Approve fee payments and concessions"),
    ],
    "Exams": [
        ("exams:read", "View exam schedules and results"),
        ("exams:write", "Manage exams and marks entry"),
    ],
    "Students": [
        ("students:read", "View student directory"),
        ("students:write", "Edit student profiles"),
    ],
    "Staff": [
        ("staff:read", "View staff directory"),
        ("staff:write", "Manage staff and operations"),
    ],
    "Hostel": [
        ("hostel:read", "View hostel occupancy and complaints"),
        ("hostel:write", "Manage room allocations and gatepasses"),
    ],
    "Library": [
        ("library:read", "View book catalog"),
        ("library:write", "Issue/Return books and manage fines"),
    ],
    "Inventory": [
        ("inventory:read", "View assets and stock"),
        ("inventory:write", "Manage inventory and allocations"),
    ],
    "Communication": [
        ("circulars:write", "Publish and manage circulars"),
    ],
    "Reports": [
        ("reports:read", "View analytics and reports"),
    ],
    "Settings": [
        ("rbac:manage", "Manage roles and permissions (Super Admin only)"),
        ("settings:write", "Update general college settings"),
    ]
}

def seed_permissions(session: Session):
    """Seed all core permissions into the database"""
    for module, perms in CORE_PERMISSIONS.items():
        for name, desc in perms:
            # Check if exists
            perm = session.exec(select(Permission).where(Permission.name == name)).first()
            if not perm:
                perm = Permission(name=name, description=desc, module=module)
                session.add(perm)
    session.commit()

async def get_user_permissions(session: Session, user_id: int) -> Set[str]:
    """
    Retrieves all unique permissions for a user across all their roles.
    Ideally, this would be cached in Redis or a per-request cache.
    """
    # Simple join to get all permission names for the user's roles
    # User -> UserRole -> Role -> RolePermission -> Permission
    statement = (
        select(Permission.name)
        .join(RolePermission)
        .join(Role)
        .join(Role.users)
        .where(Role.users.property.mapper.class_.id == user_id)
    )
    results = session.exec(statement).all()
    return set(results)

class PermissionCache:
    """Simple per-request permission cache to avoid redundant DB hits"""
    _cache = {}

    @classmethod
    def get(cls, user_id: int):
        return cls._cache.get(user_id)

    @classmethod
    def set(cls, user_id: int, permissions: Set[str]):
        cls._cache[user_id] = permissions

    @classmethod
    def clear(cls):
        cls._cache = {}
