/**
 * Library Management API Service
 * 
 * Provides methods to interact with library endpoints
 */
import axios from 'axios';

const BASE_URL = '/api/v1/library';

export const libraryApi = {
    /**
     * Get all books
     */
    listBooks: async (filters?: {
        search?: string;
        category?: string;
        available?: boolean;
    }): Promise<any[]> => {
        const response = await axios.get(`${BASE_URL}/books`, { params: filters });
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
        const response = await axios.post(`${BASE_URL}/issues`, data);
        return response.data;
    },

    /**
     * Return a book
     */
    returnBook: async (issueId: number): Promise<any> => {
        const response = await axios.post(`${BASE_URL}/issues/${issueId}/return`);
        return response.data;
    },

    /**
     * Renew a book
     */
    renewBook: async (issueId: number, newDueDate: string): Promise<any> => {
        const response = await axios.post(`${BASE_URL}/issues/${issueId}/renew`, {
            new_due_date: newDueDate
        });
        return response.data;
    },

    /**
     * Calculate fine
     */
    calculateFine: async (issueId: number): Promise<any> => {
        const response = await axios.get(`${BASE_URL}/issues/${issueId}/fine`);
        return response.data;
    },

    /**
     * Get library members
     */
    listMembers: async (): Promise<any[]> => {
        const response = await axios.get(`${BASE_URL}/members`);
        return response.data;
    },

    /**
     * Get member's issued books
     */
    getMemberBooks: async (memberId: number): Promise<any[]> => {
        const response = await axios.get(`${BASE_URL}/members/${memberId}/books`);
        return response.data;
    },
};

export default libraryApi;
