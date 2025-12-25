export enum CircularTarget {
    ALL = "ALL",
    STAFF = "STAFF",
    STUDENTS = "STUDENTS",
    PARENTS = "PARENTS",
    SPECIFIC_ROLES = "SPECIFIC_ROLES",
    SPECIFIC_DEPARTMENTS = "SPECIFIC_DEPARTMENTS"
}

export enum NotificationType {
    INFO = "INFO",
    SUCCESS = "SUCCESS",
    WARNING = "WARNING",
    ERROR = "ERROR"
}

export enum NotificationChannel {
    SMS = "SMS",
    EMAIL = "EMAIL",
    WHATSAPP = "WHATSAPP",
    PUSH = "PUSH"
}

export interface Circular {
    id: number;
    title: string;
    content: string;
    attachment_url: string | null;
    target_type: CircularTarget;
    target_ids: number[] | null;
    is_active: boolean;
    published_at: string;
    expires_at: string | null;
    author_id: number;
}

export interface Notification {
    id: number;
    user_id: number;
    title: string;
    message: string;
    type: NotificationType;
    link: string | null;
    is_read: boolean;
    created_at: string;
    read_at: string | null;
}

export interface NotificationLog {
    id: number;
    user_id: number | null;
    recipient_identifier: string;
    channel: NotificationChannel;
    message: string;
    status: string;
    created_at: string;
}

export interface CircularCreateDTO {
    title: string;
    content: string;
    attachment_url?: string;
    target_type?: CircularTarget;
    target_ids?: number[];
    expires_at?: string;
}
