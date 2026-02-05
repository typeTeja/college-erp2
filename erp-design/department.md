The client has confirmed that **Department must be a central, system-level master**, not part of the HR module.

The current implementation incorrectly places **Department under HR**, which must be refactored.

---

### Correct Definition

**Department is a Core Institutional Master** used across academic, operational, and HR modules.

It represents **academic & operational ownership**, not employee grouping.

---

### Required Refactor Instructions

#### 1️⃣ Create Central Department Master

Move / create **Department** under:

```
System / Core Masters
└── Department
```

Department must exist **independent of HR**.

---

#### 2️⃣ Department Responsibilities

Department must support:

- Academic subject ownership
- Faculty academic governance (HOD)
- Lab / Kitchen ownership
- Assets & inventory responsibility
- Duty rota control
- Department-level reporting & audits

---

#### 3️⃣ HR Module Changes

HR module must **NOT define departments**.

HR should only:

- Reference `department_id`
- Map faculty/staff to:
  - primary_department_id
  - secondary_department_id (optional)

- Use department for:
  - reporting hierarchy
  - leave approval routing
  - workload grouping

---

#### 4️⃣ Database Refactor

**New Table (Central) reference only create as per project structure:**

```
departments
- id
- department_code
- department_name
- description
- hod_faculty_id
- is_active
- created_at
```

**HR Tables (Reference Only):**

```
faculty.department_id → FK departments.id
faculty.secondary_department_id → FK departments.id
```

Remove any department table or logic embedded inside HR schema.

---

#### 5️⃣ API Refactor

✅ Correct:

```
/system/departments
```

❌ Incorrect:

```
/hr/departments
```

All modules must consume departments via the system API.

---

#### 6️⃣ Module Integrations

Department must be referenced by:

- Subject Master (ownership)
- Timetable (workload)
- Practical Labs
- Assets & Inventory
- Duty Rota
- Reports & Dashboards
- HR (staff mapping only)

---

#### 7️⃣ UI Placement

Departments must appear under:

```
Masters → Departments
```

Editable by:

- Admin
- Principal

View-only or selectable by:

- HR
- Academic admins

---

### Final Rule (Do Not Violate)

> If a concept is required **before hiring staff**, it must **not belong to HR**.

Department is such a concept.

---

### Expected Outcome

- No Department creation logic inside HR
- Single source of truth for Department
- Clean cross-module references
- No circular dependencies
