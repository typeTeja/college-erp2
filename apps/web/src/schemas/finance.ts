/**
 * Finance Domain Validation Schemas - v1.0.0
 * 
 * Zod schemas for client-side validation matching backend contract.
 * 
 * CONTRACT VERSION: v1.0.0
 * STATUS: FROZEN (2026-02-03)
 */

import { z } from 'zod';
import { FeeCategory, PaymentMode, PaymentStatus, VALIDATION_PATTERNS, VALIDATION_LIMITS } from '@/types/fee';

// ============================================================================
// Validation Patterns
// ============================================================================

export const phoneSchema = z
  .string()
  .regex(VALIDATION_PATTERNS.phone, "Phone must be exactly 10 digits");

export const academicYearSchema = z
  .string()
  .regex(VALIDATION_PATTERNS.academicYear, "Academic year must be in format YYYY-YYYY (e.g., 2024-2025)");

export const codeSchema = z
  .string()
  .min(1)
  .max(20)
  .regex(VALIDATION_PATTERNS.code, "Code must be uppercase alphanumeric with underscores");

export const amountSchema = z
  .number()
  .min(VALIDATION_LIMITS.amount.min, "Amount must be positive")
  .max(VALIDATION_LIMITS.amount.max, `Amount cannot exceed ₹${VALIDATION_LIMITS.amount.max.toLocaleString()}`)
  .multipleOf(0.01, "Amount can have at most 2 decimal places");

export const emailSchema = z
  .string()
  .email("Invalid email address");

// ============================================================================
// Fee Head Schemas
// ============================================================================

export const feeHeadCreateSchema = z.object({
  name: z.string().min(1).max(100),
  code: codeSchema,
  description: z.string().max(500).optional(),
  category: z.string().max(50).optional(),
  is_mandatory: z.boolean().optional(),
});

// ============================================================================
// Fee Structure Schemas
// ============================================================================

export const feeStructureCreateSchema = z.object({
  program_id: z.number().positive("Program ID must be positive"),
  academic_year: academicYearSchema,
  year: z.number()
    .int()
    .min(VALIDATION_LIMITS.year.min, `Year must be at least ${VALIDATION_LIMITS.year.min}`)
    .max(VALIDATION_LIMITS.year.max, `Year cannot exceed ${VALIDATION_LIMITS.year.max}`),
  slab: z.string().max(20).optional(),
  category: z.nativeEnum(FeeCategory).optional(),
  tuition_fee: amountSchema,
  library_fee: amountSchema.optional(),
  lab_fee: amountSchema.optional(),
  uniform_fee: amountSchema.optional(),
  caution_deposit: amountSchema.optional(),
  digital_fee: amountSchema.optional(),
  miscellaneous_fee: amountSchema.optional(),
  number_of_installments: z.number()
    .int()
    .min(VALIDATION_LIMITS.installments.min)
    .max(VALIDATION_LIMITS.installments.max)
    .optional(),
});

// ============================================================================
// Payment Schemas
// ============================================================================

export const feePaymentCreateSchema = z.object({
  student_fee_id: z.number().positive(),
  amount: amountSchema.refine(val => val > 0, "Amount must be greater than 0"),
  payment_mode: z.nativeEnum(PaymentMode),
  transaction_id: z.string().max(100).optional(),
  reference_number: z.string().max(100).optional(),
  bank_name: z.string().max(100).optional(),
  remarks: z.string().max(500).optional(),
});

export const paymentInitiateSchema = z.object({
  student_id: z.number().positive("Student ID must be positive"),
  student_fee_id: z.number().positive("Student fee ID must be positive"),
  amount: amountSchema.refine(val => val > 0, "Amount must be greater than 0"),
  customer_name: z.string().min(1).max(200),
  customer_email: emailSchema,
  customer_phone: phoneSchema,
});

export const paymentCallbackSchema = z.object({
  transaction_id: z.string().min(1).max(100),
  gateway_payment_id: z.string().max(100).optional(),
  gateway_signature: z.string().max(500).optional(),
  status: z.nativeEnum(PaymentStatus),
  amount: amountSchema.refine(val => val > 0, "Amount must be greater than 0"),
  payment_mode: z.nativeEnum(PaymentMode).optional(),
});

// ============================================================================
// Scholarship Schemas
// ============================================================================

export const scholarshipSlabCreateSchema = z.object({
  name: z.string().min(1).max(100),
  code: codeSchema,
  description: z.string().max(500).optional(),
  discount_type: z.enum(["PERCENTAGE", "FIXED_AMOUNT"]).optional(),
  discount_value: z.number().nonnegative(),
  min_percentage: z.number()
    .min(VALIDATION_LIMITS.percentage.min)
    .max(VALIDATION_LIMITS.percentage.max)
    .optional(),
  max_percentage: z.number()
    .min(VALIDATION_LIMITS.percentage.min)
    .max(VALIDATION_LIMITS.percentage.max)
    .optional(),
});

// ============================================================================
// Concession Schemas
// ============================================================================

export const feeConcessionCreateSchema = z.object({
  student_fee_id: z.number().positive(),
  concession_type: z.string().min(1).max(100),
  amount: amountSchema.optional(),
  percentage: z.number()
    .min(VALIDATION_LIMITS.percentage.min)
    .max(VALIDATION_LIMITS.percentage.max)
    .optional(),
  remarks: z.string().max(500).optional(),
}).refine(
  data => data.amount !== undefined || data.percentage !== undefined,
  "Either amount or percentage must be provided"
);

// ============================================================================
// Fine Schemas
// ============================================================================

export const feeFineCreateSchema = z.object({
  student_fee_id: z.number().positive(),
  installment_number: z.number().int().positive(),
  fine_amount: amountSchema.refine(val => val > 0, "Fine amount must be greater than 0"),
  reason: z.string().min(1).max(500),
});

// ============================================================================
// Filter Schemas
// ============================================================================

export const feeStructureFiltersSchema = z.object({
  academic_year: academicYearSchema.optional(),
  program_id: z.number().positive().optional(),
  year: z.number().int().min(1).max(6).optional(),
  category: z.nativeEnum(FeeCategory).optional(),
});

export const studentFeeFiltersSchema = z.object({
  student_id: z.number().positive().optional(),
  program_id: z.number().positive().optional(),
  academic_year: academicYearSchema.optional(),
  payment_status: z.string().optional(),
});

export const paymentFiltersSchema = z.object({
  student_id: z.number().positive().optional(),
  from_date: z.string().datetime().optional(),
  to_date: z.string().datetime().optional(),
  payment_mode: z.nativeEnum(PaymentMode).optional(),
});

// ============================================================================
// Type Exports (inferred from schemas)
// ============================================================================

export type FeeHeadCreateInput = z.infer<typeof feeHeadCreateSchema>;
export type FeeStructureCreateInput = z.infer<typeof feeStructureCreateSchema>;
export type FeePaymentCreateInput = z.infer<typeof feePaymentCreateSchema>;
export type PaymentInitiateInput = z.infer<typeof paymentInitiateSchema>;
export type PaymentCallbackInput = z.infer<typeof paymentCallbackSchema>;
export type ScholarshipSlabCreateInput = z.infer<typeof scholarshipSlabCreateSchema>;
export type FeeConcessionCreateInput = z.infer<typeof feeConcessionCreateSchema>;
export type FeeFineCreateInput = z.infer<typeof feeFineCreateSchema>;
export type FeeStructureFiltersInput = z.infer<typeof feeStructureFiltersSchema>;
export type StudentFeeFiltersInput = z.infer<typeof studentFeeFiltersSchema>;
export type PaymentFiltersInput = z.infer<typeof paymentFiltersSchema>;
