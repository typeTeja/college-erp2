import { api } from "./api";
import {
    TimeSlot, CreateTimeSlotDTO,
    ClassSchedule, CreateScheduleDTO,
    ClassAdjustment, CreateAdjustmentDTO, AdjustmentStatus
} from "@/types/timetable";

export const timetableService = {
    // --- Master Data ---
    getSlots: async () => {
        const response = await api.get<TimeSlot[]>("/timetable/slots");
        return response.data;
    },

    createSlot: async (data: CreateTimeSlotDTO) => {
        const response = await api.post<TimeSlot>("/timetable/slots", data);
        return response.data;
    },

    // --- Schedule Management ---
    getSchedule: async (academicYearId: number, batchSemesterId: number, sectionId?: number) => {
        const params = { academic_year_id: academicYearId, batch_semester_id: batchSemesterId, section_id: sectionId };
        const response = await api.get<ClassSchedule[]>("/timetable/entries", { params });
        return response.data;
    },

    getFacultySchedule: async (facultyId: number) => {
        const response = await api.get<ClassSchedule[]>(`/timetable/faculty/${facultyId}`);
        return response.data;
    },

    createScheduleEntry: async (data: CreateScheduleDTO) => {
        const response = await api.post<ClassSchedule>("/timetable/entries", data);
        return response.data;
    },

    validateEntry: async (data: CreateScheduleDTO) => {
        const response = await api.post<{ status: string }>("/timetable/validate", data);
        return response.data;
    },

    // --- Adjustments ---
    requestAdjustment: async (data: CreateAdjustmentDTO) => {
        const response = await api.post<ClassAdjustment>("/timetable/adjustments", data);
        return response.data;
    },

    getPendingAdjustments: async () => {
        const response = await api.get<ClassAdjustment[]>("/timetable/adjustments/pending");
        return response.data;
    },

    updateAdjustment: async (id: number, status: AdjustmentStatus, substituteFacultyId?: number) => {
        const response = await api.put<ClassAdjustment>(`/timetable/adjustments/${id}`, {
            status,
            substitute_faculty_id: substituteFacultyId
        });
        return response.data;
    }
};
