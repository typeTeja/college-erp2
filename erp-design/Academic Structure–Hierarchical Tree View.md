### 🎯 ROLE

You are a **Senior Frontend Architect + UX Engineer** building an **interactive Academic Structure Viewer** for a **College ERP system**.

Your task is to design and implement a **visual, expandable, nested tree view** that clearly represents the **academic hierarchy** and allows users to **toggle, explore, and inspect** structure nodes without confusion.

This is a **READ + MANAGE view**, not just a static diagram.

---

## 🧩 CORE DISPLAY REQUIREMENT (NON-NEGOTIABLE)

### ✅ Canonical Academic Hierarchy to Display

```
Academic Year
 └── Program
      └── Regulation
           └── Academic Batch
                └── Year
                     └── Semester
                          ├── Sections (THEORY)
                          │    ├── Section A
                          │    └── Section B
                          │
                          └── Lab Batches (PRACTICAL)
                               ├── Lab A (40)
                               ├── Lab B (40)
                               └── Lab C (40)
```

### ❌ Forbidden Visual Structures

- ❌ Lab Batches inside Sections
- ❌ Mixing theory & practical under same node
- ❌ Flat lists without hierarchy

---

## 🖥️ UI COMPONENT REQUIREMENTS

### 1️⃣ Tree View (Left Panel – Primary)

Implement a **nested, collapsible tree view** with:

- ▶ Expand / ▼ Collapse toggles
- Indentation to show hierarchy depth
- Icons to differentiate node types
- Smooth animation on expand/collapse
- Lazy loading for large trees

### Node Icons (Recommended)

- 📅 Academic Year
- 🎓 Program
- 📘 Regulation
- 🧊 Batch
- 🗂 Year
- 🧮 Semester
- 📖 Sections (Theory)
- 🔬 Lab Batches (Practical)

---

### 2️⃣ Node Interaction Rules

When a user **clicks a node**:

- Highlight the node
- Load details in **Right Panel**
- Do NOT auto-expand siblings
- Preserve expanded state on refresh (local state)

---

## 🧭 TREE BEHAVIOR RULES

### Expand / Collapse Logic

- Each node expands independently
- Parent collapse hides all children
- Toggle icons only appear if children exist

### Scroll & Usability

- Tree must be vertically scrollable
- Sticky header: “Academic Structure”
- Search box to filter nodes (by name/code)

---

## 📊 RIGHT PANEL – CONTEXT DETAILS

Based on selected node type, show:

### If Semester Selected

- Semester name
- Total sections count
- Total lab batches count
- Student strength summary

### If Section Selected (Theory)

- Section name
- Student count
- Theory subjects
- Class coordinator
- Theory timetable link

### If Lab Batch Selected (Practical)

- Lab name
- Capacity
- Assigned practical subjects
- Faculty in charge
- Practical timetable link
- Cost ledger shortcut

---

## 🧩 DATA CONTRACT (MANDATORY SHAPE)

The UI MUST expect **parallel children**, not nested ones.

### Example API Response (Semester Node)

```json
{
  "semester": {
    "id": "sem1",
    "name": "Semester 1"
  },
  "sections": [
    { "id": "secA", "name": "A", "type": "THEORY", "strength": 62 },
    { "id": "secB", "name": "B", "type": "THEORY", "strength": 58 }
  ],
  "lab_batches": [
    { "id": "labA", "name": "Lab A", "capacity": 40 },
    { "id": "labB", "name": "Lab B", "capacity": 40 },
    { "id": "labC", "name": "Lab C", "capacity": 40 }
  ]
}
```

### UI MUST Render

```
Semester 1
 ├─ Sections (2)
 │   ├─ A
 │   └─ B
 └─ Lab Batches (3)
     ├─ Lab A
     ├─ Lab B
     └─ Lab C
```

---

## 🎨 UX & VISUAL GUIDELINES

- Use **tree indentation**, not cards
- Use **badges** for:
  - Student count
  - Capacity

- Color hinting:
  - Blue → Theory
  - Green → Practical

- Avoid clutter — hierarchy clarity > decoration

---

## ⚙️ OPTIONAL ADVANCED FEATURES (IF POSSIBLE)

- Context menu (right-click):
  - View
  - Edit (role-based)
  - Audit log

- Breadcrumb on top:

  ```
  Academic Year > BHM > Batch 2024–27 > Sem 1 > Lab A
  ```

- Zoom / full-screen tree mode

---

## 🔐 ACCESS CONTROL

- Read-only for Faculty
- Editable for Admin / Academic Office
- No drag-drop unless explicitly enabled later

---

## 🧪 VALIDATION TESTS (UI MUST PASS)

1. Semester expands into **Sections + Lab Batches separately**
2. Lab batches never appear under Sections
3. Collapse Semester hides both branches
4. Clicking Section never shows practical data
5. Clicking Lab Batch never shows theory data
6. Tree state preserved on refresh

---

## 📌 FINAL UX PRINCIPLE (VERY IMPORTANT)

> “The tree must visually teach the academic rules.
> If a user misunderstands theory vs practical after seeing this view, the UI has failed.”
