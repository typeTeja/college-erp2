import { api } from '@/utils/api';
import {
    ODCApplication,
    ODCHotel,
    ODCHotelCreate,
    ODCRequest,
    ODCRequestCreate,
    StudentFeedbackSubmit,
    HotelFeedbackSubmit,
    ODCBilling,
    BillingCreate,
    BillingMarkPaid,
    PayoutBatchProcess,
    ODCPayout
} from '@/types/odc';

export const odcService = {
    // Hotels
    async getHotels(): Promise<ODCHotel[]> {
        const response = await api.get('/odc/hotels');
        return response.data;
    },

    async createHotel(data: ODCHotelCreate): Promise<ODCHotel> {
        const response = await api.post('/odc/hotels', data);
        return response.data;
    },

    // Requests
    async getRequests(): Promise<ODCRequest[]> {
        const response = await api.get('/odc/requests');
        return response.data;
    },

    async createRequest(data: ODCRequestCreate): Promise<ODCRequest> {
        const response = await api.post('/odc/requests', data);
        return response.data;
    },

    // Applications
    async getMyApplications(): Promise<ODCApplication[]> {
        const response = await api.get('/odc/my-applications');
        return response.data;
    },

    async applyForODC(requestId: number): Promise<ODCApplication> {
        const response = await api.post(`/odc/requests/${requestId}/apply`);
        return response.data;
    },

    // Feedback
    async submitStudentFeedback(applicationId: number, data: StudentFeedbackSubmit): Promise<ODCApplication> {
        const response = await api.post(`/odc/applications/${applicationId}/student-feedback`, data);
        return response.data;
    },

    async submitHotelFeedback(applicationId: number, data: HotelFeedbackSubmit): Promise<ODCApplication> {
        const response = await api.post(`/odc/applications/${applicationId}/hotel-feedback`, data);
        return response.data;
    },

    // Billing
    async getBilling(): Promise<ODCBilling[]> {
        const response = await api.get('/odc/billing');
        return response.data;
    },

    async createBilling(data: BillingCreate): Promise<ODCBilling> {
        const response = await api.post('/odc/billing', data);
        return response.data;
    },

    async markBillingPaid(billingId: number, data: BillingMarkPaid): Promise<ODCBilling> {
        const response = await api.put(`/odc/billing/${billingId}/mark-paid`, data);
        return response.data;
    },

    // Payouts
    async getPendingPayouts(): Promise<ODCApplication[]> {
        const response = await api.get('/odc/payouts/pending');
        return response.data;
    },

    async processPayouts(data: PayoutBatchProcess): Promise<ODCPayout[]> {
        const response = await api.post('/odc/payouts/process', data);
        return response.data;
    }
};
