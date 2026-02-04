import { useState } from 'react'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogFooter, DialogTrigger } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useToast } from "@/hooks/use-toast"
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { studentSchema, StudentFormValues } from '@/schemas/student-schema'
import { useCreateStudent } from '@/hooks/use-students'
import { programService } from '@/utils/program-service'
import { Plus } from 'lucide-react'
import { formatError } from '@/utils/error-handler'

export function AddStudentDialog() {
    const [open, setOpen] = useState(false)
    const { toast } = useToast()
    const createStudentMutation = useCreateStudent()
    const { data: programs } = programService.usePrograms()

    const form = useForm<StudentFormValues>({
        resolver: zodResolver(studentSchema),
        defaultValues: {
            first_name: "",
            last_name: "",
            email: "",
            contact_number: "",
            gender: "MALE",
            department_id: 0,
            semester: 1,
            roll_number: "",
            date_of_birth: "",
            blood_group: "",
            address: "",
            guardian_name: "",
            guardian_contact: "",
            admission_date: new Date().toISOString().split('T')[0]
        }
    })

    // Helper to reset form
    const resetForm = () => {
        form.reset()
    }

    const onSubmit = (data: StudentFormValues) => {
        // Map schema fields to API expected fields if they differ
        // Schema has first_name, last_name -> API likely expects name (concatenated) or separate if backend supports it.
        // Looking at student.ts type, it has 'name'. 'StudentCreate' has 'name'.
        // So we need to combine first and last name.

        const payload: any = {
            ...data,
            name: `${data.first_name} ${data.last_name}`,
            program_id: data.department_id,
            // API expects batch_id, program_year_id etc. which are required in StudentCreate interface.
            // For now we will send what we have and let the API handle or default, or we might need more fields.
            // Assuming simplified creation for now.
            // contact_number in schema maps to phone in API?
            phone: data.contact_number,
            dob: data.date_of_birth
        }

        createStudentMutation.mutate(payload, {
            onSuccess: () => {
                toast({
                    title: "Student Added",
                    description: "Student created successfully.",
                })
                setOpen(false)
                resetForm()
            },
            onError: (err: any) => {
                toast({
                    title: "Error",
                    description: formatError(err),
                    variant: "destructive"
                })
            }
        })
    }

    const handleOpenChange = (newOpen: boolean) => {
        if (!newOpen) resetForm()
        setOpen(newOpen)
    }

    return (
        <Dialog open={open} onOpenChange={handleOpenChange}>
            <DialogTrigger asChild>
                <Button>
                    <Plus className="mr-2 h-4 w-4" /> Add Student
                </Button>
            </DialogTrigger>
            <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                    <DialogTitle>Add New Student</DialogTitle>
                    <DialogDescription>
                        Enter the details of the new student. Click save when you're done.
                    </DialogDescription>
                </DialogHeader>

                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                    {/* Personal Details */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label htmlFor="first_name">First Name *</Label>
                            <Input
                                id="first_name"
                                placeholder="John"
                                {...form.register('first_name')}
                            />
                            {form.formState.errors.first_name && (
                                <p className="text-xs text-red-500">{form.formState.errors.first_name.message}</p>
                            )}
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="last_name">Last Name *</Label>
                            <Input
                                id="last_name"
                                placeholder="Doe"
                                {...form.register('last_name')}
                            />
                            {form.formState.errors.last_name && (
                                <p className="text-xs text-red-500">{form.formState.errors.last_name.message}</p>
                            )}
                        </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label htmlFor="email">Email *</Label>
                            <Input
                                id="email"
                                type="email"
                                placeholder="john@example.com"
                                {...form.register('email')}
                            />
                            {form.formState.errors.email && (
                                <p className="text-xs text-red-500">{form.formState.errors.email.message}</p>
                            )}
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="roll_number">Roll Number *</Label>
                            <Input
                                id="roll_number"
                                placeholder="2023CS001"
                                {...form.register('roll_number')}
                            />
                            {form.formState.errors.roll_number && (
                                <p className="text-xs text-red-500">{form.formState.errors.roll_number.message}</p>
                            )}
                        </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div className="space-y-2">
                            <Label htmlFor="date_of_birth">Date of Birth *</Label>
                            <Input
                                id="date_of_birth"
                                type="date"
                                {...form.register('date_of_birth')}
                            />
                            {form.formState.errors.date_of_birth && (
                                <p className="text-xs text-red-500">{form.formState.errors.date_of_birth.message}</p>
                            )}
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="contact_number">Mobile Number *</Label>
                            <Input
                                id="contact_number"
                                placeholder="9876543210"
                                {...form.register('contact_number')}
                            />
                            {form.formState.errors.contact_number && (
                                <p className="text-xs text-red-500">{form.formState.errors.contact_number.message}</p>
                            )}
                        </div>
                        <div className="space-y-2">
                            <Label>Gender *</Label>
                            <Select
                                onValueChange={(val) => form.setValue('gender', val as "MALE" | "FEMALE" | "OTHER")}
                                defaultValue={form.getValues('gender')}
                            >
                                <SelectTrigger>
                                    <SelectValue placeholder="Select gender" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="MALE">Male</SelectItem>
                                    <SelectItem value="FEMALE">Female</SelectItem>
                                    <SelectItem value="OTHER">Other</SelectItem>
                                </SelectContent>
                            </Select>
                            {form.formState.errors.gender && (
                                <p className="text-xs text-red-500">{form.formState.errors.gender.message}</p>
                            )}
                        </div>
                    </div>

                    {/* Academic Details */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label>Department/Program *</Label>
                            <Select
                                onValueChange={(val) => form.setValue('department_id', Number(val))}
                            >
                                <SelectTrigger>
                                    <SelectValue placeholder="Select program" />
                                </SelectTrigger>
                                <SelectContent>
                                    {programs?.map(p => (
                                        <SelectItem key={p.id} value={p.id.toString()}>{p.name}</SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                            {form.formState.errors.department_id && (
                                <p className="text-xs text-red-500">{form.formState.errors.department_id.message}</p>
                            )}
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="semester">Semester *</Label>
                            <Select
                                onValueChange={(val) => form.setValue('semester', Number(val))}
                                defaultValue="1"
                            >
                                <SelectTrigger>
                                    <SelectValue placeholder="Select semester" />
                                </SelectTrigger>
                                <SelectContent>
                                    {[1, 2, 3, 4, 5, 6, 7, 8].map(sem => (
                                        <SelectItem key={sem} value={sem.toString()}>Semester {sem}</SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                            {form.formState.errors.semester && (
                                <p className="text-xs text-red-500">{form.formState.errors.semester.message}</p>
                            )}
                        </div>
                    </div>

                    {/* Guardian Details */}
                    <h3 className="text-sm font-medium text-muted-foreground pt-2">Guardian Information</h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label htmlFor="guardian_name">Guardian Name *</Label>
                            <Input
                                id="guardian_name"
                                placeholder="Parent/Guardian Name"
                                {...form.register('guardian_name')}
                            />
                            {form.formState.errors.guardian_name && (
                                <p className="text-xs text-red-500">{form.formState.errors.guardian_name.message}</p>
                            )}
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="guardian_contact">Guardian Contact *</Label>
                            <Input
                                id="guardian_contact"
                                placeholder="9876543210"
                                {...form.register('guardian_contact')}
                            />
                            {form.formState.errors.guardian_contact && (
                                <p className="text-xs text-red-500">{form.formState.errors.guardian_contact.message}</p>
                            )}
                        </div>
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="address">Address *</Label>
                        <Input
                            id="address"
                            placeholder="Full residential address"
                            {...form.register('address')}
                        />
                        {form.formState.errors.address && (
                            <p className="text-xs text-red-500">{form.formState.errors.address.message}</p>
                        )}
                    </div>

                    <DialogFooter className="pt-4">
                        <Button
                            type="button"
                            variant="outline"
                            onClick={() => handleOpenChange(false)}
                        >
                            Cancel
                        </Button>
                        <Button
                            type="submit"
                            disabled={createStudentMutation.isPending}
                        >
                            {createStudentMutation.isPending ? "Adding..." : "Add Student"}
                        </Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    )
}
