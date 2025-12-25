'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { admissionsService } from '@/utils/admissions-service'
import { programService } from '@/utils/program-service'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { useToast } from '@/hooks/use-toast'

export default function QuickApplyPage() {
    const router = useRouter()
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
        group_of_study: ''
    })

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        try {
            await quickApplyMutation.mutateAsync({
                ...formData,
                program_id: parseInt(formData.program_id)
            })
            toast({
                title: "Application Submitted!",
                description: "Your quick application has been received. Please proceed to payment.",
            })
            // Redirect to a success/payment page in a real app
            // router.push('/apply/status')
        } catch (error) {
            toast({
                title: "Error",
                description: "Failed to submit application. Please try again.",
                variant: "destructive"
            })
        }
    }

    return (
        <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
            <Card className="max-w-xl mx-auto">
                <CardHeader className="text-center">
                    <CardTitle className="text-3xl font-bold">Apply Now</CardTitle>
                    <CardDescription>
                        Start your journey with Regency College. Fill in the basics to get started.
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <Label htmlFor="name">Full Name</Label>
                                <Input
                                    id="name"
                                    placeholder="John Doe"
                                    required
                                    value={formData.name}
                                    onChange={e => setFormData({ ...formData, name: e.target.value })}
                                />
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="email">Email</Label>
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
                                <Label htmlFor="phone">Mobile Number</Label>
                                <Input
                                    id="phone"
                                    placeholder="+91 98765 43210"
                                    required
                                    value={formData.phone}
                                    onChange={e => setFormData({ ...formData, phone: e.target.value })}
                                />
                            </div>
                            <div className="space-y-2">
                                <Label>Gender</Label>
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
                            <Label>Course Applying For</Label>
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
                                <Label htmlFor="state">State</Label>
                                <Input
                                    id="state"
                                    placeholder="Telangana"
                                    required
                                    value={formData.state}
                                    onChange={e => setFormData({ ...formData, state: e.target.value })}
                                />
                            </div>
                            <div className="space-y-2">
                                <Label htmlFor="board">Board (10+2)</Label>
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
                            <Label htmlFor="group">Group of Study</Label>
                            <Input
                                id="group"
                                placeholder="MPC / BiPC / CEC"
                                required
                                value={formData.group_of_study}
                                onChange={e => setFormData({ ...formData, group_of_study: e.target.value })}
                            />
                        </div>

                        <Button
                            type="submit"
                            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3"
                            disabled={quickApplyMutation.isPending}
                        >
                            {quickApplyMutation.isPending ? "Submitting..." : "Apply Now & Proceed to Payment"}
                        </Button>
                    </form>
                </CardContent>
            </Card>
        </div>
    )
}
