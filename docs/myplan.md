# ERP Domain Migration Plan (Non-Production Optimized)

## PROJECT CONTEXT

This is a College Management ERP system (FastAPI + SQLModel backend, Next.js frontend).

- **Status:** NOT in production (development/staging only)
- **Goal:** 15-20 year maintainability with zero rewrites
- **Architecture:** Strict Domain-Driven Design (DDD)
- **Timeline:** 5-6 weeks (aggressive migration)

## GOAL

1. Complete inventory of ALL legacy vs domain files
2. Migrate EVERYTHING to clean domain-driven architecture
3. Eliminate ALL architectural inconsistency and duplication
4. Execute in 5-6 weeks (aggressive, non-production timeline)

## CURRENT STATE

**Mixed architecture:**

- ✅ Domains exist: `app/domains/*` (~40-45% migrated)
- ❌ Legacy exists: `app/models/`, `app/schemas/`, `app/services/`, `app/api/v1/*.py`
- ❌ 60+ duplicate enum definitions
- ❌ 23 stub service files
- ❌ Business logic scattered everywhere

**Advantage: NOT in production**

- Can delete legacy files immediately after migration
- Can break things temporarily
- Can move fast without rollback procedures
- Can freeze feature development

**Campus domain note:**

- `campus/` is intentionally a Phase-1 grouped domain
- hostel, library, inventory, transport stay under campus
- DO NOT promote to top-level domains in this migration

---

## ARCHITECTURE RULES (MANDATORY)

A. FINAL DOMAIN STRUCTURE (STRICT)

Every domain MUST follow the SAME internal structure:

<domain>/
├── models.py # SQLModel entities ONLY
├── schemas.py # Request / Response DTOs ONLY
├── repository.py # Database access ONLY
├── services.py # Business logic ONLY
├── router.py # API endpoints ONLY (thin)
├── events.py # Domain events (can be empty initially)
└── exceptions.py # Domain-specific errors

FORBIDDEN:

- models/ folders
- services/ folders
- routers/ folders
- duplicate service.py or router.py files
- business logic outside domains/

---

B. CORE & SHARED LAYERS

app/
├── core/ # Cross-cutting infrastructure
│ ├── database.py
│ ├── transactions.py
│ ├── security.py
│ ├── permissions.py
│ ├── audit.py
│ └── exceptions.py
│
├── shared/ # Stable primitives (SINGLE SOURCE OF TRUTH)
│ ├── enums.py
│ ├── value_objects.py
│ ├── constants.py
│ └── base_models.py
│
├── domains/ # ONLY place for business logic
│ ├── admission/
│ ├── academic/
│ ├── student/
│ ├── finance/
│ ├── hr/
│ ├── communication/
│ ├── system/
│ └── campus/ # Phase-1 grouped domain ONLY
│
└── api/
└── v1/
└── router.py # Aggregates domain routers ONLY

---

## MIGRATION STEPS

### STEP 0 — CLEAN START

**Actions:**

- Create feature branch: `refactor/domain-migration`
- Freeze all new feature development
- Run current test suite and document baseline results
- Communicate migration timeline to team

**Deliverable:** Branch created, baseline documented

**Duration:** 1 day

---

### STEP 1 — INVENTORY

**Actions:**

- Scan entire `apps/api/app/` directory
- Categorize every Python file:
  - Current location (legacy/domain/mixed)
  - Target domain
  - Action needed (MOVE/MERGE/DELETE/KEEP)

**Output format:**

```
| File Path | Current Layer | Target Domain | Action |
|-----------|---------------|---------------|--------|
| app/models/student.py | legacy | student | MOVE |
| app/services/fee_service.py | legacy | finance | MOVE |
```

**Deliverable:** Complete inventory table (CSV or Markdown)

**Duration:** 2-3 days

---

### STEP 1.5 — DEPENDENCY GRAPH

**Actions:**

- Map cross-domain dependencies
- Define migration order (dependency-first):
  1. `shared/enums` (no dependencies)
  2. `system/` (infrastructure)
  3. `hr/` (faculty, staff)
  4. `academic/` (depends on hr)
  5. `student/` (depends on academic)
  6. `admission/` (depends on student)
  7. `finance/` (depends on student)
  8. `communication/` (depends on student)
  9. `campus/` (depends on student)
- Identify and break circular imports

**Deliverable:** Migration order diagram + circular import fixes

**Duration:** 1 day

---

### STEP 2 — ENUM CONSOLIDATION

**Actions:**

1. Create `app/shared/enums.py`
2. Find ALL enum definitions (60+ across codebase)
3. Consolidate into single file with clear namespacing:

   ```python
   # Payment Domain
   class PaymentStatus(str, Enum): ...
   class PaymentMode(str, Enum): ...

   # Academic Domain
   class ExamType(str, Enum): ...
   class AttendanceStatus(str, Enum): ...
   ```

4. Update ALL imports across codebase
5. Delete old enum files
6. Run tests

**Deliverable:**

- `app/shared/enums.py` with all enums
- List of deleted enum files
- All tests passing

**Duration:** 2-3 days

---

### STEP 2.5 — REPOSITORY PATTERN (OPTIONAL BUT RECOMMENDED)

**Actions:**

1. Create `app/shared/base_repository.py`:

   ```python
   class BaseRepository:
       def __init__(self, session: Session):
           self.session = session

       def get(self, id: int): ...
       def list(self, skip: int, limit: int): ...
       def create(self, obj): ...
       def update(self, id: int, data): ...
       def delete(self, id: int): ...
   ```

2. Create repository for one domain as template
3. Document pattern for other domains

**Deliverable:** Base repository + example implementation

**Duration:** 1 day

---

### STEP 3 — DOMAIN MIGRATION (ONE AT A TIME)

**For EACH domain (in dependency order):**

1. **Create domain structure:**

   ```
   app/domains/<domain>/
   ├── models.py       # SQLModel entities ONLY
   ├── schemas.py      # Request/Response DTOs ONLY
   ├── repository.py   # Database access ONLY
   ├── services.py     # Business logic ONLY
   ├── router.py       # API endpoints ONLY (thin)
   ├── events.py       # Domain events (empty for now)
   └── exceptions.py   # Domain-specific errors
   ```

2. **Move files:**
   - Consolidate `app/models/<domain>/*` → `models.py`
   - Consolidate `app/schemas/<domain>/*` → `schemas.py`
   - Consolidate `app/services/<domain>_service.py` → `services.py`
   - Move `app/api/v1/<domain>.py` → `router.py`
   - Extract DB queries → `repository.py`

3. **Fix imports** across entire codebase

4. **DELETE legacy files immediately**

5. **Test:**
   - Run pytest suite
   - Manual smoke test critical flows

6. **Commit** with message: `refactor: migrate <domain> to domain structure`

**Deliverable (per domain):**

- Clean domain structure
- All tests passing
- Legacy files deleted
- Git commit

**Duration:** 1-2 days per domain × 9 domains = **2-3 weeks**

---

### STEP 3.5 — TESTING (AFTER EACH DOMAIN)

**Actions:**

- Run full pytest suite
- Manual smoke tests:
  - Login flow
  - Create application
  - Confirm admission
  - Record payment
  - View student dashboard
  - Generate report

**Deliverable:** Test results documented

**Duration:** 30 minutes per domain (included in Step 3)

---

### STEP 4 — ALEMBIC COORDINATION

**Actions:**

1. Update `app/models/__init__.py` to import all domain models:

   ```python
   # Import all domain models for Alembic autogenerate
   from app.domains.student.models import Student, StudentDocument
   from app.domains.academic.models import Batch, Section, Subject
   # ... etc
   ```

2. Test Alembic:

   ```bash
   alembic revision --autogenerate -m "test_migration"
   ```

3. Verify it detects NO changes (schema unchanged)

4. Delete test migration file

**Deliverable:** Alembic working, no schema drift

**Duration:** 1 day

---

### STEP 5 — TRANSACTION SAFETY

**Actions:**
Identify critical multi-step operations and wrap in explicit transactions:

```python
# Before (UNSAFE)
def confirm_admission(application_id: int):
    app = get_application(application_id)
    app.status = "ADMITTED"
    session.commit()  # ❌ Partial commit

    student = create_student(app)  # ❌ If this fails, app is already admitted!
    session.commit()

# After (SAFE)
def confirm_admission(application_id: int):
    with session.begin():  # ✅ Atomic transaction
        app = get_application(application_id)
        app.status = "ADMITTED"
        student = create_student(app)
        # Both succeed or both rollback
```

**Critical flows:**

- Admission confirmation
- Payment processing (Easebuzz)
- Student promotion/detention
- Exam result publishing
- Hostel allocation

**Deliverable:** List of files updated with transactions

**Duration:** 2 days

---

### STEP 6 — LOGICAL AGGREGATE REVIEW

**Actions:**
Document (NO code changes) logical aggregates:

**Student Aggregate:**

- Root: `Student`
- Children: `StudentDocument`, `StudentContactInfo`, `StudentFamilyInfo`
- Ownership: Student owns all child entities
- Cross-domain: Referenced by `Admission`, `Finance`, `Academic`

**Application Aggregate:**

- Root: `Application`
- Children: `ApplicationPayment`, `ApplicationDocument`
- Ownership: Application owns payments and documents
- Cross-domain: Creates `Student` on confirmation

**Faculty Aggregate:**

- Root: `Faculty`
- Children: `FacultyQualification`, `FacultyExperience`
- Ownership: Faculty owns qualifications
- Cross-domain: Referenced by `Academic` (timetable, attendance)

**Deliverable:** Aggregate documentation (Markdown)

**Duration:** 1 day

---

### STEP 7 — DOCUMENTATION UPDATE

**Actions:**

1. Update `README.md` with new architecture
2. Create architecture diagram (Mermaid or image)
3. Document domain boundaries
4. Update developer onboarding guide

**Deliverable:** Updated documentation

**Duration:** 1 day

---

## FINAL OUTPUT (STRICT FORMAT)

After completing all steps, provide:

1. ✅ **Inventory table** (all files categorized)
2. ✅ **Migration order** (dependency graph)
3. ✅ **Deleted files list** (legacy files removed)
4. ✅ **Final folder structure** (post-migration)
5. ✅ **Test results** (all passing)
6. ✅ **Transaction safety report** (critical flows wrapped)
7. ✅ **Aggregate documentation** (logical boundaries)
8. ✅ **Architecture diagram** (visual representation)

---

## TIMELINE SUMMARY

| Week         | Focus            | Deliverables                                |
| ------------ | ---------------- | ------------------------------------------- |
| **Week 1**   | Foundation       | Inventory, dependencies, enum consolidation |
| **Week 2-3** | Core domains     | hr → academic → student                     |
| **Week 4**   | Business domains | admission → finance → communication         |
| **Week 5**   | Campus + Safety  | campus migration, transactions, Alembic     |
| **Week 6**   | Polish           | Aggregate review, documentation             |

**Total: 5-6 weeks**

## CONSTRAINTS

- ✅ NOT in production → can move aggressively
- ❌ DO NOT invent new features
- ❌ DO NOT change business rules
- ❌ DO NOT change database schema (except via Alembic)
- ✅ CAN delete legacy files immediately after verification
- ✅ CAN break things temporarily (fix before merging)
- ✅ Migration must be testable and reversible (git)
- ✅ Campus is Phase-1 grouped domain ONLY
- ✅ Architecture clarity > short-term convenience

---

## SUCCESS CRITERIA

After migration is complete:

- ✅ **Zero business logic outside `domains/`**
- ✅ **Zero duplicate enums** (single source: `app/shared/enums.py`)
- ✅ **Zero stub service files**
- ✅ **Zero legacy folders** (`app/models/`, `app/schemas/`, `app/services/` deleted)
- ✅ **All domains follow identical structure** (models.py, schemas.py, repository.py, services.py, router.py)
- ✅ **All tests passing**
- ✅ **Alembic autogenerate works**
- ✅ **Critical flows have explicit transactions**
- ✅ **Documentation updated**
- ✅ **New developers can identify ownership instantly**

---

## EXECUTION CHECKLIST

Use this to track progress:

```markdown
### Week 1: Foundation

- [ ] Step 0: Clean start (branch, baseline)
- [ ] Step 1: Complete inventory
- [ ] Step 1.5: Dependency graph
- [ ] Step 2: Enum consolidation
- [ ] Step 2.5: Repository pattern (optional)

### Week 2-3: Core Domains

- [ ] Migrate: system/
- [ ] Migrate: hr/
- [ ] Migrate: academic/
- [ ] Migrate: student/

### Week 4: Business Domains

- [ ] Migrate: admission/
- [ ] Migrate: finance/
- [ ] Migrate: communication/

### Week 5: Campus + Safety

- [ ] Migrate: campus/
- [ ] Step 4: Alembic coordination
- [ ] Step 5: Transaction safety

### Week 6: Polish

- [ ] Step 6: Aggregate review
- [ ] Step 7: Documentation
- [ ] Final testing
- [ ] Merge to main
```
