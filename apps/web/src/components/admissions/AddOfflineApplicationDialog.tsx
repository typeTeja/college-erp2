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
    const quickApplyMutation = admissionsService.useQuickApply()

    const form = useForm<AdmissionFormValues>({
        resolver: zodResolver(admissionSchema),
        defaultValues: {
            student_name: "",
            email: "",
            phone: "",
            gender: "MALE",
            program_id: 0,
            state: "",
            board: "",
            group_of_study: "",
            fee_mode: "OFFLINE",
            status: "PENDING",
            documents_submitted: false,
            fee_paid: false
        }
    })

    const onSubmit = (data: AdmissionFormValues) => {
        quickApplyMutation.mutate({
            ...data,
            name: data.student_name, // Map back to API expected format
            program_id: Number(data.course_id)
        }, {
            onSuccess: (res: any) => {
                toast({
                    title: "Application Created!",
                    description: `Application ${res.application_number} created successfully.`,
                })
                form.reset()
                onOpenChange(false)
            },
            onError: (err: any) => {
                toast({
                    title: "Error",
                    description: err.response?.data?.detail || "Failed to create application.",
                    variant: "destructive"
                })
            }
        })
    }

    // Reset form when dialog closes
    const handleOpenChange = (open: boolean) => {
        if (!open) form.reset()
        onOpenChange(open)
    }

    return (
        <Dialog open={open} onOpenChange={handleOpenChange}>
            <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                    <DialogTitle>Add Offline Application</DialogTitle>
                    <DialogDescription>
                        Create an application for a walk-in student who applied at the office.
                    </DialogDescription>
                </DialogHeader>

                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label htmlFor="student_name">Full Name *</Label>
                            <Input
                                id="student_name"
                                placeholder="John Doe"
                                {...form.register('student_name')}
                            />
                            {form.formState.errors.student_name && (
                                <p className="text-xs text-red-500">{form.formState.errors.student_name.message}</p>
                            )}
                        </div>
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
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label htmlFor="phone">Mobile Number *</Label>
                            <Input
                                id="phone"
                                placeholder="9876543210"
                                {...form.register('phone')}
                            />
                            {form.formState.errors.phone && (
                                <p className="text-xs text-red-500">{form.formState.errors.phone.message}</p>
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

                    <div className="space-y-2">
                        <Label>Program *</Label>
                        <Select
                            onValueChange={(val) => form.setValue('course_id', Number(val))}
                            defaultValue={form.getValues('course_id')?.toString() || undefined}
                        >
                            <SelectTrigger>
                                <SelectValue placeholder="Select a program" />
                            </SelectTrigger>
                            <SelectContent>
                                {programs?.map(p => (
                                    <SelectItem key={p.id} value={p.id.toString()}>{p.name}</SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                        {form.formState.errors.course_id && (
                            <p className="text-xs text-red-500">{form.formState.errors.course_id.message}</p>
                        )}
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label htmlFor="state">State *</Label>
                            <Input
                                id="state"
                                placeholder="Karnataka"
                                {...form.register('state')}
                            />
                            {form.formState.errors.state && (
                                <p className="text-xs text-red-500">{form.formState.errors.state.message}</p>
                            )}
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="board">Board (10+2) *</Label>
                            <Input
                                id="board"
                                placeholder="CBSE / State Board"
                                {...form.register('board')}
                            />
                            {form.formState.errors.board && (
                                <p className="text-xs text-red-500">{form.formState.errors.board.message}</p>
                            )}
                        </div>
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="group_of_study">Group of Study *</Label>
                        <Input
                            id="group_of_study"
                            placeholder="MPC / BiPC / CEC"
                            {...form.register('group_of_study')}
                        />
                        {form.formState.errors.group_of_study && (
                            <p className="text-xs text-red-500">{form.formState.errors.group_of_study.message}</p>
                        )}
                    </div>

                    <div className="space-y-2">
                        <Label>Payment Mode *</Label>
                        <RadioGroup
                            onValueChange={(val) => form.setValue('fee_mode', val as "ONLINE" | "OFFLINE")}
                            defaultValue={form.getValues('fee_mode')}
                        >
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value="ONLINE" id="online" />
                                <Label htmlFor="online" className="font-normal cursor-pointer">Online Payment</Label>
                            </div>
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value="OFFLINE" id="offline" />
                                <Label htmlFor="offline" className="font-normal cursor-pointer">Offline Payment (Pay at College)</Label>
                            </div>
                        </RadioGroup>
                        <p className="text-xs text-muted-foreground">
                            {form.watch('fee_mode') === 'ONLINE'
                                ? "Student will receive payment link via email"
                                : "Student can pay at the college office"}
                        </p>
                    </div>

                    <DialogFooter>
                        <Button
                            type="button"
                            variant="outline"
                            onClick={() => handleOpenChange(false)}
                        >
                            Cancel
                        </Button>
                        <Button
                            type="submit"
                            disabled={quickApplyMutation.isPending}
                        >
                            {quickApplyMutation.isPending ? "Creating..." : "Create Application"}
                        </Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    )
}
