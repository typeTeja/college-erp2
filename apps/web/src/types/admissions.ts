/**
 * Admission Domain Types - v2.0.0
 * 
 * TypeScript types matching backend Admission domain contract.
 * Includes comprehensive details for Step 2 Admission Form.
 * 
 * CONTRACT VERSION: v2.0.0
 * STATUS: ACTIVE (2026-02-04)
 */

// ============================================================================
// Enums
// ============================================================================

export enum ApplicationStatus {
  APPLIED = "APPLIED",
  QUICK_APPLY_SUBMITTED = "QUICK_APPLY_SUBMITTED",
  LOGGED_IN = "LOGGED_IN",
  FORM_IN_PROGRESS = "FORM_IN_PROGRESS",
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
  CONDUCT_CERTIFICATE = "CONDUCT_CERTIFICATE", // Added
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

// [NEW] Enums for Step 2
export enum Gender {
  MALE = "MALE",
  FEMALE = "FEMALE",
  OTHER = "OTHER"
}

export enum BloodGroup {
  A_POS = "A_POS",
  A_NEG = "A_NEG",
  B_POS = "B_POS",
  B_NEG = "B_NEG",
  AB_POS = "AB_POS",
  AB_NEG = "AB_NEG",
  O_POS = "O_POS",
  O_NEG = "O_NEG"
}

export enum Religion {
  HINDU = "HINDU",
  MUSLIM = "MUSLIM",
  CHRISTIAN = "CHRISTIAN",
  SIKH = "SIKH",
  BUDDHIST = "BUDDHIST",
  JAIN = "JAIN",
  PARSI = "PARSI",
  OTHER = "OTHER",
  PREFER_NOT_TO_SAY = "PREFER_NOT_TO_SAY"
}

export enum CasteCategory {
  GENERAL = "GENERAL",
  OC = "OC",
  BC_A = "BC_A",
  BC_B = "BC_B",
  BC_C = "BC_C",
  BC_D = "BC_D",
  BC_E = "BC_E",
  SC = "SC",
  ST = "ST",
  EWS = "EWS"
}

export enum ParentRelation {
  FATHER = "FATHER",
  MOTHER = "MOTHER",
  GUARDIAN = "GUARDIAN",
  GRANDFATHER = "GRANDFATHER",
  GRANDMOTHER = "GRANDMOTHER",
  UNCLE = "UNCLE",
  AUNT = "AUNT",
  SIBLING = "SIBLING",
  OTHER = "OTHER"
}

export enum EducationLevel {
  SSC = "SSC",
  INTERMEDIATE = "INTERMEDIATE",
  DIPLOMA = "DIPLOMA",
  DEGREE = "DEGREE",
  POST_GRADUATE = "POST_GRADUATE"
}

export enum EducationBoard {
  CBSE = "CBSE",
  ICSE = "ICSE",
  STATE_BOARD = "STATE_BOARD",
  IB = "IB",
  NIOS = "NIOS",
  UNIVERSITY = "UNIVERSITY",
  OTHER = "OTHER"
}

export enum ActivityLevel {
  COLLEGE = "COLLEGE",
  DISTRICT = "DISTRICT",
  STATE = "STATE",
  NATIONAL = "NATIONAL",
  INTERNATIONAL = "INTERNATIONAL"
}

export enum AddressType {
  PERMANENT = "PERMANENT",
  CURRENT = "CURRENT",
  GUARDIAN = "GUARDIAN"
}


// ============================================================================
// Sub-Models (Nested Details)
// ============================================================================

export interface ApplicationAddress {
  id?: number;
  application_id?: number;
  address_type: AddressType;
  address_line: string;
  village_city: string;
  district?: string;
  state: string;
  country: string;
  pincode: string;
  telephone_residence?: string;
  telephone_office?: string;
  is_same_as_permanent?: boolean; // UI only
}

export interface ApplicationParent {
  id?: number;
  application_id?: number;
  relation: ParentRelation;
  name: string;
  gender?: Gender;
  mobile: string;
  email?: string;
  qualification?: string;
  occupation?: string;
  annual_income?: number;
  bank_account_number?: string;
  bank_name?: string;
  bank_ifsc?: string;
  is_primary_contact: boolean;
}

export interface ApplicationEducation {
  id?: number;
  application_id?: number;
  level: EducationLevel;
  institution_name: string;
  institution_address?: string;
  institution_code?: string;
  board: EducationBoard;
  board_other?: string;
  hall_ticket_number?: string;
  year_of_passing?: number;
  secured_marks?: number;
  total_marks?: number;
  percentage?: number;
  grade?: string;
  cgpa?: number;
}

export interface ApplicationBankDetails {
  id?: number;
  application_id?: number;
  account_holder_name: string;
  bank_name: string;
  branch_name: string;
  account_number: string;
  ifsc_code: string;
  is_verified?: boolean;
}

export interface ApplicationHealth {
  id?: number;
  application_id?: number;
  is_medically_fit: boolean;
  practitioner_name?: string;
  practitioner_registration_number?: string;
  certificate_date?: string;
  certificate_place?: string;
  // UI/Extended fields (not in backend yet)
  blood_group?: BloodGroup;
  height_cm?: number;
  weight_kg?: number;
  disability_status?: boolean;
  disability_details?: string;
  has_chronic_illness?: boolean;
  chronic_illness_details?: string;
  allergies?: string;
  doctor_name?: string;
  doctor_phone?: string;
}

// ============================================================================
// Request Schemas (Create/Update)
// ============================================================================

export interface ApplicationCreate {
  name: string;
  email: string;
  phone: string;
  gender: Gender | string; // Supporting both for now
  program_id: number;
  state: string;
  board: string;
  group_of_study: string;
  fee_mode?: PaymentMode;
}

export interface ApplicationUpdate {
  aadhaar_number?: string;
  father_name?: string;
  father_phone?: string;
  address?: string;
  previous_marks_percentage?: number;
  applied_for_scholarship?: boolean;
  hostel_required?: boolean;
}

// Comprehensive Update Schema for Step 2
export interface ApplicationCompleteSubmit {
  // Personal
  date_of_birth?: string; // ISO Date
  gender?: Gender;
  blood_group?: BloodGroup;
  religion?: Religion;
  caste_category?: CasteCategory;
  nationality: string;
  mother_tongue?: string;
  identification_mark_1?: string;
  identification_mark_2?: string;

  // Previous Details (Legacy string fields)
  aadhaar_number?: string;
  father_name?: string;
  father_phone?: string;

  // Extra Curricular
  extra_curricular_activities?: string;
  activity_level?: ActivityLevel;
  activity_sponsored_by?: string;
  hobbies?: string;

  // Nested Lists
  parents: ApplicationParent[];
  addresses: ApplicationAddress[];
  education_history: ApplicationEducation[];
  bank_details?: ApplicationBankDetails;
  health_info?: ApplicationHealth;

  // Flags
  student_declaration_accepted: boolean;
  parent_declaration_accepted: boolean;
  hostel_required?: boolean;
  transport_required?: boolean;
  applied_for_scholarship?: boolean;
}

export interface ApplicationPaymentCreate {
  application_id: number;
  amount: number;
  payment_mode: PaymentMode;
  transaction_id?: string;
  payment_proof_url?: string;
}

// ============================================================================
// Response Schemas (Read)
// ============================================================================

export interface ProgramShort {
  id: number;
  name: string;
}

export interface ApplicationRead {
  id: number;
  application_number: string;
  name: string;
  email: string;
  phone: string;
  gender: string;
  program_id: number;
  program?: ProgramShort;
  payment_status?: string;
  state: string;
  board: string;
  group_of_study: string;
  status: ApplicationStatus;
  fee_mode: PaymentMode;
  application_fee: number;
  portal_user_id?: number;

  // Basic Legacy Fields
  aadhaar_number?: string;
  father_name?: string;
  father_phone?: string;
  address?: string;
  previous_marks_percentage?: number;
  applied_for_scholarship: boolean;
  hostel_required: boolean;

  // New Step 2 Fields
  date_of_birth?: string;
  blood_group?: BloodGroup;
  religion?: Religion;
  caste_category?: CasteCategory;
  nationality?: string;
  mother_tongue?: string;
  identification_mark_1?: string;
  identification_mark_2?: string;

  // Nested Relationships
  parents?: ApplicationParent[];
  addresses?: ApplicationAddress[];
  education_history?: ApplicationEducation[];
  bank_details?: ApplicationBankDetails;
  health_info?: ApplicationHealth;

  // Payment info
  payment_proof_url?: string;
  offline_payment_verified: boolean;
  documents_verified: boolean;
  offline_payment_verified_by?: number;
  offline_payment_verified_at?: string;

  // Metadata
  student_id?: number;
  current_step: number;
  last_saved_at: string;
  created_at: string;
  updated_at: string;

  // Relationships
  documents?: ApplicationDocument[];
  payments?: ApplicationPaymentRead[];

  student_declaration_accepted: boolean;
  parent_declaration_accepted: boolean;
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
  payment_date?: string;
  created_at: string;
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
  verified_at?: string;
  uploaded_at: string;
}

export interface ActivityLog {
  id: number;
  application_id: number;
  activity_type: ActivityType;
  description: string;
  extra_data?: Record<string, any>;
  performed_by?: number;
  ip_address?: string;
  created_at: string;
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
  id: number;
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

export interface AdmissionSettings {
  id: number;
  application_fee_enabled: boolean;
  application_fee_amount: number;
  online_payment_enabled: boolean;
  offline_payment_enabled: boolean;
  payment_gateway: string;
  send_credentials_email: boolean;
  send_credentials_sms: boolean;
  auto_create_student_account: boolean;
  portal_base_url: string;
  updated_at: string;
}

export interface AdmissionSettingsUpdate {
  application_fee_enabled?: boolean;
  application_fee_amount?: number;
  online_payment_enabled?: boolean;
  offline_payment_enabled?: boolean;
  send_credentials_email?: boolean;
  send_credentials_sms?: boolean;
  auto_create_student_account?: boolean;
  portal_base_url?: string;
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
  payment_url?: string;
  access_key?: string;
  error?: string;
  txnid?: string;
}


// ============================================================================
// Legacy Compatibility
// ============================================================================

/** @deprecated Use ApplicationCreate instead */
export interface QuickApplyData extends QuickApplyRequest { }

/** @deprecated Use ApplicationUpdate instead */
export interface FullApplicationData extends ApplicationUpdate { }

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
export interface Application extends ApplicationRead { }

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
