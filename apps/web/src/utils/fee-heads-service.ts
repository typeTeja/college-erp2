import { api } from './api';

export interface FeeHead {
    id: number;
    name: string;
    code: string;
    description?: string;
    is_refundable: boolean;
    is_recurring: boolean;
    is_mandatory: boolean;
    display_order: number;
    is_active: boolean;
}

export interface FeeHeadCreate {
    name: string;
    code: string;
    description?: string;
    is_refundable?: boolean;
    is_recurring?: boolean;
    is_mandatory?: boolean;
    display_order?: number;
}

/**
 * Fetch all fee heads
 */
export async function getFeeHeads(isActive?: boolean): Promise<FeeHead[]> {
    const params = isActive !== undefined ? { is_active: isActive } : {};
    const response = await api.get<FeeHead[]>('/master/fee-heads', { params });
    return response.data;
}

/**
 * Create a new fee head
 */
export async function createFeeHead(data: FeeHeadCreate): Promise<FeeHead> {
    const response = await api.post<FeeHead>('/master/fee-heads', data);
    return response.data;
}

/**
 * Update an existing fee head
 */
export async function updateFeeHead(id: number, data: Partial<FeeHeadCreate>): Promise<FeeHead> {
    const response = await api.patch<FeeHead>(`/master/fee-heads/${id}`, data);
    return response.data;
}

/**
 * Delete a fee head
 */
export async function deleteFeeHead(id: number): Promise<void> {
    await api.delete(`/master/fee-heads/${id}`);
}
