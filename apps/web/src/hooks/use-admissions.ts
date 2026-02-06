/**
 * Admission Domain React Query Hooks - Consolidated
 */

import { useQuery, useMutation, useQueryClient, type UseQueryOptions, type UseMutationOptions } from '@tanstack/react-query';
import admissionApi from '@/services/admission-api';
import type {
    ApplicationCreate,
    ApplicationRead,
    ApplicationUpdate,
    QuickApplyRequest,
    QuickApplyResponse,
    OfflinePaymentVerifyRequest,
    DocumentVerifyRequest,
    ApplicationDocument,
    ActivityLog,
} from '@/types/admissions';
import { queryKeys } from '@/config/react-query';

// ============================================================================
// Query Keys
// ============================================================================

export const admissionKeys = {
    all: ['admissions'] as const,
    lists: () => [...admissionKeys.all, 'list'] as const,
    list: (filters?: Record<string, any>) => [...admissionKeys.lists(), filters] as const,
    details: () => [...admissionKeys.all, 'detail'] as const,
    detail: (id: number) => [...admissionKeys.details(), id] as const,
    myApplication: () => [...admissionKeys.all, 'my-application'] as const,
    activity: (id: number) => [...admissionKeys.detail(id), 'activity'] as const,
    settings: () => [...admissionKeys.all, 'settings'] as const,
    paymentConfig: () => [...admissionKeys.all, 'payment-config'] as const,
};

// ============================================================================
// Queries
// ============================================================================

/**
 * Get list of applications
 */
export const useApplications = (
    filters?: {
        status?: string;
        program_id?: number;
        academic_year?: string;
        search?: string;
        show_deleted?: boolean;
    },
    options?: Omit<UseQueryOptions<ApplicationRead[]>, 'queryKey' | 'queryFn'>
) => {
    return useQuery({
        queryKey: queryKeys.admissions.list(filters),
        queryFn: () => admissionApi.list(filters),
        ...options,
    });
};

/**
 * Alias for useApplications to support existing dashboard code
 */
export const useAdmissions = useApplications;

/**
 * Get single application
 */
export const useApplication = (
    id: number,
    options?: Omit<UseQueryOptions<ApplicationRead>, 'queryKey' | 'queryFn'>
) => {
    return useQuery({
        queryKey: queryKeys.admissions.detail(id),
        queryFn: () => admissionApi.get(id),
        enabled: !!id,
        ...options,
    });
};

/**
 * Get my application (student portal)
 */
export const useMyApplication = (
    options?: Omit<UseQueryOptions<ApplicationRead>, 'queryKey' | 'queryFn'>
) => {
    return useQuery({
        queryKey: admissionKeys.myApplication(),
        queryFn: () => admissionApi.getMyApplication(),
        ...options,
    });
};

/**
 * Get application activity log
 */
export const useApplicationActivity = (
    id: number,
    options?: Omit<UseQueryOptions<ActivityLog[]>, 'queryKey' | 'queryFn'>
) => {
    return useQuery({
        queryKey: queryKeys.admissions.detail(id),
        queryFn: () => admissionApi.getActivity(id),
        enabled: !!id,
        ...options,
    });
};

/**
 * Get payment configuration
 */
export const usePaymentConfig = (
    options?: Omit<UseQueryOptions<any>, 'queryKey' | 'queryFn'>
) => {
    return useQuery({
        queryKey: admissionKeys.paymentConfig(),
        queryFn: () => admissionApi.getPaymentConfig(),
        ...options,
    });
};

/**
 * Get admission settings (admin)
 */
export const useAdmissionSettings = (
    options?: Omit<UseQueryOptions<any>, 'queryKey' | 'queryFn'>
) => {
    return useQuery({
        queryKey: admissionKeys.settings(),
        queryFn: () => admissionApi.getSettings(),
        ...options,
    });
};

// ============================================================================
// Mutations
// ============================================================================

/**
 * Create application
 */
export const useCreateApplication = (
    options?: UseMutationOptions<ApplicationRead, Error, ApplicationCreate>
) => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: ApplicationCreate) => admissionApi.create(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.admissions.lists() });
        },
        ...options,
    });
};

/**
 * Quick apply v2
 */
export const useQuickApply = (
    options?: UseMutationOptions<QuickApplyResponse, Error, QuickApplyRequest>
) => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: QuickApplyRequest) => admissionApi.quickApplyV2(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.admissions.lists() });
        },
        ...options,
    });
};

/**
 * Update application
 */
export const useUpdateApplication = (
    options?: UseMutationOptions<ApplicationRead, Error, { id: number; data: ApplicationUpdate }>
) => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, data }: { id: number; data: ApplicationUpdate }) =>
            admissionApi.update(id, data),
        onSuccess: (_, variables) => {
            queryClient.invalidateQueries({ queryKey: queryKeys.admissions.detail(variables.id) });
            queryClient.invalidateQueries({ queryKey: queryKeys.admissions.lists() });
        },
        ...options,
    });
};

/**
 * Confirm admission (Triggers student creation)
 */
export const useConfirmAdmission = (
    options?: UseMutationOptions<ApplicationRead, Error, number>
) => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (id: number) => admissionApi.confirmAdmission(id),
        onSuccess: (_, id) => {
            queryClient.invalidateQueries({ queryKey: queryKeys.admissions.detail(id) });
            queryClient.invalidateQueries({ queryKey: queryKeys.admissions.lists() });
        },
        ...options,
    });
};

/**
 * Delete application
 */
export const useDeleteApplication = (
    options?: UseMutationOptions<{ message: string }, Error, { id: number; reason: string }>
) => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, reason }: { id: number; reason: string }) =>
            admissionApi.delete(id, reason),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.admissions.lists() });
        },
        ...options,
    });
};

/**
 * Restore application
 */
export const useRestoreApplication = (
    options?: UseMutationOptions<ApplicationRead, Error, number>
) => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (id: number) => admissionApi.restore(id),
        onSuccess: (_, id) => {
            queryClient.invalidateQueries({ queryKey: queryKeys.admissions.detail(id) });
            queryClient.invalidateQueries({ queryKey: queryKeys.admissions.lists() });
        },
        ...options,
    });
};

/**
 * Update admission settings
 */
export const useUpdateAdmissionSettings = (
    options?: UseMutationOptions<{ message: string }, Error, any>
) => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: any) => admissionApi.updateSettings(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: admissionKeys.settings() });
        },
        ...options,
    });
};

/**
 * Upload document
 */
export const useUploadDocument = (
    options?: UseMutationOptions<
        ApplicationDocument,
        Error,
        { id: number; file: File; documentType: string }
    >
) => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, file, documentType }) =>
            admissionApi.uploadDocument(id, file, documentType),
        onSuccess: (_, variables) => {
            queryClient.invalidateQueries({ queryKey: queryKeys.admissions.detail(variables.id) });
        },
        ...options,
    });
};

/**
 * Verify document
 */
export const useVerifyDocument = (
    options?: UseMutationOptions<
        ApplicationDocument,
        Error,
        { applicationId: number; documentId: number; data: DocumentVerifyRequest }
    >
) => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ applicationId, documentId, data }) =>
            admissionApi.verifyDocument(applicationId, documentId, data),
        onSuccess: (_, variables) => {
            queryClient.invalidateQueries({ queryKey: queryKeys.admissions.detail(variables.applicationId) });
        },
        ...options,
    });
};

/**
 * Verify offline payment
 */
export const useVerifyOfflinePayment = (
    options?: UseMutationOptions<
        ApplicationRead,
        Error,
        { id: number; data: OfflinePaymentVerifyRequest }
    >
) => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, data }) => admissionApi.verifyOfflinePayment(id, data),
        onSuccess: (_, variables) => {
            queryClient.invalidateQueries({ queryKey: queryKeys.admissions.detail(variables.id) });
            queryClient.invalidateQueries({ queryKey: queryKeys.admissions.lists() });
        },
        ...options,
    });
};
