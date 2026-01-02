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

interface AddOfflineApplicationDialogProps {
    open: boolean
    onOpenChange: (open: boolean) => void
}

export default function AddOfflineApplicationDialog({ open, onOpenChange }: AddOfflineApplicationDialogProps) {
    const { toast } = useToast()
    const { data: programs } = programService.usePrograms()
    const quickApplyMutation = admissionsService.useQuickApply()

    const [formData, setFormData] = useState({
        name: '',
        email: '',
        phone: '',
        gender: '',
        program_id: '',
        state: '',
        board: '',
        group_of_study: '',
        fee_mode: FeeMode.OFFLINE // Default to offline for walk-in applications
    })

    const resetForm = () => {
        setFormData({
            name: '',
            email: '',
            phone: '',
            gender: '',
            program_id: '',
            state: '',
            board: '',
            group_of_study: '',
            fee_mode: FeeMode.OFFLINE
        })
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()

        // Validation
        if (!formData.name || !formData.email || !formData.phone || !formData.gender ||
            !formData.program_id || !formData.state || !formData.board || !formData.group_of_study) {
            toast({
                title: "Validation Error",
                description: "Please fill in all required fields",
                variant: "destructive"
            })
            return
        }

        try {
            const application = await quickApplyMutation.mutateAsync({
                ...formData,
                program_id: parseInt(formData.program_id)
            })

            toast({
                title: "Application Created!",
                description: `Application ${application.application_number} created successfully.`,
            })

            resetForm()
            onOpenChange(false)
        } catch (error: any) {
            toast({
                title: "Error",
                description: error.response?.data?.detail || "Failed to create application. Please try again.",
                variant: "destructive"
            })
        }
    }

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                    <DialogTitle>Add Offline Application</DialogTitle>
                    <DialogDescription>
                        Create an application for a walk-in student who applied at the office.
                    </DialogDescription>
                </DialogHeader>

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label htmlFor="name">Full Name *</Label>
                            <Input
                                id="name"
                                placeholder="John Doe"
                                required
                                value={formData.name}
                                onChange={e => setFormData({ ...formData, name: e.target.value })}
                                autoFocus
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="email">Email *</Label>
                            <Input
                                id="email"
                                type="email"
                                placeholder="john@example.com"
                                required
                                value={formData.email}
                                onChange={e => setFormData({ ...formData, email: e.target.value })}
                            />
                        </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label htmlFor="phone">Mobile Number *</Label>
                            <Input
                                id="phone"
                                placeholder="9876543210"
                                required
                                value={formData.phone}
                                onChange={e => setFormData({ ...formData, phone: e.target.value })}
                            />
                        </div>
                        <div className="space-y-2">
                            <Label>Gender *</Label>
                            <Select onValueChange={v => setFormData({ ...formData, gender: v })} required>
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
                        <Select onValueChange={v => setFormData({ ...formData, program_id: v })} required>
                            <SelectTrigger>
                                <SelectValue placeholder="Select a program" />
                            </SelectTrigger>
                            <SelectContent>
                                {programs?.map(p => (
                                    <SelectItem key={p.id} value={p.id.toString()}>{p.name}</SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label htmlFor="state">State *</Label>
                            <Input
                                id="state"
                                placeholder="Karnataka"
                                required
                                value={formData.state}
                                onChange={e => setFormData({ ...formData, state: e.target.value })}
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="board">Board (10+2) *</Label>
                            <Input
                                id="board"
                                placeholder="CBSE / State Board"
                                required
                                value={formData.board}
                                onChange={e => setFormData({ ...formData, board: e.target.value })}
                            />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="group">Group of Study *</Label>
                        <Input
                            id="group"
                            placeholder="MPC / BiPC / CEC"
                            required
                            value={formData.group_of_study}
                            onChange={e => setFormData({ ...formData, group_of_study: e.target.value })}
                        />
                    </div>

                    <div className="space-y-2">
                        <Label>Payment Mode *</Label>
                        <RadioGroup
                            value={formData.fee_mode}
                            onValueChange={(v) => setFormData({ ...formData, fee_mode: v as FeeMode })}
                        >
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value={FeeMode.ONLINE} id="online" />
                                <Label htmlFor="online" className="font-normal cursor-pointer">
                                    Online Payment
                                </Label>
                            </div>
                            <div className="flex items-center space-x-2">
                                <RadioGroupItem value={FeeMode.OFFLINE} id="offline" />
                                <Label htmlFor="offline" className="font-normal cursor-pointer">
                                    Offline Payment (Pay at College)
                                </Label>
                            </div>
                        </RadioGroup>
                        <p className="text-xs text-muted-foreground">
                            {formData.fee_mode === FeeMode.ONLINE
                                ? "Student will receive payment link via email"
                                : "Student can pay at the college office"}
                        </p>
                    </div>

                    <DialogFooter>
                        <Button
                            type="button"
                            variant="outline"
                            onClick={() => {
                                resetForm()
                                onOpenChange(false)
                            }}
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
