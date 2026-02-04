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
        const response = await api.post('/academic/exams/internal', data);
        return response.data;
    },

    /**
     * Get details of a specific internal exam
     */
    get: async (id: number): Promise<any> => {
        const response = await api.get(`/academic/exams/internal/${id}`);
        return response.data;
    },

    /**
     * Record marks for a student
     */
    markStudentMarks: async (data: {
        student_id: number;
        internal_exam_subject_id: number;
        marks_obtained: number;
        is_absent?: boolean;
        remarks?: string;
    }): Promise<any> => {
        const response = await api.post('/academic/exams/internal/marks', data);
        return response.data;
    },

    /**
     * Get all internal exams (Placeholder for list endpoint)
     */
    list: async (filters?: any): Promise<any[]> => {
        // Note: Generic list endpoint needs implementation in backend if required
        const response = await api.get('/academic/batches');
        return response.data;
    },
};

export default internalExamApi;
