PROBLEM SUMMARY:
---------------
The 2nd stage application form has 7 steps and is very long.
If submission fails or the user exits midway:
- All entered data is lost
- User must start again
- Causes frustration and drop-offs

Additionally:
- Uploaded documents in step 7 are not viewable
- No full application preview
- No downloadable / printable PDF for reference

---------------------------------------------------
TASK 1: Design Save-on-Every-Step Architecture
---------------------------------------------------
Implement a robust "Save & Resume" system.

Requirements:
- Automatically save data after EACH step
- Save on:
  - Next button
  - Step change
  - Optional auto-save (debounced)
- Partial data must be valid and stored safely

Database:
- Application record must support PARTIAL completion
- Track:
  - current_step (1–7)
  - last_saved_at
  - completion_status (DRAFT / SUBMITTED)
- Each step’s data should be:
  - Saved incrementally
  - Updatable independently

---------------------------------------------------
TASK 2: Resume From Last Completed Step
---------------------------------------------------
When user:
- Logs in again
- Reopens application link

System must:
- Load saved data from DB
- Pre-fill all completed steps automatically
- Redirect user to:
  → the LAST INCOMPLETE STEP (based on current_step)
- Prevent data overwrite unless user edits fields

Ensure:
- Works for both:
  - Logged-in applicants
  - Token-based applicant access (pre-login)

---------------------------------------------------
TASK 3: Step-wise Validation Strategy
---------------------------------------------------
Validation rules:
- Validate ONLY the current step when saving
- Do NOT enforce future-step validations
- Allow draft saving with incomplete overall form

Final submit:
- Validate ALL steps together
- Block submission if any required data missing

---------------------------------------------------
TASK 4: Full Application Preview (Before Final Submit)
---------------------------------------------------
Add a "Preview Application" feature.

Requirements:
- Read-only consolidated view of ALL 7 steps
- Clearly show:
  - Personal details
  - Academic details
  - Parent details
  - Hostel selection
  - Uploaded documents list
- Allow user to:
  - Go back to any step for editing
  - Confirm correctness before final submit

---------------------------------------------------
TASK 5: Downloadable & Printable PDF
---------------------------------------------------
Generate a full application PDF.

PDF Requirements:
- Clean, official format
- College header + logo
- Application number
- All form data
- Document list (file names)
- Declaration section
- Date & signature placeholder

Access:
- Download PDF
- Print PDF
- Available:
  - After save (draft)
  - After final submission

Storage:
- Either:
  - Generate on-demand OR
  - Store generated PDF in MinIO

---------------------------------------------------
TASK 6: Fix Document View Issue (Step 7)
---------------------------------------------------
Investigate why uploaded documents are not viewable.

Check:
- MinIO object URL generation
- Authentication / presigned URL expiry
- Incorrect content-type
- Frontend link rendering
- Route protection or middleware(proxy.ts) blocking

Fix Requirements:
- Each uploaded document must have:
  - View button
  - Download button
- Use:
  - Presigned URLs OR
  - Secure proxy API
- Must work for:
  - Applicant
  - Admin

---------------------------------------------------
TASK 7: UX & Safety Enhancements
---------------------------------------------------
Implement:
- Visual step progress indicator
- “Saved ✓” confirmation after each step
- Warning before leaving page if unsaved changes
- Auto-save debounce (e.g. every 5–10 seconds)
- Graceful recovery on network failure

---------------------------------------------------
TASK 8: Audit & Logs
---------------------------------------------------
Track:
- Step save events
- Final submission timestamp
- IP / user reference (if available)
- PDF generation events

---------------------------------------------------
EXPECTED OUTPUT:
---------------------------------------------------
1. Database changes required
2. API design for step save & resume
3. Resume logic flow
4. Preview screen structure
5. PDF generation approach
6. Root cause + fix for document view issue
7. Edge cases & test checklist

IMPORTANT:
---------------------------------------------------
- Do NOT force full submission at each step
- Do NOT lose user-entered data
- Do NOT expose MinIO files publicly
- UX must prioritize applicant convenience
- Solution must be ERP-grade and scalable
- keep in mind 20 year of life span for this application.     