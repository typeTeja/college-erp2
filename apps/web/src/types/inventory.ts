export enum AssetCategory {
    UNIFORM = "UNIFORM",
    IT_EQUIPMENT = "IT_EQUIPMENT",
    LAB_EQUIPMENT = "LAB_EQUIPMENT",
    FURNITURE = "FURNITURE",
    STATIONERY = "STATIONERY",
    OTHERS = "OTHERS"
}

export enum AllocationStatus {
    ISSUED = "ISSUED",
    RETURNED = "RETURNED",
    DAMAGED = "DAMAGED",
    LOST = "LOST"
}

export enum UniformSize {
    XS = "XS",
    S = "S",
    M = "M",
    L = "L",
    XL = "XL",
    XXL = "XXL",
    CUSTOM = "CUSTOM"
}

export interface Asset {
    id: number;
    name: string;
    category: AssetCategory;
    description: string | null;
    qr_code: string | null;
    unit: string;
    total_stock: number;
    available_stock: number;
    reorder_level: number;
    unit_price: number;
    created_at: string;
    updated_at: string;
}

export interface AssetAllocation {
    id: number;
    asset_id: number;
    student_id: number | null;
    faculty_id: number | null;
    department_name: string | null;
    quantity: number;
    allocated_at: string;
    due_date: string | null;
    returned_at: string | null;
    status: AllocationStatus;
    remarks: string | null;
}

export interface AssetMaintenance {
    id: number;
    asset_id: number;
    maintenance_date: string;
    description: string;
    cost: number;
    performed_by: string | null;
    next_due_date: string | null;
}

export interface AssetAudit {
    id: number;
    asset_id: number;
    audit_date: string;
    expected_stock: number;
    actual_stock: number;
    variance: number;
    audited_by: string;
    remarks: string | null;
}

export interface UniformAllocation {
    id: number;
    student_id: number;
    item_name: string;
    size: UniformSize;
    quantity: number;
    is_paid: boolean;
    issued_at: string | null;
    status: string;
}

export interface AssetCreateDTO {
    name: string;
    category: AssetCategory;
    description?: string;
    qr_code?: string;
    unit?: string;
    total_stock?: number;
    available_stock?: number;
    reorder_level?: number;
    unit_price?: number;
}

export interface AllocationCreateDTO {
    asset_id: number;
    student_id?: number;
    faculty_id?: number;
    department_name?: string;
    quantity?: number;
    due_date?: string;
    remarks?: string;
}

export interface AuditCreateDTO {
    asset_id: number;
    actual_stock: number;
    audited_by: string;
    remarks?: string;
}
