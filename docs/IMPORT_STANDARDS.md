# Import Standards

## Overview

All new code MUST use domain-based imports. Legacy `app.models.*` imports are blocked by pre-commit hooks.

## ✅ Correct Imports

### Models

```python
# Academic domain
from app.domains.academic.models import Program, AcademicBatch, Regulation

# HR domain
from app.domains.hr.models import Department, Staff, Faculty

# Auth domain
from app.domains.auth.models import AuthUser, Role, Permission

# Finance domain
from app.domains.finance.models import Payment, FeeStructure

# Student domain
from app.domains.student.models import Student, Parent

# Admission domain
from app.domains.admission.models import Application, ApplicationPayment
```

### Enums

```python
# Always from shared
from app.shared.enums import (
    ApplicationStatus,
    PaymentStatus,
    ProgramType,
    ProgramStatus
)
```

### Schemas

```python
# Domain-specific schemas
from app.domains.admission.schemas import ApplicationCreate, ApplicationRead
from app.domains.finance.schemas import PaymentCreate
from app.domains.academic.schemas import ProgramCreate
```

## ❌ Blocked Imports (Legacy)

```python
# These will fail pre-commit hook
from app.models.program import Program  # ❌
from app.models.department import Department  # ❌
from app.models.user import User  # ❌
```

## Migration Guide

### Old → New

| Old (Blocked)           | New (Required)                     |
| ----------------------- | ---------------------------------- |
| `app.models.program`    | `app.domains.academic.models`      |
| `app.models.department` | `app.domains.hr.models`            |
| `app.models.user`       | `app.domains.auth.models.AuthUser` |

### TYPE_CHECKING Imports

For avoiding circular dependencies:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domains.academic.models import Program
    from app.domains.student.models import Student
```

## Enforcement

### Pre-commit Hook

- Automatically checks all staged Python files
- Blocks commits with legacy imports
- Provides helpful error messages

### Bypass (Emergency Only)

```bash
git commit --no-verify  # Use sparingly!
```

## Contract Versioning

### Frozen Schemas

Schemas marked with version tags are frozen:

```python
"""
**CONTRACT VERSION: v1.0.0**
**STATUS: FROZEN (2026-02-03)**
"""
```

Changes require:

1. Version bump
2. Deprecation notice (if breaking)
3. Team approval

### Breaking Changes Policy

- Enum additions: ✅ Safe
- New optional fields: ✅ Safe
- Required field changes: ⚠️ 6-month deprecation
- Enum removals: ⚠️ 6-month deprecation
- Type changes: ⚠️ Major version bump

## Questions?

Contact the backend team or refer to:

- [Admission Contract](apps/api/docs/admission_frontend_contract_v1.md)
- [Implementation Plan](../.gemini/antigravity/brain/*/implementation_plan.md)
