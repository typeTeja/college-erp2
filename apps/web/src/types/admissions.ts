/**
 * Admission Domain Types - v1.0.0
 * 
 * TypeScript types matching backend Admission domain contract.
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

export enum ApplicationStatus {
  PENDING_PAYMENT = "PENDING_PAYMENT",
  PAYMENT_FAILED = "PAYMENT_FAILED",
  PAID = "PAID",
  FORM_COMPLETED = "FORM_COMPLETED",
  UNDER_REVIEW = "UNDER_REVIEW",
  APPROVED = "APPROVED",
  ADMITTED = "ADMITTED",
  REJECTED = "REJECTED",
  WITHDRAWN = "WITHDRAWN"
}

export enum PaymentStatus {
  PENDING = "PENDING",
  SUCCESS = "SUCCESS",
  FAILED = "FAILED",
  REFUNDED = "REFUNDED"
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

export enum DocumentType {
  PHOTO = "PHOTO",
  AADHAAR = "AADHAAR",
  TENTH_MARKSHEET = "TENTH_MARKSHEET",
  TWELFTH_MARKSHEET = "TWELFTH_MARKSHEET",
  MIGRATION_CERTIFICATE = "MIGRATION_CERTIFICATE",
  TRANSFER_CERTIFICATE = "TRANSFER_CERTIFICATE",
  CASTE_CERTIFICATE = "CASTE_CERTIFICATE",
  INCOME_CERTIFICATE = "INCOME_CERTIFICATE",
  OTHER = "OTHER"
}

export enum DocumentStatus {
  UPLOADED = "UPLOADED",
  VERIFIED = "VERIFIED",
  REJECTED = "REJECTED"
}

export enum ActivityType {
  APPLICATION_CREATED = "APPLICATION_CREATED",
  PAYMENT_INITIATED = "PAYMENT_INITIATED",
  PAYMENT_SUCCESS = "PAYMENT_SUCCESS",
  PAYMENT_FAILED = "PAYMENT_FAILED",
  OFFLINE_PAYMENT_VERIFIED = "OFFLINE_PAYMENT_VERIFIED",
  FORM_COMPLETED = "FORM_COMPLETED",
  DOCUMENT_UPLOADED = "DOCUMENT_UPLOADED",
  DOCUMENT_VERIFIED = "DOCUMENT_VERIFIED",
  DOCUMENT_REJECTED = "DOCUMENT_REJECTED",
  STATUS_CHANGED = "STATUS_CHANGED",
  ADMISSION_CONFIRMED = "ADMISSION_CONFIRMED",
  ADMISSION_REJECTED = "ADMISSION_REJECTED"
}

// ============================================================================
// Request Schemas (Create/Update)
// ============================================================================

export interface ApplicationCreate {
  name: string;                    // 1-200 chars
  email: string;                   // Valid email
  phone: string;                   // Exactly 10 digits (^\d{10}$)
  gender: string;                  // 1-20 chars
  program_id: number;              // > 0
  state: string;                   // 1-100 chars
  board: string;                   // 1-100 chars
  group_of_study: string;          // 1-100 chars
  fee_mode?: PaymentMode;          // Default: ONLINE
}

export interface ApplicationUpdate {
  aadhaar_number?: string;         // Exactly 12 digits (^\d{12}$)
  father_name?: string;            // Max 200 chars
  father_phone?: string;           // Exactly 10 digits
  address?: string;                // Max 500 chars
  previous_marks_percentage?: number; // 0-100, 2 decimals
  applied_for_scholarship?: boolean;
  hostel_required?: boolean;
}

export interface ApplicationPaymentCreate {
  application_id: number;
  amount: number;                  // > 0, 2 decimals
  payment_mode: PaymentMode;
  transaction_id?: string;         // Max 100 chars
  payment_proof_url?: string;
}

// ============================================================================
// Response Schemas (Read)
// ============================================================================

export interface ApplicationRead {
  id: number;
  application_number: string;
  name: string;
  email: string;
  phone: string;
  gender: string;
  program_id: number;
  state: string;
  board: string;
  group_of_study: string;
  status: ApplicationStatus;
  fee_mode: PaymentMode;
  
  // Optional full fields
  aadhaar_number?: string;
  father_name?: string;
  father_phone?: string;
  address?: string;
  previous_marks_percentage?: number;
  applied_for_scholarship: boolean;
  hostel_required: boolean;
  
  // Payment info
  payment_proof_url?: string;
  offline_payment_verified: boolean;
  offline_payment_verified_by?: number;
  offline_payment_verified_at?: string; // ISO 8601
  
  // Metadata
  student_id?: number;
  created_at: string;              // ISO 8601
  updated_at: string;              // ISO 8601
  deleted_at?: string;             // ISO 8601
  
  // Relationships
  documents?: ApplicationDocument[];
  payments?: ApplicationPaymentRead[];
}

export interface ApplicationPaymentRead {
  id: number;
  application_id: number;
  amount: number;
  payment_mode: PaymentMode;
  payment_status: PaymentStatus;
  transaction_id?: string;
  payment_proof_url?: string;
  gateway_order_id?: string;
  gateway_payment_id?: string;
  payment_date?: string;           // ISO 8601
  created_at: string;              // ISO 8601
}

export interface ApplicationDocument {
  id: number;
  application_id: number;
  document_type: DocumentType;
  file_url: string;
  file_name: string;
  file_size: number;
  status: DocumentStatus;
  rejection_reason?: string;
  verified_by?: number;
  verified_at?: string;            // ISO 8601
  uploaded_at: string;             // ISO 8601
}

export interface ActivityLog {
  id: number;
  application_id: number;
  activity_type: ActivityType;
  description: string;
  extra_data?: Record<string, any>;
  performed_by?: number;
  ip_address?: string;
  created_at: string;              // ISO 8601
}

// ============================================================================
// Special Request/Response Types
// ============================================================================

export interface QuickApplyRequest {
  name: string;
  email: string;
  phone: string;
  gender: string;
  program_id: number;
  state: string;
  board: string;
  group_of_study: string;
}

export interface QuickApplyResponse {
  application_number: string;
  portal_username?: string;
  portal_password?: string;
  message: string;
}

export interface PaymentConfigResponse {
  fee_enabled: boolean;
  fee_amount: number;
  online_enabled: boolean;
  offline_enabled: boolean;
  payment_gateway: string;
}

export interface OfflinePaymentVerifyRequest {
  verified: boolean;
  payment_proof_url?: string;
  mode?: PaymentMode;
  transaction_id?: string;
}

export interface DocumentVerifyRequest {
  verified: boolean;
  remarks?: string;
}

export interface PaymentInitiateRequest {
  application_id: number;
  amount: number;
}

export interface PaymentInitiateResponse {
  status: string;
  payment_url: string;
  txnid: string;
}

// ============================================================================
// Legacy Compatibility (Deprecated - use new types above)
// ============================================================================

/** @deprecated Use ApplicationCreate instead */
export interface QuickApplyData extends QuickApplyRequest {}

/** @deprecated Use ApplicationUpdate instead */
export interface FullApplicationData extends ApplicationUpdate {}

/** @deprecated Use OfflinePaymentVerifyRequest instead */
export interface OfflinePaymentVerify {
  payment_proof_url: string;
  verified: boolean;
}

/** @deprecated Use DocumentVerifyRequest instead */
export interface DocumentVerify {
  status: DocumentStatus;
  rejection_reason?: string;
}

/** @deprecated Use ApplicationRead instead */
export interface Application extends ApplicationRead {}

/** @deprecated Use PaymentStatus instead */
export enum ApplicationPaymentStatus {
  PENDING = "PENDING",
  SUCCESS = "SUCCESS",
  FAILED = "FAILED"
}

/** @deprecated Use PaymentMode instead */
export enum FeeMode {
  ONLINE = "ONLINE",
  OFFLINE = "OFFLINE"
}
