export enum BookStatus {
    AVAILABLE = "AVAILABLE",
    ISSUED = "ISSUED",
    LOST = "LOST",
    DAMAGED = "DAMAGED"
}

export interface Book {
    id: number;
    title: string;
    author: string;
    isbn: string;
    publisher?: string;
    category?: string;
    location?: string;
    total_copies: number;
    available_copies: number;
    status: BookStatus;
}

export interface BookIssue {
    id: number;
    book_id: number;
    student_id: number;
    issue_date: string;
    due_date: string;
    return_date?: string;
    is_returned: boolean;
}

export interface LibraryFine {
    id: number;
    book_issue_id: number;
    amount: number;
    is_paid: boolean;
    payment_date?: string;
    remarks?: string;
}
