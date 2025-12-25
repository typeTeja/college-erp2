import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/lib/api';
import {
    HostelBlock, HostelRoom, BedAllocation,
    GatePass, HostelComplaint
} from '@/types/hostel';

export const hostelService = {
    // Blocks
    useBlocks: () => {
        return useQuery({
            queryKey: ['hostel-blocks'],
            queryFn: async () => {
                const { data } = await api.get<HostelBlock[]>('/hostel/blocks');
                return data;
            }
        });
    },

    useCreateBlock: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (block: Partial<HostelBlock>) => {
                const { data } = await api.post<HostelBlock>('/hostel/blocks', block);
                return data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['hostel-blocks'] });
            }
        });
    },

    // Rooms
    useRooms: (blockId?: number) => {
        return useQuery({
            queryKey: ['hostel-rooms', blockId],
            queryFn: async () => {
                const url = blockId ? `/hostel/rooms?block_id=${blockId}` : '/hostel/rooms';
                const { data } = await api.get<HostelRoom[]>(url);
                return data;
            }
        });
    },

    useCreateRoom: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (room: Partial<HostelRoom>) => {
                const { data } = await api.post<HostelRoom>('/hostel/rooms', room);
                return data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['hostel-rooms'] });
            }
        });
    },

    // Allocations
    useAllocateBed: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (allocation: Partial<BedAllocation>) => {
                const { data } = await api.post<BedAllocation>('/hostel/allocate', allocation);
                return data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['hostel-rooms'] });
                queryClient.invalidateQueries({ queryKey: ['hostel-allocations'] });
            }
        });
    },

    // Complaints
    useComplaints: () => {
        return useQuery({
            queryKey: ['hostel-complaints'],
            queryFn: async () => {
                const { data } = await api.get<HostelComplaint[]>('/hostel/complaints');
                return data;
            }
        });
    },

    useCreateComplaint: () => {
        const queryClient = useQueryClient();
        return useMutation({
            mutationFn: async (complaint: Partial<HostelComplaint>) => {
                const { data } = await api.post<HostelComplaint>('/hostel/complaints', complaint);
                return data;
            },
            onSuccess: () => {
                queryClient.invalidateQueries({ queryKey: ['hostel-complaints'] });
            }
        });
    }
};
