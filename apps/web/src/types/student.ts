export interface Student {
    id: number;

    // Basic Information
    admission_number: string;
    name: string;
    middle_name?: string;
    dob?: string;

    // Contact Information
    phone?: string;
    email?: string;
    alternate_mobile?: string;

    // Address Information
    current_address?: string;
    permanent_address?: string;
    city?: string;
    state?: string;
    pincode?: string;

    // Demographics
    gender?: string;
    blood_group?: string;
    aadhaar_number?: string;
    nationality?: string;
    religion?: string;
    caste_category?: string;

    // Parent Details
    father_name?: string;
    father_mobile?: string;
    father_email?: string;
    father_occupation?: string;

    mother_name?: string;
    mother_mobile?: string;
    mother_email?: string;
    mother_occupation?: string;

    // Guardian Details
    guardian_name?: string;
    guardian_mobile?: string;
    guardian_relation?: string;

    // Emergency Contact
    emergency_contact_name?: string;
    emergency_contact_mobile?: string;
    emergency_contact_relation?: string;

    // Previous Education
    previous_qualification?: string;
    previous_institution?: string;
    previous_institution_city?: string;
    previous_institution_district?: string;
    previous_board?: string;
    previous_marks?: number;
    previous_percentage?: number;
    previous_year_of_passing?: number;

    // Documents
    documents?: Record<string, string>; // {document_type: url}

    // Portal Access
    portal_user_id?: number;
    portal_last_login?: string;

    // Fee Tracking
    fee_structure_id?: number;
    total_fee?: number;
    paid_amount?: number;
    pending_amount?: number;

    // Academic Links
    user_id?: number;
    program_id?: number;
    batch_id?: number;
    program_year_id?: number;
    batch_semester_id?: number;
    section_id?: number;
    practical_batch_id?: number;

    // Legacy fields (for backward compatibility)
    current_year?: number;
    current_semester?: number;
    section?: string;
    roll_number?: string;
    program_name?: string;

    // Flags
    hostel_required?: boolean;
    transport_required?: boolean;
    scholarship_category?: string;
    lateral_entry?: boolean;

    // Status
    status: string;

    // Deactivation Tracking
    deactivated_at?: string;
    deactivated_by?: number;
    deactivation_reason?: string;

    // Metadata
    created_from?: string;
    created_at?: string;
    updated_at?: string;
}

export interface StudentCreate {
    admission_number: string;
    name: string;
    middle_name?: string;
    dob?: string;
    phone?: string;
    email?: string;
    gender?: string;
    program_id: number;
    batch_id: number;
    program_year_id: number;
    batch_semester_id: number;
    section_id?: number;

    // All other fields optional for creation
    [key: string]: any;
}

export interface StudentUpdate {
    name?: string;
    middle_name?: string;
    dob?: string;
    phone?: string;
    email?: string;
    alternate_mobile?: string;
    current_address?: string;
    permanent_address?: string;
    city?: string;
    state?: string;
    pincode?: string;
    gender?: string;
    blood_group?: string;
    nationality?: string;
    religion?: string;
    caste_category?: string;

    // Parent details
    father_name?: string;
    father_mobile?: string;
    father_email?: string;
    father_occupation?: string;
    mother_name?: string;
    mother_mobile?: string;
    mother_email?: string;
    mother_occupation?: string;

    // Guardian details
    guardian_name?: string;
    guardian_mobile?: string;
    guardian_relation?: string;

    // Emergency contact
    emergency_contact_name?: string;
    emergency_contact_mobile?: string;
    emergency_contact_relation?: string;

    // Previous education
    previous_qualification?: string;
    previous_institution?: string;
    previous_institution_city?: string;
    previous_institution_district?: string;
    previous_board?: string;
    previous_marks?: number;
    previous_percentage?: number;
    previous_year_of_passing?: number;

    // Academic updates
    section_id?: number;
    practical_batch_id?: number;

    // Flags
    hostel_required?: boolean;
    transport_required?: boolean;
    status?: string;
}
