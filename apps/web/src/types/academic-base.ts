/**
 * Shared Academic Types & Enums
 * Single source of truth derived from backend app/shared/enums.py
 */

export enum ProgramType {
  UG = "UG",
  PG = "PG",
  DIPLOMA = "DIPLOMA",
  CERTIFICATE = "CERTIFICATE",
  PHD = "PHD"
}

export enum ProgramStatus {
  DRAFT = "DRAFT",
  ACTIVE = "ACTIVE",
  ARCHIVED = "ARCHIVED"
}

export enum AttendanceStatus {
  PRESENT = "PRESENT",
  ABSENT = "ABSENT",
  LATE = "LATE",
  ON_DUTY = "ON_DUTY"
}

export enum SessionStatus {
  SCHEDULED = "SCHEDULED",
  COMPLETED = "COMPLETED",
  CANCELLED = "CANCELLED"
}

export enum ExamType {
  MID_TERM = "MID_TERM",
  FINAL = "FINAL",
  INTERNAL = "INTERNAL",
  PRACTICAL = "PRACTICAL",
  BOTH = "BOTH"
}

export enum ExamStatus {
  DRAFT = "DRAFT",
  PUBLISHED = "PUBLISHED",
  COMPLETED = "COMPLETED"
}

export enum ExamResultStatus {
  PASS = "PASS",
  FAIL = "FAIL",
  ABSENT = "ABSENT",
  DETAINED = "DETAINED",
  WITHHELD = "WITHHELD"
}

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

export enum AcademicYearStatus {
  UPCOMING = "UPCOMING",
  ACTIVE = "ACTIVE",
  COMPLETED = "COMPLETED"
}

export enum SubjectType {
  THEORY = "THEORY",
  PRACTICAL = "PRACTICAL",
  PROJECT = "PROJECT",
  ELECTIVE = "ELECTIVE",
  AUDIT = "AUDIT"
}

export enum EvaluationType {
  THEORY_ONLY = "THEORY_ONLY",
  PRACTICAL_ONLY = "PRACTICAL_ONLY",
  THEORY_AND_PRACTICAL = "THEORY_AND_PRACTICAL",
  PROJECT = "PROJECT"
}

export enum PromotionRuleType {
  CREDIT_PERCENTAGE = "CREDIT_PERCENTAGE",
  CREDIT_COUNT = "CREDIT_COUNT",
  BACKLOG_COUNT = "BACKLOG_COUNT"
}

export enum RegulationStatus {
  DRAFT = "DRAFT",
  ACTIVE = "ACTIVE",
  ARCHIVED = "ARCHIVED"
}

export enum BatchStatus {
  ACTIVE = "ACTIVE",
  COMPLETED = "COMPLETED",
  ARCHIVED = "ARCHIVED"
}

export enum SemesterStatus {
  UPCOMING = "UPCOMING",
  ACTIVE = "ACTIVE",
  COMPLETED = "COMPLETED"
}

/**
 * Standard API Response wrapper for Academic Domain
 */
export interface AcademicApiResponse<T> {
  data: T;
  message?: string;
  status: number;
}

export interface AcademicYear {
  id: number;
  year: string;
  start_date: string;
  end_date: string;
  is_current: boolean;
  status: AcademicYearStatus;
  created_at?: string;
}

export interface AcademicYearCreateData {
  year: string;
  start_date: string;
  end_date: string;
  is_current?: boolean;
  status?: AcademicYearStatus;
}
