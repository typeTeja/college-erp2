/**
 * Student Management Hooks
 * 
 * Custom React Query hooks for student operations
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import studentApi from '@/services/student-api';
import { queryKeys } from '@/config/react-query';
import { Student } from '@/types/student';

// ============================================================================
// Query Hooks
// ============================================================================

/**
 * Fetch list of students with filters
 */
export function useStudents(filters?: {
    program_id?: number;
    year?: number;
    semester?: number;
    status?: string;
    search?: string;
}) {
    return useQuery({
        queryKey: queryKeys.students.list(filters),
        queryFn: () => studentApi.list(filters),
    });
}

/**
 * Fetch a single student by ID
 */
export function useStudent(id: number, enabled = true) {
    return useQuery({
        queryKey: queryKeys.students.detail(id),
        queryFn: () => studentApi.get(id),
        enabled: enabled && !!id,
    });
}

/**
 * Fetch student activity
 */
export function useStudentActivity(id: number) {
    return useQuery({
        queryKey: [...queryKeys.students.detail(id), 'activity'],
        queryFn: () => studentApi.getActivity(id),
        enabled: !!id,
    });
}

// ============================================================================
// Mutation Hooks
// ============================================================================

/**
 * Create a new student
 */
export function useCreateStudent() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: Partial<Student>) => studentApi.create(data),
        onSuccess: () => {
            // Invalidate and refetch students list
            queryClient.invalidateQueries({ queryKey: queryKeys.students.lists() });
        },
    });
}

/**
 * Update a student
 */
export function useUpdateStudent() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, data }: { id: number; data: Partial<Student> }) =>
            studentApi.update(id, data),
        onSuccess: (_, variables) => {
            // Invalidate specific student and lists
            queryClient.invalidateQueries({ queryKey: queryKeys.students.detail(variables.id) });
            queryClient.invalidateQueries({ queryKey: queryKeys.students.lists() });
        },
    });
}

/**
 * Delete a student
 */
export function useDeleteStudent() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (id: number) => studentApi.delete(id),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.students.lists() });
        },
    });
}

/**
 * Upload student document
 */
export function useUploadStudentDocument() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, file, documentType }: { id: number; file: File; documentType: string }) =>
            studentApi.uploadDocument(id, file, documentType),
        onSuccess: (_, variables) => {
            queryClient.invalidateQueries({ queryKey: queryKeys.students.detail(variables.id) });
        },
    });
}

/**
 * Deactivate a student
 */
export function useDeactivateStudent() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, reason }: { id: number; reason: string }) =>
            studentApi.deactivate(id, reason),
        onSuccess: (_, variables) => {
            queryClient.invalidateQueries({ queryKey: queryKeys.students.detail(variables.id) });
            queryClient.invalidateQueries({ queryKey: queryKeys.students.lists() });
        },
    });
}

/**
 * Reactivate a student
 */
export function useReactivateStudent() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (id: number) => studentApi.reactivate(id),
        onSuccess: (_, id) => {
            queryClient.invalidateQueries({ queryKey: queryKeys.students.detail(id) });
            queryClient.invalidateQueries({ queryKey: queryKeys.students.lists() });
        },
    });
}
