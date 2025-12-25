export interface Staff {
    id: number;
    user_id?: number;
    name: string;
    email: string;
    mobile: string;
    department?: string;
    designation: string;
    join_date: string; // ISO Date
    shift_id?: number;
    is_active: boolean;
}

export interface StaffCreateDTO {
    name: string;
    email: string;
    mobile: string;
    department?: string;
    designation: string;
    join_date: string;
    shift_id?: number;
}

export interface StaffUpdateDTO {
    name?: string;
    email?: string;
    mobile?: string;
    department?: string;
    designation?: string;
    shift_id?: number;
    is_active?: boolean;
}

export interface Shift {
    id: number;
    name: string;
    start_time: string; // "HH:MM:SS"
    end_time: string;
    description?: string;
}

export enum TicketStatus {
    OPEN = "OPEN",
    IN_PROGRESS = "IN_PROGRESS",
    RESOLVED = "RESOLVED",
    CLOSED = "CLOSED"
}

export enum TicketPriority {
    LOW = "LOW",
    MEDIUM = "MEDIUM",
    HIGH = "HIGH",
    CRITICAL = "CRITICAL"
}

export interface MaintenanceTicket {
    id: number;
    title: string;
    description?: string;
    location: string;
    priority: TicketPriority;
    status: TicketStatus;
    created_at: string;
    updated_at: string;
    reported_by_id: number;
    assigned_to_id?: number;
}

export interface MaintenanceTicketCreateDTO {
    title: string;
    description?: string;
    location: string;
    priority: TicketPriority;
}
