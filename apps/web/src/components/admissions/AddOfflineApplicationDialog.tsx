'use client'

import { useState } from 'react'
import { admissionsService } from '@/utils/admissions-service'
import { programService } from '@/utils/program-service'
import { FeeMode } from '@/types/admissions'
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { useToast } from '@/hooks/use-toast'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { admissionSchema, AdmissionFormValues } from '@/schemas/admission-schema'
// Removed missing form components imports

interface AddOfflineApplicationDialogProps {
    open: boolean
    onOpenChange: (open: boolean) => void
}

export default function AddOfflineApplicationDialog({ open, onOpenChange }: AddOfflineApplicationDialogProps) {
    const { toast } = useToast()
    const { data: programs } = programService.usePrograms()
    const createMutation = admissionsService.useCreateOfflineApplication()
    const [isFullEntry, setIsFullEntry] = useState(false)

    const form = useForm<AdmissionFormValues>({
        resolver: zodResolver(admissionSchema),
        defaultValues: {
            student_name: "",
            email: "",
            phone: "",
            gender: "MALE",
            course_id: 0,
            state: "",
            board: "",
            group_of_study: "",
            fee_mode: FeeMode.OFFLINE,
            status: "PENDING",
            documents_submitted: false,
            fee_paid: false,
            // Full entry defaults
            is_full_entry: false,
            is_paid: false,
            applied_for_scholarship: false,
            hostel_required: false,
        }
    })

    const onSubmit = (data: AdmissionFormValues) => {
        createMutation.mutate({
            ...data,
            name: data.student_name, // Map back to API expected format
            program_id: Number(data.course_id),
            is_full_entry: isFullEntry // Explicitly pass toggle state
        }, {
            onSuccess: (res: any) => {
                toast({
                    title: "Application Created!",
                    description: `Application ${res.application_number} created successfully.`,
                })
                form.reset()
                setIsFullEntry(false)
                onOpenChange(false)
            },
            onError: (err: any) => {
                let errorMessage = "Failed to create application.";
                try {
                    if (err.response?.data?.detail) {
                        const detail = err.response.data.detail;
                        if (typeof detail === 'string') {
                            errorMessage = detail;
                        } else if (Array.isArray(detail)) {
                            errorMessage = detail.map((e: any) => e.msg).join(", ");
                        } else if (typeof detail === 'object') {
                            errorMessage = JSON.stringify(detail);
                        } else {
                            errorMessage = String(detail);
                        }
                    }
                } catch (e) {
                    console.error("Error parsing API error", e);
                    errorMessage = "An unexpected error occurred while creating the application.";
                }
                
                toast({
                    title: "Error",
                    description: errorMessage,
                    variant: "destructive"
                })
            }
        })
    }

    // Reset form when dialog closes
    const handleOpenChange = (open: boolean) => {
        if (!open) {
            form.reset()
            setIsFullEntry(false)
        }
        onOpenChange(open)
    }

    return (
        <Dialog open={open} onOpenChange={handleOpenChange}>
            <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                    <DialogTitle>Add Offline Application</DialogTitle>
                    <DialogDescription>
                        Create an application for a walk-in student. Toggle "Full Entry" to fill all details now.
                    </DialogDescription>
                </DialogHeader>

                <div className="flex items-center space-x-2 py-2">
                    <input
                        type="checkbox"
                        id="fullEntry"
                        className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        checked={isFullEntry}
                        onChange={(e) => {
                            setIsFullEntry(e.target.checked)
                            form.setValue('is_full_entry', e.target.checked)
                        }}
                    />
                    <Label htmlFor="fullEntry" className="font-medium text-blue-700 cursor-pointer">
                        Enable Full Entry Mode (Stage 1 + Stage 2)
                    </Label>
                </div>

                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                    {/* Basic Details (Always Visible) */}
                    <div className="space-y-4 border rounded-lg p-4 bg-gray-50">
                        <h3 className="font-semibold text-gray-700">Basic Information</h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <Label htmlFor="student_name">Full Name *</Label>
                                <Input id="student_name" placeholder="John Doe" {...form.register('student_name')} />
                                {form.formState.errors.student_name && <p className="text-xs text-red-500">{form.formState.errors.student_name.message}</p>}
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="email">Email *</Label>
                                <Input id="email" type="email" placeholder="john@example.com" {...form.register('email')} />
                                {form.formState.errors.email && <p className="text-xs text-red-500">{form.formState.errors.email.message}</p>}
                            </div>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <Label htmlFor="phone">Mobile Number *</Label>
                                <Input id="phone" placeholder="9876543210" {...form.register('phone')} />
                                {form.formState.errors.phone && <p className="text-xs text-red-500">{form.formState.errors.phone.message}</p>}
                            </div>
                            <div className="space-y-2">
                                <Label>Gender *</Label>
                                <Select onValueChange={(val) => form.setValue('gender', val as any)} defaultValue="MALE">
                                    <SelectTrigger>
                                        <SelectValue placeholder="Select gender" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        <SelectItem value="MALE">Male</SelectItem>
                                        <SelectItem value="FEMALE">Female</SelectItem>
                                        <SelectItem value="OTHER">Other</SelectItem>
                                    </SelectContent>
                                </Select>
                            </div>
                        </div>

                        <div className="space-y-2">
                            <Label>Program *</Label>
                            <Select onValueChange={(val) => form.setValue('course_id', Number(val))}>
                                <SelectTrigger>
                                    <SelectValue placeholder="Select a program" />
                                </SelectTrigger>
                                <SelectContent>
                                    {programs?.map(p => (
                                        <SelectItem key={p.id} value={p.id.toString()}>{p.name}</SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                            {form.formState.errors.course_id && <p className="text-xs text-red-500">{form.formState.errors.course_id.message}</p>}
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div className="space-y-2">
                                <Label htmlFor="state">State *</Label>
                                <Input id="state" placeholder="Karnataka" {...form.register('state')} />
                                {form.formState.errors.state && <p className="text-xs text-red-500">{form.formState.errors.state.message}</p>}
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="board">Board (10+2) *</Label>
                                <Input id="board" placeholder="CBSE" {...form.register('board')} />
                                {form.formState.errors.board && <p className="text-xs text-red-500">{form.formState.errors.board.message}</p>}
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="group_of_study">Group *</Label>
                                <Input id="group_of_study" placeholder="MPC" {...form.register('group_of_study')} />
                                {form.formState.errors.group_of_study && <p className="text-xs text-red-500">{form.formState.errors.group_of_study.message}</p>}
                            </div>
                        </div>
                    </div>

                    {/* Extended Details (Only Visible in Full Entry Mode) */}
                    {isFullEntry && (
                        <div className="space-y-4 border rounded-lg p-4 bg-blue-50">
                            <h3 className="font-semibold text-blue-700">Full Admission Details</h3>
                            
                            {/* Personal & Family */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label htmlFor="aadhaar_number">Aadhaar Number</Label>
                                    <Input id="aadhaar_number" placeholder="1234 5678 9012" {...form.register('aadhaar_number')} />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="father_name">Father's Name</Label>
                                    <Input id="father_name" placeholder="Parent Name" {...form.register('father_name')} />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="father_phone">Father's Phone</Label>
                                    <Input id="father_phone" placeholder="Parent Mobile" {...form.register('father_phone')} />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="previous_marks_percentage">Previous Marks %</Label>
                                    <Input id="previous_marks_percentage" type="number" step="0.01" placeholder="85.5" {...form.register('previous_marks_percentage')} />
                                </div>
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="address">Address</Label>
                                <Input id="address" placeholder="Full Address" {...form.register('address')} />
                            </div>

                            <div className="flex gap-6 pt-2">
                                <div className="flex items-center space-x-2">
                                    <input type="checkbox" id="scholarship" className="h-4 w-4 text-blue-600 rounded" {...form.register('applied_for_scholarship')} />
                                    <Label htmlFor="scholarship" className="font-normal cursor-pointer">Apply for Scholarship</Label>
                                </div>
                                <div className="flex items-center space-x-2">
                                    <input type="checkbox" id="hostel" className="h-4 w-4 text-blue-600 rounded" {...form.register('hostel_required')} />
                                    <Label htmlFor="hostel" className="font-normal cursor-pointer">Hostel Required</Label>
                                </div>
                            </div>
                        </div>
                    )}

                    <div className="space-y-2 p-4 border rounded-lg">
                        <Label>Payment & Status</Label>
                        <RadioGroup
                            onValueChange={(val) => form.setValue('fee_mode', val as FeeMode)}
                            defaultValue="OFFLINE"
                            className="flex gap-4"
                        >
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value="OFFLINE" id="offline" />
                                <Label htmlFor="offline" className="cursor-pointer">Offline (Cash/DD)</Label>
                            </div>
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value="ONLINE" id="online" />
                                <Label htmlFor="online" className="cursor-pointer">Online Link</Label>
                            </div>
                        </RadioGroup>
                        
                        {isFullEntry && form.watch('fee_mode') === 'OFFLINE' && (
                            <div className="mt-4 flex items-center space-x-2 bg-green-50 p-2 rounded">
                                <input 
                                    type="checkbox" 
                                    id="is_paid" 
                                    className="h-4 w-4 text-green-600 rounded" 
                                    {...form.register('is_paid')}
                                />
                                <Label htmlFor="is_paid" className="font-medium text-green-700 cursor-pointer">
                                    Mark Application Fee as PAID immediately
                                </Label>
                            </div>
                        )}
                    </div>

                    <DialogFooter>
                        <Button type="button" variant="outline" onClick={() => handleOpenChange(false)}>Cancel</Button>
                        <Button type="submit" disabled={createMutation.isPending}>
                            {createMutation.isPending ? "Creating..." : isFullEntry ? "Create Full Application" : "Quick Add"}
                        </Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    )
}
