Below is the **complete functional workflow** for your  
 **Academic Program → Batch → Year → Semester → Section → Practical Batch → Subjects hierarchy.**

---

# **🔷 MASTER 1 — PROGRAM CREATION WORKFLOW**

### **Screen: `Programs Master`**

| Field | Type | Validation |
| ----- | ----- | ----- |
| Program Code | Text | Unique (BHM, BCTCA) |
| Program Name | Text | Required |
| Short Name | Text | Required |
| Duration Years | Number | \> 0 |
| Total Semesters | Auto | \= duration\_years × 2 |
| Semester Based | Boolean | Default TRUE |
| Department | Dropdown | From Department Master |
| RNET Required | Boolean | Yes / No |
| Allow Installments | Boolean | Yes / No |
| Description | Text Area | Optional |
| Is Active | Toggle | Default ON |

### **System Actions**

* Calculate `total_semesters = duration_years * 2`

* Validate uniqueness of program\_code.

---

# **🔷 MASTER 2 — ACADEMIC BATCH CREATION**

### **Screen: `Academic Batch Master`**

| Field | Type | Auto / Manual |
| ----- | ----- | ----- |
| Program | Dropdown | Select BHM |
| Joining Year | Year | Manual |
| Duration Years | Auto | From Program |
| Start Year | Auto | \= Joining Year |
| End Year | Auto | \= Joining Year \+ Duration |
| Batch Code | Auto | `2024-2027` |
| Batch Name | Auto | `Batch 2024-2027` |
| Total Students | Number | Manual |
| Current Year | Auto | \= 1 |
| Status | Auto | active |

### **System Actions**

When batch is saved:

1. Auto-generate Program Years

2. Auto-generate Semesters under each Year

---

# **🔷 MASTER 3 — PROGRAM YEAR AUTO GENERATION**

For 3 Year program:

| Year No | Year Name |
| ----- | ----- |
| 1 | 1st Year |
| 2 | 2nd Year |
| 3 | 3rd Year |

---

# **🔷 MASTER 4 — SEMESTER AUTO GENERATION**

| Program Year | Semesters Created |
| ----- | ----- |
| 1st Year | Sem 1, Sem 2 |
| 2nd Year | Sem 3, Sem 4 |
| 3rd Year | Sem 5, Sem 6 |

---

# **🔷 MASTER 5 — SECTION MASTER**

### **Screen: `Sections Master`**

| Field |
| ----- |
| Section Name (A / B / C) |
| Max Students |
| Is Active |

### **Mapping**

Admin selects:

`Program → Batch → Year → Semester → Add Sections`

Example:

| Semester | Sections |
| ----- | ----- |
| Sem 1 | A, B |
| Sem 2 | A, B |

---

# **🔷 MASTER 6 — PRACTICAL BATCHES (Lab / Kitchen Groups)**

### **Screen: `Practical Batch Master`**

| Field |
| ----- |
| Batch Name (A1, A2, B1) |
| Section |
| Max Strength |
| Purpose (Bakery Lab / Hot Kitchen etc.) |

Mapping Path:

`Program → Batch → Year → Semester → Section → Add Practical Batches`

---

# **🔷 MASTER 7 — SUBJECT MASTER**

### **Screen: `Subjects Master`**

| Field |
| ----- |
| Subject Code |
| Subject Name |
| Subject Type (Theory / Practical) |
| Credits |
| Max Marks |
| Program |
| Semester |
| Is Active |

---

# **🔷 COMPLETE HIERARCHY FLOW**

`Academic Year (2024-25)`  
`└── Program (BHM)`  
    `└── Academic Batch (2024-2027)`  
        `└── Program Year (1st Year)`  
            `└── Semester 1`  
                `└── Section A`  
                    `└── Practical Batch A1`  
                    `└── Practical Batch A2`  
                `└── Subjects`

---

# **🔷 API RESPONSE STRUCTURE**

### **Endpoint**

`GET /api/academic-structure/hierarchy/{program_id}`

### **Response**

`{`  
  `"program": {`  
    `"program_code": "BHM",`  
    `"program_name": "Bachelor of Hotel Management"`  
  `},`  
  `"years": [`  
    `{`  
      `"year": {`  
        `"year_no": 1,`  
        `"year_name": "1st Year"`  
      `},`  
      `"semesters": [`  
        `{`  
          `"semester": {`  
            `"semester_no": 1,`  
            `"semester_name": "Semester 1"`  
          `},`  
          `"sections": [`  
            `{`  
              `"section": {`  
                `"name": "A"`  
              `},`  
              `"batches": [`  
                `{ "batch_name": "A1" },`  
                `{ "batch_name": "A2" }`  
              `],`  
              `"subjects": [`  
                `{ "subject_code": "FNB101", "subject_name": "Food Production I" }`  
              `]`  
            `}`  
          `]`  
        `}`  
      `]`  
    `}`  
  `]`  
`}`

---

# **🔷 WHY THIS WORKFLOW IS CRITICAL**

This master hierarchy automatically powers:

| Module | Dependency |
| ----- | ----- |
| Student Admission | Program \+ Batch |
| Attendance | Section \+ Practical Batch |
| Exam Hall Ticket | Semester \+ Subject |
| Result Processing | Subject \+ Semester |
| Fee Mapping | Program \+ Batch |
| Hostel Allocation | Batch |
| IET Tracking | Program \+ Semester |
| Migration | Batch Year Progression |

---

This is the **academic backbone** of your entire College ERP.  
 Once this is implemented correctly, all other modules become simple configurations.

When creating a Batch like **2026–29**, you only select the **Program \+ Regulation**  
 and the ERP automatically applies **subjects, credits, marks pattern & promotion rules**.

---

# 

# 

# 

# 

# 

# 

#  **– REGULATION ENGINE**

**College ERP – Academic Control System**

---

## **1\. PURPOSE**

To manage:

* Academic regulations batch-wise

* Subject structure per semester

* Marks & exam pattern

* Credit-based promotion system

* Automatic academic migration

---

## **2\. DATABASE DESIGN**

---

### **2.1 `regulations`**

| Field | Type |
| ----- | ----- |
| id | UUID |
| regulation\_code | VARCHAR(10) |
| regulation\_name | VARCHAR(100) |
| program\_id | UUID |
| promotion\_model | ENUM('CREDIT\_BASED') |
| year1\_to\_year2\_min\_percentage | INT |
| year2\_to\_year3\_min\_year2\_percentage | INT |
| min\_internal\_pass | INT |
| min\_external\_pass | INT |
| min\_total\_pass | INT |
| is\_active | BOOLEAN |
| created\_at | DATETIME |

---

### **2.2 `regulation_semesters`**

| Field | Type |
| ----- | ----- |
| id | UUID |
| regulation\_id | UUID |
| program\_year | INT |
| semester\_no | INT |
| total\_credits | INT |

---

### **2.3 `regulation_subjects`**

| Field | Type |
| ----- | ----- |
| id | UUID |
| regulation\_id | UUID |
| program\_id | UUID |
| subject\_code | VARCHAR(20) |
| subject\_name | VARCHAR(100) |
| short\_name | VARCHAR(20) |
| subject\_type | ENUM('THEORY','PRACTICAL','INTERNSHIP') |
| program\_year | INT |
| semester\_no | INT |
| hours\_per\_session | INT |
| credits | INT |
| internal\_max | INT |
| external\_max | INT |
| total\_max | INT |
| passing\_percentage | INT |
| has\_exam | BOOLEAN |
| has\_assignments | BOOLEAN |
| evaluation\_type | ENUM('EXAM','CONTINUOUS','ATTENDANCE\_ONLY','CERTIFICATION') |
| is\_active | BOOLEAN |

---

### **2.4 `regulation_promotion_rules`**

| regulation\_id | from\_year | to\_year | min\_prev\_year\_pct | min\_current\_year\_pct |
| ----- | ----- | ----- | ----- | ----- |
| R26 | 1 | 2 | 50 | 0 |
| R26 | 2 | 3 | 100 | 50 |

---

## **3\. SUBJECT CREATION LOGIC (UI → REGULATION)**

### **Add Subject Fields**

| UI Field | DB Column |
| ----- | ----- |
| Subject Code | subject\_code |
| Subject Name | subject\_name |
| Program | program\_id |
| Subject Type | subject\_type |
| Program Year | program\_year |
| Semester | semester\_no |
| Hours / Session | hours\_per\_session |
| Short Name | short\_name |
| Max Marks | total\_max |
| Mid Exam Marks | internal\_max |
| Passing % | passing\_percentage |
| Credits | credits |
| Has Exam | has\_exam |
| Has Assignments | has\_assignments |
| Active | is\_active |

### **Auto Calculation**

`IF has_exam = false:`  
    `evaluation_type = 'CONTINUOUS'`  
    `external_max = 0`  
`ELSE:`  
    `evaluation_type = 'EXAM'`  
    `external_max = total_max - internal_max`

---

## **4\. BATCH CREATION LOGIC**

When Batch is created:

`COPY regulation_subjects → batch_subjects`  
`COPY regulation_semesters → batch_semesters`  
`COPY regulation_promotion_rules → batch_promotion_rules`

---

## **5\. PROMOTION ENGINE (CREDIT BASED)**

`year1_total = credits(Sem1 + Sem2)`  
`year2_total = credits(Sem3 + Sem4)`

`earned_year1 = passed_credits(Sem1 + Sem2)`  
`earned_year2 = passed_credits(Sem3 + Sem4)`

`IF student_year == 1:`  
    `IF earned_year1 >= year1_total * 0.50 → PROMOTE`

`IF student_year == 2:`  
    `IF earned_year1 == year1_total AND earned_year2 >= year2_total * 0.50 → PROMOTE`

---

## **6\. RESULT ENTRY LOGIC**

| Evaluation Type | Entry |
| ----- | ----- |
| EXAM | Internal \+ External |
| CONTINUOUS | Internal only |
| ATTENDANCE\_ONLY | Attendance % |
| CERTIFICATION | Upload Certificate |

---

## **7\. SYSTEM GUARANTEE**

| Feature | Supported |
| ----- | ----- |
| Regulation auto-applies to batch | ✔ |
| Credit-based promotions | ✔ |
| No-exam subjects | ✔ |
| Future syllabus safe | ✔ |
| Autonomous college ready | ✔ |

