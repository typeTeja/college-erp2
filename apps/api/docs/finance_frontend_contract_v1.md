# Finance Domain - Frontend Contract Export

# Version: v1.0.0

# Status: FROZEN (2026-02-03)

## Quick Reference

### Base URL

```
Production: https://api.rchmct.org/api/v1/finance
Development: http://localhost:8000/api/v1/finance
```

### Authentication

All endpoints require Bearer token in Authorization header:

```
Authorization: Bearer <jwt_token>
```

---

## Endpoints

### 1. Initiate Payment

**POST** `/payments/initiate`

**Request Body:**

```typescript
{
  student_id: number; // > 0
  student_fee_id: number; // > 0
  amount: number; // 0-1000000 (₹10 lakh max), 2 decimals
  customer_name: string; // 1-200 chars
  customer_email: string; // Valid email
  customer_phone: string; // Exactly 10 digits (^\d{10}$)
}
```

**Response:** `PaymentInitiateResponse`

---

### 2. Payment Callback (Webhook)

**POST** `/payments/callback`

**Request Body:**

```typescript
{
  transaction_id: string;       // 1-100 chars
  gateway_payment_id?: string;  // Max 100 chars
  gateway_signature?: string;   // Max 500 chars
  status: PaymentStatus;        // INITIATED | SUCCESS | FAILED | REFUNDED
  amount: number;               // > 0
  payment_mode?: PaymentMode;   // ONLINE | OFFLINE | CASH | CHEQUE | DD
}
```

**Response:** Success/failure status

---

### 3. Get Payment Status

**GET** `/payments/{payment_id}`

**Response:** `OnlinePaymentRead`

---

### 4. List Student Payments

**GET** `/payments/student/{student_id}?skip=0&limit=100`

**Query Parameters:**

- `skip`: number (default: 0)
- `limit`: number (default: 100, max: 1000)

**Response:** `OnlinePaymentRead[]`

---

## TypeScript Schemas

### Enums

```typescript
enum PaymentStatus {
  INITIATED = "INITIATED",
  PENDING = "PENDING",
  SUCCESS = "SUCCESS",
  FAILED = "FAILED",
  REFUNDED = "REFUNDED",
}

enum PaymentMode {
  ONLINE = "ONLINE",
  OFFLINE = "OFFLINE",
  CASH = "CASH",
  CHEQUE = "CHEQUE",
  DD = "DD",
  NEFT = "NEFT",
  RTGS = "RTGS",
  UPI = "UPI",
}

enum FeeCategory {
  GENERAL = "GENERAL",
  SC = "SC",
  ST = "ST",
  OBC = "OBC",
  EWS = "EWS",
}
```

### Request Schemas

```typescript
interface PaymentInitiateRequest {
  student_id: number;
  student_fee_id: number;
  amount: number;
  customer_name: string;
  customer_email: string;
  customer_phone: string;
}

interface PaymentCallbackData {
  transaction_id: string;
  gateway_payment_id?: string;
  gateway_signature?: string;
  status: PaymentStatus;
  amount: number;
  payment_mode?: PaymentMode;
}

interface FeeStructureCreate {
  program_id: number;
  academic_year: string; // Format: "2024-2025"
  year: number; // 1-6
  slab?: string; // Default: "GENERAL"
  category?: FeeCategory;
  tuition_fee: number;
  library_fee?: number;
  lab_fee?: number;
  uniform_fee?: number;
  caution_deposit?: number;
  digital_fee?: number;
  miscellaneous_fee?: number;
  number_of_installments?: number; // 1-12, default: 4
}

interface FeePaymentCreate {
  student_fee_id: number;
  amount: number;
  payment_mode: PaymentMode;
  transaction_id?: string;
  reference_number?: string;
  bank_name?: string;
  remarks?: string;
}

interface ScholarshipSlabCreate {
  name: string;
  code: string; // Uppercase alphanumeric (^[A-Z0-9_]+$)
  description?: string;
  discount_type?: string; // "PERCENTAGE" | "FIXED_AMOUNT"
  discount_value: number;
  min_percentage?: number; // 0-100
  max_percentage?: number; // 0-100
}
```

### Response Schemas

```typescript
interface PaymentInitiateResponse {
  payment_url: string;
  transaction_id: string;
  gateway_order_id: string;
  amount: number;
  currency: string; // Default: "INR"
}

interface OnlinePaymentRead {
  id: number;
  idempotency_key: string;
  student_id: number;
  amount: number;
  payment_status: PaymentStatus;
  gateway_transaction_id?: string;
  gateway_order_id?: string;
  customer_name: string;
  customer_email: string;
  customer_phone: string;
  receipt_number?: string;
  receipt_url?: string;
  initiated_at: string; // ISO 8601
  completed_at?: string; // ISO 8601
}

interface FeeStructureRead {
  id: number;
  program_id: number;
  academic_year: string;
  year: number;
  slab: string;
  category: FeeCategory;
  total_annual_fee: number;
  total_amount: number;
  installment_amount: number;
  is_active: boolean;
  created_at: string; // ISO 8601
}

interface FeePaymentRead {
  id: number;
  student_fee_id: number;
  amount: number;
  payment_mode: PaymentMode;
  payment_status: PaymentStatus;
  transaction_id?: string;
  payment_date?: string; // ISO 8601
  created_at: string; // ISO 8601
}

interface ScholarshipSlabRead {
  id: number;
  name: string;
  code: string;
  description?: string;
  discount_type: string;
  discount_value: number;
  is_active: boolean;
  created_at: string; // ISO 8601
}
```

---

## Validation Rules

### Phone Number

- **Pattern:** `^\d{10}$`
- **Example:** `9876543210`
- **Error:** "Phone must be exactly 10 digits"

### Amount

- **Range:** 0 < amount ≤ 1,000,000 (₹10 lakh)
- **Decimals:** Exactly 2
- **Example:** `50000.00`
- **Error:** "Amount must be positive" or "Amount exceeds maximum limit"

### Academic Year

- **Pattern:** `^\d{4}-\d{4}$`
- **Example:** `2024-2025`
- **Error:** "Invalid academic year format"

### Code (Fee Head, Scholarship)

- **Pattern:** `^[A-Z0-9_]+$`
- **Example:** `TUITION_FEE`, `GOLD_SCHOLARSHIP`
- **Error:** "Code must be uppercase alphanumeric with underscores"

### Year

- **Range:** 1-6
- **Example:** `1` (First year)
- **Error:** "Year must be between 1 and 6"

### Installments

- **Range:** 1-12
- **Example:** `4` (Quarterly)
- **Error:** "Number of installments must be between 1 and 12"

---

## Error Responses

All errors follow this format:

```typescript
{
  detail: string | ValidationError[];
}

interface ValidationError {
  loc: string[];
  msg: string;
  type: string;
}
```

**Example:**

```json
{
  "detail": [
    {
      "loc": ["body", "customer_phone"],
      "msg": "String should match pattern '^\\d{10}$'",
      "type": "string_pattern_mismatch"
    }
  ]
}
```

---

## Status Codes

- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Validation error
- `401 Unauthorized` - Missing/invalid token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error (Pydantic)
- `500 Internal Server Error` - Server error

---

## Payment Flow

### Online Payment

1. **Initiate:** `POST /payments/initiate` → Get `payment_url`
2. **Redirect:** User completes payment on gateway
3. **Callback:** Gateway calls `POST /payments/callback`
4. **Verify:** Check `GET /payments/{payment_id}` for status
5. **Receipt:** Download from `receipt_url` if available

### Offline Payment

1. **Create:** `POST /fee-payments` with `payment_mode: OFFLINE`
2. **Verify:** Admin verifies payment
3. **Update:** Status changes to `SUCCESS`

---

## Notes for Frontend

1. **Date/Time Format:** All timestamps are ISO 8601 strings
2. **Enums:** Use exact string values (case-sensitive)
3. **Optional Fields:** May be `null` or omitted in responses
4. **Validation:** Client-side validation should match server rules
5. **Idempotency:** Use `idempotency_key` for webhook protection
6. **Currency:** Always INR (₹) unless specified

---

## Contract Guarantees

✅ **Frozen:** No breaking changes without major version bump  
✅ **Validated:** All requests validated server-side  
✅ **Type-Safe:** Pydantic ensures runtime type checking  
✅ **Backward Compatible:** New optional fields only

**Version:** v1.0.0  
**Last Updated:** 2026-02-03  
**Contact:** Backend team for questions
