import { api } from './api';

export interface ScholarshipSlab {
    id: number;
    name: string;
    code: string;
    description?: string;
    min_percentage: number;
    max_percentage: number;
    discount_type: 'PERCENTAGE' | 'FIXED';
    discount_value: number;
    max_discount_amount?: number;
    applicable_fee_heads: number[]; // Array of fee_head IDs
    academic_year_id?: number;
    program_id?: number;
    is_active: boolean;
}

export interface ScholarshipSlabCreate {
    name: string;
    code: string;
    description?: string;
    min_percentage: number;
    max_percentage: number;
    discount_type: 'PERCENTAGE' | 'FIXED';
    discount_value: number;
    max_discount_amount?: number;
    applicable_fee_heads?: number[];
    academic_year_id?: number;
    program_id?: number;
}

/**
 * Fetch all scholarship slabs
 */
export async function getScholarshipSlabs(isActive?: boolean): Promise<ScholarshipSlab[]> {
    const params = isActive !== undefined ? { is_active: isActive } : {};
    const response = await api.get<ScholarshipSlab[]>('/master/scholarship-slabs', { params });
    return response.data;
}

/**
 * Create a new scholarship slab
 */
export async function createScholarshipSlab(data: ScholarshipSlabCreate): Promise<ScholarshipSlab> {
    const response = await api.post<ScholarshipSlab>('/master/scholarship-slabs', data);
    return response.data;
}

/**
 * Update an existing scholarship slab
 */
export async function updateScholarshipSlab(id: number, data: Partial<ScholarshipSlabCreate>): Promise<ScholarshipSlab> {
    const response = await api.patch<ScholarshipSlab>(`/master/scholarship-slabs/${id}`, data);
    return response.data;
}

/**
 * Delete a scholarship slab
 */
export async function deleteScholarshipSlab(id: number): Promise<void> {
    await api.delete(`/master/scholarship-slabs/${id}`);
}
