import { api } from './api';
import { BulkBatchSetupRequest, BulkBatchSetupResponse } from '@/types/bulk-setup';

export const bulkSetupService = {
    /**
     * Create entire academic structure in one operation
     */
    createBulkBatch: async (data: BulkBatchSetupRequest): Promise<BulkBatchSetupResponse> => {
        const response = await api.post<BulkBatchSetupResponse>('/batches/bulk-setup', data);
        return response.data;
    },
};
