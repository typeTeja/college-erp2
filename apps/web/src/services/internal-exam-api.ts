/**
 * Internal Exam API Service
 * 
 * Provides methods to interact with internal exam endpoints
 */
import axios from 'axios';

const BASE_URL = '/api/v1/internal-exams';

// ============================================================================
// Internal Exam APIs
// ============================================================================

export const internalExamApi = {
    /**
     * Create a new internal exam
     */
    create: async (data: any): Promise<any> => {
        const response = await axios.post(BASE_URL, data);
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
        const response = await axios.get(BASE_URL, { params: filters });
        return response.data;
    },

    /**
     * Get a specific exam
     */
    get: async (id: number): Promise<any> => {
        const response = await axios.get(`${BASE_URL}/${id}`);
        return response.data;
    },

    /**
     * Update an exam
     */
    update: async (id: number, data: any): Promise<any> => {
        const response = await axios.put(`${BASE_URL}/${id}`, data);
        return response.data;
    },

    /**
     * Delete an exam
     */
    delete: async (id: number): Promise<void> => {
        await axios.delete(`${BASE_URL}/${id}`);
    },

    /**
     * Enter marks for an exam
     */
    enterMarks: async (examId: number, marks: any[]): Promise<any> => {
        const response = await axios.post(`${BASE_URL}/${examId}/marks`, { marks });
        return response.data;
    },

    /**
     * Calculate grades for an exam
     */
    calculateGrades: async (examId: number): Promise<any> => {
        const response = await axios.post(`${BASE_URL}/${examId}/calculate-grades`);
        return response.data;
    },

    /**
     * Publish results
     */
    publishResults: async (examId: number): Promise<any> => {
        const response = await axios.post(`${BASE_URL}/${examId}/publish`);
        return response.data;
    },

    /**
     * Get exam marks
     */
    getMarks: async (examId: number, filters?: { section_id?: number }): Promise<any[]> => {
        const response = await axios.get(`${BASE_URL}/${examId}/marks`, { params: filters });
        return response.data;
    },

    /**
     * Get student result
     */
    getStudentResult: async (examId: number, studentId: number): Promise<any> => {
        const response = await axios.get(`${BASE_URL}/${examId}/students/${studentId}/result`);
        return response.data;
    },
};

export default internalExamApi;
