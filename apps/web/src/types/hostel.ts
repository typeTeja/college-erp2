export enum HostelType {
    BOYS = "BOYS",
    GIRLS = "GIRLS",
    STAFF = "STAFF",
    GUEST = "GUEST"
}

export enum RoomType {
    AC = "AC",
    NON_AC = "NON_AC",
    SUITE = "SUITE"
}

export enum GatePassType {
    LOCAL = "LOCAL",
    HOME = "HOME",
    EMERGENCY = "EMERGENCY"
}

export enum GatePassStatus {
    PENDING = "PENDING",
    APPROVED = "APPROVED",
    REJECTED = "REJECTED",
    OUT = "OUT",
    RETURNED = "RETURNED",
    EXPIRED = "EXPIRED"
}

export enum ComplaintStatus {
    OPEN = "OPEN",
    IN_PROGRESS = "IN_PROGRESS",
    RESOLVED = "RESOLVED",
    CLOSED = "CLOSED"
}

export interface HostelBlock {
    id: number;
    name: string;
    type: HostelType;
    total_floors: number;
    warden_name?: string;
    contact_number?: string;
}

export interface HostelRoom {
    id: number;
    block_id: number;
    room_number: string;
    floor: number;
    capacity: number;
    current_occupancy: number;
    room_type: RoomType;
    monthly_rent: number;
    is_active: boolean;
}

export interface BedAllocation {
    id: number;
    room_id: number;
    bed_number: string;
    student_id?: number;
    faculty_id?: number;
    allocation_date: string;
    deallocation_date?: string;
    is_active: boolean;
}

export interface GatePass {
    id: number;
    student_id: number;
    type: GatePassType;
    out_time: string;
    expected_in_time: string;
    actual_in_time?: string;
    reason: string;
    status: GatePassStatus;
    approved_by?: number;
    remarks?: string;
}

export interface HostelComplaint {
    id: number;
    student_id: number;
    room_id: number;
    category: string;
    description: string;
    priority: string;
    status: ComplaintStatus;
    resolution_note?: string;
    resolved_at?: string;
    created_at: string;
}
