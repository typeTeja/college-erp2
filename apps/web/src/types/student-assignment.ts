/**
 * Student Assignment Types
 */

export interface StudentSectionAssignment {
    id: number;
    student_id: number;
    section_id: number;
    batch_id: number;
    semester_no: number;
    assignment_type: 'AUTO' | 'MANUAL' | 'RULE_BASED';
    assigned_at: string;
    assigned_by: number | null;
    is_active: boolean;
}

export interface AutoAssignRequest {
    batch_id: number;
    semester_no: number;
}

export interface AutoAssignResponse {
    assigned_count: number;
    unassigned_count: number;
    message: string;
}

export interface StudentSectionAssignmentCreate {
    student_id: number;
    section_id: number;
    batch_id: number;
    semester_no: number;
    assignment_type?: string;
}

export interface ReassignRequest {
    new_section_id: number;
}

export interface SectionRosterStudent {
    assignment_id: number;
    student_id: number;
    student_name: string;
    admission_number: string;
    assignment_type: string;
    assigned_at: string;
}

export interface SectionRosterResponse {
    section_id: number;
    section_name: string;
    section_code: string;
    current_strength: number;
    max_strength: number;
    students: SectionRosterStudent[];
}

export interface UnassignedStudent {
    id: number;
    name: string;
    roll_number: string;
    email: string;
}

export interface UnassignedStudentsResponse {
    batch_id: number;
    semester_no: number;
    count: number;
    students: UnassignedStudent[];
}
