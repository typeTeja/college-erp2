"""
Central Models Import

This file serves as a central import point for all models.
All models are now organized in domain-specific modules under app/domains/.

Note: Only importing models that actually exist in the domains.
Some models like Department, Program may not exist yet in consolidated domains.
"""

# Auth Domain Models
from app.domains.auth.models import (
    AuthUser as User,  # Alias for backward compatibility
    Role,
    Permission,
    UserRole,
    RolePermission,
)

# System Domain Models
from app.domains.system.models import (
    SystemSetting,
    InstituteInfo,
    AuditLog,
    PermissionAuditLog,
    FileMetadata,
    ImportLog,
)

# HR Domain Models
from app.domains.hr.models import (
    Designation,
    Staff,
    Faculty,
)

# Academic Domain Models - Import what actually exists
from app.domains.academic.models import *

# Student Domain Models
from app.domains.student.models import *

# Admission Domain Models
from app.domains.admission.models import *

# Finance Domain Models
from app.domains.finance.models import *

# Communication Domain Models
from app.domains.communication.models import *

# Campus Domain Models
from app.domains.campus.hostel.models import *
from app.domains.campus.library.models import *
from app.domains.campus.inventory.models import *
from app.domains.campus.transport.models import *
from app.domains.campus.infrastructure.models import *

# Note: __all__ is not defined to allow all models to be imported
# This is intentional to support dynamic model discovery
