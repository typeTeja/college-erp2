/**
 * Fee Management Hooks
 * 
 * Custom React Query hooks for fee operations
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import feeApi from '@/services/fee-api';
import { queryKeys } from '@/config/react-query';

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
        queryFn: () => feeApi.listFeeStructures(filters),
    });
}

export function useCreateFeeStructure() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: feeApi.createFeeStructure,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.fees.structures.all });
        },
    });
}

// ============================================================================
// Student Fee Hooks
// ============================================================================

export function useStudentFees(filters?: {
    student_id?: number;
    program_id?: number;
    academic_year?: string;
    payment_status?: string;
}) {
    return useQuery({
        queryKey: queryKeys.fees.studentFees.list(filters),
        queryFn: () => feeApi.listStudentFees(filters),
    });
}

export function useStudentFeeSummary(studentId: number) {
    return useQuery({
        queryKey: queryKeys.fees.studentFees.summary(studentId),
        queryFn: () => feeApi.getStudentFeeSummary(studentId),
        enabled: !!studentId,
    });
}

export function useAssignFeeStructure() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: feeApi.assignFeeStructure,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.fees.studentFees.all });
        },
    });
}

// ============================================================================
// Payment Hooks
// ============================================================================

export function useFeePayments(filters?: {
    student_id?: number;
    from_date?: string;
    to_date?: string;
    payment_mode?: string;
}) {
    return useQuery({
        queryKey: queryKeys.fees.payments.list(filters),
        queryFn: () => feeApi.listPayments(filters),
    });
}

export function useRecordPayment() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: feeApi.recordPayment,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.fees.payments.all });
            queryClient.invalidateQueries({ queryKey: queryKeys.fees.studentFees.all });
        },
    });
}

// ============================================================================
// Concession Hooks
// ============================================================================

export function useApplyConcession() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: feeApi.applyConcession,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.fees.studentFees.all });
        },
    });
}
