/**
 * Faculty Management Hooks
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { queryKeys } from '@/config/react-query';

// Placeholder - will need actual API service
const facultyApi = {
    list: async (filters?: any) => {
        const response = await fetch('/api/v1/faculty');
        return response.json();
    },
    getProfile: async () => {
        const response = await fetch('/api/v1/faculty/me');
        return response.json();
    }
};

export function useFaculty(filters?: {
    department?: string;
    search?: string;
}) {
    return useQuery({
        queryKey: ['faculty', 'list', filters],
        queryFn: () => facultyApi.list(filters),
    });
}

export function useMyProfile() {
    return useQuery({
        queryKey: ['faculty', 'profile'],
        queryFn: () => facultyApi.getProfile(),
    });
}

export function useCreateFaculty() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: any) => facultyApi.list(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['faculty'] });
        },
    });
}
