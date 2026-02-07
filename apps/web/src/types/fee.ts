/**
 * Finance Domain Types - v1.0.0
 * 
 * TypeScript types matching backend Finance domain contract.
 * 
 * CONTRACT VERSION: v1.0.0
 * STATUS: FROZEN (2026-02-03)
 * 
 * Breaking changes policy:
 * - Enum additions: Safe (backward compatible)
 * - New optional fields: Safe
 * - Required field changes: Requires migration + deprecation
 * - Enum removals: 6-month deprecation period
 */

// ============================================================================
// Enums
// ============================================================================

export enum FeeCategory {
  GENERAL = "GENERAL",
  SC = "SC",
  ST = "ST",
  OBC = "OBC",
  EWS = "EWS"
}

export enum PaymentMode {
  ONLINE = "ONLINE",
  OFFLINE = "OFFLINE",
  CASH = "CASH",
  CHEQUE = "CHEQUE",
  DD = "DD",
  NEFT = "NEFT",
  RTGS = "RTGS",
  UPI = "UPI"
}

export enum PaymentStatus {
  INITIATED = "INITIATED",
  PENDING = "PENDING",
  SUCCESS = "SUCCESS",
  FAILED = "FAILED",
  REFUNDED = "REFUNDED"
}

// ============================================================================
// Fee Head Schemas
// ============================================================================

export interface FeeHeadCreate {
  name: string;                    // 1-100 chars
  code: string;                    // 1-20 chars, pattern: ^[A-Z0-9_]+$
  description?: string;            // Max 500 chars
  category?: string;               // Max 50 chars, default: "ACADEMIC"
  is_mandatory?: boolean;          // Default: true
}

export interface FeeHeadRead {
  id: number;
  name: string;
  code: string;
  description?: string;
  category: string;
  is_mandatory: boolean;
  is_active: boolean;
  created_at: string;              // ISO 8601
}

// ============================================================================
// Fee Structure Schemas
// ============================================================================

export interface FeeStructureCreate {
  program_id: number;              // > 0
  academic_year: string;           // Pattern: ^\d{4}-\d{4}$ (e.g., "2024-2025")
  year: number;                    // 1-6
  slab?: string;                   // Max 20 chars, default: "GENERAL"
  category?: FeeCategory;          // Default: GENERAL
  tuition_fee: number;             // >= 0, 2 decimals
  library_fee?: number;            // >= 0, 2 decimals, default: 0
  lab_fee?: number;                // >= 0, 2 decimals, default: 0
  uniform_fee?: number;            // >= 0, 2 decimals, default: 0
  caution_deposit?: number;        // >= 0, 2 decimals, default: 0
  digital_fee?: number;            // >= 0, 2 decimals, default: 0
  miscellaneous_fee?: number;      // >= 0, 2 decimals, default: 0
  number_of_installments?: number; // 1-12, default: 4
  
  // Backward compatibility (deprecated - for existing UI components)
  /** @deprecated Use individual fee fields instead */
  components?: FeeComponent[];
  /** @deprecated Use number_of_installments instead */
  installments?: FeeInstallment[];
}

export interface FeeStructureRead {
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
  created_at: string;              // ISO 8601
}

// ============================================================================
// Fee Payment Schemas
// ============================================================================

export interface FeePaymentCreate {
  student_fee_id: number;          // > 0
  amount: number;                  // > 0, <= 1000000, 2 decimals
  payment_mode: PaymentMode;
  transaction_id?: string;         // Max 100 chars
  reference_number?: string;       // Max 100 chars
  bank_name?: string;              // Max 100 chars
  remarks?: string;                // Max 500 chars
}

export interface FeePaymentRead {
  id: number;
  student_fee_id: number;
  amount: number;
  payment_mode: PaymentMode;
  payment_status: PaymentStatus;
  transaction_id?: string;
  payment_date?: string;           // ISO 8601
  created_at: string;              // ISO 8601
}

// ============================================================================
// Online Payment Schemas
// ============================================================================

export interface PaymentInitiateRequest {
  student_id: number;              // > 0
  student_fee_id: number;          // > 0
  amount: number;                  // 0 < amount <= 1000000, 2 decimals
  customer_name: string;           // 1-200 chars
  customer_email: string;          // Valid email
  customer_phone: string;          // Exactly 10 digits (^\d{10}$)
}

export interface PaymentInitiateResponse {
  payment_url: string;
  transaction_id: string;
  gateway_order_id: string;
  amount: number;
  currency: string;                // Default: "INR"
}

export interface PaymentCallbackData {
  transaction_id: string;          // 1-100 chars
  gateway_payment_id?: string;     // Max 100 chars
  gateway_signature?: string;      // Max 500 chars
  status: PaymentStatus;
  amount: number;                  // > 0
  payment_mode?: PaymentMode;
}

export interface OnlinePaymentRead {
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
  initiated_at: string;            // ISO 8601
  completed_at?: string;           // ISO 8601
}

// ============================================================================
// Scholarship Schemas
// ============================================================================

export interface ScholarshipSlabCreate {
  name: string;                    // 1-100 chars
  code: string;                    // 1-20 chars, pattern: ^[A-Z0-9_]+$
  description?: string;            // Max 500 chars
  discount_type?: string;          // "PERCENTAGE" | "FIXED_AMOUNT"
  discount_value: number;          // >= 0
  min_percentage?: number;         // 0-100
  max_percentage?: number;         // 0-100
}

export interface ScholarshipSlabRead {
  id: number;
  name: string;
  code: string;
  description?: string;
  discount_type: string;
  discount_value: number;
  is_active: boolean;
  created_at: string;              // ISO 8601
}

// ============================================================================
// Student Fee Types (Extended)
// ============================================================================

export interface StudentFee {
  id: number;
  student_id: number;
  fee_structure_id: number;
  academic_year: string;
  total_fee: number;
  concession_amount: number;
  fine_amount: number;
  paid_amount: number;
  balance: number;
  is_blocked: boolean;
  created_at: string;
  updated_at: string;
}

export interface StudentFeeCreate {
  student_id: number;
  fee_structure_id: number;
  academic_year: string;
}

export interface StudentFeeSummary {
  student_id: number;
  student_name: string;
  admission_number: string;
  academic_year: string;
  total_fee: number;
  concession_amount: number;
  fine_amount: number;
  paid_amount: number;
  balance: number;
  is_blocked: boolean;
  student_fee_id: number;
  customer_email: string;
  customer_phone: string;
  installments: InstallmentDetail[];
  payments: PaymentDetail[];
}

export interface InstallmentDetail {
  installment_number: number;
  amount: number;
  due_date: string;
  status: "paid" | "pending" | "overdue";
}

export interface PaymentDetail {
  id: number;
  amount: number;
  payment_mode: PaymentMode;
  payment_date: string | null;
  status: PaymentStatus;
}

// ============================================================================
// Concession Types
// ============================================================================

export interface FeeConcession {
  id: number;
  student_fee_id: number;
  concession_type: string;
  amount: number;
  percentage?: number;
  approved_by?: string;
  approved_at?: string;
  remarks?: string;
  created_at: string;
}

export interface FeeConcessionCreate {
  student_fee_id: number;
  concession_type: string;
  amount?: number;
  percentage?: number;
  remarks?: string;
}

// ============================================================================
// Fine Types
// ============================================================================

export interface FeeFine {
  id: number;
  student_fee_id: number;
  installment_number: number;
  fine_amount: number;
  reason: string;
  waived: boolean;
  waived_by?: string;
  waived_at?: string;
  created_at: string;
}

export interface FeeFineCreate {
  student_fee_id: number;
  installment_number: number;
  fine_amount: number;
  reason: string;
}

// ============================================================================
// Defaulter Types
// ============================================================================

export interface FeeDefaulter {
  student_id: number;
  student_name: string;
  admission_number: string;
  program: string;
  year: number;
  total_due: number;
  overdue_installments: number;
  last_payment_date?: string;
  days_overdue: number;
}

// ============================================================================
// Filter Types
// ============================================================================

export interface FeeStructureFilters {
  academic_year?: string;
  program_id?: number;
  year?: number;
  category?: FeeCategory;
}

export interface StudentFeeFilters {
  student_id?: number;
  program_id?: number;
  academic_year?: string;
  payment_status?: string;
}

export interface PaymentFilters {
  student_id?: number;
  from_date?: string;
  to_date?: string;
  payment_mode?: PaymentMode;
}

// ============================================================================
// Component Types (for Fee Structure)
// ============================================================================

export interface FeeComponent {
  id?: number;
  name: string;
  amount: number;
  is_refundable: boolean;
}

export interface FeeInstallment {
  id?: number;
  installment_number: number;
  amount: number;
  due_date: string; // ISO date
}

// ============================================================================
// Validation Patterns (for client-side validation)
// ============================================================================

export const VALIDATION_PATTERNS = {
  phone: /^\d{10}$/,
  academicYear: /^\d{4}-\d{4}$/,
  code: /^[A-Z0-9_]+$/,
} as const;

export const VALIDATION_LIMITS = {
  amount: {
    min: 0,
    max: 1000000,
    decimals: 2,
  },
  year: {
    min: 1,
    max: 6,
  },
  installments: {
    min: 1,
    max: 12,
  },
  percentage: {
    min: 0,
    max: 100,
  },
} as const;
