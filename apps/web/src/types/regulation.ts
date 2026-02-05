import { ProgramType, RegulationStatus } from './academic-base';

export interface Regulation {
  id: number;
  name: string;
  program_id: number;
  program_type: ProgramType;
  total_credits: number;
  duration_years: number;
  has_credit_based_detention: boolean;
  min_sgpa: number;
  min_cgpa: number;
  internal_pass_percentage: number;
  external_pass_percentage: number;
  total_pass_percentage: number;
  is_locked: boolean;
  created_at: string;
}

export interface RegulationCreateData {
  name: string;
  program_id: number;
  program_type?: ProgramType;
  total_credits: number;
  duration_years: number;
  has_credit_based_detention?: boolean;
  min_sgpa?: number;
  min_cgpa?: number;
  internal_pass_percentage?: number;
  external_pass_percentage?: number;
  total_pass_percentage?: number;
}
