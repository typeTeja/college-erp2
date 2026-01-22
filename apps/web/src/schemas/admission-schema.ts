import { z } from 'zod';
import { FeeMode } from '@/types/admissions';

export const admissionSchema = z.object({
    application_number: z.string().optional(), // Auto-generated
    student_name: z.string().min(2, "Student name is required"),
    email: z.string().email("Invalid email address"),
    phone: z.string().regex(/^\d{10}$/, { message: "Phone number must be 10 digits" }),
    gender: z.enum(["MALE", "FEMALE", "OTHER"]),
    course_id: z.number().min(1, "Course selection is required"),
    state: z.string().min(2, "State is required"),
    board: z.string().min(2, "Board is required"),
    group_of_study: z.string().min(2, "Group of study is required"),
    fee_mode: z.nativeEnum(FeeMode),
    academic_year: z.string().optional(),
    status: z.enum(["PENDING", "APPROVED", "REJECTED", "WITHDRAWN"]),
    documents_submitted: z.boolean(),
    fee_paid: z.boolean(),
    remarks: z.string().optional(),
    
    // Stage 2 Fields (Optional for full entry)
    aadhaar_number: z.string().regex(/^\d{12}$/, "Aadhaar must be 12 digits").optional().or(z.literal('')),
    father_name: z.string().optional(),
    father_phone: z.string().regex(/^\d{10}$/, "Phone must be 10 digits").optional().or(z.literal('')),
    address: z.string().optional(),
    previous_marks_percentage: z.coerce.number().min(0).max(100).optional(),
    applied_for_scholarship: z.boolean().default(false),
    hostel_required: z.boolean().default(false),
    is_full_entry: z.boolean().default(false), // Toggle for UI
    is_paid: z.boolean().default(false), // Admin checkbox
});

export type AdmissionFormValues = z.infer<typeof admissionSchema>;
