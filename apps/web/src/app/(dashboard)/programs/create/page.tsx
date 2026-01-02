'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { programService } from '@/utils/program-service'
import { programService as programServiceUtils } from '@/utils/program-service' // Fixing potential name crash if needed
import { ProgramCreateData, ProgramType } from '@/types/program'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { useToast } from '@/hooks/use-toast'
import { ChevronRight, ChevronLeft, Check, AlertCircle } from 'lucide-react'
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"

// Mock Departments for now - In real app, fetch from department service
const DEPARTMENTS = [
    { id: 1, name: "Computer Science & Engineering" },
    { id: 2, name: "Electronics & Communication" },
    { id: 3, name: "Mechanical Engineering" },
    { id: 4, name: "Business Administration" },
    { id: 5, name: "Science & Humanities" }
]

export default function CreateProgramPage() {
    const router = useRouter()
    const { toast } = useToast()
    const createMutation = programService.useCreateProgram()
    const [step, setStep] = useState(1)

    const [formData, setFormData] = useState<ProgramCreateData>({
        name: '',
        code: '',
        program_type: ProgramType.UG,
        department_id: 0,
        duration_years: 4,
        description: '',
        eligibility_criteria: '',
        total_credits: 0
    })

    const handleNext = () => {
        if (step === 1) {
            if (!formData.name || !formData.code || !formData.department_id) {
                toast({ title: "Please fill all required fields", variant: "destructive" })
                return
            }
        }
        setStep(prev => prev + 1)
    }

    const handleBack = () => {
        setStep(prev => prev - 1)
    }

    const handleSubmit = async () => {
        try {
            await createMutation.mutateAsync(formData)
            toast({ title: "Program Created Successfully!" })
            router.push('/programs')
        } catch (error: any) {
            toast({
                title: "Error creating program",
                description: error.response?.data?.detail || "Something went wrong",
                variant: "destructive"
            })
        }
    }

    return (
        <div className="max-w-3xl mx-auto py-8">
            <div className="mb-8">
                <Link href="/programs" className="text-sm text-muted-foreground hover:underline mb-2 block">
                    &larr; Back to Programs
                </Link>
                <h1 className="text-3xl font-bold">Create New Program</h1>
                <p className="text-muted-foreground">Define a new academic program and its structure.</p>
            </div>

            {/* Steps Indicator */}
            <div className="flex items-center mb-8 space-x-4">
                {[1, 2, 3].map((s) => (
                    <div key={s} className="flex items-center">
                        <div className={`
                            flex items-center justify-center w-8 h-8 rounded-full border-2 
                            ${step === s ? 'border-primary bg-primary text-primary-foreground' :
                                step > s ? 'border-primary bg-primary text-primary-foreground' : 'border-muted-foreground text-muted-foreground'}
                        `}>
                            {step > s ? <Check className="h-4 w-4" /> : s}
                        </div>
                        {s < 3 && <div className={`w-12 h-1 ml-4 ${step > s ? 'bg-primary' : 'bg-muted'}`} />}
                    </div>
                ))}
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>
                        {step === 1 ? "Basic Information" :
                            step === 2 ? "Structure & Configuration" :
                                "Review & Create"}
                    </CardTitle>
                    <CardDescription>
                        {step === 1 ? "Enter the program details correctly." :
                            step === 2 ? "Define the duration and type." :
                                "Verify details before creating."}
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                    {step === 1 && (
                        <>
                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label>Program Name *</Label>
                                    <Input
                                        placeholder="e.g. B.Tech Computer Science"
                                        value={formData.name}
                                        onChange={e => setFormData({ ...formData, name: e.target.value })}
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label>Program Code *</Label>
                                    <Input
                                        placeholder="e.g. BTECH-CSE"
                                        value={formData.code}
                                        onChange={e => setFormData({ ...formData, code: e.target.value.toUpperCase() })}
                                    />
                                </div>
                            </div>
                            <div className="space-y-2">
                                <Label>Department *</Label>
                                <Select
                                    value={formData.department_id ? formData.department_id.toString() : ""}
                                    onValueChange={v => setFormData({ ...formData, department_id: parseInt(v) })}
                                >
                                    <SelectTrigger>
                                        <SelectValue placeholder="Select Department" />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {DEPARTMENTS.map(dept => (
                                            <SelectItem key={dept.id} value={dept.id.toString()}>
                                                {dept.name}
                                            </SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            </div>
                            <div className="space-y-2">
                                <Label>Description</Label>
                                <Textarea
                                    placeholder="Brief description of the program outcomes..."
                                    value={formData.description || ''}
                                    onChange={e => setFormData({ ...formData, description: e.target.value })}
                                />
                            </div>
                        </>
                    )}

                    {step === 2 && (
                        <>
                            <div className="space-y-2">
                                <Label>Program Type</Label>
                                <Select
                                    value={formData.program_type}
                                    onValueChange={v => setFormData({ ...formData, program_type: v as ProgramType })}
                                >
                                    <SelectTrigger>
                                        <SelectValue />
                                    </SelectTrigger>
                                    <SelectContent>
                                        {Object.values(ProgramType).map(t => (
                                            <SelectItem key={t} value={t}>{t}</SelectItem>
                                        ))}
                                    </SelectContent>
                                </Select>
                            </div>
                            <div className="grid grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label>Duration (Years)</Label>
                                    <Input
                                        type="number"
                                        min={1}
                                        max={6}
                                        value={formData.duration_years}
                                        onChange={e => setFormData({ ...formData, duration_years: parseInt(e.target.value) })}
                                    />
                                    <p className="text-xs text-muted-foreground">
                                        Standard: 4 for B.Tech, 2 for MBA/M.Tech
                                    </p>
                                </div>
                                <div className="space-y-2">
                                    <Label>Total Credits</Label>
                                    <Input
                                        type="number"
                                        placeholder="160"
                                        value={formData.total_credits || ''}
                                        onChange={e => setFormData({ ...formData, total_credits: parseInt(e.target.value) })}
                                    />
                                </div>
                            </div>
                            <div className="space-y-2">
                                <Label>Eligibility Criteria</Label>
                                <Textarea
                                    placeholder="e.g. 10+2 with 60% aggregate..."
                                    value={formData.eligibility_criteria || ''}
                                    onChange={e => setFormData({ ...formData, eligibility_criteria: e.target.value })}
                                />
                            </div>

                            <Alert>
                                <AlertCircle className="h-4 w-4" />
                                <AlertTitle>Automatic Structure Generation</AlertTitle>
                                <AlertDescription>
                                    Creating this program will automatically generate {formData.duration_years} Years
                                    and {formData.duration_years * 2} Semesters. You can customize them later.
                                </AlertDescription>
                            </Alert>
                        </>
                    )}

                    {step === 3 && (
                        <div className="space-y-4">
                            <div className="grid grid-cols-2 gap-4 text-sm">
                                <div>
                                    <span className="text-muted-foreground">Name:</span>
                                    <p className="font-medium">{formData.name}</p>
                                </div>
                                <div>
                                    <span className="text-muted-foreground">Code:</span>
                                    <p className="font-medium">{formData.code}</p>
                                </div>
                                <div>
                                    <span className="text-muted-foreground">Type:</span>
                                    <p className="font-medium">{formData.program_type}</p>
                                </div>
                                <div>
                                    <span className="text-muted-foreground">Duration:</span>
                                    <p className="font-medium">{formData.duration_years} Years</p>
                                </div>
                            </div>
                            <div className="bg-muted p-4 rounded-lg">
                                <h4 className="font-medium mb-2">Structure Preview</h4>
                                <ul className="list-disc list-inside text-sm space-y-1">
                                    {Array.from({ length: formData.duration_years }).map((_, i) => (
                                        <li key={i}>
                                            Year {i + 1}: Semester {i * 2 + 1}, Semester {i * 2 + 2}
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        </div>
                    )}
                </CardContent>
                <CardFooter className="flex justify-between">
                    <Button variant="outline" onClick={handleBack} disabled={step === 1}>
                        <ChevronLeft className="mr-2 h-4 w-4" /> Back
                    </Button>

                    {step < 3 ? (
                        <Button onClick={handleNext}>
                            Next <ChevronRight className="ml-2 h-4 w-4" />
                        </Button>
                    ) : (
                        <Button onClick={handleSubmit} disabled={createMutation.isPending}>
                            {createMutation.isPending ? "Creating..." : "Create Program"}
                        </Button>
                    )}
                </CardFooter>
            </Card>
        </div>
    )
}
