/**
 * University Exam API Service
 * 
 * Provides methods to interact with university exam endpoints
 */
import axios from 'axios';

const BASE_URL = '/api/v1/university-exams';

export const universityExamApi = {
    /**
     * Register student for university exam
     */
    register: async (data: any): Promise<any> => {
        const response = await axios.post(`${BASE_URL}/registrations`, data);
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
        const response = await axios.get(`${BASE_URL}/registrations`, { params: filters });
        return response.data;
    },

    /**
     * Get all university exams
     */
    list: async (filters?: { academic_year?: string; semester?: number }): Promise<any[]> => {
        const response = await axios.get(BASE_URL, { params: filters });
        return response.data;
    },

    /**
     * Enter exam results
     */
    enterResults: async (examId: number, results: any[]): Promise<any> => {
        const response = await axios.post(`${BASE_URL}/${examId}/results`, { results });
        return response.data;
    },

    /**
     * Get student results
     */
    getStudentResults: async (studentId: number, semester?: number): Promise<any[]> => {
        const response = await axios.get(`${BASE_URL}/students/${studentId}/results`, {
            params: { semester }
        });
        return response.data;
    },

    /**
     * Generate transcript
     */
    generateTranscript: async (studentId: number): Promise<any> => {
        const response = await axios.post(`${BASE_URL}/students/${studentId}/transcript`);
        return response.data;
    },

    /**
     * Download transcript
     */
    downloadTranscript: async (studentId: number): Promise<Blob> => {
        const response = await axios.get(`${BASE_URL}/students/${studentId}/transcript/download`, {
            responseType: 'blob'
        });
        return response.data;
    },
};

export default universityExamApi;
