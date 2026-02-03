# Admission Domain - Frontend Contract Export

# Version: v1.0.0

# Status: FROZEN (2026-02-03)

## Quick Reference

### Base URL

```
Production: https://api.rchmct.org/api/v1/admission
Development: http://localhost:8000/api/v1/admission
```

### Authentication

All endpoints require Bearer token in Authorization header:

```
Authorization: Bearer <jwt_token>
```

---

## Endpoints

### 1. Quick Apply (Stage 1)

**POST** `/applications`

**Request Body:**

```typescript
{
  name: string;              // 1-200 chars
  email: string;             // Valid email
  phone: string;             // Exactly 10 digits (^\d{10}$)
  gender: "MALE" | "FEMALE" | "OTHER";
  program_id: number;        // > 0
  state: string;             // 1-100 chars
  board: string;             // 1-100 chars
  group_of_study: string;    // 1-50 chars (e.g., "MPC", "BiPC")
  fee_mode?: "ONLINE" | "OFFLINE";  // Default: "ONLINE"
}
```

**Response:** `ApplicationRead` (see schemas below)

---

### 2. Complete Application (Stage 2)

**PATCH** `/applications/{application_id}`

**Request Body (all optional):**

```typescript
{
  aadhaar_number?: string;           // Exactly 12 digits (^\d{12}$)
  father_name?: string;              // 1-200 chars
  father_phone?: string;             // Exactly 10 digits (^\d{10}$)
  address?: string;                  // 1-500 chars
  previous_marks_percentage?: number; // 0-100
  applied_for_scholarship?: boolean;
  hostel_required?: boolean;
  status?: ApplicationStatus;        // See enum below
}
```

**Response:** `ApplicationRead`

---

### 3. Get Application

**GET** `/applications/{application_id}`

**Response:** `ApplicationRead`

---

### 4. List Applications

**GET** `/applications?skip=0&limit=100&status=PAID`

**Query Parameters:**

- `skip`: number (default: 0)
- `limit`: number (default: 100, max: 1000)
- `status`: ApplicationStatus (optional filter)

**Response:** `ApplicationRead[]`

---

## TypeScript Schemas

### Enums

```typescript
enum ApplicationStatus {
  // Legacy
  APPLIED = "APPLIED",

  // Workflow
  QUICK_APPLY_SUBMITTED = "QUICK_APPLY_SUBMITTED",
  LOGGED_IN = "LOGGED_IN",
  FORM_IN_PROGRESS = "FORM_IN_PROGRESS",

  // Payment
  PENDING_PAYMENT = "PENDING_PAYMENT",
  PAYMENT_FAILED = "PAYMENT_FAILED",
  PAID = "PAID",

  // Processing
  FORM_COMPLETED = "FORM_COMPLETED",
  UNDER_REVIEW = "UNDER_REVIEW",
  APPROVED = "APPROVED",
  ADMITTED = "ADMITTED",
  REJECTED = "REJECTED",
  WITHDRAWN = "WITHDRAWN",
}

enum FeeMode {
  ONLINE = "ONLINE",
  OFFLINE = "OFFLINE",
}

enum ApplicationPaymentStatus {
  PENDING = "PENDING",
  SUCCESS = "SUCCESS",
  FAILED = "FAILED",
}

enum DocumentType {
  PHOTO = "PHOTO",
  AADHAAR = "AADHAAR",
  TENTH_MARKSHEET = "TENTH_MARKSHEET",
  TWELFTH_MARKSHEET = "TWELFTH_MARKSHEET",
  MIGRATION_CERTIFICATE = "MIGRATION_CERTIFICATE",
  TRANSFER_CERTIFICATE = "TRANSFER_CERTIFICATE",
  CASTE_CERTIFICATE = "CASTE_CERTIFICATE",
  INCOME_CERTIFICATE = "INCOME_CERTIFICATE",
  OTHER = "OTHER",
}

enum DocumentStatus {
  UPLOADED = "UPLOADED",
  VERIFIED = "VERIFIED",
  REJECTED = "REJECTED",
}
```

### Request Schemas

```typescript
interface ApplicationCreate {
  name: string;
  email: string;
  phone: string;
  gender: string;
  program_id: number;
  state: string;
  board: string;
  group_of_study: string;
  fee_mode?: FeeMode;
}

interface ApplicationUpdate {
  aadhaar_number?: string;
  father_name?: string;
  father_phone?: string;
  address?: string;
  previous_marks_percentage?: number;
  applied_for_scholarship?: boolean;
  hostel_required?: boolean;
  status?: ApplicationStatus;
}
```

### Response Schemas

```typescript
interface ApplicationRead {
  id: number;
  application_number: string;

  // Stage 1 fields
  name: string;
  email: string;
  phone: string;
  gender: string;
  program_id: number;
  state: string;
  board: string;
  group_of_study: string;

  // Stage 2 fields
  aadhaar_number?: string;
  father_name?: string;
  father_phone?: string;
  address?: string;
  previous_marks_percentage?: number;
  applied_for_scholarship: boolean;
  hostel_required: boolean;

  // Photo
  photo_url?: string;

  // Portal access
  portal_user_id?: number;
  portal_first_login?: string; // ISO 8601
  portal_last_login?: string; // ISO 8601

  // Completion tracking
  quick_apply_completed_at?: string; // ISO 8601
  full_form_started_at?: string;
  full_form_completed_at?: string;

  // Payment
  application_fee: number;
  payment_status: ApplicationPaymentStatus;
  payment_id?: string;
  payment_date?: string; // ISO 8601
  fee_mode: FeeMode;
  payment_proof_url?: string;
  offline_payment_verified: boolean;

  // Hall ticket
  hall_ticket_number?: string;
  hall_ticket_generated: boolean;
  hall_ticket_url?: string;

  // Entrance exam
  entrance_marks?: number;
  entrance_percentage?: number;

  // Scholarship
  scholarship_slab_id?: number;
  scholarship_amount?: number;
  scholarship_percentage?: number;

  // Offer letter
  offer_letter_url?: string;
  offer_letter_generated: boolean;

  // Confirmation
  first_installment_paid: boolean;
  first_installment_amount?: number;
  admission_number?: string;
  admission_date?: string; // ISO 8601

  // Documents
  documents_verified: boolean;

  // Status
  status: ApplicationStatus;
  created_at: string; // ISO 8601
  updated_at: string; // ISO 8601

  // Soft delete
  is_deleted: boolean;
}

interface ApplicationPaymentRead {
  id: number;
  transaction_id: string;
  amount: number;
  status: ApplicationPaymentStatus;
  payment_method?: string;
  paid_at?: string; // ISO 8601
  created_at: string; // ISO 8601
}

interface ApplicationDocumentRead {
  id: number;
  document_type: DocumentType;
  file_url: string;
  file_name: string;
  file_size: number;
  status: DocumentStatus;
  rejection_reason?: string;
  verified_at?: string; // ISO 8601
  uploaded_at: string; // ISO 8601
}
```

---

## Validation Rules

### Phone Number

- **Pattern:** `^\d{10}$`
- **Example:** `9876543210`
- **Error:** "Phone must be exactly 10 digits"

### Aadhaar Number

- **Pattern:** `^\d{12}$`
- **Example:** `123456789012`
- **Error:** "Aadhaar must be exactly 12 digits"

### Email

- **Built-in validation**
- **Example:** `student@example.com`

### Percentage

- **Range:** 0-100
- **Example:** `85.5`
- **Error:** "Percentage must be between 0 and 100"

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
      "loc": ["body", "phone"],
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

## Notes for Frontend

1. **Date/Time Format:** All timestamps are ISO 8601 strings
2. **Enums:** Use exact string values (case-sensitive)
3. **Optional Fields:** May be `null` or omitted in responses
4. **Validation:** Client-side validation should match server rules
5. **Pagination:** Use `skip` and `limit` for list endpoints

---

## Contract Guarantees

✅ **Frozen:** No breaking changes without major version bump  
✅ **Validated:** All requests validated server-side  
✅ **Type-Safe:** Pydantic ensures runtime type checking  
✅ **Backward Compatible:** New optional fields only

**Version:** v1.0.0  
**Last Updated:** 2026-02-03  
**Contact:** Backend team for questions
