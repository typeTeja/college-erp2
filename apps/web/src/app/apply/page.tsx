'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { admissionApi } from '@/services/admission-api'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { useToast } from '@/hooks/use-toast'
import { useQuery } from '@tanstack/react-query'
import { api } from '@/utils/api'

interface Program {
    id: number
    name: string
}

export default function QuickApplyPage() {
    const router = useRouter()
    const { toast } = useToast()

    // Fetch programs
    const { data: programs } = useQuery<Program[]>({
        queryKey: ['programs'],
        queryFn: async () => {
            const response = await api.get('/programs')
            return response.data
        }
    })

    const [formData, setFormData] = useState({
        name: '',
        email: '',
        phone: '',
        gender: '',
        program_id: '',
        state: '',
        board: '',
        group_of_study: '',
    })

    const [isSubmitting, setIsSubmitting] = useState(false)

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setIsSubmitting(true)

        try {
            const response = await admissionApi.quickApplyV2({
                ...formData,
                program_id: parseInt(formData.program_id)
            })

            // Store credentials in session storage for success page
            sessionStorage.setItem('quickApplyResponse', JSON.stringify(response))

            toast({
                title: "Application Submitted!",
                description: response.message,
            })

            // Redirect to success page
            router.push('/apply/success')
        } catch (error: any) {
            console.error('Quick Apply error:', error)
            toast({
                title: "Error",
                description: error.response?.data?.detail || "Failed to submit application. Please try again.",
                variant: "destructive"
            })
        } finally {
            setIsSubmitting(false)
        }
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12 px-4 sm:px-6 lg:px-8">
            <Card className="max-w-2xl mx-auto shadow-xl">
                <CardHeader className="text-center bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-t-lg">
                    <CardTitle className="text-3xl font-bold">Quick Apply</CardTitle>
                    <CardDescription className="text-blue-100">
                        Start your journey with us. Fill in the basics to get started.
                    </CardDescription>
                </CardHeader>
                <CardContent className="mt-6">
                    <form onSubmit={handleSubmit} className="space-y-6">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div className="space-y-2">
                                <Label htmlFor="name">Full Name *</Label>
                                <Input
                                    id="name"
                                    placeholder="John Doe"
                                    required
                                    value={formData.name}
                                    onChange={e => setFormData({ ...formData, name: e.target.value })}
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
                                    placeholder="+91 98765 43210"
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
                            <Label>Course Applying For *</Label>
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
                                    placeholder="Telangana"
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

                        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                            <p className="text-sm text-blue-800">
                                <strong>What happens next?</strong><br />
                                After submission, you'll receive login credentials via email and SMS to access your student portal and complete the remaining application steps.
                            </p>
                        </div>

                        <Button
                            type="submit"
                            className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold py-3 text-lg"
                            disabled={isSubmitting}
                        >
                            {isSubmitting ? "Submitting..." : "Submit Application"}
                        </Button>
                    </form>
                </CardContent>
            </Card>
        </div>
    )
}
