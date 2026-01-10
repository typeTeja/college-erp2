/**
 * Batch Cloning API Service
 */
import { api } from './api';
import type { BatchCloneRequest, BatchCloneResponse } from '@/types/batch-cloning';

export const batchCloningService = {
    /**
     * Clone an existing batch structure
     */
    cloneBatch: async (batchId: number, data: BatchCloneRequest): Promise<BatchCloneResponse> => {
        const response = await api.post<BatchCloneResponse>(
            `/batches/${batchId}/clone`,
            data
        );
        return response.data;
    }
};
