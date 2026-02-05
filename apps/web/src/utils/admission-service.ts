import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { 
    getBoards, createBoard, updateBoard, deleteBoard, Board,
    getLeadSources, createLeadSource, updateLeadSource, deleteLeadSource, LeadSource,
    getReservationCategories, createReservationCategory, updateReservationCategory, deleteReservationCategory, ReservationCategory
} from './master-data-service';
import { toast } from 'sonner';

export const admissionService = {
    // ----------------------------------------------------------------------
    // Board Hooks
    // ----------------------------------------------------------------------
    
    useBoards: (isActive?: boolean) => {
        return useQuery({
            queryKey: ['boards', { isActive }],
            queryFn: () => getBoards(isActive)
        });
    },

    useCreateBoard: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: (data: Partial<Board>) => createBoard(data),
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['boards'] });
                toast.success('Board created successfully');
            },
            onError: (error: any) => {
                toast.error(error.response?.data?.detail || 'Failed to create board');
            }
        });
    },

    useUpdateBoard: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: ({ id, data }: { id: number; data: Partial<Board> }) => updateBoard(id, data),
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['boards'] });
                toast.success('Board updated successfully');
            },
            onError: (error: any) => {
                toast.error(error.response?.data?.detail || 'Failed to update board');
            }
        });
    },

    useDeleteBoard: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: (id: number) => deleteBoard(id),
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['boards'] });
                toast.success('Board deleted successfully');
            },
            onError: (error: any) => {
                toast.error(error.response?.data?.detail || 'Failed to delete board');
            }
        });
    },

    // ----------------------------------------------------------------------
    // Lead Source Hooks
    // ----------------------------------------------------------------------
    
    useLeadSources: (isActive?: boolean) => {
        return useQuery({
            queryKey: ['lead-sources', { isActive }],
            queryFn: () => getLeadSources(isActive)
        });
    },

    useCreateLeadSource: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: (data: Partial<LeadSource>) => createLeadSource(data),
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['lead-sources'] });
                toast.success('Lead Source created successfully');
            },
            onError: (error: any) => {
                toast.error(error.response?.data?.detail || 'Failed to create lead source');
            }
        });
    },

    useUpdateLeadSource: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: ({ id, data }: { id: number; data: Partial<LeadSource> }) => updateLeadSource(id, data),
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['lead-sources'] });
                toast.success('Lead Source updated successfully');
            },
            onError: (error: any) => {
                toast.error(error.response?.data?.detail || 'Failed to update lead source');
            }
        });
    },

    useDeleteLeadSource: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: (id: number) => deleteLeadSource(id),
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['lead-sources'] });
                toast.success('Lead Source deleted successfully');
            },
            onError: (error: any) => {
                toast.error(error.response?.data?.detail || 'Failed to delete lead source');
            }
        });
    },

    // ----------------------------------------------------------------------
    // Reservation Category Hooks
    // ----------------------------------------------------------------------
    
    useReservationCategories: (isActive?: boolean) => {
        return useQuery({
            queryKey: ['reservation-categories', { isActive }],
            queryFn: () => getReservationCategories(isActive)
        });
    },

    useCreateReservationCategory: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: (data: Partial<ReservationCategory>) => createReservationCategory(data),
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['reservation-categories'] });
                toast.success('Category created successfully');
            },
            onError: (error: any) => {
                toast.error(error.response?.data?.detail || 'Failed to create category');
            }
        });
    },

    useUpdateReservationCategory: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: ({ id, data }: { id: number; data: Partial<ReservationCategory> }) => updateReservationCategory(id, data),
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['reservation-categories'] });
                toast.success('Category updated successfully');
            },
            onError: (error: any) => {
                toast.error(error.response?.data?.detail || 'Failed to update category');
            }
        });
    },

    useDeleteReservationCategory: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: (id: number) => deleteReservationCategory(id),
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['reservation-categories'] });
                toast.success('Category deleted successfully');
            },
            onError: (error: any) => {
                toast.error(error.response?.data?.detail || 'Failed to delete category');
            }
        });
    }
};
