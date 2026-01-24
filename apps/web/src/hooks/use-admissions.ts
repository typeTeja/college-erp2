/**
 * Admission & Application Hooks
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import admissionApi from '@/services/admission-api';
import { queryKeys } from '@/config/react-query';

export function useAdmissions(filters?: {
    status?: string;
    program_id?: number;
    academic_year?: string;
    search?: string;
    show_deleted?: boolean;
}) {
    return useQuery({
        queryKey: queryKeys.admissions.list(filters),
        queryFn: () => admissionApi.list(filters),
    });
}

export function useAdmission(id: number, enabled = true) {
    return useQuery({
        queryKey: queryKeys.admissions.detail(id),
        queryFn: () => admissionApi.get(id),
        enabled: enabled && !!id,
    });
}

export function useCreateAdmission() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: admissionApi.create,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.admissions.lists() });
        },
    });
}

export function useUpdateAdmission() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, data }: { id: number; data: any }) =>
            admissionApi.update(id, data),
        onSuccess: (_, variables) => {
            queryClient.invalidateQueries({ queryKey: queryKeys.admissions.detail(variables.id) });
            queryClient.invalidateQueries({ queryKey: queryKeys.admissions.lists() });
        },
    });
}

export function useUploadAdmissionDocument() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, file, documentType }: { id: number; file: File; documentType: string }) =>
            admissionApi.uploadDocument(id, file, documentType),
        onSuccess: (_, variables) => {
            queryClient.invalidateQueries({ queryKey: queryKeys.admissions.detail(variables.id) });
        },
    });
}

export function useGenerateHallTicket() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (id: number) => admissionApi.generateHallTicket(id),
        onSuccess: (_, id) => {
            queryClient.invalidateQueries({ queryKey: queryKeys.admissions.detail(id) });
        },
    });
}

export function useInitiateAdmissionPayment() {
    return useMutation({
        mutationFn: ({ id, amount }: { id: number; amount: number }) =>
            admissionApi.initiatePayment(id, amount),
    });
}

export function useConfirmAdmission() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (id: number) => admissionApi.update(id, { status: 'ADMITTED' }),
        onSuccess: (_, id) => {
            queryClient.invalidateQueries({ queryKey: queryKeys.admissions.detail(id) });
            queryClient.invalidateQueries({ queryKey: queryKeys.admissions.lists() });
        },
    });
}

export function useDeleteApplication() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, reason }: { id: number; reason: string }) =>
            admissionApi.delete(id, reason),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.admissions.lists() });
        },
    });
}

export function useRestoreApplication() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (id: number) => admissionApi.restore(id),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.admissions.lists() });
        },
    });
}

