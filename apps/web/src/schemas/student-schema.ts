import { z } from 'zod';

export const studentSchema = z.object({
    first_name: z.string().min(2, "First name is required"),
    last_name: z.string().min(2, "Last name is required"),
    email: z.string().email("Invalid email address"),
    roll_number: z.string().min(1, "Roll number is required"),
    date_of_birth: z.string().refine((date) => !isNaN(Date.parse(date)), { message: "Invalid date" }),
    gender: z.enum(["MALE", "FEMALE", "OTHER"]),
    blood_group: z.string().optional(),
    contact_number: z.string().regex(/^\d{10}$/, { message: "Mobile number must be 10 digits" }),
    address: z.string().min(5, "Address is too short"),
    guardian_name: z.string().min(2, "Guardian name is required"),
    guardian_contact: z.string().regex(/^\d{10}$/, { message: "Guardian number must be 10 digits" }),
    admission_date: z.string().optional(),
    department_id: z.number().min(1, "Department is required"),
    semester: z.number().min(1, "Semester is required"),
});

export type StudentFormValues = z.infer<typeof studentSchema>;
