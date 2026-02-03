/**
 * Admission Domain Validation Schemas - v1.0.0
 * 
 * Zod schemas for client-side validation matching backend contract.
 * 
 * CONTRACT VERSION: v1.0.0
 * STATUS: FROZEN (2026-02-03)
 */

import { z } from 'zod';
import { ApplicationStatus, PaymentMode, PaymentStatus, DocumentType } from '@/types/admissions';

// ============================================================================
// Validation Patterns
// ============================================================================

export const phoneSchema = z
  .string()
  .regex(/^\d{10}$/, "Phone must be exactly 10 digits");

export const aadhaarSchema = z
  .string()
  .regex(/^\d{12}$/, "Aadhaar must be exactly 12 digits");

export const percentageSchema = z
  .number()
  .min(0, "Percentage must be at least 0")
  .max(100, "Percentage cannot exceed 100")
  .multipleOf(0.01, "Percentage can have at most 2 decimal places");

export const emailSchema = z
  .string()
  .email("Invalid email address");

// ============================================================================
// Application Schemas
// ============================================================================

export const applicationCreateSchema = z.object({
  name: z.string().min(1, "Name is required").max(200, "Name too long"),
  email: emailSchema,
  phone: phoneSchema,
  gender: z.string().min(1).max(20),
  program_id: z.number().positive("Program ID must be positive"),
  state: z.string().min(1).max(100),
  board: z.string().min(1).max(100),
  group_of_study: z.string().min(1).max(100),
  fee_mode: z.nativeEnum(PaymentMode).optional(),
});

export const applicationUpdateSchema = z.object({
  aadhaar_number: aadhaarSchema.optional(),
  father_name: z.string().max(200).optional(),
  father_phone: phoneSchema.optional(),
  address: z.string().max(500).optional(),
  previous_marks_percentage: percentageSchema.optional(),
  applied_for_scholarship: z.boolean().optional(),
  hostel_required: z.boolean().optional(),
});

export const applicationPaymentCreateSchema = z.object({
  application_id: z.number().positive(),
  amount: z.number().positive().multipleOf(0.01),
  payment_mode: z.nativeEnum(PaymentMode),
  transaction_id: z.string().max(100).optional(),
  payment_proof_url: z.string().url().optional(),
});

// ============================================================================
// Quick Apply Schema
// ============================================================================

export const quickApplySchema = z.object({
  name: z.string().min(1, "Name is required").max(200),
  email: emailSchema,
  phone: phoneSchema,
  gender: z.string().min(1).max(20),
  program_id: z.number().positive("Please select a program"),
  state: z.string().min(1, "State is required").max(100),
  board: z.string().min(1, "Board is required").max(100),
  group_of_study: z.string().min(1, "Group of study is required").max(100),
});

// ============================================================================
// Document Schemas
// ============================================================================

export const documentVerifySchema = z.object({
  verified: z.boolean(),
  remarks: z.string().max(500).optional(),
});

// ============================================================================
// Payment Schemas
// ============================================================================

export const offlinePaymentVerifySchema = z.object({
  verified: z.boolean(),
  payment_proof_url: z.string().url().optional(),
  mode: z.nativeEnum(PaymentMode).optional(),
  transaction_id: z.string().max(100).optional(),
});

// ============================================================================
// Settings Schema
// ============================================================================

export const admissionSettingsSchema = z.object({
  application_fee_enabled: z.boolean().optional(),
  application_fee_amount: z.number().nonnegative().multipleOf(0.01).optional(),
  online_payment_enabled: z.boolean().optional(),
  offline_payment_enabled: z.boolean().optional(),
  send_credentials_email: z.boolean().optional(),
  send_credentials_sms: z.boolean().optional(),
  auto_create_student_account: z.boolean().optional(),
  portal_base_url: z.string().url().optional(),
});

// ============================================================================
// Type Exports (inferred from schemas)
// ============================================================================

export type ApplicationCreateInput = z.infer<typeof applicationCreateSchema>;
export type ApplicationUpdateInput = z.infer<typeof applicationUpdateSchema>;
export type QuickApplyInput = z.infer<typeof quickApplySchema>;
export type DocumentVerifyInput = z.infer<typeof documentVerifySchema>;
export type OfflinePaymentVerifyInput = z.infer<typeof offlinePaymentVerifySchema>;
export type AdmissionSettingsInput = z.infer<typeof admissionSettingsSchema>;
