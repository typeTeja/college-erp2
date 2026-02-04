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
    SelectionUpdate,
    PayoutBatchProcess,
    ODCPayout
} from '@/types/odc';

export const odcService = {
    // Hotels
    async getHotels(): Promise<ODCHotel[]> {
        const response = await api.get('/students/odc/hotels');
        return response.data;
    },

    async createHotel(data: ODCHotelCreate): Promise<ODCHotel> {
        const response = await api.post('/students/odc/hotels', data);
        return response.data;
    },

    // Requests
    async getRequests(): Promise<ODCRequest[]> {
        const response = await api.get('/students/odc/requests');
        return response.data;
    },

    async createRequest(data: ODCRequestCreate): Promise<ODCRequest> {
        const response = await api.post('/students/odc/requests', data);
        return response.data;
    },

    // Applications
    async getMyApplications(): Promise<ODCApplication[]> {
        const response = await api.get('/students/odc/my-applications');
        return response.data;
    },

    async getRequestApplications(requestId: number): Promise<ODCApplication[]> {
        const response = await api.get(`/students/odc/requests/${requestId}/applications`);
        return response.data;
    },

    async applyForODC(requestId: number): Promise<ODCApplication> {
        const response = await api.post(`/students/odc/requests/${requestId}/apply`);
        return response.data;
    },

    // Feedback
    async submitStudentFeedback(applicationId: number, data: StudentFeedbackSubmit): Promise<ODCApplication> {
        const response = await api.post(`/students/odc/applications/${applicationId}/student-feedback`, data);
        return response.data;
    },

    async submitHotelFeedback(applicationId: number, data: HotelFeedbackSubmit): Promise<ODCApplication> {
        const response = await api.post(`/students/odc/applications/${applicationId}/hotel-feedback`, data);
        return response.data;
    },

    async selectStudents(data: SelectionUpdate): Promise<ODCApplication[]> {
        const response = await api.post('/students/odc/applications/select', data);
        return response.data;
    },

    // Billing
    async getBilling(): Promise<ODCBilling[]> {
        const response = await api.get('/students/odc/billing');
        return response.data;
    },

    async createBilling(data: BillingCreate): Promise<ODCBilling> {
        const response = await api.post('/students/odc/billing', data);
        return response.data;
    },

    async markBillingPaid(billingId: number, data: BillingMarkPaid): Promise<ODCBilling> {
        const response = await api.put(`/students/odc/billing/${billingId}/mark-paid`, data);
        return response.data;
    },

    // Payouts
    async getPendingPayouts(): Promise<ODCApplication[]> {
        const response = await api.get('/students/odc/payouts/pending');
        return response.data;
    },

    async processPayouts(data: PayoutBatchProcess): Promise<ODCPayout[]> {
        const response = await api.post('/students/odc/payouts/process', data);
        return response.data;
    }
};
