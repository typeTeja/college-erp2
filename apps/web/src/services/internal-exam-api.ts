/**
 * Internal Exam API Service
 * 
 * Provides methods to interact with internal exam endpoints
 */
import { api } from '@/utils/api';


// ============================================================================
// Internal Exam APIs
// ============================================================================

export const internalExamApi = {
    /**
     * Create a new internal exam
     */
    create: async (data: any): Promise<any> => {
        const response = await api.post('/internal-exams', data);
        return response.data;
    },

    /**
     * Get all internal exams
     */
    list: async (filters?: {
        program_id?: number;
        year?: number;
        semester?: number;
        exam_type?: string;
        academic_year?: string;
    }): Promise<any[]> => {
        const response = await api.get('/internal-exams', { params: filters });
        return response.data;
    },

    /**
     * Get a specific exam
     */
    get: async (id: number): Promise<any> => {
        const response = await api.get(`/${id}`);
        return response.data;
    },

    /**
     * Update an exam
     */
    update: async (id: number, data: any): Promise<any> => {
        const response = await api.put(`/${id}`, data);
        return response.data;
    },

    /**
     * Delete an exam
     */
    delete: async (id: number): Promise<void> => {
        await api.delete(`/${id}`);
    },

    /**
     * Enter marks for an exam
     */
    enterMarks: async (examId: number, marks: any[]): Promise<any> => {
        const response = await api.post(`/${examId}/marks`, { marks });
        return response.data;
    },

    /**
     * Calculate grades for an exam
     */
    calculateGrades: async (examId: number): Promise<any> => {
        const response = await api.post(`/${examId}/calculate-grades`);
        return response.data;
    },

    /**
     * Publish results
     */
    publishResults: async (examId: number): Promise<any> => {
        const response = await api.post(`/${examId}/publish`);
        return response.data;
    },

    /**
     * Get exam marks
     */
    getMarks: async (examId: number, filters?: { section_id?: number }): Promise<any[]> => {
        const response = await api.get(`/${examId}/marks`, { params: filters });
        return response.data;
    },

    /**
     * Get student result
     */
    getStudentResult: async (examId: number, studentId: number): Promise<any> => {
        const response = await api.get(`/${examId}/students/${studentId}/result`);
        return response.data;
    },
};

export default internalExamApi;
