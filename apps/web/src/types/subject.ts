import { SubjectType, EvaluationType } from './academic-base';

export interface Subject {
  id: number;
  code: string;
  name: string;
  short_name?: string | null;
  subject_type: SubjectType;
  evaluation_type: EvaluationType;
  department_id?: number | null;
  created_at: string;
}

export interface SubjectCreateData {
  code: string;
  name: string;
  short_name?: string | null;
  subject_type: SubjectType;
  evaluation_type: EvaluationType;
  department_id?: number | null;
}

export interface SubjectConfig {
  id: number;
  subject_id: number;
  regulation_id: number;
  credits: number;
  internal_max_marks: number;
  external_max_marks: number;
  total_max_marks: number;
  is_active: boolean;
}

export interface RegulationSubject extends Subject {
  regulation_subject_id: number;
  semester_number: number;
  credits: number;
  is_elective: boolean;
  group_name?: string | null;
}
