**PROMPT STARTS BELOW**

---

You are an expert ERP architect and database modeller.
Generate **complete, realistic, relational SEED DATA** for a College Management ERP based on the full ERP specification provided (all modules, roles, workflows, and ODC requirements). The ERP includes modules described in the SRS: admissions, student master, faculty, subjects, timetable, attendance, exam, fees, library, hostel, ODC, monitoring, gatepass, SSE, accounts, security, etc.  

### **1️⃣ Generate Seed Data for ALL User Roles**

Create complete records for each role:

* Super Admin
* Principal / Management
* Admission Officer
* Student Support Executive (SSE)
* Accounts Team
* Faculty (10 sample faculty with departments, subjects, timetable slots)
* Students (30 students across Years 1–3, multiple sections/batches)
* Parents (linked to students)
* Library Staff
* Hostel Warden
* Security Staff
* Exam Cell Staff
* Placement/ODC Coordinator

For each user include:

```
id
role
name
email
mobile
password-hash placeholder
profile fields
department (if applicable)
permissions (JSON)
```

### **2️⃣ Student Master Seed Data**

For 30 sample students include:

* Personal details
* Parent details
* Course → Year → Semester → Section mapping
* Admission status (Confirmed)
* Fee plan (installments + paid/unpaid)
* Attendance summary (random realistic %)
* Internal marks (Mid-1, Mid-2, Assignment)
* Practical performance sample
* Gatepass history (2–3 entries)
* Library issued books
* Hostel status: 10 hostel, 20 day scholars

### **3️⃣ Faculty & Academic Seed Data**

Generate:

* Departments (Front Office, F&B, Housekeeping, Kitchen, Bakery, Management)
* Subject master list for BHM/BCT across Sem1–Sem6
* Theory + Practical subjects
* Elective groups with students
* Lesson plan: 3 units per subject with topics
* Faculty → Subject mapping
* Faculty timetable (realistic weekly schedule)
* Faculty attendance (late/early sample entries)

### **4️⃣ Timetable Seed Data**

Create a complete timetable for:

* Year 1 Sem1 Section A
* Year 2 Sem3 Section A
* Year 3 Sem5 Section A

Include:

* Theory hour slots
* Practical 2/4/6-hour blocks
* Library period
* Elective groups
* Faculty mapping

### **5️⃣ Attendance Seed Data**

Generate:

#### Student Attendance

* Daily attendance for 2 sample weeks
* Period-wise attendance for theory + practical
* Attendance % calculations
* Auto shortfall tagging for <75%

#### Faculty Attendance

* Late entry
* Early exit
* CCL earned
* Leave entries

### **6️⃣ Exam Module Seed Data**

Generate:

* Mid-1 & Mid-2 marks
* Assignment marks
* Internal mark calculation
* Exam timetable
* Sample OMR marks input (for 5 students)
* Re-exam eligibility for 2 students

### **7️⃣ Finance / Fees Seed Data**

Include:

* Fee structure (Course + Academic Year)
* Scholarships (3 slabs applied to students)
* Installments
* Paid / due amounts
* Fines
* Easebuzz payment transaction samples

### **8️⃣ Library Seed Data**

Generate:

* Book master (20 books + topics)
* Issue/return logs
* QR IDs
* 5 recommendation requests

### **9️⃣ Hostel Seed Data**

Generate:

* Block → Floor → Room → Bed mapping
* 10 students allocated
* In/Out logs
* Daily menu sample
* Monthly hostel P&L (expenses + revenue)

### **🔟 Full ODC Module Seed Data (Real-World Simulation)**

Create a complete realistic scenario for ODC:

#### Hotels

* 5 partner hotels with contact details
* 10 ODC request entries (event type, date, headcount, rate)

#### Student Selection

Use selection priorities:

* 3rd year → highest
* 2nd year → medium
* 1st year → only low-priority ODC

Include:

* Student shortlist
* Parent consent (YES/NO)
* Rejection reasons

#### Hotel Attendance & Performance

For each ODC event include:

* Student attendance
* Hours worked
* Performance score

#### Billing & Settlement

Generate:

* Hotel bill amount (rate × headcount × hours)
* Student payout calculation
* College share (if applicable)
* Final settlement status (Pending / Settled)
* CSV export sample rows

### **🔟 Bonus: Monitoring & Discipline Seed Data**

* L1, L2, L3 Issues
* SSE call logs
* Parent meeting notes

### **FORMAT REQUIRED**

Output seed data in ANY ONE of the following formats:

* **JSON Seed Files** (preferred)
* SQL INSERT statements
* Prisma Seed Script (TS)
* CSV blocks

Ensure relationships remain valid and foreign keys match.

---

**PROMPT ENDS**