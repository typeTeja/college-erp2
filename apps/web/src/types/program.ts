import { ProgramType, ProgramStatus } from './academic-base';

export interface Program {
  id: number;
  code: string;
  name: string;
  alias?: string | null;
  program_type: ProgramType;
  department_id: number | null;
  duration_years: number;
  number_of_semesters: number;
  status: ProgramStatus;
  created_at: string;
}

export interface ProgramCreateData {
  code: string;
  name: string;
  alias?: string | null;
  program_type: ProgramType;
  department_id?: number | null;
  duration_years: number;
  number_of_semesters: number;
  status?: ProgramStatus;
}
