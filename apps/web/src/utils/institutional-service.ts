import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from './api';
import { 
    Department, DepartmentCreateData, 
    Designation, DesignationCreateData 
} from '@/types/institutional';
import { toast } from 'sonner';

export const institutionalService = {
    // ----------------------------------------------------------------------
    // Department Hooks
    // ----------------------------------------------------------------------
    
    useDepartments: () => {
        return useQuery({
            queryKey: ['departments'],
            queryFn: async () => {
                const response = await api.get<Department[]>('/system/departments');
                return response.data;
            }
        });
    },

    useCreateDepartment: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (data: DepartmentCreateData) => {
                const response = await api.post<Department>('/system/departments', data);
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['departments'] });
                toast.success('Department created successfully');
            },
            onError: (error: any) => {
                toast.error(error.response?.data?.detail || 'Failed to create department');
            }
        });
    },

    useUpdateDepartment: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async ({ id, data }: { id: number; data: Partial<DepartmentCreateData> }) => {
                const response = await api.patch<Department>(`/system/departments/${id}`, data);
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['departments'] });
                toast.success('Department updated successfully');
            },
            onError: (error: any) => {
                toast.error(error.response?.data?.detail || 'Failed to update department');
            }
        });
    },

    useDeleteDepartment: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (id: number) => {
                await api.delete(`/system/departments/${id}`);
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['departments'] });
                toast.success('Department deleted successfully');
            },
            onError: (error: any) => {
                toast.error(error.response?.data?.detail || 'Failed to delete department');
            }
        });
    },

    // ----------------------------------------------------------------------
    // Designation Hooks
    // ----------------------------------------------------------------------
    
    useDesignations: (isTeaching?: boolean) => {
        return useQuery({
            queryKey: ['designations', { isTeaching }],
            queryFn: async () => {
                const response = await api.get<Designation[]>('/hr/designations', {
                    params: isTeaching !== undefined ? { is_teaching: isTeaching } : {}
                });
                return response.data;
            }
        });
    },

    useCreateDesignation: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (data: DesignationCreateData) => {
                const response = await api.post<Designation>('/hr/designations', data);
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['designations'] });
                toast.success('Designation created successfully');
            },
            onError: (error: any) => {
                toast.error(error.response?.data?.detail || 'Failed to create designation');
            }
        });
    },

    useUpdateDesignation: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async ({ id, data }: { id: number; data: Partial<DesignationCreateData> }) => {
                const response = await api.patch<Designation>(`/hr/designations/${id}`, data);
                return response.data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['designations'] });
                toast.success('Designation updated successfully');
            },
            onError: (error: any) => {
                toast.error(error.response?.data?.detail || 'Failed to update designation');
            }
        });
    },

    useDeleteDesignation: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (id: number) => {
                await api.delete(`/hr/designations/${id}`);
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['designations'] });
                toast.success('Designation deleted successfully');
            },
            onError: (error: any) => {
                toast.error(error.response?.data?.detail || 'Failed to delete designation');
            }
        });
    }
};
