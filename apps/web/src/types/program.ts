import { ProgramType, ProgramStatus } from './academic-base';

export interface Program {
  id: number;
  name: string;        // Course Name
  code: string;        // Course Code
  alias: string | null; // Short Name
  program_type: ProgramType;
  department_id: number | null;
  duration_years: number;
  number_of_semesters: number;
  status: ProgramStatus;
  
  // Logic Toggles (Strict spec)
  semester_system: boolean;
  rnet_required: boolean;
  allow_installments: boolean;
  is_active: boolean;
  
  created_at: string;
}

export interface ProgramCreateData {
  name: string;
  code: string;
  alias: string | null;
  program_type: ProgramType;
  department_id: number | null;
  duration_years: number;
  
  // Logic Toggles (Strict spec)
  semester_system: boolean;
  rnet_required: boolean;
  allow_installments: boolean;
  
  status: ProgramStatus;
  is_active?: boolean;
}
