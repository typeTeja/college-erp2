**Role:**
You are a **Principal Software Architect (DDD + Academic Systems expert)**.
Your task is to implement the **Academic Structure** with **correct lab batch distribution logic** for a College ERP.

This prompt **supersedes all previous academic prompts**.

---

## 🔒 SCOPE LOCK (DO NOT VIOLATE)

Work **ONLY** on:

- Academic Structure
- Program → Batch → Semester → Section → Lab Batch → Subject

🚫 Do NOT touch:

- Students
- Attendance
- Exams
- Fees
- Hostel / ODC
- RBAC / Auth
- Frontend UI

---

## 🎯 CORE PROBLEM TO SOLVE (LAB DISTRIBUTION)

### Given Academic Reality

```
Semester 1
 ├── Sections
 │    ├── Section A (60 students)
 │    └── Section B (60 students)
 │
 └── Lab Batches (SHARED ACROSS SECTIONS)
      ├── Lab Batch A (40 students)
      ├── Lab Batch B (40 students)
      └── Lab Batch C (40 students)
```

⚠️ **Critical Insight**
Lab batches:

- ❌ Do NOT belong to a single section
- ❌ Are NOT split per section
- ✅ Are shared at **semester level**
- ✅ Pull students from **multiple sections**

---

## 🧠 CORRECT ACADEMIC MODEL (MANDATORY)

### ✅ Correct Hierarchy

```
Program
 └── AcademicBatch
     └── BatchYear
         └── BatchSemester
             ├── Sections
             │    ├── Section A
             │    └── Section B
             │
             └── PracticalBatches
                  ├── Lab Batch A
                  ├── Lab Batch B
                  └── Lab Batch C
```

🚫 **PracticalBatch MUST NOT be under Section**

---

## 📦 MODELS TO IMPLEMENT (ACADEMIC ONLY)

### Required Models

1. `Program`
2. `Regulation`
3. `RegulationSemester`
4. `RegulationSubject`
5. `AcademicBatch`
6. `BatchYear`
7. `BatchSemester`
8. `Section`
9. `PracticalBatch`
10. `BatchSubject`
11. `PracticalBatchStudent` (JOIN TABLE — REQUIRED)

---

## 🔗 KEY RELATIONSHIP RULES (NON-NEGOTIABLE)

### 1️⃣ Section

- Belongs to `BatchSemester`
- Used for:
  - Theory subjects
  - Roll numbering
  - Class identity

### 2️⃣ PracticalBatch

- Belongs to `BatchSemester`
- NOT linked to Section
- Has:
  - Capacity
  - Lab type (Kitchen / Bakery / FO / Housekeeping)

### 3️⃣ PracticalBatchStudent (CRITICAL)

This table **solves the lab distribution issue**.

It maps:

```
Student → PracticalBatch
```

Rules:

- A student belongs to:
  - ONE Section
  - ONE PracticalBatch per practical subject

- Students from different sections CAN be in the same lab batch

---

## 🧩 SUBJECT RULES

### Theory Subject

- Linked to:
  - BatchSemester
  - Section (implicitly via student)

### Practical Subject

- Linked to:
  - BatchSemester
  - PracticalBatch

- Attendance & evaluation happen at **PracticalBatch level**

🚫 Never link practical subjects directly to Section.

---

## ⚙️ BATCH CREATION AUTOMATION (MANDATORY)

When `AcademicBatch` is created:

System must:

1. Auto-generate:
   - BatchYears
   - BatchSemesters

2. Allow Admin to create:
   - Sections (A, B, C…)
   - PracticalBatches (A, B, C…)

3. Copy:
   - RegulationSubjects → BatchSubjects

4. Allow **manual or rule-based student → lab batch allocation**

⚠️ Auto-allocation is optional, but structure must support it.

---

## 🧠 DESIGN PRINCIPLES (DO NOT BREAK)

1. **Sections = academic identity**
2. **Lab batches = operational grouping**
3. **Lab batches are semester-scoped, not section-scoped**
4. **Student–Lab relationship is many-to-one**
5. **Academic structure must reflect real college operations**

---

## 🚦 SYSTEM GUARANTEES

Before stopping, ensure:

- App boots cleanly
- DB initializes without FK hacks
- No circular dependencies
- Academic APIs load correctly
- Structure supports:
  - 120 students
  - 2 sections
  - 3 shared lab batches

If any fails → STOP.

---

## ✅ SUCCESS CRITERIA

You are DONE only when:

- Sections and lab batches coexist correctly
- Lab batches can span multiple sections
- Student → Lab allocation is clean and extensible
- No future module (attendance/exams) will require restructuring

---

## 🧠 FINAL RULE (WRITE THIS IN STONE)

> **Sections divide classrooms.
> Lab batches divide physical capacity.
> Never mix the two.**

## Strategic Advice (Important)

🔵 You Did One Thing Extremely Right

- Your Academic + Regulation design is:
  - Future-proof
  - Autonomous-college ready
  - NAAC / UGC friendly

- Much better than 90% of college ERPs

- Don’t dilute it by rushing.

## 🔵 Recommended Dev Rule (Write This Down)

No module is allowed to exist unless its parent master is complete

If:

- Attendance exists → Subject must exist
- Subject exists → Regulation must exist
- Regulation exists → Program must exist
