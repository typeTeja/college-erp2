export interface Subject {
    id: number;
    code: string;
    name: string;
    credits: number;
    description?: string;
    semester_id: number;
    faculty_id?: number;
}
