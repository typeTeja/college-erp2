/**
 * University Exam API Service
 * 
 * Provides methods to interact with university exam endpoints
 */
import { api } from '@/utils/api';


export const universityExamApi = {
    /**
     * Register student for university exam
     */
    register: async (data: any): Promise<any> => {
        const response = await api.post(`/registrations`, data);
        return response.data;
    },

    /**
     * Get all registrations
     */
    listRegistrations: async (filters?: {
        student_id?: number;
        exam_id?: number;
        semester?: number;
    }): Promise<any[]> => {
        const response = await api.get(`/registrations`, { params: filters });
        return response.data;
    },

    /**
     * Get all university exams
     */
    list: async (filters?: { academic_year?: string; semester?: number }): Promise<any[]> => {
        const response = await api.get('/university-exams', { params: filters });
        return response.data;
    },

    /**
     * Enter exam results
     */
    enterResults: async (examId: number, results: any[]): Promise<any> => {
        const response = await api.post(`/${examId}/results`, { results });
        return response.data;
    },

    /**
     * Get student results
     */
    getStudentResults: async (studentId: number, semester?: number): Promise<any[]> => {
        const response = await api.get(`/students/${studentId}/results`, {
            params: { semester }
        });
        return response.data;
    },

    /**
     * Generate transcript
     */
    generateTranscript: async (studentId: number): Promise<any> => {
        const response = await api.post(`/students/${studentId}/transcript`);
        return response.data;
    },

    /**
     * Download transcript
     */
    downloadTranscript: async (studentId: number): Promise<Blob> => {
        const response = await api.get(`/students/${studentId}/transcript/download`, {
            responseType: 'blob'
        });
        return response.data;
    },
};

export default universityExamApi;
