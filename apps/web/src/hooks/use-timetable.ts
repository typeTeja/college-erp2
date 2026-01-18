/**
 * Timetable Management Hooks
 */
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

// Placeholder - will need actual API service
const timetableApi = {
    getSlots: async () => {
        const response = await fetch('/api/v1/timetable/slots');
        // Mock response for now if not exists
        return response.ok ? response.json() : [];
    },
    getSchedule: async (academicYearId: number, semesterId: number, sectionId?: number) => {
        const params = new URLSearchParams({
            academic_year_id: academicYearId.toString(),
            semester_id: semesterId.toString()
        });
        if (sectionId) params.append('section_id', sectionId.toString());

        const response = await fetch(`/api/v1/timetable?${params.toString()}`);
        return response.ok ? response.json() : [];
    },
    createEntry: async (data: any) => {
        const response = await fetch('/api/v1/timetable/entries', {
            method: 'POST',
            body: JSON.stringify(data),
            headers: { 'Content-Type': 'application/json' }
        });
        if (!response.ok) throw new Error('Failed to create timetable entry');
        return response.json();
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
