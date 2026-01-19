import { z } from 'zod';

export const staffSchema = z.object({
    name: z.string().min(2, { message: "Name must be at least 2 characters" }),
    email: z.string().email({ message: "Invalid email address" }),
    mobile: z.string().regex(/^\d{10}$/, { message: "Mobile number must be 10 digits" }),
    department: z.string().optional(),
    designation: z.string().min(2, { message: "Designation is required" }),
    join_date: z.string().refine((date) => !isNaN(Date.parse(date)), { message: "Invalid date" }),
    shift_id: z.number().optional(),
});

export type StaffFormValues = z.infer<typeof staffSchema>;
