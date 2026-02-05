import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { 
    getFeeHeads, createFeeHead, updateFeeHead, deleteFeeHead,
    FeeHead
} from './master-data-service';
import { toast } from 'sonner';

export const financeService = {
    // ----------------------------------------------------------------------
    // Fee Head Hooks
    // ----------------------------------------------------------------------
    
    useFeeHeads: (isActive?: boolean) => {
        return useQuery({
            queryKey: ['fee-heads', { isActive }],
            queryFn: () => getFeeHeads(isActive)
        });
    },

    useCreateFeeHead: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: (data: Partial<FeeHead>) => createFeeHead(data),
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['fee-heads'] });
                toast.success('Fee Head created successfully');
            },
            onError: (error: any) => {
                toast.error(error.response?.data?.detail || 'Failed to create fee head');
            }
        });
    },

    useUpdateFeeHead: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: ({ id, data }: { id: number; data: Partial<FeeHead> }) => updateFeeHead(id, data),
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['fee-heads'] });
                toast.success('Fee Head updated successfully');
            },
            onError: (error: any) => {
                toast.error(error.response?.data?.detail || 'Failed to update fee head');
            }
        });
    },

    useDeleteFeeHead: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: (id: number) => deleteFeeHead(id),
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['fee-heads'] });
                toast.success('Fee Head deleted successfully');
            },
            onError: (error: any) => {
                toast.error(error.response?.data?.detail || 'Failed to delete fee head');
            }
        });
    }
};
