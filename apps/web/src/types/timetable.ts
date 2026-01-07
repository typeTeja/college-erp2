export enum DayOfWeek {
    MONDAY = "MONDAY",
    TUESDAY = "TUESDAY",
    WEDNESDAY = "WEDNESDAY",
    THURSDAY = "THURSDAY",
    FRIDAY = "FRIDAY",
    SATURDAY = "SATURDAY",
    SUNDAY = "SUNDAY"
}

export enum SlotType {
    THEORY = "THEORY",
    PRACTICAL = "PRACTICAL",
    BREAK = "BREAK",
    ASSEMBLY = "ASSEMBLY"
}

export enum AdjustmentStatus {
    REQUESTED = "REQUESTED",
    APPROVED = "APPROVED",
    REJECTED = "REJECTED",
    COMPLETED = "COMPLETED"
}

export interface TimeSlot {
    id: number;
    name: string;
    start_time: string; // HH:MM:SS
    end_time: string;
    type: SlotType;
    is_active: boolean;
}

export interface Classroom {
    id: number;
    room_number: string;
    capacity: number;
    type: string;
    is_active: boolean;
}

export interface ClassSchedule {
    id: number;
    academic_year_id: number;
    batch_semester_id: number;
    section_id?: number;
    day_of_week: DayOfWeek;
    period_id: number;
    subject_id?: number;
    faculty_id?: number;
    room_id?: number;

    // Expanded details
    period?: TimeSlot;
    subject_name?: string;
    faculty_name?: string;
    room_number?: string;
}

export interface ClassAdjustment {
    id: number;
    timetable_entry_id: number;
    date: string;
    original_faculty_id: number;
    substitute_faculty_id?: number;
    status: AdjustmentStatus;
    reason?: string;
    created_at: string;

    // Expanded
    original_faculty_name?: string;
    substitute_faculty_name?: string;
    subject_name?: string;
}

export interface CreateTimeSlotDTO {
    name: string;
    start_time: string;
    end_time: string;
    type: SlotType;
}

export interface CreateScheduleDTO {
    academic_year_id: number;
    batch_semester_id: number;
    section_id?: number;
    day_of_week: DayOfWeek;
    period_id: number;
    subject_id?: number;
    faculty_id?: number;
    room_id?: number;
}

export interface CreateAdjustmentDTO {
    timetable_entry_id: number;
    date: string; // YYYY-MM-DD
    original_faculty_id: number;
    reason?: string;
}
