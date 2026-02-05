import { BatchStatus, SemesterStatus } from './academic-base';

export interface AcademicBatch {
  id: number;
  batch_code: string;
  batch_name: string;
  program_id: number;
  regulation_id: number;
  joining_year: number;
  start_year: number;
  end_year: number;
  current_year: number;
  current_semester: number;
  total_students: number;
  status: BatchStatus;
  is_active: boolean;
  created_at: string;
}

export interface BatchSemester {
  id: number;
  batch_id: number;
  semester_number: number;
  academic_year_id: number;
  start_date: string;
  end_date: string;
  status: SemesterStatus;
  is_current: boolean;
  created_at: string;
}

export interface BatchSubject {
  id: number;
  batch_semester_id: number;
  subject_id: number;
  regulation_subject_id: number;
  faculty_id?: number | null;
  is_active: boolean;
}

export interface Section {
  id: number;
  name: string;
  batch_id: number;
  semester_no: number;
  capacity: number;
  current_strength: number;
}

export interface PracticalBatch {
  id: number;
  name: string;
  code: string;
  batch_semester_id: number;
  capacity: number;
  current_strength: number;
}

export interface ProgramYear {
  id: number;
  name: string;
  year_number: number;
  batch_id: number;
  is_current: boolean;
}
