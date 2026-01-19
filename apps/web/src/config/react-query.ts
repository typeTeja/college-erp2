/**
 * React Query Configuration
 * 
 * Central configuration for TanStack Query (React Query)
 */
import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            staleTime: 5 * 60 * 1000,
            gcTime: 10 * 60 * 1000,
            retry: 3,
            retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
            refetchOnWindowFocus: false,
            refetchOnReconnect: true,
            refetchOnMount: true,
        },
        mutations: {
            retry: 1,
            retryDelay: 1000,
        },
    },
});

// Query keys factory for consistent cache keys
export const queryKeys = {
    // Students
    students: {
        all: ['students'] as const,
        lists: () => ['students', 'list'] as const,
        list: (filters?: any) => ['students', 'list', { filters }] as const,
        details: () => ['students', 'detail'] as const,
        detail: (id: number) => ['students', 'detail', id] as const,
    },

    // Admissions
    admissions: {
        all: ['admissions'] as const,
        lists: () => ['admissions', 'list'] as const,
        list: (filters?: any) => ['admissions', 'list', { filters }] as const,
        details: () => ['admissions', 'detail'] as const,
        detail: (id: number) => ['admissions', 'detail', id] as const,
    },

    // Fees


    // Exams
    exams: {
        internal: {
            all: ['exams', 'internal'] as const,
            list: (filters?: any) => ['exams', 'internal', { filters }] as const,
            detail: (id: number) => ['exams', 'internal', id] as const,
            marks: (examId: number) => ['exams', 'internal', 'marks', examId] as const,
        },
    },

    // Fees extended
    fees: {
        all: ['fees'] as const,
        structures: {
            all: ['fees', 'structures'] as const,
            list: (filters?: any) => ['fees', 'structures', { filters }] as const,
        },
        studentFees: {
            all: ['fees', 'student-fees'] as const,
            list: (filters?: any) => ['fees', 'student-fees', { filters }] as const,
            summary: (studentId: number) => ['fees', 'student-fees', 'summary', studentId] as const,
        },
        payments: {
            all: ['fees', 'payments'] as const,
            list: (filters?: any) => ['fees', 'payments', { filters }] as const,
        },
        concessions: {
            all: ['fees', 'concessions'] as const,
            list: (studentFeeId?: number) => ['fees', 'concessions', { studentFeeId }] as const,
        },
    },

    // Portal
    portal: {
        all: ['portal'] as const,
        dashboard: ['portal', 'dashboard'],
        notifications: ['portal', 'notifications'],
        profile: ['portal', 'profile'],
    },

    // Analytics
    analytics: {
        dashboard: ['analytics', 'dashboard'] as const,
        trends: (type: string, filters?: any) => ['analytics', 'trends', type, { filters }] as const,
    },

    // Hostel
    hostel: {
        all: ['hostel'] as const,
        hostels: ['hostel', 'hostels'] as const,
        rooms: (filters?: any) => ['hostel', 'rooms', { filters }] as const,
    },

    // Library
    library: {
        books: {
            all: ['library', 'books'] as const,
            list: (filters?: any) => ['library', 'books', { filters }] as const,
        },
        members: ['library', 'members'] as const,
    },
};
