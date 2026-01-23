/**
 * Timetable Management Hooks
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '@/utils/api';

// Placeholder - will need actual API service
const timetableApi = {
    getSlots: async () => {
        const response = await api.get('/timetable/slots');
        return response.data;
    },
    getSchedule: async (academicYearId: number, semesterId: number, sectionId?: number) => {
        const params = {
            academic_year_id: academicYearId,
            semester_id: semesterId,
            ...(sectionId && { section_id: sectionId })
        };
        const response = await api.get('/timetable', { params });
        return response.data;
    },
    createEntry: async (data: any) => {
        const response = await api.post('/timetable/entries', data);
        return response.data;
    }
};

export function useTimeSlots() {
    return useQuery({
        queryKey: ['timetable', 'slots'],
        queryFn: timetableApi.getSlots
    });
}

export function useTimetableSchedule(academicYearId: number, semesterId: number | null, sectionId?: number) {
    return useQuery({
        queryKey: ['timetable', academicYearId, semesterId, sectionId],
        queryFn: () => timetableApi.getSchedule(academicYearId, semesterId!, sectionId),
        enabled: !!semesterId
    });
}

export function useCreateTimetableEntry() {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: (data: any) => timetableApi.createEntry(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['timetable'] });
        },
    });
}
