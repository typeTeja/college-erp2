import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from './api';
import { Faculty, FacultyCreateDTO, FacultyUpdateDTO } from '@/types/faculty';

export const facultyService = {
    useFaculties: (department?: string) => {
        return useQuery({
            queryKey: ['faculties', department],
            queryFn: async () => {
                const response = await api.get<Faculty[]>('/faculty/', {
                    params: { department }
                });
                return response.data;
            }
        });
    },

    useFaculty: (id: number) => {
        return useQuery({
            queryKey: ['faculty', id],
            queryFn: async () => {
                const response = await api.get<Faculty>(`/faculty/${id}`);
                return response.data;
            },
            enabled: !!id
        });
    },

    useCreateFaculty: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (data: FacultyCreateDTO) => {
                const response = await api.post<Faculty>('/faculty/', data);
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['faculties'] });
            }
        });
    },

    useMyProfile: () => {
        return useQuery({
            queryKey: ['faculty-me'],
            queryFn: async () => {
                const response = await api.get<Faculty>('/faculty/me');
                return response.data;
            }
        });
    }
};
