from typing import List, Set, Optional
import json
import logging
from fastapi import Request
from sqlmodel import select, Session
import redis
# Import directly from domains to avoid circular dependency with app.models
from app.domains.auth.models import Permission, RolePermission, Role, AuthUser
from app.config.settings import settings

logger = logging.getLogger(__name__)

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

class RBACService:
    """
    Robust RBAC Service with multi-level caching:
    1. Request-local cache (handled by FastAPI dependency scope implicity if using injection, 
       but we can add an explicit layer if needed).
    2. Redis cache (shared, TTL 5m).
    3. Database fallback.
    """
    
    _redis: Optional[redis.Redis] = None
    CACHE_TTL = 300  # 5 minutes
    # Refined prefix as per feedback
    CACHE_PREFIX = "rbac:user:"
    
    @classmethod
    def get_redis(cls) -> Optional[redis.Redis]:
        """Lazy load Redis connection. Returns None if connection fails."""
        if cls._redis is None:
            if not settings.REDIS_URL:
                 logger.warning("REDIS_URL not set. Caching disabled.")
                 return None
            try:
                cls._redis = redis.from_url(
                    settings.REDIS_URL,
                    decode_responses=True
                )
                # Test connection
                cls._redis.ping()
            except Exception as e:
                logger.error(f"Failed to connect to Redis: {e}")
                cls._redis = None
        return cls._redis

    @classmethod
    def _get_cache_key(cls, user_id: int) -> str:
        return f"{cls.CACHE_PREFIX}{user_id}:permissions"

    @classmethod
    def get_user_permissions(cls, session: Session, user_id: int) -> Set[str]:
        """
        Get permissions for a user, using Cache -> DB strategy.
        Safely falls back to DB if Redis is unavailable.
        """
        redis_client = cls.get_redis()
        
        # 1. Try Cache
        if redis_client:
            try:
                cached = redis_client.get(cls._get_cache_key(user_id))
                if cached:
                    return set(json.loads(cached))
            except Exception as e:
                logger.warning(f"Redis cache read error: {e}")
                
        # 2. DB Query (Fallback)
        statement = (
            select(Permission.name)
            .join(RolePermission)
            .join(Role)
            .join(Role.users)
            .where(Role.users.property.mapper.class_.id == user_id)
        )
        results = session.exec(statement).all()
        perms = set(results)
        
        # 3. Update Cache
        if redis_client:
            try:
                # Deterministic serialization (sorted list)
                sorted_perms = sorted(list(perms))
                redis_client.setex(
                    cls._get_cache_key(user_id),
                    cls.CACHE_TTL,
                    json.dumps(sorted_perms)
                )
            except Exception as e:
                 logger.error(f"Failed to set Redis cache: {e}")
                 
        return perms

    @classmethod
    def invalidate_user_cache(cls, user_id: int):
        """Invalidate permissions cache for a specific user"""
        redis_client = cls.get_redis()
        if not redis_client:
            return
            
        try:
            redis_client.delete(cls._get_cache_key(user_id))
            logger.info(f"Invalidated RBAC cache for user_id={user_id}")
        except Exception as e:
            logger.error(f"Failed to invalidate user cache: {e}")

    @classmethod
    def invalidate_role_cache(cls, session: Session, role_id: int):
        """
        Invalidate cache for all users with a specific role.
        """
        try:
            # Find all users with this role
            role = session.get(Role, role_id)
            if role:
                for user in role.users:
                    cls.invalidate_user_cache(user.id)
                logger.info(f"Invalidated RBAC cache for role_id={role_id} (users={len(role.users)})")
        except Exception as e:
            logger.error(f"Failed to invalidate role cache: {e}")

# Maintain backward compatibility
async def get_user_permissions(session: Session, user_id: int) -> Set[str]:
    """Deprecated: Use RBACService.get_user_permissions"""
    return RBACService.get_user_permissions(session, user_id)
