# Easebuzz Payment Gateway Integration (FastAPI)

This document provides a comprehensive guide to the Easebuzz Payment Gateway integration in the College ERP API (FastAPI).

## 1. Architecture Overview

The integration follows a decoupled service-based architecture:

*   **Service Layer (`app/services/easebuzz_service.py`)**:
    *   Handles strict SHA512 hash generation and verification.
    *   Manages communication with Easebuzz API (Initiate Link).
    *   Logic is isolated from HTTP transport details.

*   **API Layer (`app/api/v1/easebuzz.py`)**:
    *   Exposes REST endpoints (`/payment/initiate`, `/payment/response`, `/payment/webhook`).
    *   Handles Request/Response lifecycle.
    *   Uses Pydantic models for validation.

*   **Configuration (`app/config/settings.py`)**:
    *   Loads credentials (`KEY`, `SALT`, `ENV`) from environment variables.

## 2. Environment Variable Setup

Add the following to your `.env` file:

```env
EASEBUZZ_MERCHANT_KEY=your_merchant_key
EASEBUZZ_SALT=your_salt
EASEBUZZ_ENV=test  # Use 'test' for sandbox, 'prod' for live
```

**Note:** Ensure you are using credentials for the correct environment (Test vs Prod).

## 3. Folder Structure

```
apps/api/app/
├── api/
│   └── v1/
│       ├── easebuzz.py          # API Endpoints
│       └── router.py            # Route Registration
├── config/
│   └── settings.py              # Env Configuration
├── schemas/
│   └── easebuzz.py              # Pydantic Models
└── services/
    └── easebuzz_service.py      # Core Business Logic
```

## 4. API Usage & Testing

### A. Initiate Payment

**Endpoint:** `POST /api/v1/payment/initiate`

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/payment/initiate \
-H "Content-Type: application/json" \
-d '{
    "amount": 100.00,
    "firstname": "Test Student",
    "email": "test@example.com",
    "phone": "9999999999",
    "productinfo": "Application Fee",
    "udf1": "ApplicationNo123"
}'
```

**Response:**
```json
{
    "status": 1,
    "data": "https://testpay.easebuzz.in/pay/...",
    "payment_url": "https://testpay.easebuzz.in/pay/...",
    "txnid": "TXN-1234567890"
}
```

### B. Handle Response (Redirect)

Easebuzz redirects the user to `/api/v1/payment/response` (or your configured `surl`).

*   **Method:** POST (Form Data)
*   **Action:** Verifies hash, logs status, returns JSON confirmation.

### C. Webhook

Easebuzz posts to `/api/v1/payment/webhook`.

*   **Method:** POST (Form Data)
*   **Action:** Verifies hash, updates transaction status in background (TODO).

## 5. Testing with Easebuzz Test Cards

1.  **Initiate Payment:** Use the curl command above.
2.  **Redirect:** Open the `payment_url` in browser.
3.  **Payment Page:** Select "Net Banking" -> Select any Bank (e.g. Test Bank).
4.  **Simulation:**
    *   Select "Success" to trigger success response.
    *   Select "Failure" to trigger failure response.
5.  **Verification:** Check server logs (`INFO: Payment Successful: ...`).

## 6. Common Mistakes & Troubleshooting

1.  **Hash Mismatch:**
    *   Ensure strict order of parameters in hash generation.
    *   `salt` is at the end for Request, at the start for Response.
    *   Ensure float amounts are converted to string exactly as sent (e.g., `100.0` vs `100.00`). Easebuzz usually expects 2 decimal places? *Actually, just passing the string representation is key.*

2.  **Redirect 405 Method Not Allowed:**
    *   Easebuzz redirects using **POST**. Ensure your `surl`/`furl` endpoints accept POST.

3.  **Cross-Origin (CORS):**
    *   If calling from frontend, ensure API headers allow the origin.

4.  **HTTPS:**
    *   Live environment requires HTTPS for all URLs (`surl`, `furl`, `webhook`).

EASEBUZZ_MERCHANT_KEY=your_key_here
EASEBUZZ_SALT=your_salt_here
EASEBUZZ_ENV=test