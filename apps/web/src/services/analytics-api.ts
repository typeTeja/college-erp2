/**
 * Analytics & Reporting API Service
 * 
 * Provides methods to interact with analytics endpoints
 */
import { api } from '@/utils/api';


export const analyticsApi = {
    /**
     * Get dashboard summary
     */
    getDashboardSummary: async (): Promise<any> => {
        const response = await api.get(`/dashboard`);
        return response.data;
    },

    /**
     * Get enrollment trends
     */
    getEnrollmentTrends: async (filters?: {
        from_year?: string;
        to_year?: string;
    }): Promise<any> => {
        const response = await api.get(`/trends/enrollment`, { params: filters });
        return response.data;
    },

    /**
     * Get fee analytics
     */
    getFeeAnalytics: async (filters?: {
        academic_year?: string;
    }): Promise<any> => {
        const response = await api.get(`/finance/fees`, { params: filters });
        return response.data;
    },

    /**
     * Get exam performance
     */
    getExamPerformance: async (filters?: {
        program_id?: number;
        semester?: number;
    }): Promise<any> => {
        const response = await api.get(`/academics/performance`, { params: filters });
        return response.data;
    },

    /**
     * Generate custom report
     */
    generateCustomReport: async (data: {
        report_type: string;
        filters: any;
    }): Promise<any> => {
        const response = await api.post(`/reports/custom`, data);
        return response.data;
    },

    /**
     * Export data
     */
    exportData: async (type: string, filters?: any): Promise<Blob> => {
        const response = await api.post(`/export/${type}`, filters, {
            responseType: 'blob'
        });
        return response.data;
    },
};

export default analyticsApi;
