
TASK 1: Understand Current Flow
----------------------------------
**Findings:**
1.  **Current Flow**:
    -   Frontend calls `downloadReceiptPublic` -> `GET /v2/public/receipt/{app_no}`.
    -   Backend `GET /v2/public/receipt/{app_no}` currently returns `{ "url": "/api/v1/.../download" }`.
    -   Frontend opens this API URL.
    -   Backend `GET .../download` generates PDF on-fly and streams it.
2.  **Issue**: Users report "Authentication Error". Since the backend endpoint generates on-fly and streams, it *should* work if public. However, if the user expects MinIO storage, this flow is incorrect.
3.  **MinIO Usage**: `pdf_service.generate_receipt` exists and uploads to MinIO, but is NOT called by the current public endpoint.

----------------------------------
TASK 2: Identify Root Cause
----------------------------------
**Root Cause**:
-   The system currently uses an API proxy method (`StreamingResponse`) which might be failing due to environment config (Nginx/Auth headers) or simply because it doesn't align with the requirement to use stored MinIO files.
-   The user explicitly wants "Use MinIO Presigned URL", implying the current "Generate on fly" approach is either buggy or not the desired architecture.

----------------------------------
TASK 3: Fix Strategy (Choose Correct One)
----------------------------------
**Selected: OPTION A (Presigned URL)**

**Reasoning:**
-   **Performance**: Offloads file serving to MinIO/S3.
-   **Persistence**: Determines if receipt was actually generated/stored.
-   **Security**: Presigned URLs are time-limited and secure without requiring public buckets.
-   **Simplicity**: Frontend just opens a URL; no auth headers needed for the MinIO link.

----------------------------------
TASK 4: Correct Implementation Details
----------------------------------

**Backend Changes (`apps/api/app/domains/admission/router.py`):**
1.  Modify `get_receipt_url` (`GET /v2/public/receipt/{application_number}`):
    -   **Inputs**: `application_number`.
    -   **Logic**:
        1.  Verify Application & Successful Payment.
        2.  Construct Filename: `Receipt_{app.application_number}_{payment.transaction_id}.pdf`.
        3.  Check if file exists in MinIO (using `storage_service.file_exists`).
        4.  **Lazy Generation**: If not exists, call `pdf_service.generate_receipt(...)` (which uploads it).
        5.  Generate **Presigned URL** (`storage_service.get_presigned_url`).
        6.  Return `{ "url": presigned_url }`.

**Frontend Changes**:
-   None required (assuming it consumes `response.url`).

**Edge Cases**:
-   **Lazy Generation**: Ensures that if the receipt wasn't generated during payment callback (for whatever reason), it is generated on demand.

----------------------------------
TASK 5: Edge Cases & Validation
----------------------------------
- [ ] Receipt missing -> Generated on fly -> Presigned URL returned.
- [ ] Payment not found -> 404 Error.
- [ ] Presigned URL expiry -> 15 minutes default.
