/**
 * Portal & Notification Types
 */

export interface StudentPortalAccess {
    id: number;
    student_id: number;
    username: string;
    is_active: boolean;
    last_login?: string;
    login_count: number;
    failed_login_attempts: number;
    account_locked: boolean;
    locked_until?: string;
    password_changed_at?: string;
    created_at: string;
    updated_at: string;
}

export interface StudentActivity {
    id: number;
    student_id: number;
    activity_type: string;
    activity_description: string;
    ip_address?: string;
    user_agent?: string;
    metadata?: Record<string, any>;
    created_at: string;
}

export interface Notification {
    id: number;
    student_id: number;
    title: string;
    message: string;
    notification_type: 'info' | 'warning' | 'success' | 'error';
    is_read: boolean;
    read_at?: string;
    action_url?: string;
    metadata?: Record<string, any>;
    created_at: string;
    updated_at: string;
}

export interface PortalDashboard {
    student: {
        id: number;
        name: string;
        admission_number: string;
        program: string;
        year: number;
        semester: number;
    };
    attendance: {
        total_classes: number;
        attended: number;
        percentage: number;
    };
    fees: {
        total_amount: number;
        paid_amount: number;
        pending_amount: number;
    };
    exams: {
        upcoming: number;
        completed: number;
    };
    notifications: {
        unread_count: number;
        recent: Notification[];
    };
}

// Request types
export interface ChangePasswordRequest {
    current_password: string;
    new_password: string;
}

export interface ProfileUpdateRequest {
    phone?: string;
    email?: string;
    current_address?: string;
    emergency_contact_name?: string;
    emergency_contact_mobile?: string;
}
