
TASK 1: Search Existing Implementation
------------------------------------
**STATUS: PARTIALLY IMPLEMENTED (Broken/Missing Backend)**

**Findings:**
1.  **Database / Models:**
    *   `Application` model (`apps/api/app/domains/admission/models/application.py`) **ALREADY HAS** full soft delete support:
        *   `is_deleted` (bool)
        *   `deleted_at` (datetime)
        *   `deleted_by` (user_id)
        *   `delete_reason` (str)
    *   `FileMetadata` (`system` domain) has `deleted_at`.
    *   Other models (`Department`, `Student`, etc.) only use `is_active` (Deactivation, not Trash).

2.  **Frontend Code:**
    *   `apps/web/src/hooks/use-admissions.ts` has hooks `useDeleteApplication` and `useRestoreApplication`.
    *   `apps/web/src/services/admission-api.ts` defines endpoints:
        *   Delete: `DELETE /admissions/v2/applications/{id}?reason=...`
        *   Restore: `POST /admissions/v2/applications/{id}/restore`

3.  **Backend API (The Gap):**
    *   **CRITICAL MISSING PIECE:** The endpoints `DELETE /v2/applications/{id}` and `POST /v2/applications/{id}/restore` are **NOT DEFINED** in `apps/api/app/domains/admission/router.py`.
    *   There is support for *filtering* deleted applications (`show_deleted=True` in `list_applications`), but no way to actually delete/restore them via API.

**Conclusion:**
The "Safe Delete" feature exists in concept and data model but is **broken** because the backend endpoints are missing. Refactoring is not needed; we just need to implement the missing endpoints.

--------------------------------------------------

TASK 2: Design Proper Soft Delete (Move to Trash)
--------------------------------------------------

**Decision:** **REUSE & FIX** existing implementation.

**Data Model (Existing - Reusing):**
- Table: `application`
- Fields: `is_deleted`, `deleted_at`, `deleted_by`, `delete_reason`

**API Changes Required:**
1.  **Implement `DELETE /admissions/v2/applications/{id}`**
    - **Logic:**
        - Check permissions (Admin/SuperAdmin).
        - Update `is_deleted=True`, `deleted_at=now()`, `deleted_by=current_user`, `delete_reason=reason`.
        - **Audit:** Log `APPLICATION_DELETED`.
    - **Validation:**
        - Warn/Prevent if `payment_status` is `SUCCESS` (Require special confirmation or "Force Delete" flag?).

2.  **Implement `POST /admissions/v2/applications/{id}/restore`**
    - **Logic:**
        - Check permissions.
        - Update `is_deleted=False`, `deleted_at=None`, etc.
        - **Audit:** Log `APPLICATION_RESTORED`.

3.  **Verify `GET /admin/applications`**
    - Ensure `show_deleted=True` works correctly (already seems implemented in router, need to verify service logic).

**UI / UX:**
- The frontend hooks (`useDeleteApplication`, `useRestoreApplication`) are likely already wired to UI buttons.
- **Action:** Once backend is fixed, verify the UI "Trash" or "Restore" buttons work as expected.

**Risks:**
- **Data Integrity:** ensuring `application_number` uniqueness doesn't conflict if we "undelete" a record (unlikely as app numbers are random/unique).
- **Payment:** We should strictly control deleting PAID applications.

--------------------------------------------------

**NEXT STEPS:**
1.  Approve this design.
2.  Implement the endpoints in `apps/api/domains/admission/router.py`.
3.  Verify from Frontend.
