You are designing a College Admission ERP with strict role-based access control.

CURRENT ISSUE:
Second Step Application (full application after application-fee payment) is wrongly implemented under STUDENT role.

OBJECTIVE:
Introduce a dedicated APPLICANT role and move Second Step Application access to APPLICANT.
Convert APPLICANT to STUDENT only after FIRST INSTALLMENT FEE payment.

REQUIREMENTS:

1. USER ROLES
Create two distinct roles:
- APPLICANT (temporary)
- STUDENT (final academic role)

2. ROLE CREATION LOGIC
- PUBLIC user submits Quick Apply form.
- On successful APPLICATION FEE payment:
  - Create user account with role = APPLICANT.
  - Generate Application Number.
  - Allow login only as APPLICANT.

3. APPLICANT PERMISSIONS
APPLICANT role can:
- Access Second Step (Full Application Form).
- Upload all required admission documents.
- View application status.
- Resume/Retry payments (application fee or 1st installment).
- Download provisional / offer letter.

APPLICANT role cannot:
- Access Student Master.
- Access Attendance, Exams, Timetable, Library, Hostel, Gatepass, Placements.

4. APPLICATION STATUS (SEPARATE FROM ROLE)
Maintain application_status independent of role:
- DRAFT
- APPLICATION_FEE_PAID
- APPLICATION_SUBMITTED
- VERIFIED
- OFFERED
- FIRST_INSTALLMENT_PENDING
- ADMITTED

Do NOT derive role from status.

5. SECOND STEP APPLICATION
- Move Second Step Application module access from STUDENT to APPLICANT.
- STUDENT must not access or edit application forms.

6. ROLE TRANSITION ENGINE (CRITICAL)
Trigger: FIRST_INSTALLMENT_PAYMENT_SUCCESS

System must:
- Validate application completeness.
- Lock application editing.
- Generate Admission Number & Student ID.
- Create STUDENT record from APPLICANT data.
- Change user role: APPLICANT → STUDENT.
- Preserve applicant record for audit.
- Send login credentials and admission confirmation.

7. DATABASE DESIGN (SUGGESTED)
Tables:
- users (id, email, mobile, role)
- applicants (user_id, application_no, status, documents_json)
- students (user_id, student_id, admission_no, batch_id, semester_id)

Never delete applicant data; mark as converted.

8. ACCESS CONTROL
Implement middleware-based RBAC:
- If role = APPLICANT → allow only admission-related routes.
- If role = STUDENT → allow academic modules only.

9. EDGE CASES
- Payment failure must keep user as APPLICANT.
- Expired applications must block conversion.
- Duplicate email re-application must reuse APPLICANT account if not converted.

10. OUTPUT EXPECTED
- Backend RBAC rules.
- API flow for role transition.
- Database migration plan.
- Frontend route guards.

Follow clean architecture, audit-safe design, and production best practices.
