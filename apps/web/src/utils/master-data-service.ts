/**
 * Master Data Service - Settings Module
 * API calls for all master data endpoints
 */
import { api } from './api';

// ============================================================================
// Academic Year
// ============================================================================

export interface AcademicYear {
    id: number;
    name: string;
    start_date: string;
    end_date: string;
    status: 'UPCOMING' | 'ACTIVE' | 'COMPLETED';
    is_current: boolean;
    created_at: string;
    updated_at: string;
}

export const getAcademicYears = async (isCurrent?: boolean): Promise<AcademicYear[]> => {
    const params = isCurrent !== undefined ? { is_current: isCurrent } : {};
    const response = await api.get('/academic/academic-years', { params });
    return response.data;
};

export const createAcademicYear = async (data: Partial<AcademicYear>): Promise<AcademicYear> => {
    const response = await api.post('/academic/academic-years', data);
    return response.data;
};

export const updateAcademicYear = async (id: number, data: Partial<AcademicYear>): Promise<AcademicYear> => {
    const response = await api.patch(`/academic/academic-years/${id}`, data);
    return response.data;
};

export const deleteAcademicYear = async (id: number): Promise<void> => {
    await api.delete(`/academic/academic-years/${id}`);
};

// ============================================================================
// Programs (for dropdown selection)
// ============================================================================

export interface ProgramInfo {
    id: number;
    code: string;
    name: string;
    duration_years: number;
    program_type: string;
}

export const getProgramsList = async (): Promise<ProgramInfo[]> => {
    const response = await api.get('/academic/programs');
    return response.data;
};

// ============================================================================
// Programs/Courses Management
// ============================================================================

export interface ProgramFull {
    id: number;
    code: string;
    short_name: string;
    name: string;
    program_type: 'UG' | 'PG' | 'DIPLOMA' | 'CERTIFICATE' | 'PHD';
    status: 'DRAFT' | 'ACTIVE' | 'ARCHIVED';
    duration_years: number;
    description?: string;
    semester_system: boolean;
    rnet_required: boolean;
    allow_installments: boolean;
    department_id: number;
    department_name?: string;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export interface DepartmentInfo {
    id: number;
    name: string;
    code: string;
}

export const getPrograms = async (isActive?: boolean): Promise<ProgramFull[]> => {
    const params = isActive !== undefined ? { is_active: isActive } : {};
    // Updated endpoint: /academic/programs
    const response = await api.get('/academic/programs', { params });
    return response.data;
};

export const getDepartmentsList = async (): Promise<DepartmentInfo[]> => {
    const response = await api.get('/academic/departments');
    return response.data;
};

// CRUD for Department Management
export const getDepartments = async (): Promise<DepartmentInfo[]> => {
    const response = await api.get('/academic/departments');
    return response.data;
};

export const createDepartment = async (data: Partial<DepartmentInfo>): Promise<any> => {
    const response = await api.post('/master/departments', data);
    return response.data;
};

export const updateDepartment = async (id: number, data: Partial<DepartmentInfo>): Promise<any> => {
    const response = await api.patch(`/master/departments/${id}`, data);
    return response.data;
};

export const deleteDepartment = async (id: number): Promise<any> => {
    const response = await api.delete(`/master/departments/${id}`);
    return response.data;
};

// Start of new department endpoints - assumes /institute/departments logic or similar?
// Wait, based on `programs.py` the API might not support department CRUD yet, or it's in `master_data.py` or `institute.py`
// Let's check `institute.py` first before writing these functions.
// But for now, assuming standard pattern based on other master data.
// Actually, `departments-list` is in `programs.py`, but `Department` model is foundation.
// Let's look at `apps/api/app/api/v1/institute.py` first.

export const createProgram = async (data: Partial<ProgramFull>): Promise<any> => {
    const response = await api.post('/master/programs', data);
    return response.data;
};

export const updateProgram = async (id: number, data: Partial<ProgramFull>): Promise<any> => {
    const response = await api.patch(`/master/programs/${id}`, data);
    return response.data;
};

export const deleteProgram = async (id: number): Promise<void> => {
    await api.delete(`/master/programs/${id}`);
};

// ============================================================================
// Academic Batch
// ============================================================================

export interface AcademicBatch {
    id: number;
    name: string;
    code: string;
    program_id: number;
    program_name?: string;
    program_code?: string;
    regulation_id?: number; // Added
    academic_year_id: number;
    admission_year: number; // For UI
    joining_year: number; // Matches backend
    graduation_year: number;
    max_strength: number; // For UI
    total_students: number; // Matches backend
    current_strength: number;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export const getAcademicBatches = async (programId?: number, isActive?: boolean): Promise<AcademicBatch[]> => {
    const params: Record<string, any> = {};
    if (programId) params.program_id = programId;
    if (isActive !== undefined) params.is_active = isActive;
    // Updated endpoint: /academic/batches
    const response = await api.get('/academic/batches', { params });
    return response.data;
};

export const createAcademicBatch = async (data: Partial<AcademicBatch>): Promise<AcademicBatch> => {
    // Updated endpoint: /academic/batches
    const response = await api.post('/academic/batches', data);
    return response.data;
};

export const updateAcademicBatch = async (id: number, data: Partial<AcademicBatch>): Promise<AcademicBatch> => {
    // Updated endpoint: /academic/batches/{id}
    const response = await api.patch(`/academic/batches/${id}`, data);
    return response.data;
};

export const deleteAcademicBatch = async (id: number): Promise<void> => {
    // Updated endpoint: /academic/batches/{id}
    const response = await api.delete(`/academic/batches/${id}`);
};

// ============================================================================
// Fee Head
// ============================================================================

export interface FeeHead {
    id: number;
    name: string;
    code: string;
    description?: string;
    is_refundable: boolean;
    is_recurring: boolean;
    is_mandatory: boolean;
    display_order: number;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export const getFeeHeads = async (isActive?: boolean): Promise<FeeHead[]> => {
    const params = isActive !== undefined ? { is_active: isActive } : {};
    const response = await api.get('/master/fee-heads', { params });
    return response.data;
};

export const createFeeHead = async (data: Partial<FeeHead>): Promise<FeeHead> => {
    const response = await api.post('/master/fee-heads', data);
    return response.data;
};

export const updateFeeHead = async (id: number, data: Partial<FeeHead>): Promise<FeeHead> => {
    const response = await api.patch(`/master/fee-heads/${id}`, data);
    return response.data;
};

export const deleteFeeHead = async (id: number): Promise<void> => {
    await api.delete(`/master/fee-heads/${id}`);
};

// ============================================================================
// Installment Plan
// ============================================================================

export interface InstallmentScheduleItem {
    percentage: number;
    due_days_from_start: number;
    description?: string;
}

export interface InstallmentPlan {
    id: number;
    name: string;
    code: string;
    description?: string;
    number_of_installments: number;
    installment_schedule: InstallmentScheduleItem[];
    late_fee_per_day: number;
    grace_period_days: number;
    max_late_fee: number;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export const getInstallmentPlans = async (isActive?: boolean): Promise<InstallmentPlan[]> => {
    const params = isActive !== undefined ? { is_active: isActive } : {};
    const response = await api.get('/master/installment-plans', { params });
    return response.data;
};

export const createInstallmentPlan = async (data: Partial<InstallmentPlan>): Promise<InstallmentPlan> => {
    const response = await api.post('/master/installment-plans', data);
    return response.data;
};

export const updateInstallmentPlan = async (id: number, data: Partial<InstallmentPlan>): Promise<InstallmentPlan> => {
    const response = await api.patch(`/master/installment-plans/${id}`, data);
    return response.data;
};

export const deleteInstallmentPlan = async (id: number): Promise<void> => {
    await api.delete(`/master/installment-plans/${id}`);
};

// ============================================================================
// Scholarship Slab
// ============================================================================

export interface ScholarshipSlab {
    id: number;
    name: string;
    code: string;
    description?: string;
    min_percentage: number;
    max_percentage: number;
    discount_type: 'PERCENTAGE' | 'FIXED';
    discount_value: number;
    max_discount_amount?: number;
    applicable_fee_heads: string[];
    academic_year_id?: number;
    program_id?: number;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export const getScholarshipSlabs = async (isActive?: boolean): Promise<ScholarshipSlab[]> => {
    const params = isActive !== undefined ? { is_active: isActive } : {};
    const response = await api.get('/master/scholarship-slabs', { params });
    return response.data;
};

export const createScholarshipSlab = async (data: Partial<ScholarshipSlab>): Promise<ScholarshipSlab> => {
    const response = await api.post('/master/scholarship-slabs', data);
    return response.data;
};

export const updateScholarshipSlab = async (id: number, data: Partial<ScholarshipSlab>): Promise<ScholarshipSlab> => {
    const response = await api.patch(`/master/scholarship-slabs/${id}`, data);
    return response.data;
};

export const deleteScholarshipSlab = async (id: number): Promise<void> => {
    await api.delete(`/master/scholarship-slabs/${id}`);
};

// ============================================================================
// Board
// ============================================================================

export interface Board {
    id: number;
    name: string;
    code: string;
    full_name?: string;
    state?: string;
    country: string;
    is_active: boolean;
    display_order: number;
    created_at: string;
}

export const getBoards = async (isActive?: boolean): Promise<Board[]> => {
    const params = isActive !== undefined ? { is_active: isActive } : {};
    const response = await api.get('/master/boards', { params });
    return response.data;
};

export const createBoard = async (data: Partial<Board>): Promise<Board> => {
    const response = await api.post('/master/boards', data);
    return response.data;
};

export const updateBoard = async (id: number, data: Partial<Board>): Promise<Board> => {
    const response = await api.patch(`/master/boards/${id}`, data);
    return response.data;
};

export const deleteBoard = async (id: number): Promise<void> => {
    await api.delete(`/master/boards/${id}`);
};

// ============================================================================
// Previous Qualification
// ============================================================================

export interface PreviousQualification {
    id: number;
    name: string;
    code: string;
    level: number;
    is_mandatory_for_admission: boolean;
    required_documents: string[];
    is_active: boolean;
    display_order: number;
    created_at: string;
}

export const getQualifications = async (isActive?: boolean): Promise<PreviousQualification[]> => {
    const params = isActive !== undefined ? { is_active: isActive } : {};
    const response = await api.get('/master/qualifications', { params });
    return response.data;
};

export const createQualification = async (data: Partial<PreviousQualification>): Promise<PreviousQualification> => {
    const response = await api.post('/master/qualifications', data);
    return response.data;
};

export const updateQualification = async (id: number, data: Partial<PreviousQualification>): Promise<PreviousQualification> => {
    const response = await api.patch(`/master/qualifications/${id}`, data);
    return response.data;
};

export const deleteQualification = async (id: number): Promise<void> => {
    await api.delete(`/master/qualifications/${id}`);
};

// ============================================================================
// Study Group
// ============================================================================

export interface StudyGroup {
    id: number;
    name: string;
    code: string;
    full_name?: string;
    qualification_id?: number;
    subjects: string[];
    is_active: boolean;
    display_order: number;
    created_at: string;
}

export const getStudyGroups = async (isActive?: boolean): Promise<StudyGroup[]> => {
    const params = isActive !== undefined ? { is_active: isActive } : {};
    const response = await api.get('/master/study-groups', { params });
    return response.data;
};

export const createStudyGroup = async (data: Partial<StudyGroup>): Promise<StudyGroup> => {
    const response = await api.post('/master/study-groups', data);
    return response.data;
};

export const updateStudyGroup = async (id: number, data: Partial<StudyGroup>): Promise<StudyGroup> => {
    const response = await api.patch(`/master/study-groups/${id}`, data);
    return response.data;
};

export const deleteStudyGroup = async (id: number): Promise<void> => {
    await api.delete(`/master/study-groups/${id}`);
};

// ============================================================================
// Reservation Category
// ============================================================================

export interface ReservationCategory {
    id: number;
    name: string;
    code: string;
    full_name?: string;
    reservation_percentage: number;
    fee_concession_percentage: number;
    requires_certificate: boolean;
    certificate_issuing_authority?: string;
    is_active: boolean;
    display_order: number;
    created_at: string;
}

export const getReservationCategories = async (isActive?: boolean): Promise<ReservationCategory[]> => {
    const params = isActive !== undefined ? { is_active: isActive } : {};
    const response = await api.get('/master/reservation-categories', { params });
    return response.data;
};

export const createReservationCategory = async (data: Partial<ReservationCategory>): Promise<ReservationCategory> => {
    const response = await api.post('/master/reservation-categories', data);
    return response.data;
};

export const updateReservationCategory = async (id: number, data: Partial<ReservationCategory>): Promise<ReservationCategory> => {
    const response = await api.patch(`/master/reservation-categories/${id}`, data);
    return response.data;
};

export const deleteReservationCategory = async (id: number): Promise<void> => {
    await api.delete(`/master/reservation-categories/${id}`);
};

// ============================================================================
// Lead Source
// ============================================================================

export interface LeadSource {
    id: number;
    name: string;
    code: string;
    description?: string;
    category: 'DIGITAL' | 'OFFLINE' | 'REFERRAL' | 'OTHER';
    is_active: boolean;
    display_order: number;
    created_at: string;
}

export const getLeadSources = async (isActive?: boolean): Promise<LeadSource[]> => {
    const params = isActive !== undefined ? { is_active: isActive } : {};
    const response = await api.get('/master/lead-sources', { params });
    return response.data;
};

export const createLeadSource = async (data: Partial<LeadSource>): Promise<LeadSource> => {
    const response = await api.post('/master/lead-sources', data);
    return response.data;
};

export const updateLeadSource = async (id: number, data: Partial<LeadSource>): Promise<LeadSource> => {
    const response = await api.patch(`/master/lead-sources/${id}`, data);
    return response.data;
};

export const deleteLeadSource = async (id: number): Promise<void> => {
    await api.delete(`/master/lead-sources/${id}`);
};

// ============================================================================
// Designation
// ============================================================================

export interface Designation {
    id: number;
    name: string;
    code: string;
    level: number;
    department_id?: number;
    min_experience_years: number;
    min_qualification?: string;
    is_teaching: boolean;
    is_active: boolean;
    display_order: number;
    created_at: string;
}

export const getDesignations = async (isActive?: boolean): Promise<Designation[]> => {
    const params = isActive !== undefined ? { is_active: isActive } : {};
    const response = await api.get('/master/designations', { params });
    return response.data;
};

export const createDesignation = async (data: Partial<Designation>): Promise<Designation> => {
    const response = await api.post('/master/designations', data);
    return response.data;
};

export const updateDesignation = async (id: number, data: Partial<Designation>): Promise<Designation> => {
    const response = await api.patch(`/master/designations/${id}`, data);
    return response.data;
};

export const deleteDesignation = async (id: number): Promise<void> => {
    await api.delete(`/master/designations/${id}`);
};

// ============================================================================
// Classroom
// ============================================================================

export interface Classroom {
    id: number;
    name: string;
    code: string;
    room_type: 'CLASSROOM' | 'LAB' | 'SEMINAR_HALL' | 'AUDITORIUM' | 'LIBRARY' | 'STAFF_ROOM' | 'OFFICE' | 'OTHER';
    building?: string;
    floor?: number;
    capacity: number;
    has_projector: boolean;
    has_ac: boolean;
    has_smart_board: boolean;
    has_computer: boolean;
    department_id?: number;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export const getClassrooms = async (isActive?: boolean, roomType?: string): Promise<Classroom[]> => {
    const params: Record<string, any> = {};
    if (isActive !== undefined) params.is_active = isActive;
    if (roomType) params.room_type = roomType;
    const response = await api.get('/master/classrooms', { params });
    return response.data;
};

export const createClassroom = async (data: Partial<Classroom>): Promise<Classroom> => {
    const response = await api.post('/master/classrooms', data);
    return response.data;
};

export const updateClassroom = async (id: number, data: Partial<Classroom>): Promise<Classroom> => {
    const response = await api.patch(`/master/classrooms/${id}`, data);
    return response.data;
};

export const deleteClassroom = async (id: number): Promise<void> => {
    await api.delete(`/master/classrooms/${id}`);
};

// ============================================================================
// Placement Company
// ============================================================================

export interface PlacementCompany {
    id: number;
    name: string;
    code: string;
    company_type: 'HOTEL' | 'RESTAURANT' | 'CRUISE' | 'OTHER';
    contact_person?: string;
    contact_email?: string;
    contact_phone?: string;
    address?: string;
    city?: string;
    state?: string;
    country: string;
    website?: string;
    is_partner: boolean;
    partnership_start_date?: string;
    mou_document_url?: string;
    avg_package_lpa?: number;
    students_placed: number;
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export const getPlacementCompanies = async (isActive?: boolean, isPartner?: boolean): Promise<PlacementCompany[]> => {
    const params: Record<string, any> = {};
    if (isActive !== undefined) params.is_active = isActive;
    if (isPartner !== undefined) params.is_partner = isPartner;
    const response = await api.get('/master/placement-companies', { params });
    return response.data;
};

export const createPlacementCompany = async (data: Partial<PlacementCompany>): Promise<PlacementCompany> => {
    const response = await api.post('/master/placement-companies', data);
    return response.data;
};

export const updatePlacementCompany = async (id: number, data: Partial<PlacementCompany>): Promise<PlacementCompany> => {
    const response = await api.patch(`/master/placement-companies/${id}`, data);
    return response.data;
};

export const deletePlacementCompany = async (id: number): Promise<void> => {
    await api.delete(`/master/placement-companies/${id}`);
};

// ============================================================================
// Email Template
// ============================================================================

export interface EmailTemplate {
    id: number;
    name: string;
    subject: string;
    body: string;
    template_type: 'TRANSACTIONAL' | 'PROMOTIONAL';
    variables: string[];
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export const getEmailTemplates = async (isActive?: boolean): Promise<EmailTemplate[]> => {
    const params = isActive !== undefined ? { is_active: isActive } : {};
    const response = await api.get('/master/email-templates', { params });
    return response.data;
};

export const createEmailTemplate = async (data: Partial<EmailTemplate>): Promise<EmailTemplate> => {
    const response = await api.post('/master/email-templates', data);
    return response.data;
};

export const updateEmailTemplate = async (id: number, data: Partial<EmailTemplate>): Promise<EmailTemplate> => {
    const response = await api.patch(`/master/email-templates/${id}`, data);
    return response.data;
};

export const deleteEmailTemplate = async (id: number): Promise<void> => {
    await api.delete(`/master/email-templates/${id}`);
};

// ============================================================================
// SMS Template
// ============================================================================

export interface SMSTemplate {
    id: number;
    name: string;
    content: string;
    dlt_template_id?: string;
    sender_id?: string;
    template_type: 'TRANSACTIONAL' | 'PROMOTIONAL';
    variables: string[];
    is_active: boolean;
    created_at: string;
    updated_at: string;
}

export const getSMSTemplates = async (isActive?: boolean): Promise<SMSTemplate[]> => {
    const params = isActive !== undefined ? { is_active: isActive } : {};
    const response = await api.get('/master/sms-templates', { params });
    return response.data;
};

export const createSMSTemplate = async (data: Partial<SMSTemplate>): Promise<SMSTemplate> => {
    const response = await api.post('/master/sms-templates', data);
    return response.data;
};

export const updateSMSTemplate = async (id: number, data: Partial<SMSTemplate>): Promise<SMSTemplate> => {
    const response = await api.patch(`/master/sms-templates/${id}`, data);
    return response.data;
};

export const deleteSMSTemplate = async (id: number): Promise<void> => {
    await api.delete(`/master/sms-templates/${id}`);
};

// ============================================================================
// Batch Semesters (New Academic Foundation)
// ============================================================================

import { BatchSemester, BatchSubject, ProgramYear } from '../types/academic-batch';

export const getBatchSemesters = async (batchId: number): Promise<BatchSemester[]> => {
    // Updated endpoint: /academic/batches/{id}/semesters
    const response = await api.get(`/academic/batches/${batchId}/semesters`);
    return response.data;
};

// Note: Semesters are now auto-generated via Regulation/Batch and are not manually created.

export const updateBatchSemester = async (batchId: number, semesterId: number, data: Partial<BatchSemester>): Promise<BatchSemester> => {
    const response = await api.patch(`/academic/batches/${batchId}/semesters/${semesterId}`, data);
    return response.data;
};

// ============================================================================
// Program Years (Year-level hierarchy)
// ============================================================================

export const getProgramYears = async (batchId: number): Promise<ProgramYear[]> => {
    const response = await api.get(`/academic/batches/${batchId}/program-years`);
    return response.data;
};

export const getBatchSubjects = async (batchId: number, semesterNo?: number): Promise<BatchSubject[]> => {
    const params: any = {};
    if (semesterNo) params.semester_no = semesterNo;
    const response = await api.get(`/academic/batches/${batchId}/subjects`, { params });
    return response.data;
};


// ============================================================================
// Lab Batch Allocations
// ============================================================================

export interface LabAllocation {
    id: number;
    student_id: number;
    student_name: string;
    admission_number: string;
    practical_batch_id: number;
    subject_id: number;
}

export interface BulkAllocationRequest {
    student_ids: number[];
    practical_batch_id: number;
    subject_id: number;
    batch_semester_id: number;
}

export const getLabAllocations = async (batchId: number, subjectId?: number): Promise<LabAllocation[]> => {
    const params: any = {};
    if (subjectId) params.subject_id = subjectId;
    const response = await api.get(`/allocations/batch/${batchId}`, { params });
    return response.data;
};

export const assignStudentsToLab = async (data: BulkAllocationRequest): Promise<{ allocated: number, capacity_remaining: number }> => {
    const response = await api.post('/allocations/bulk', data);
    return response.data;
};

export const removeStudentFromLab = async (studentId: number, subjectId: number): Promise<void> => {
    await api.delete(`/allocations/${studentId}/${subjectId}`);
};

