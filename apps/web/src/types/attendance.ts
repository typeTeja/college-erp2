// Minimal interfaces for relations
export interface Student {
    id: number;
    name: string;
    admission_number: string;
}

export interface Faculty {
    id: number;
    user: { full_name: string };
}

export interface Subject {
    id: number;
    name: string;
    code: string;
}

export enum AttendanceStatus {
    PRESENT = "PRESENT",
    ABSENT = "ABSENT",
    LATE = "LATE",
    ON_DUTY = "ON_DUTY"
}

export enum SessionStatus {
    SCHEDULED = "SCHEDULED",
    COMPLETED = "COMPLETED",
    CANCELLED = "CANCELLED"
}

export interface AttendanceSession {
    id: number;
    subject_id: number;
    faculty_id: number;
    program_id: number;
    program_year_id: number;
    semester: number;
    section: string;
    session_date: string; // ISO date string
    start_time: string; // ISO time string
    end_time: string; // ISO time string
    topic_covered?: string;
    status: SessionStatus;
    created_at: string;
    updated_at: string;
    subject?: Subject;
    faculty?: Faculty;
}

export interface AttendanceRecord {
    id: number;
    session_id: number;
    student_id: number;
    status: AttendanceStatus;
    remarks?: string;
    student?: Student;
}

export interface AttendanceStats {
    total_classes: number;
    present: number;
    absent: number;
    late: number;
    on_duty: number;
    attendance_percentage: number;
}

export interface CreateSessionDTO {
    subject_id: number;
    faculty_id: number;
    program_id: number;
    program_year_id: number;
    semester: number;
    section: string;
    session_date: string;
    start_time: string;
    end_time: string;
    topic_covered?: string;
}

export interface UpdateRecordDTO {
    student_id: number;
    status: AttendanceStatus;
    remarks?: string;
}

export interface BulkMarkAttendanceDTO {
    session_id: number;
    records: UpdateRecordDTO[];
}
