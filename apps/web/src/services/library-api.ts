/**
 * Library Management API Service
 * 
 * Provides methods to interact with library endpoints
 */
import { api } from '@/utils/api';


export const libraryApi = {
    /**
     * Get all books
     */
    listBooks: async (filters?: {
        search?: string;
        category?: string;
        available?: boolean;
    }): Promise<any[]> => {
        const response = await api.get(`/books`, { params: filters });
        return response.data;
    },

    /**
     * Issue a book
     */
    issueBook: async (data: {
        book_id: number;
        member_id: number;
        due_date: string;
    }): Promise<any> => {
        const response = await api.post(`/issues`, data);
        return response.data;
    },

    /**
     * Return a book
     */
    returnBook: async (issueId: number): Promise<any> => {
        const response = await api.post(`/issues/${issueId}/return`);
        return response.data;
    },

    /**
     * Renew a book
     */
    renewBook: async (issueId: number, newDueDate: string): Promise<any> => {
        const response = await api.post(`/issues/${issueId}/renew`, {
            new_due_date: newDueDate
        });
        return response.data;
    },

    /**
     * Calculate fine
     */
    calculateFine: async (issueId: number): Promise<any> => {
        const response = await api.get(`/issues/${issueId}/fine`);
        return response.data;
    },

    /**
     * Get library members
     */
    listMembers: async (): Promise<any[]> => {
        const response = await api.get(`/members`);
        return response.data;
    },

    /**
     * Get member's issued books
     */
    getMemberBooks: async (memberId: number): Promise<any[]> => {
        const response = await api.get(`/members/${memberId}/books`);
        return response.data;
    },
};

export default libraryApi;
