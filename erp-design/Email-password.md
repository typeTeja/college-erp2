
TASK 1: Verify Existing Credential Logic
----------------------------------
**Verified:**
-   Credentials generated in `create_portal_account_after_payment`.
-   Password is NOT stored in plain text (only hash in DB).
-   Original password cannot be retrieved.
-   Frontend DOES NOT have a "Reset Password" page implementation.

----------------------------------
TASK 2: Design Secure Resend Credentials Feature
----------------------------------
**Selected Strategy: Option B (New Temporary Password)**

**Reasoning:**
-   Frontend lacks "Forgot Password / Reset Password" screens. Building them is out of scope for a quick fix.
-   Users expecting "Resend Credentials" likely want the password directly (as per original flow).
-   Generating a new random password and sending it is secure enough if sent to the registered email/phone.

----------------------------------
TASK 3: Security Rules
----------------------------------
-   **Invalidate Old Password:** The new password overwrites the old hash immediately.
-   **Notification:** Send via Email AND SMS (if enabled).
-   **Audit:** Log who triggered the resend.

----------------------------------
TASK 4: Backend Implementation
----------------------------------
**Endpoint:** `POST /admissions/v2/applications/{id}/resend-credentials`
**Permission:** Super Admin / Admin.

**Logic:**
1.  Get Application & User.
2.  Generate `new_password = secrets.token_urlsafe(8)`.
3.  Update `User.hashed_password`.
4.  Call `email_service.send_portal_credentials(..., password=new_password)`.
5.  Call `sms_service.send_portal_credentials(...)`.
6.  Log Activity (`CREDENTIALS_RESENT`).

----------------------------------
TASK 5: Email Template Requirements
----------------------------------
-   Reuse existing `PORTAL_CREDENTIALS_EMAIL_TEMPLATE` but maybe prefix subject with "Updated: ".
-   Actually, the existing template says "Here are your login credentials". It fits perfectly for a reset too.

----------------------------------
TASK 6: Audit & Compliance
----------------------------------
-   Log `ActivityType.CREDENTIALS_RESENT` (New type).

----------------------------------
EXPECTED OUTPUT:
----------------------------------
1.  Backend Endpoint.
2.  Service Method in `AdmissionService`.
3.  Frontend Button in Admin View.
