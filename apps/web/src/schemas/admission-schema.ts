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
});

export type AdmissionFormValues = z.infer<typeof admissionSchema>;
