import { api } from "@/utils/api";
import { AttendanceSession, AttendanceRecord, AttendanceStats, CreateSessionDTO, BulkMarkAttendanceDTO } from "@/types/attendance";

export const attendanceService = {
    createSession: async (data: CreateSessionDTO): Promise<AttendanceSession> => {
        const response = await api.post("/attendance/sessions", data);
        return response.data;
    },

    getSessions: async (params?: { faculty_id?: number }): Promise<AttendanceSession[]> => {
        const response = await api.get("/attendance/sessions", { params });
        return response.data;
    },

    getSessionById: async (id: number): Promise<AttendanceSession> => {
        const response = await api.get(`/attendance/sessions/${id}`);
        return response.data;
    },

    markBulkAttendance: async (data: BulkMarkAttendanceDTO): Promise<AttendanceRecord[]> => {
        const response = await api.post("/attendance/mark", data);
        return response.data;
    },

    getStudentStats: async (studentId: number): Promise<AttendanceStats> => {
        const response = await api.get(`/attendance/student/${studentId}/stats`);
        return response.data;
    },

    getStudentHistory: async (studentId: number): Promise<AttendanceRecord[]> => {
        const response = await api.get(`/attendance/student/${studentId}/history`);
        return response.data;
    },
};
