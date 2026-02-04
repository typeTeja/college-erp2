/**
 * Attendance API Service
 * 
 * Provides methods to interact with attendance endpoints
 */
import { api } from '@/utils/api';

export const attendanceApi = {
    /**
     * Create a new attendance session
     */
    createSession: async (data: {
        subject_id: number;
        faculty_id: number;
        program_id: number;
        program_year_id: number;
        semester: number;
        section?: string;
        session_date: string;
        start_time: string;
        end_time: string;
    }): Promise<any> => {
        const response = await api.post('/academic/attendance/sessions', data);
        return response.data;
    },

    /**
     * Mark bulk attendance for a session
     */
    markAttendance: async (data: {
        session_id: number;
        attendance_data: {
            student_id: number;
            status: 'PRESENT' | 'ABSENT' | 'LATE' | 'ON_DUTY';
            remarks?: string;
        }[];
    }): Promise<any> => {
        const response = await api.post('/academic/attendance/mark', data);
        return response.data;
    },

    /**
     * Get all attendance records for a specific session
     */
    getSessionRecords: async (sessionId: number): Promise<any[]> => {
        const response = await api.get(`/academic/attendance/sessions/${sessionId}/records`);
        return response.data;
    },

    /**
     * Get attendance summary for a student
     */
    getStudentSummary: async (studentId: number, subjectId?: number): Promise<any> => {
        const response = await api.get(`/academic/attendance/student/${studentId}/summary`, {
            params: { subject_id: subjectId }
        });
        return response.data;
    },
};

export default attendanceApi;
