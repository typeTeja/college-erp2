/**
 * Facility Management Types
 * Library, Hostel, Transport
 */

// Library Types
export interface Book {
    id: number;
    isbn: string;
    title: string;
    author: string;
    publisher?: string;
    category: string;
    total_copies: number;
    available_copies: number;
    rack_number?: string;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export interface LibraryMember {
    id: number;
    student_id: number;
    member_id: string;
    membership_type: string;
    valid_from: string;
    valid_until: string;
    is_active: boolean;
    created_at: string;
}

export interface BookIssue {
    id: number;
    book_id: number;
    member_id: number;
    issue_date: string;
    due_date: string;
    return_date?: string;
    fine_amount: number;
    fine_paid: boolean;
    status: 'issued' | 'returned' | 'overdue';
    created_at: string;
    updated_at: string;
}

// Hostel Types
export interface Hostel {
    id: number;
    name: string;
    hostel_type: 'boys' | 'girls';
    warden_name?: string;
    warden_contact?: string;
    total_rooms: number;
    occupied_rooms: number;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export interface Room {
    id: number;
    hostel_id: number;
    room_number: string;
    room_type: 'single' | 'double' | 'triple' | 'quad';
    floor: number;
    capacity: number;
    occupied_beds: number;
    is_available: boolean;
    created_at: string;
    updated_at: string;
}

export interface RoomAllocation {
    id: number;
    student_id: number;
    room_id: number;
    bed_number?: string;
    from_date: string;
    to_date?: string;
    vacate_date?: string;
    status: 'active' | 'vacated';
    created_at: string;
    updated_at: string;
}

export interface MaintenanceRequest {
    id: number;
    room_id: number;
    student_id: number;
    request_type: string;
    description: string;
    priority: 'low' | 'medium' | 'high';
    status: 'pending' | 'in_progress' | 'completed' | 'rejected';
    assigned_to?: number;
    resolved_at?: string;
    created_at: string;
    updated_at: string;
}

// Transport Types
export interface Vehicle {
    id: number;
    vehicle_number: string;
    vehicle_type: string;
    capacity: number;
    driver_id?: number;
    status: 'active' | 'maintenance' | 'inactive';
    created_at: string;
    updated_at: string;
}

export interface Route {
    id: number;
    route_name: string;
    route_code: string;
    start_point: string;
    end_point: string;
    stops: string[];
    distance_km: number;
    fare_amount: number;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export interface TransportAllocation {
    id: number;
    student_id: number;
    route_id: number;
    pickup_point: string;
    from_date: string;
    to_date?: string;
    status: 'active' | 'inactive';
    created_at: string;
    updated_at: string;
}

export interface VehicleTracking {
    id: number;
    vehicle_id: number;
    latitude: number;
    longitude: number;
    speed?: number;
    timestamp: string;
    created_at: string;
}

// Request types
export interface BookIssueRequest {
    book_id: number;
    member_id: number;
    due_date: string;
}

export interface RoomAllocationRequest {
    student_id: number;
    room_id: number;
    from_date: string;
    to_date?: string;
}

export interface TransportAllocationRequest {
    student_id: number;
    route_id: number;
    pickup_point: string;
    from_date: string;
}
