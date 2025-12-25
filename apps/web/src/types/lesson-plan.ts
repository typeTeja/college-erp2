export enum TopicStatus {
    PENDING = "PENDING",
    COMPLETED = "COMPLETED",
}

export enum QuestionType {
    MCQ = "MCQ",
    THEORETICAL = "THEORETICAL",
    PRACTICAL = "PRACTICAL",
}

export enum DifficultyLevel {
    EASY = "EASY",
    MEDIUM = "MEDIUM",
    HARD = "HARD",
}

export interface SyllabusTopic {
    id: number;
    lesson_plan_id: number;
    unit_number: number;
    title: string;
    description: string | null;
    planned_date: string | null;
    completion_date: string | null;
    status: TopicStatus;
}

export interface LessonPlan {
    id: number;
    subject_id: number;
    faculty_id: number;
    academic_year: string;
    total_hours_planned: number;
    created_at: string;
    updated_at: string;
    topics: SyllabusTopic[];
}

export interface Question {
    id: number;
    bank_id: number;
    topic_id: number | null;
    text: string;
    type: QuestionType;
    difficulty: DifficultyLevel;
    marks: number;
    answer_key: string | null;
    options: string | null; // JSON string
}

export interface QuestionBank {
    id: number;
    subject_id: number;
    questions: Question[];
}

export interface PaperGenerateRequest {
    subject_id: number;
    total_marks: number;
    easy_weight: number;
    medium_weight: number;
    hard_weight: number;
    topics?: number[];
}

export interface LessonPlanCreate {
    subject_id: number;
    faculty_id: number;
    academic_year: string;
    total_hours_planned: number;
    topics: {
        unit_number: number;
        title: string;
        description?: string;
        planned_date?: string;
    }[];
}
