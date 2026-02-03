/**
 * Finance Domain React Query Hooks - v1.0.0
 * 
 * Custom hooks for finance/fee data fetching and mutations.
 * 
 * CONTRACT VERSION: v1.0.0
 * STATUS: FROZEN (2026-02-03)
 */

import { useQuery, useMutation, useQueryClient, type UseQueryOptions, type UseMutationOptions } from '@tanstack/react-query';
import { feeApi } from '@/services/fee-api';
import type {
  FeeStructureCreate,
  FeeStructureRead,
  FeeStructureFilters,
  FeePaymentCreate,
  FeePaymentRead,
  PaymentInitiateRequest,
  PaymentInitiateResponse,
  StudentFee,
  StudentFeeCreate,
  StudentFeeSummary,
  StudentFeeFilters,
  FeeConcessionCreate,
  FeeConcession,
  FeeFineCreate,
  FeeFine,
  FeeDefaulter,
  PaymentFilters,
  ScholarshipSlabCreate,
  ScholarshipSlabRead,
} from '@/types/fee';

// ============================================================================
// Query Keys
// ============================================================================

export const financeKeys = {
  all: ['finance'] as const,
  feeStructures: () => [...financeKeys.all, 'fee-structures'] as const,
  feeStructure: (filters?: FeeStructureFilters) => [...financeKeys.feeStructures(), filters] as const,
  feeStructureDetail: (id: number) => [...financeKeys.feeStructures(), id] as const,
  studentFees: () => [...financeKeys.all, 'student-fees'] as const,
  studentFee: (filters?: StudentFeeFilters) => [...financeKeys.studentFees(), filters] as const,
  studentFeeSummary: (studentId: number) => [...financeKeys.studentFees(), studentId, 'summary'] as const,
  payments: () => [...financeKeys.all, 'payments'] as const,
  payment: (filters?: PaymentFilters) => [...financeKeys.payments(), filters] as const,
  paymentDetail: (id: number) => [...financeKeys.payments(), id] as const,
  concessions: (studentFeeId?: number) => [...financeKeys.all, 'concessions', studentFeeId] as const,
  fines: (studentFeeId?: number) => [...financeKeys.all, 'fines', studentFeeId] as const,
  scholarships: () => [...financeKeys.all, 'scholarships'] as const,
  defaulters: (params?: Record<string, any>) => [...financeKeys.all, 'defaulters', params] as const,
  reports: {
    collection: (params: Record<string, any>) => [...financeKeys.all, 'reports', 'collection', params] as const,
    outstanding: (params?: Record<string, any>) => [...financeKeys.all, 'reports', 'outstanding', params] as const,
  },
};

// ============================================================================
// Fee Structure Queries
// ============================================================================

/**
 * Get list of fee structures
 */
export const useFeeStructures = (
  filters?: FeeStructureFilters,
  options?: Omit<UseQueryOptions<FeeStructureRead[]>, 'queryKey' | 'queryFn'>
) => {
  return useQuery({
    queryKey: financeKeys.feeStructure(filters),
    queryFn: () => feeApi.listFeeStructures(filters),
    ...options,
  });
};

/**
 * Get single fee structure
 */
export const useFeeStructure = (
  id: number,
  options?: Omit<UseQueryOptions<FeeStructureRead>, 'queryKey' | 'queryFn'>
) => {
  return useQuery({
    queryKey: financeKeys.feeStructureDetail(id),
    queryFn: () => feeApi.getFeeStructure(id),
    enabled: !!id,
    ...options,
  });
};

// ============================================================================
// Student Fee Queries
// ============================================================================

/**
 * Get list of student fees
 */
export const useStudentFees = (
  filters?: StudentFeeFilters,
  options?: Omit<UseQueryOptions<StudentFee[]>, 'queryKey' | 'queryFn'>
) => {
  return useQuery({
    queryKey: financeKeys.studentFee(filters),
    queryFn: () => feeApi.listStudentFees(filters),
    ...options,
  });
};

/**
 * Get student fee summary
 */
export const useStudentFeeSummary = (
  studentId: number,
  options?: Omit<UseQueryOptions<StudentFeeSummary>, 'queryKey' | 'queryFn'>
) => {
  return useQuery({
    queryKey: financeKeys.studentFeeSummary(studentId),
    queryFn: () => feeApi.getStudentFeeSummary(studentId),
    enabled: !!studentId,
    ...options,
  });
};

// ============================================================================
// Payment Queries
// ============================================================================

/**
 * Get list of payments
 */
export const usePayments = (
  filters?: PaymentFilters,
  options?: Omit<UseQueryOptions<FeePaymentRead[]>, 'queryKey' | 'queryFn'>
) => {
  return useQuery({
    queryKey: financeKeys.payment(filters),
    queryFn: () => feeApi.listPayments(filters),
    ...options,
  });
};

/**
 * Get payment by ID
 */
export const usePayment = (
  id: number,
  options?: Omit<UseQueryOptions<FeePaymentRead>, 'queryKey' | 'queryFn'>
) => {
  return useQuery({
    queryKey: financeKeys.paymentDetail(id),
    queryFn: () => feeApi.getPayment(id),
    enabled: !!id,
    ...options,
  });
};

// ============================================================================
// Concession & Fine Queries
// ============================================================================

/**
 * Get concessions for a student fee
 */
export const useConcessions = (
  studentFeeId: number,
  options?: Omit<UseQueryOptions<FeeConcession[]>, 'queryKey' | 'queryFn'>
) => {
  return useQuery({
    queryKey: financeKeys.concessions(studentFeeId),
    queryFn: () => feeApi.listConcessions(studentFeeId),
    enabled: !!studentFeeId,
    ...options,
  });
};

/**
 * Get fines for a student fee
 */
export const useFines = (
  studentFeeId: number,
  options?: Omit<UseQueryOptions<FeeFine[]>, 'queryKey' | 'queryFn'>
) => {
  return useQuery({
    queryKey: financeKeys.fines(studentFeeId),
    queryFn: () => feeApi.listFines(studentFeeId),
    enabled: !!studentFeeId,
    ...options,
  });
};

// ============================================================================
// Scholarship Queries
// ============================================================================

/**
 * Get scholarship slabs
 */
export const useScholarshipSlabs = (
  options?: Omit<UseQueryOptions<ScholarshipSlabRead[]>, 'queryKey' | 'queryFn'>
) => {
  return useQuery({
    queryKey: financeKeys.scholarships(),
    queryFn: () => feeApi.listScholarshipSlabs(),
    ...options,
  });
};

// ============================================================================
// Defaulter Queries
// ============================================================================

/**
 * Get fee defaulters
 */
export const useDefaulters = (
  params?: { program_id?: number; year?: number; min_due_amount?: number },
  options?: Omit<UseQueryOptions<FeeDefaulter[]>, 'queryKey' | 'queryFn'>
) => {
  return useQuery({
    queryKey: financeKeys.defaulters(params),
    queryFn: () => feeApi.getDefaulters(params),
    ...options,
  });
};

// ============================================================================
// Report Queries
// ============================================================================

/**
 * Get fee collection report
 */
export const useCollectionReport = (
  params: { from_date: string; to_date: string; program_id?: number },
  options?: Omit<UseQueryOptions<any>, 'queryKey' | 'queryFn'>
) => {
  return useQuery({
    queryKey: financeKeys.reports.collection(params),
    queryFn: () => feeApi.getCollectionReport(params),
    enabled: !!params.from_date && !!params.to_date,
    ...options,
  });
};

/**
 * Get outstanding fees report
 */
export const useOutstandingReport = (
  params?: { program_id?: number; academic_year?: string },
  options?: Omit<UseQueryOptions<any>, 'queryKey' | 'queryFn'>
) => {
  return useQuery({
    queryKey: financeKeys.reports.outstanding(params),
    queryFn: () => feeApi.getOutstandingReport(params),
    ...options,
  });
};

// ============================================================================
// Mutations
// ============================================================================

/**
 * Create fee structure
 */
export const useCreateFeeStructure = (
  options?: UseMutationOptions<FeeStructureRead, Error, FeeStructureCreate>
) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: FeeStructureCreate) => feeApi.createFeeStructure(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: financeKeys.feeStructures() });
    },
    ...options,
  });
};

/**
 * Update fee structure
 */
export const useUpdateFeeStructure = (
  options?: UseMutationOptions<FeeStructureRead, Error, { id: number; data: Partial<FeeStructureCreate> }>
) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }) => feeApi.updateFeeStructure(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: financeKeys.feeStructureDetail(variables.id) });
      queryClient.invalidateQueries({ queryKey: financeKeys.feeStructures() });
    },
    ...options,
  });
};

/**
 * Delete fee structure
 */
export const useDeleteFeeStructure = (
  options?: UseMutationOptions<{ message: string }, Error, number>
) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => feeApi.deleteFeeStructure(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: financeKeys.feeStructures() });
    },
    ...options,
  });
};

/**
 * Create student fee
 */
export const useCreateStudentFee = (
  options?: UseMutationOptions<StudentFee, Error, StudentFeeCreate>
) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: StudentFeeCreate) => feeApi.createStudentFee(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: financeKeys.studentFees() });
    },
    ...options,
  });
};

/**
 * Create payment
 */
export const useCreatePayment = (
  options?: UseMutationOptions<FeePaymentRead, Error, FeePaymentCreate>
) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: FeePaymentCreate) => feeApi.createPayment(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: financeKeys.payments() });
      queryClient.invalidateQueries({ queryKey: financeKeys.studentFees() });
    },
    ...options,
  });
};

/**
 * Initiate online payment
 */
export const useInitiatePayment = (
  options?: UseMutationOptions<PaymentInitiateResponse, Error, PaymentInitiateRequest>
) => {
  return useMutation({
    mutationFn: (data: PaymentInitiateRequest) => feeApi.initiatePayment(data),
    ...options,
  });
};

/**
 * Create concession
 */
export const useCreateConcession = (
  options?: UseMutationOptions<FeeConcession, Error, FeeConcessionCreate>
) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: FeeConcessionCreate) => feeApi.createConcession(data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: financeKeys.concessions(variables.student_fee_id) });
      queryClient.invalidateQueries({ queryKey: financeKeys.studentFees() });
    },
    ...options,
  });
};

/**
 * Delete concession
 */
export const useDeleteConcession = (
  options?: UseMutationOptions<{ message: string }, Error, { id: number; studentFeeId: number }>
) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id }) => feeApi.deleteConcession(id),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: financeKeys.concessions(variables.studentFeeId) });
      queryClient.invalidateQueries({ queryKey: financeKeys.studentFees() });
    },
    ...options,
  });
};

/**
 * Create fine
 */
export const useCreateFine = (
  options?: UseMutationOptions<FeeFine, Error, FeeFineCreate>
) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: FeeFineCreate) => feeApi.createFine(data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: financeKeys.fines(variables.student_fee_id) });
      queryClient.invalidateQueries({ queryKey: financeKeys.studentFees() });
    },
    ...options,
  });
};

/**
 * Waive fine
 */
export const useWaiveFine = (
  options?: UseMutationOptions<FeeFine, Error, { id: number; studentFeeId: number }>
) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id }) => feeApi.waiveFine(id),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: financeKeys.fines(variables.studentFeeId) });
      queryClient.invalidateQueries({ queryKey: financeKeys.studentFees() });
    },
    ...options,
  });
};

/**
 * Create scholarship slab
 */
export const useCreateScholarshipSlab = (
  options?: UseMutationOptions<ScholarshipSlabRead, Error, ScholarshipSlabCreate>
) => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: ScholarshipSlabCreate) => feeApi.createScholarshipSlab(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: financeKeys.scholarships() });
    },
    ...options,
  });
};
