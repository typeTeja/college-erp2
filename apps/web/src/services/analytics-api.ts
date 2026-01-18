/**
 * Analytics & Reporting API Service
 * 
 * Provides methods to interact with analytics endpoints
 */
import axios from 'axios';

const BASE_URL = '/api/v1/analytics';

export const analyticsApi = {
    /**
     * Get dashboard summary
     */
    getDashboardSummary: async (): Promise<any> => {
        const response = await axios.get(`${BASE_URL}/dashboard`);
        return response.data;
    },

    /**
     * Get enrollment trends
     */
    getEnrollmentTrends: async (filters?: {
        from_year?: string;
        to_year?: string;
    }): Promise<any> => {
        const response = await axios.get(`${BASE_URL}/trends/enrollment`, { params: filters });
        return response.data;
    },

    /**
     * Get fee analytics
     */
    getFeeAnalytics: async (filters?: {
        academic_year?: string;
    }): Promise<any> => {
        const response = await axios.get(`${BASE_URL}/finance/fees`, { params: filters });
        return response.data;
    },

    /**
     * Get exam performance
     */
    getExamPerformance: async (filters?: {
        program_id?: number;
        semester?: number;
    }): Promise<any> => {
        const response = await axios.get(`${BASE_URL}/academics/performance`, { params: filters });
        return response.data;
    },

    /**
     * Generate custom report
     */
    generateCustomReport: async (data: {
        report_type: string;
        filters: any;
    }): Promise<any> => {
        const response = await axios.post(`${BASE_URL}/reports/custom`, data);
        return response.data;
    },

    /**
     * Export data
     */
    exportData: async (type: string, filters?: any): Promise<Blob> => {
        const response = await axios.post(`${BASE_URL}/export/${type}`, filters, {
            responseType: 'blob'
        });
        return response.data;
    },
};

export default analyticsApi;
