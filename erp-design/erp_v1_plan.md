# **✅ PART INDEX (what you will receive)**

### **PART 1 — Executive Summary & System Overview**

* Purpose, goals, stakeholders

* High-level solution summary

* Terminology glossary

* Business objectives & constraints

### **PART 2 — Technical Architecture**

* System architecture diagram

* Technology stack

* Micro-modules structure

* Deployment topologies

* DevOps workflows

* Security & Governance

* Performance & Availability goals

### **PART 3 — Data Architecture & Database Specification**

* Full ER diagram

* Complete Postgresql schema (all modules)

* DB naming conventions

* Indexing strategy

* Archival & backup requirements

### **PART 4 — Admissions & Student Onboarding**

(including your simplified public quick-apply form \+ full application)

* Public application (minimal fields)

* Easebuzz fee payments

* Document upload workflow

* Manual entrance exam \+ marks → scholarship scoring rules

* Auto scholarship engine

* Admissions offer generation

* Student account auto-creation

* Status workflow diagrams

### **PART 5 — Academic Structure**

* Course master, class, section

* Year → Semester → Batch

* Subject master (theory/practical parameters)

* Lesson plan (units → topics → expected periods)

* Course mapping & dependencies

### **PART 6 — Attendance & Practical Modules**

* Theory attendance

* Practical session attendance

* Practical performance scoring model

* Daily practical cost recording

* Cost ledger workflow

* Student cost allocation workflow

### **PART 7 — Timetable & Faculty Management**

* Timetable logic (theory/practical hour mapping)

* Faculty workload rules

* Class adjustment ledger

* Classroom conflict detection engine

### **PART 8 — Exams, Internal Marks, Re-Exam Module & Question Bank**

* Mid exam structure

* Assignment logic

* Internal marks calculation

* Re-exam eligibility logic

* Re-exam scheduling

* Re-exam marks entry \+ replacement policy

* Question bank structure

* Auto paper generation engine

* OCR / QR exam paper scanning

### **PART 9 — Finance & Fees Module**

* Academic year fee structures

* Multi-installment logic

* Fee concessions workflow

* Fine management

* Auto-blocking rules (exam, promotion)

* Re-exam fee handling

* Practical cost recovery

* Easebuzz integration (initiate \+ webhook \+ reconciliation)

### **PART 10 — Extended Modules**

#### **Placements Module**

* Employer management

* Placement drives

* Student applications

* Interview rounds

* Offer management

* Placement analytics

#### **ODC Module**

* Hotel request

* Student selection priorities

* ODC confirmations

* Billing & student payouts

#### **Hostel Module**

* Bed allocation

* Food & menu planning

* Gatepass

* P\&L

#### **Library**

* Book master

* Topic index

* Scan entry/exit

* Issues/returns

* Fine logic

#### **Student Monitoring**

* Issue → L1 → L2 → L3 escalations

* Parent communication (recording)

* Action notes & evidence

# **1\. Introduction**

## **1.1 Purpose of the Document**

This Software Requirements Specification (SRS) defines the complete functional, non-functional, operational, and regulatory requirements for the **College Management ERP System** developed for **Regency College of Hotel Management**.

It serves as a formal reference for:

* Management & Academic Leadership

* ERP Development Team

* QA & Testing Team

* System Integrators

* External Vendors & Auditors

All modules, workflows, rules, and constraints are documented comprehensively.  
 Technical details (API, database schema) are provided in a separate **ANNEXURE** as agreed.

---

## **1.2 Scope of the System**

The ERP system will automate and streamline all academic, administrative, financial, and compliance processes across the college lifecycle, including:

* Admissions & Scholarship Processing

* Student Master & Document Management

* Faculty Management

* Timetable & Class Scheduling

* Attendance (Theory \+ Practical)

* Practical Cost Ledger & Recovery

* Internal Exams, Re-Exams, Question Bank, Auto Paper Generation

* Fee Management & Easebuzz Integration

* Placements & Employer Coordination

* ODC (Hotel Training), Hostel, Library

* Student Monitoring & Discipline

* Gatepass System, Visitor Management

* Reports, Dashboards & Notifications

The system will support:

* Students

* Faculty

* Exam Cell

* Administration

* Finance / Accounts

* Training & Placement Office

* Hostel & Library Staff

* Management / Principal

---

## **1.3 Definitions, Acronyms & Abbreviations**

| Term | Definition |
| ----- | ----- |
| ERP | Enterprise Resource Planning System |
| SSE | Student Support Executive |
| ODC | Outdoor Catering (Hotel Training) |
| PCR | Practical Cost Record |
| Mid Exams | Internal periodic examinations |
| L1/L2/L3 | Escalation levels in student monitoring |
| AGO | Academic Governance Office |
| Easebuzz | Payment gateway provider |
| OCR | Optical Character Recognition system |
| COE | Controller of Examinations |
| PCO | Practical Cost Officer |
| DB | Database |

---

## **1.4 Intended Audience**

* College Management & Board Members

* Department Heads

* ERP Development Team

* QA Testers

* Integration Partners (Easebuzz, SMS Providers, OCR Vendors)

* Accreditation Agencies (NAAC / AICTE / UGC)

---

## **1.5 System Overview (High-Level Description)**

The ERP consists of multiple interconnected modules running on a central web-based platform accessible via browser and mobile devices.

### **Major System Themes**

1. **End-to-End Academic Lifecycle Automation**  
    From admission → academics → exams → placements.

2. **Centralized Data Repository**  
    Single source of truth for all student, faculty, institutional data.

3. **Role-Based Access Control (RBAC)**  
    Secure, controlled access for different user groups.

4. **Workflow-Driven Processes**  
    Approvals → notifications → documents → logs.

5. **Deep Integration**

   * Payment gateway (Easebuzz)

   * OCR for answer sheets

   * Biometric attendance

   * SMS/WhatsApp Providers

6. **Audit-Ready & Compliant**  
    Record retention, audit trails, role permissions, and archival features included.

---

## **1.6 References**

* IEEE-830 SRS Standard

* College academic regulations

* UGC/AICTE guidelines

* Scholarship and examination rules specified by the institution

* Easebuzz Payment Gateway Documentation

* Internal attendance and promotion regulations

---

## **1.7 Document Structure**

This SRS document is organized into sections aligned with IEEE-830 standards:

* **Part 1:** Executive Summary & System Overview

* **Part 2:** Overall Description

* **Part 3:** System Features (Module-wise Functional Requirements)

* **Part 4:** External Interface Requirements

* **Part 5:** Non-functional Requirements

* **Part 6:** Other Requirements (Compliance, Security, Audit, Backup)

**ANNEXURES (Separate Document):**

* API specifications

* Database schema (posgressql)

* Integration details (OCR, Easebuzz etc.)

* Background job workflows

---

# **✅ PART 1 COMPLETE**

# **PART 2 — OVERALL DESCRIPTION (UPDATED WITH LEAVE MANAGEMENT MODULE)**

*(Final, Complete Version — IEEE-830 SRS Format)*

---

# **2\. Overall Description**

## **2.1 Product Perspective**

*(unchanged except referencing leave module)*  
 The ERP is a unified system covering admissions, attendance, exams, finances, hostel, library, placements, ODC, uniforms, assets, and **staff leave management**.

---

## **2.2 System Functions (High-Level Summary)**

All previous modules remain unchanged.

A new major module is added below:

---

# **🔵 M. Leave Management Module (NEW)**

### **Purpose**

To automate the process of applying, approving, tracking, adjusting classes, and maintaining the leave ledger for all faculty and staff members.

### **Scope**

The leave system covers:

* Faculty

* Admin staff

* Department heads

* Support staff

* Principal approval workflow

---

## **M1. Leave Types Supported**

System must support configurable leave types:

| Leave Type | Description | Deduction Impact |
| ----- | ----- | ----- |
| **CL – Casual Leave** | Short, personal leave | No salary deduction |
| **SL – Sick Leave** | Health-related leave | No salary deduction |
| **EL – Earned Leave** | Long-term leave | May encash/adjust |
| **Comp Off** | Given for extra working days | No salary deduction |
| **LOP – Loss of Pay** | When leave balance insufficient | Salary deduction |

Leave balances are configurable per role/year.

---

## **M2. Leave Application Workflow**

1. Staff applies for leave through portal:

   * Leave type

   * Date(s)

   * Reason

   * Supporting documents (optional)

   * Class adjustment plan (faculty only)

2. System checks:

   * Eligibility

   * Leave balance available

   * Conflicts (exam days, invigilation, timetable slots)

3. Leave sent to Reporting Head for approval.

4. Reporting Head can:

   * Approve

   * Reject

   * Forward to Principal (e.g., \>2 days leave)

5. Upon approval, ERP:

   * Updates leave ledger

   * Updates timetable (faculty)

   * Sends notification to department, SSE (if class impacted)

   * Marks future attendance sessions as “On Leave” for faculty

---

## **M3. Class Adjustment Workflow (Faculty Only)**

When a faculty applies for leave:

1. ERP identifies all classes scheduled during leave period using timetable.

2. Faculty must propose class adjustment options:

   * Alternate faculty

   * Swap sessions

   * Reschedule class

3. ERP validates no timetable conflicts.

4. Substitute faculty receives notification and must accept or reject.

5. Once finalized:

   * Adjustment recorded in **Class Adjustment Ledger**

   * Students notified automatically

   * Attendance device expects new substitute for those periods

---

## **M4. Leave Ledger (Eligibility, Utilisation, Balance)**

Each staff member has a leave ledger:

* Annual eligible leave

* Leave utilised

* Leave balance

* Encashable leave (if applicable)

* LOP applied

Ledger updates automatically when leave is:

* Approved

* Cancelled

* Modified

* Converted to LOP

Principal/Admin can override ledger entries with justification.

---

## **M5. Integration with Other Modules**

| Module | Integration |
| ----- | ----- |
| **Attendance** | Faculty on leave auto-marked as “On Duty/Leave” |
| **Timetable** | Class adjustment updates the slot with substitute faculty |
| **Class Adjustment Ledger** | Stores class changes due to leave |
| **Payroll (future module)** | LOP affects salary |
| **Notifications** | Alerts to faculty, HOD, SSE, substitute |
| **Uniform/Assets** | Not affected |
| **Student Monitoring** | Adjusted classes update student records |

---

## **M6. Leave Reporting & Dashboards**

### **Department Dashboard**

* Staff on leave today

* Upcoming leaves

* Leave balance summary per staff

### **HR/Admin Dashboard**

* Monthly leave usage

* LOP summary

* High absenteeism detection

* Average leave consumption per department

### **Audit Log**

* Every application, approval, rejection, modification is recorded.

---

## **M7. Constraints**

* No backdated leave unless Admin overrides.

* Faculty leave cannot overlap invigilation/exam duty unless approved by Exam Cell.

* LOP applied automatically when leave balance insufficient.

* Class adjustment MUST be completed before leave approval.

---

## **M8. Assumptions**

* Leave policy is defined by management.

* Reporting Head hierarchy is predefined.

* Substitute faculty will respond promptly to adjustment requests.

---

## **M9. Phasing**

### **Phase 1**

* Leave application

* Leave approval

* Leave ledger

### **Phase 2**

* Class adjustment workflow

* Calendar-based leave view

* Department dashboards

### **Phase 3**

* Payroll integration

* Auto-detection of absenteeism patterns

* Mobile app push notifications

---

# **⭐ LEAVE MODULE SUCCESSFULLY ADDED TO PART 2**

Your **PART 2 — Overall Description** is now fully updated with:

* Uniform Module

* Asset Management Module

* Leave Management Module

* QR Scanning Enhancements

* All previous modules

# **🔵 PART 3 — MODULE 1: ADMISSIONS & STUDENT ONBOARDING (COMPLETE, UPDATED)**

### ***(Copy/Paste Ready — Updated with New Requirements)***

---

# **3.1 Admissions Module**

## **3.1.1 Purpose**

To manage the end-to-end admission workflow starting from a minimal quick-application form to full admission confirmation, including document verification, hostel assignment, fee processing, scholarship decisions, ID card generation, original document tracking, and OMR-based entrance exams.

---

## **3.1.2 Scope**

This module covers:

* Quick online form (short fields for maximum conversions)

* Application fee payment & payment failure tracking

* Full application form completion

* Document uploads & original certificate submission tracking

* Migration & equivalency certificate tracking (for non-local students)

* Entrance exam OMR sheet generation

* Scholarship calculation

* Admission confirmation

* Tentative admission vs Confirmed admission logic

* Hostel assignment & hostel undertaking generation

* ID card generation with validity period

* Internal circular module

* Uploading university marks memos for students/parents

---

## **3.1.3 Actors**

* Applicant

* Admissions Officer

* Accounts Staff

* Hostel Warden

* Principal / Approval Authority

* Exam Cell

* System (automations)

---

# **3.1.4 Functional Requirements (FR)**

---

# **🔹 FR1: Quick Application Form (Public Link — Minimal Fields)**

The ERP shall provide a mobile-friendly, minimalistic form with mandatory fields:

**Required Fields:**

* Full Name

* Date of Birth

* Gender

* Mobile Number

* Email ID

* State

* Address (short)

* Board (CBSE/ICSE/State Board)

* Group of Study (MPC/BiPC/CEC/HEC/Other)

* Father Name

* Father Mobile Number

* Course Applying For

* Checkbox: **“I agree to terms & conditions”**

### **Additional Requirements:**

* If payment fails, ERP must store the application as **“Payment Failed – Follow-up Required”**

* Admissions team must have a **follow-up dashboard** showing:

  * Payment failed

  * Pending payment

  * Not completed full form

Purpose: *To nurture leads and convert them immediately.*

---

# **🔹 FR2: Application Fee Payment (Easebuzz) \+ Failure Tracking**

* System generates a payment link via Easebuzz

* ERP listens to webhook to confirm payment

* Status updated to:

  * **“Fee Paid”** (success)

  * **“Payment Failed”**

  * **“Pending Payment”**

A dedicated **“Abandoned Applications Funnel”** is required to follow up failed payments.

---

# **🔹 FR3: Full Application Form Unlock (Post Payment)**

After fee payment, system unlocks full application form:

Sections include:

### **Personal Details**

* Aadhaar number

* Identification marks

* Complete address

### **Education Details**

* Previous qualification

* Board

* Year of passing

* Max marks

* Secured marks / grade

### **Parent & Guardian Details**

* Father & mother name

* Mobile numbers & email

* Local guardian (if applicable)

### **Hostel Requirement**

* Student selects **YES/NO**

* If YES:

  * Hostel undertaking generated

  * Hostel fee added to fee plan

  * Status \= **“Hostel Requested”**

---

# **🔹 FR4: Mandatory Documents Upload (Expanded Requirements)**

System must support uploads of:

* Medical certificate

* All study certificates (multiple files allowed)

* Photo

* Signature

* Anti-ragging affidavit

* Substance abuse affidavit

* Transfer certificate (if applicable)

* Migration certificate (for non-locals)

* Equivalency certificate (if required by Board)

### **NEW: Non-local Student Document Tracking**

If board ≠ Telangana/Andhra Pradesh:

* System must **automatically require**

  * Migration certificate

  * Equivalency certificate

* Document status visible in student and admin portal

### **NEW: Original Document Submission Register**

ERP must track:

* Which original certificates were submitted

* Document numbers

* Submission date

* Return date (if applicable)

System generates **Original Certificate Acknowledgement Slip** (PDF) for students.

---

# **🔹 FR5: Entrance Exam & OMR Sheet Generation**

If entrance exam conducted:

* ERP generates an **OMR Sheet** with:

  * Student name

  * Application number

  * Course applied

  * Subject code

  * QR code for automated evaluation (optional)

Exam cell enters:

* OMR marks

* Previous marks percentage → point conversion

* Entrance exam percentage → point conversion

* Weighted average for scholarship slab

---

# **🔹 FR6: Scholarship Calculation**

Scholarship rules:

* Configurable slabs

* System calculates automatically

* Admin/HOD override allowed with justification

* Scholarship reflected in fee structure at confirmation

---

# **🔹 FR7: Application Verification Before Confirmation**

Admissions officer must verify the following **before** student can be confirmed:

* Minimum required fields filled

* All mandatory documents uploaded

* Migration/equivalency (if applicable)

* Original certificates submitted (optional stage)

* Entrance exam marks (if applicable)

* Hostel requirement confirmed

If incomplete → status remains **“Tentative Admission”**

---

# **🔹 FR8: Tentative Admission vs Confirmed Admission Logic**

### **Tentative Admission**

A student becomes *Tentatively Admitted* when:

* Application submitted

* Fee unpaid OR

* Missing documents OR

* Pending verification

### **Confirmed Admission**

Triggered only when:

1. Student pays **1st Installment Fee**

2. All critical documents are verified

3. Hostel decision finalized

After these:

* Student ID generated

* Student added to batch/semester

* ID card issued

* Login credentials created

---

# **🔹 FR9: Hostel Assignment & Undertaking Generation**

If student opts for hostel:

* Hostel warden receives request

* Room/bed allocated

* Hostel undertaking generated in PDF

* Hostel fees added to fee plan

* Student must digitally sign undertaking (optional)

Status updated to:  
 ➡️ **“Hostel Allotted”**

---

# **🔹 FR10: ID Card Generation With Validity Period**

ID card must contain:

* Photo

* Student name

* Course \+ Year

* Admission Number

* **Validity From – Validity To**

  * 1-year course → 1 year validity

  * 3-year course → 3 years validity

QR Code \= **Admission Number**

ID card downloadable from student portal.

---

# **🔹 FR11: Internal Circulars Module (NEW)**

System must allow:

### **For Staff:**

* Admin/HOD upload internal circulars

* Viewable by relevant staff based on department/role

* Avoid paper circulation entirely

### **For Students:**

* Circulars tagged as “Student Circular” display in student/parent portal

* Examples:

  * Exam instructions

  * Attendance warnings

  * Fest notices

  * Holiday circulars

Circulars must support attachments.

---

# **🔹 FR12: Upload University Exam Marks Memos**

After each semester's university result:

* Exam cell uploads marks memo (PDF or image)

* System maps it to a student

* Students & parents can view/download memo from portal

* Maintain history for all semesters

---

# **🔹 FR13: Notifications**

System sends notifications for:

* Payment pending

* Missing documents

* Hostel confirmation

* Offer letter

* Admission confirmation

* Circulars

* OMR exam schedule

* ID card generation

Channels: SMS, Email, WhatsApp (optional)

---

# **🔹 FR14: Audit Requirements**

System shall log:

* Every document upload

* Verification actions

* Scholarship overrides

* Fee payments

* Hostel allotment

* ID card generation

* Circular publishing

---

# **⭐ MODULE 1 (ADMISSIONS) — UPDATED & COMPLETE**

This version includes **ALL enhancements you requested**.

# **🔵 PART 3 — MODULE 2: STUDENT MASTER & PROFILE MANAGEMENT**

### ***(FINAL UPDATED VERSION WITH FULL ATTENDANCE REQUIREMENTS)***

**Copy/Paste Ready**

---

# **3.2 Student Master Module**

---

# **3.2.1 Purpose**

The Student Master Module maintains a **centralized, detailed, lifelong record** of each student, including:

* Personal & academic details

* Attendance (daily, period-wise, subject-wise)

* Internal & external exam marks

* Assignments, practical evaluations

* Behavioral records (L1/L2/L3)

* University memos

* ODC, internships, placements

* Achievements, participation, club memberships

* Gatepass usage

* Hostel, library, uniform, asset interactions

* Bank details

* Fee association

* ID card lifecycle

* Parent interactions & undertakings

It is the core module powering all other ERP features.

---

# **3.2.4 Functional Requirements (FR)**

*(All earlier FRs included; below is the enhanced attendance section and integrated module specification.)*

---

# **🔵 FR – ATTENDANCE MANAGEMENT (STUDENT MASTER SECTION)**

The Student Master module must store **complete attendance data** with real-time insights, shortage alerts, notifications, and eligibility linkage.

---

# **FR Attendance 1: Daily & Period-wise Attendance Storage**

The system must store the following:

### **A. Daily Attendance**

* Present

* Absent

* Late

* On duty

* Leave approved

### **B. Period-Wise Attendance**

Each timetable session must record:

* Subject

* Faculty

* Period number

* Topic taught (linked to lesson plan)

* Attendance status

### **C. Practical Attendance**

Must store:

* Practical attendance

* Practical performance scores (grooming, record, viva, task, etc.)

---

# **FR Attendance 2: Subject-Wise Attendance % Calculation**

The ERP shall maintain:

* **Attendance % per subject**

* Attendance % per practical subject

* Combined attendance %

**Formula:**  
 `Attendance % = (Sessions Attended / Sessions Conducted) × 100`

Attendance is recalculated:

* Daily

* Weekly

* Monthly

* Semester-wise

Stored inside Student Master.

---

# **FR Attendance 3: Monthly, Semester and Yearly Attendance Summaries**

ERP shall store:

### **Monthly Attendance Summary:**

* Total periods conducted

* Total attended

* Subject-wise attendance %

### **Semester Attendance Summary:**

* Overall %

* Subject-wise %

* Practical attendance %

### **Yearly Attendance Summary:**

* Consolidated report

* Detention risk %

Admin can export reports anytime.

---

# **FR Attendance 4: 75% Rule Enforcement**

ERP must enforce:

### **RULE: Student must maintain ≥75% attendance per subject.**

### **If \<75%:**

System must automatically:

* Flag the student as **“Attendance Shortage”**

* Block:

  * Hall ticket generation

  * Internal exam eligibility (configurable)

  * ODC participation (if enabled by college)

  * Placement rounds (if poor attendance persists)

Status visible to:

* Student

* Parent

* Faculty

* SSE

---

# **FR Attendance 5: Shortage Alerts & Notifications (Continuous)**

System must send automated notifications:

### **Alert Trigger:**

If attendance in ANY subject \< **75%**.

### **Notification Recipients:**

* Student

* Parent

* SSE (Student Support Executive)

* Class Coordinator

### **Notification Types:**

* SMS

* Email

* WhatsApp (optional)

* In-app alert

### **Alert Frequency:**

* Immediate when shortage occurs

* Weekly summary

* 3-day reminders before exams start

* Final warning before hall ticket blocking

### **Content Example:**

“Your attendance for SUBJECT: XYZ is 68%. Minimum required is 75%. Please attend regularly to avoid detention/hall ticket restrictions.”

---

# **FR Attendance 6: Attendance History in Student Master**

ERP must store complete attendance history for:

* Each period

* Each subject

* Each month

* Each semester

* Each year

Reports must show:

* Graphs (trend lines)

* Best/worst attendance subjects

* Days absent

* Days late

* Practical attendance breakdown

---

# **FR Attendance 7: Attendance-based Behavioral Flags**

If a student’s attendance remains below threshold for continuous weeks or months:

System must create:

* **Automatic L1 issue** (faculty level)

* If continues → L2 SSE escalation

* If unresolved → L3 Principal intervention

All escalations stored in Student Master.

---

# **FR Attendance 8: Attendance Integration with All Modules**

| Module | Integration |
| ----- | ----- |
| **Exams** | Block internal/university hall tickets if \<75% |
| **Student Monitoring** | Low attendance triggers L1/L2/L3 |
| **Placements** | Attendance affects eligibility |
| **ODC** | Student not allowed if attendance low |
| **Hostel** | Warden sees hostel student attendance |
| **Time Table** | Attendance only allowed during active slots |

---

# **⭐ UPDATED STUDENT MASTER — FULL INTEGRATED MODULE (INCLUDING ATTENDANCE)**

For completeness, the Student Master now stores:

### **✔ Personal details**

### **✔ Academic details**

### **✔ Parent/guardian data**

### **✔ Address information**

### **✔ Certificates (uploaded \+ originals register)**

### **✔ Hostel status**

### **✔ ID card lifecycle**

### **✔ Migration/detention status**

### **✔ Promotion history**

### **✔ Fee associations**

### **✔ University exam memos**

### **✔ Internal exam marks (Mid 1, Mid 2\)**

### **✔ Assignment marks**

### **✔ Practical internal marks**

### **✔ Attendance (daily, period, subject, summary)**

### **✔ Subject-wise \<75% shortage alerts \+ notifications**

### **✔ Issues (L1, L2, L3)**

### **✔ Notices**

### **✔ Parent interactions & undertakings**

### **✔ Industrial training**

### **✔ ODC information**

### **✔ Placements**

### **✔ Clubs membership**

### **✔ Achievements, awards**

### **✔ Gatepass usage (month/semester/year wise)**

### **✔ Student bank account details**

### **✔ Time table mapping**

### **✔ Elective subject mapping**

### **✔ Previous results**

---

# **⭐ MODULE 2 FULLY UPDATED — FINAL VERSION (WITH ATTENDANCE ENHANCEMENTS)**

# **PART 3 — MODULE 3: FACULTY & STAFF MANAGEMENT (FINAL EXTENDED VERSION)**

### ***This is the complete SRS version including all enhancements.***

---

# **3.3 Faculty & Staff Management Module**

---

# **3.3.1 Purpose**

The Faculty & Staff Management Module handles:

* Onboarding & induction

* Document storage & HR compliance

* Department assignment

* Timetable & subject allocation

* Leave & substitution workflows

* Class adjustment ledger (CR/DR)

* Tools/assets responsibility

* Library access & procurement recommendations

* Duty Rota (student assignments for departmental duties)

* Exam role management

* Student academic performance dashboards

* ODC visibility

* Feedback cycles

* Advanced attendance & HR policy enforcement

---

# **3.3.2 Scope (UPDATED)**

The module includes:

### **A. Faculty Onboarding & Induction Module (NEW)**

Upon onboarding:

* HR loads the standard *Induction Checklist*

* Examples of induction items:

  * HR Orientation

  * IT System Training

  * Library rules

  * Exam Cell briefing

  * ODC policies

  * Attendance & leave rules

  * Academic regulations

  * Safety induction

  * Department policies

  * Asset responsibilities

Each induction point contains:

* Task name

* Responsible staff (HOD/HR/Library/etc.)

* Due date

* Confirmation button: **“I Confirm I Have Understood This”**

* Digital signature (optional)

Completion required before:

* First class assignment

* Exam duties

* Full ERP access

### **B. Academic Responsibilities**

* Subjects

* Timetable

* Lesson plan progress

* Class adjustments

* Student performance analytics

### **C. Operational Responsibilities**

* Department assets

* Inventory verification

* Duty Rota supervision

* Student monitoring & attendance control

---

# **3.3.4 Functional Requirements (FR)**

---

# **🔹 FR1: Faculty Profile (Same as earlier, no change needed)**

---

# **🔹 FR2: Document Upload & Verification**

(Refer previous version — unchanged)

---

# **🔹 FR3: Library Access for Staff (Enhanced with New Workflow)**

### **Library Privileges:**

* Borrow books

* Reserve books

* Renewals

* Entry via QR

### **Book Recommendation Workflow (UPDATED)**

Faculty → Library Officer → HOD Approval → Principal Approval → Procurement → Status Update

Statuses include:

* Received

* Ordered

* Approved

* Rejected

* Pending

Faculty can track entire chain from request → approval → procurement.

---

# **🔹 FR4: Department Assignment**

Faculty assigned to:

* Primary department

* Optional secondary department

System links faculty to:

* Departmental assets

* Department duty rota

* Department stock audits

---

# **🔹 FR5: Subject & Class Assignment (Updated Structure)**

Supports mapping:

**Course → Year → Semester → Section → Group → Subject**

Includes:

* Theory subjects

* Practical subjects (2/4/6 hour blocks)

* Elective subjects

* Language/lab-based subgroups

Qualification match suggested during assignment.

---

# **🔹 FR6: Timetable Mapping**

(As previously documented)

---

# **🔵 FR7: Advanced Attendance Policies for Faculty (UPDATED)**

The ERP shall implement strict HR attendance rules:

### **A. Late Arrival/ Early Leaving Tracking**

System must:

* Mark LATE if after threshold time

* Mark EARLY LEAVE if before threshold time

* Track monthly limits (configurable)

### **B. Permission Management**

Faculty may apply for:

* Late permission

* Early permission

Limits:

* Configurable (e.g., 3 per month)

* Beyond limit → **automatic LOP (Loss of Pay)**

### **C. Automatic LOP Rules**

ERP must apply:

* **Half-day LOP** if late/early threshold exceeds

* **Full-day LOP** if repeated breaches occur

### **D. Compensatory Off (CCL) Rules**

If faculty works **extra hours**, ERP must:

* Track extra duty hours

* Convert extra hours into CCL based on rule (*Example: 8 hours \= 1 CCL*)

* Requires approval: HOD → Principal

System must notify faculty when they have pending CCL to utilize.

---

# **🔵 FR8: Leave & Substitution Workflow (UPDATED AGAIN)**

### **Step 1 — Leave Application**

Includes:

* Reason

* Leave dates

* Attachment (medical/etc.)

* Proposed substitute faculty (optional)

---

### **Step 2 — ERP Timetable Checking**

ERP identifies:

* All scheduled sessions (theory/practical/electives)

* Adds these as **CR entries** in Class Adjustment Ledger

---

### **Step 3 — Substitute Faculty Assignment**

ERP suggests based on:

* Availability

* Qualification

* Free timetable slots

Notifications sent to:

* Substitute faculty

* Class incharge

* Admin office

---

### **Step 4 — Substitute Approval Flow**

1. Substitute faculty accepts/rejects

2. HOD verifies substitution

3. Class incharge confirms allotment

4. Principal approves (if required)

If NO scheduled class:  
 → No incharge approval required.

---

### **Step 5 — Compensatory Class (DR Entry)**

When original faculty recovers missed class:

* Marks recovery in ERP

* DR entry recorded

* CR – DR re-calculated

---

### **Step 6 — End-of-Semester Requirement**

Ledger must satisfy:

**CR – DR \= 0**  
 Otherwise:

* Marks entry blocked

* HOD notified

* Principal escalated

---

# **🔹 FR9: Class Adjustment Ledger (CR/DR)**

Shows:

* Missed classes (CR)

* Recovered classes (DR)

* Pending classes

* Substitute faculty details

* Approval status

---

# **🔹 FR10: Assets & Tools Responsibility (UPDATED)**

Each department assigns a **faculty-in-charge** who must:

* Maintain departmental stock

* Conduct periodic QR-stock verification

* Report shortage/loss

* Verify tools issued to students

ERP must support:

* Monthly audits

* Variance reports

* Faculty responsibility report

---

# **🔵 FR11: Duty Rota Module (NEW)**

A NEW system must allocate students to departmental duties:

### **Duty Areas**

* Housekeeping

* F\&B Service

* Kitchen labs

* Bakery labs

* Front office labs

* Stores

* Library

* Admin support

### **Rules for Auto-Assignment**

System assigns students based on:

* Year ratio (3rd year : 2nd year : 1st year \= configurable)

* Practical performance

* Discipline records

* Attendance

* Availability

### **Student Allocation Output**

* Duty department

* Date & time slot

* Team lead (student)

* Faculty-in-charge

### **Attendance**

Attendance automatically marked for duty hours (OD — On Duty).

### **Tracking**

ERP tracks:

* Completion of duty

* Remarks from faculty

* Duty performance score (optional)

---

# **🔹 FR12: Exam Module Access**

(Same as earlier version)

---

# **🔹 FR13: Student Performance Dashboard**

(Same as earlier but integrated with Duty Rota & monitoring)

---

# **🔹 FR14: Student Monitoring Integration**

(Same as earlier)

---

# **🔹 FR15: ODC View for Faculty**

(Same as earlier)

---

# **🔹 FR16: Faculty Feedback System**

(Same as earlier)

---

# **🔹 FR17: Reports (UPDATED)**

Reports must include:

### **Academic**

* Workload report

* Subject-wise attendance hours

* Class adjustment ledger

* Lesson plan progress report

### **Departmental**

* Stock register (assets/tools)

* Department-level audit variance

* Duty Rota report

* Tools issued & returned

### **HR**

* Attendance report (late/early/LOP)

* Leave ledger

* CCL earned & used

### **Library**

* Books borrowed

* Recommendations list & approval status

### **Exam**

* Marks entry pending/completed

* Invigilation duties

---

# **⭐ MODULE 3 — FULL & FINAL VERSION COMPLETE**

This now includes:

✔ Induction module  
 ✔ Library procurement workflow with HOD→Principal approvals  
 ✔ Advanced attendance rules (late/early/LOP/CCL)  
 ✔ Enhanced leave flow  
 ✔ Duty Rota module  
 ✔ Department asset responsibility  
 ✔ New reports  
 ✔ All previous functional requirements

# **🔵 PART 3 — MODULE 4: COURSE, SUBJECT, LESSON PLAN, ELECTIVES & QUESTION BANK MANAGEMENT**

---

# **3.4 COURSE, SUBJECT, LESSON PLAN & ELECTIVES MODULE**

### ***(FINAL FULL VERSION — ALL CHANGES APPLIED)***

---

# **3.4.1 Purpose**

The Course, Subject, Lesson Plan & Electives Module defines, manages, and controls the **entire academic structure** of Regency College.  
 This includes:

* Academic hierarchy

* Course/Year/Semester design

* Sections, batches, elective groups

* Subject master (theory/practical/elective/audit)

* Lesson plans

* Assignments

* Syllabus progress

* Mandatory library period

* Internal evaluation logic

* Practical internal evaluation

* Question bank creation

* Auto question paper generation

The module integrates with **attendance, exams, timetable, and student master**.

---

# **3.4.2 Academic Structure (FINAL UPDATED HIERARCHY)**

ERP shall support the following complete academic hierarchy:

**Academic Year → Course → Year → Semester → Section → Batch → Elective Group → Subject**

---

### **A. Academic Year**

Examples: 2024–25, 2025–26

---

### **B. Course (Programs)**

* BHM

* BCT

* CCCB

* And other hospitality programs

Mapping: **Academic Year → Course**

---

### **C. Year of Study**

* Year 1

* Year 2

* Year 3

Mapping: **Course → Year**

---

### **D. Semesters (1 to 6\)**

* Semester 1

* Semester 2

* Semester 3

* Semester 4

* Semester 5

* Semester 6

Mapping: **Year → Semesters**

---

### **E. Sections**

Each semester includes:

* Section 1 / Section 2 (or A/B)

---

### **F. Batches (for practicals & electives)**

* Batch A

* Batch B

* Batch C

---

### **G. Elective Groups**

Used for:

* Elective subjects

* Skill modules

* Language groups

* Lab/practical batches

Multiple groups supported per batch.

---

# **3.4.3 Subject Master (FINAL VERSION)**

Each subject must contain:

---

## **A. Subject Fields**

* Subject Name

* Subject Code

* Course → Year → Semester → Section → Batch → Group mapping

* Subject Type:

  * Theory

  * Practical (2/4/6 hours)

  * Elective

  * Audit / Non-exam Learning Subject

---

## **B. Subject Category (UPDATED)**

There are two categories:

---

### **1\. Subject WITH Exam (Evaluated Subject)**

Includes:

* Mid-1

* Mid-2

* Assignment

* Practical internal (if applicable)

### **⭐ Internal Mark Calculation (FINAL RULE):**

**Final Internal \= ((Mid-1 \+ Mid-2) / 2\) \+ Assignment Marks**

System auto-calculates final internal marks.

---

### **2\. Subject WITHOUT Exam (Audit / Learning-only)**

* NO Mid exam

* NO Assignment

* NO Internal evaluation

* NO practical score

* ONLY attendance \+ syllabus tracking

* Mandatory Library Period is included here

* Appears in result sheet as:  
   **"Audit Course – No Marks Evaluated"**

---

## **C. Weekly & Total Hours**

* Weekly hours required

* Total semester hours required

* Practical block hours (2/4/6 hours)

System must ensure timetable mapping matches hour requirements.

---

# **3.4.4 Elective Subject Management**

### **A. Elective Setup**

* Elective category

* Elective groups

* Max capacity

* Faculty assignment

### **B. Student Selection Workflow**

* Students choose elective through portal

* System validates capacity

* Group allocated automatically

* Timetable adjusts group-wise

### **C. Reporting**

* Elective strength

* Allocation list

* Capacity vs enrolled

---

# **3.4.5 Lesson Plan Management (FINAL UPDATED VERSION)**

Lesson Plan follows:

**Unit → Topic → Subtopic → Assignment → Question Bank items**

### **A. Fields:**

* Unit number

* Topic name

* Subtopics

* Estimated hours

* Required readings

* Practical task (if applicable)

---

## **Assignment Mapping Inside Lesson Plan**

Assignments can be added per topic.

Fields:

* Assignment Title

* Assignment Type

  * Written

  * Case Study

  * Practical

  * Presentation

  * Project

* Maximum Marks

* Rubric/criteria

* Submission timeline

* Topic linkage

Assignments apply ONLY to **subjects with exam**.

---

## **Lesson Plan Tracking**

* Faculty marks topic completed using attendance

* Completion % updated in real-time

* HOD dashboard shows delays

Students see:

* Completed topics

* Upcoming topics

---

# **3.4.6 Syllabus Progress Tracking**

ERP must track:

* Topic completed

* Pending topics

* Lesson variance (planned vs actual)

Reports:

* Faculty progress report

* Subject-wise syllabus report

* Class-wise syllabus status

---

# **3.4.7 Mandatory Library Period**

Library period is:

* A compulsory **Audit subject**

* Appears in timetable weekly

* No marks

* Attendance compulsory

* Shown in student timetable as "Library"

---

# **3.4.8 Practical Internal Evaluation (FINAL RULE)**

For all practical subjects:

### **Daily evaluation parameters:**

* Grooming

* Record work

* Viva

* Task performance

* Practical competency

ERP computes **Practical Internal Marks** from daily evaluation.

Appears separately from theory internal marks.

---

# **3.4.9 Question Bank Management (FINAL VERSION)**

Question Bank linked to:

* Units

* Topics

* Subtopics

### **Each question contains:**

* Question Type (MCQ / Short / Long / Case Study)

* Marks

* Difficulty Level (Easy/Medium/Hard)

* Topic

* Section mapping (A/B/C)

* Active/Inactive toggle

Faculty can bulk upload questions.

---

# **3.4.10 Auto Question Paper Generator (FINAL VERSION)**

ERP generates question papers using rules set by Exam Cell.

### **Auto-generation uses:**

* Section rules

  * Section A → 5 questions × 2 marks

  * Section B → 3 questions × 5 marks

  * Section C → Long answer

### **Question Selection Logic:**

1. Select questions ONLY from **completed syllabus topics**

2. Maintain difficulty %

3. Avoid previous paper questions

4. Randomize for multiple sets (A/B/C)

ERP logs:

* Question paper history

* Questions selected

* Total marks

---

# **3.4.11 Integration with Attendance**

Attendance screen must show:

* Topic taught

* Link to lesson plan

* Practical evaluation input fields

Topic completion triggers syllabus update.

---

# **3.4.12 Integration with Exam Module**

Subject master links to:

* Internal marks

* Practical marks

* Re-exam eligibility

* University exam mapping

ERP blocks internal marks entry until syllabus completion % meets threshold (optional configuration).

---

# **3.4.13 Integration with Student Master**

Students can view:

* Subjects

* Electives

* Lesson plan

* Completed topics

* Assignments

* Internal marks

* Practical marks

Audit subjects appear separately.

---

# **3.4.14 Reports**

### **Academic Structure**

* Course–Year–Semester–Section matrix

* Subject list

* Electives and allocations

### **Lesson Plan Reports**

* Topic completion

* Faculty variance analysis

* Assignment status

### **Evaluation Reports**

* Internal marks report

* Practical internal marks

* Audit course attendance

### **Question Bank Reports**

* Question distribution

* Difficulty matrix

* Question paper generation logs

---

# **⭐ MODULE 4 — FULL FINAL VERSION COMPLETE**

This version includes:

✔ Subjects without exam (Audit / No assessment)  
 ✔ Correct internal marks formula  
 ✔ Practical daily evaluation logic  
 ✔ Assignment embedded in lesson plan  
 ✔ Fully functional question bank  
 ✔ Auto question paper generator  
 ✔ Full academic structure  
 ✔ Mandatory library period  
 ✔ Integration with exams, attendance, student master

