/**
 * Fee Management Hooks
 * 
 * Custom React Query hooks for fee operations
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import feeApi from '@/services/fee-api';
import { queryKeys } from '@/config/react-query';
import { FeeStructureCreate, StudentFeeCreate, FeePaymentCreate, FeeConcessionCreate } from '@/types/fee';

// ============================================================================
// Fee Structure Hooks
// ============================================================================

export function useFeeStructures(filters?: {
    program_id?: number;
    academic_year?: string;
    is_active?: boolean;
}) {
    return useQuery({
        queryKey: queryKeys.fees.structures.list(filters),
        queryFn: () => feeApi.structures.list(filters),
    });
}

export function useCreateFeeStructure() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: FeeStructureCreate) => feeApi.structures.create(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.fees.structures.all });
            queryClient.invalidateQueries({ queryKey: queryKeys.fees.all });
        },
    });
}

// ============================================================================
// Student Fee Hooks
// ============================================================================

export function useStudentFees(filters?: any) {
    return useQuery({
        queryKey: queryKeys.fees.studentFees.list(filters),
        queryFn: () => feeApi.studentFees.list(filters),
    });
}

export function useStudentFeeSummary(studentId: number) {
    return useQuery({
        queryKey: queryKeys.fees.studentFees.summary(studentId),
        queryFn: () => feeApi.studentFees.getSummary(studentId),
        enabled: !!studentId,
    });
}

export function useAssignFeeStructure() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: StudentFeeCreate) => feeApi.studentFees.assign(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.fees.studentFees.all });
            queryClient.invalidateQueries({ queryKey: queryKeys.fees.all });
        },
    });
}

// ============================================================================
// Payment Hooks
// ============================================================================

export function useFeePayments(filters?: any) {
    return useQuery({
        queryKey: queryKeys.fees.payments.list(filters),
        queryFn: () => feeApi.payments.list(filters),
    });
}

export function useRecordPayment() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: FeePaymentCreate) => feeApi.payments.record(data),
        onSuccess: (_, variables) => {
            queryClient.invalidateQueries({ queryKey: queryKeys.fees.payments.all });
            queryClient.invalidateQueries({ queryKey: queryKeys.fees.studentFees.all });
            // Invalidate specific student fee summary
            if (variables.student_fee_id) {
                // We might need to map student_fee_id to student_id or invalidate all summaries
                // For now, let's keep it simple
            }
        },
    });
}

// ============================================================================
// Concession Hooks
// ============================================================================

export function useApplyConcession() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: FeeConcessionCreate) => feeApi.concessions.apply(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.fees.all });
        },
    });
}
