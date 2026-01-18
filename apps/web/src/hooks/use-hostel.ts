/**
 * Hostel Management Hooks
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import hostelApi from '@/services/hostel-api';
import { queryKeys } from '@/config/react-query';

export function useHostels() {
    return useQuery({
        queryKey: queryKeys.hostel.hostels,
        queryFn: () => hostelApi.listHostels(),
    });
}

export function useRooms(filters?: {
    hostel_id?: number;
    available?: boolean;
    room_type?: string;
}) {
    return useQuery({
        queryKey: queryKeys.hostel.rooms(filters),
        queryFn: () => hostelApi.listRooms(filters),
    });
}

export function useAllocateRoom() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: {
            student_id: number;
            room_id: number;
            from_date: string;
            to_date?: string;
        }) => hostelApi.allocateRoom(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.hostel.rooms() });
        },
    });
}

export function useVacateRoom() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ allocationId, vacateDate }: { allocationId: number; vacateDate: string }) =>
            hostelApi.vacateRoom(allocationId, vacateDate),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: queryKeys.hostel.rooms() });
        },
    });
}

export function useHostelStatistics(hostelId?: number) {
    return useQuery({
        queryKey: [...queryKeys.hostel.all, 'statistics', hostelId],
        queryFn: () => hostelApi.getStatistics(hostelId),
    });
}
