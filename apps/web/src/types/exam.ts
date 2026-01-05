export enum ExamType {
    MID_TERM = "MID_TERM",
    FINAL = "FINAL",
    INTERNAL = "INTERNAL",
    PRACTICAL = "PRACTICAL",
}

export enum ExamStatus {
    DRAFT = "DRAFT",
    PUBLISHED = "PUBLISHED",
    COMPLETED = "COMPLETED",
}

export interface Exam {
    id: number;
    name: string;
    exam_type: ExamType;
    academic_year: string;
    batch_semester_id: number;
    start_date: string;
    end_date: string;
    status: ExamStatus;
    description?: string;
}

export interface ExamSchedule {
    id: number;
    exam_id: number;
    subject_id: number;
    exam_date: string;
    start_time: string;
    end_time: string;
    max_marks: number;
    subject_name?: string;
}

export interface ExamResult {
    id: number;
    exam_schedule_id: number;
    student_id: number;
    marks_obtained: number;
    grade?: string;
    remarks?: string;
    is_absent: boolean;
    student_name?: string;
    subject_name?: string;
    exam_name?: string;
}

export interface CreateExamDTO {
    name: string;
    exam_type: ExamType;
    academic_year: string;
    batch_semester_id: number;
    start_date: string;
    end_date: string;
    description?: string;
}

export interface CreateScheduleDTO {
    exam_id: number;
    subject_id: number;
    exam_date: string;
    start_time: string;
    end_time: string;
    max_marks: number;
}

export interface BulkMarksEntryDTO {
    exam_schedule_id: number;
    records: {
        exam_schedule_id: number;
        student_id: number;
        marks_obtained: number;
        grade?: string;
        remarks?: string;
        is_absent: boolean;
    }[];
}
