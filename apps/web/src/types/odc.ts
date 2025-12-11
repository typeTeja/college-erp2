export enum GenderPreference {
    MALE = "MALE",
    FEMALE = "FEMALE",
    ANY = "ANY"
}

export enum ODCStatus {
    OPEN = "OPEN",
    CLOSED = "CLOSED",
    COMPLETED = "COMPLETED",
    CANCELLED = "CANCELLED"
}

export enum ApplicationStatus {
    APPLIED = "APPLIED",
    SELECTED = "SELECTED",
    REJECTED = "REJECTED",
    ATTENDED = "ATTENDED",
    ABSENT = "ABSENT",
    WITHDRAWN = "WITHDRAWN"
}

export enum PayoutStatus {
    PENDING = "PENDING",
    PAID = "PAID"
}

export interface ODCHotel {
    id: number;
    name: string;
    address: string;
    contact_person: string;
    phone: string;
    email?: string;
    default_pay_rate?: number;
    is_active: boolean;
}

export interface ODCHotelCreate {
    name: string;
    address: string;
    contact_person: string;
    phone: string;
    email?: string;
    default_pay_rate?: number;
}

export interface ODCRequest {
    id: number;
    hotel_id: number;
    event_name: string;
    event_date: string; // ISO Date
    report_time: string; // ISO DateTime
    duration_hours: number;
    vacancies: number;
    gender_preference: GenderPreference;
    pay_amount: number;
    transport_provided: boolean;
    status: ODCStatus;
    created_at: string;

    // Flattened / Expanded
    hotel_name?: string;
}

export interface ODCRequestCreate {
    hotel_id: number;
    event_name: string;
    event_date: string;
    report_time: string;
    duration_hours: number;
    vacancies: number;
    gender_preference: GenderPreference;
    pay_amount: number;
    transport_provided: boolean;
}

export interface ODCApplication {
    id: number;
    request_id: number;
    student_id: number;
    status: ApplicationStatus;
    applied_at: string;

    // Expanded
    event_name?: string;
    event_date?: string;
}

export interface SelectionUpdate {
    application_ids: number[];
    status: ApplicationStatus;
    remarks?: string;
}

export enum BillingStatus {
    DRAFT = "DRAFT",
    SENT = "SENT",
    PAID = "PAID",
    CANCELLED = "CANCELLED"
}

export enum PaymentMethod {
    CASH = "CASH",
    BANK_TRANSFER = "BANK_TRANSFER",
    UPI = "UPI",
    CHEQUE = "CHEQUE"
}

// Feedback interfaces
export interface StudentFeedbackSubmit {
    student_feedback: string;
    student_rating: number; // 1-5
}

export interface HotelFeedbackSubmit {
    hotel_feedback: string;
    hotel_rating: number; // 1-5
}

// Billing interfaces
export interface ODCBilling {
    id: number;
    request_id: number;
    invoice_number: string;
    total_students: number;
    amount_per_student: number;
    total_amount: number;
    status: BillingStatus;
    invoice_date: string;
    due_date?: string;
    paid_date?: string;
    payment_method?: PaymentMethod;
    payment_reference?: string;
    notes?: string;
    created_at: string;

    // Expanded
    event_name?: string;
    hotel_name?: string;
}

export interface BillingCreate {
    request_id: number;
    invoice_date: string;
    due_date?: string;
    notes?: string;
}

export interface BillingMarkPaid {
    payment_method: PaymentMethod;
    payment_reference?: string;
    paid_date: string;
    notes?: string;
}

// Payout interfaces
export interface ODCPayout {
    id: number;
    application_id: number;
    amount: number;
    payment_method: PaymentMethod;
    transaction_reference?: string;
    payout_date: string;
    processed_at: string;
    notes?: string;

    // Expanded
    student_name?: string;
    event_name?: string;
}

export interface PayoutBatchProcess {
    application_ids: number[];
    payment_method: PaymentMethod;
    payout_date: string;
    notes?: string;
}

