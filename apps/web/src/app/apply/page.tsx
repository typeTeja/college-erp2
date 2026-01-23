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

    // Fetch payment configuration
    const { data: paymentConfig } = useQuery({
        queryKey: ['payment-config'],
        queryFn: () => admissionApi.getPaymentConfig(),
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
        payment_mode: 'ONLINE', // Default to online
    })

    const [isSubmitting, setIsSubmitting] = useState(false)

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setIsSubmitting(true)

        try {
            // Call Quick Apply API
            const response = await admissionApi.quickApplyV2({
                name: formData.name,
                email: formData.email,
                phone: formData.phone,
                gender: formData.gender,
                program_id: parseInt(formData.program_id),
                state: formData.state,
                board: formData.board,
                group_of_study: formData.group_of_study
            })

            // Store credentials and payment info in session storage for success page
            const storageData = {
                ...response,
                payment_mode: formData.payment_mode,
                fee_amount: paymentConfig?.fee_amount || 0,
                fee_enabled: paymentConfig?.fee_enabled || false
            }
            console.log('Form Submit: Saving to session storage:', storageData)
            sessionStorage.setItem('quickApplyResponse', JSON.stringify(storageData))

            toast({
                title: "Application Submitted!",
                description: response.message,
            })

            console.log('Form Submit: Redirecting to success page')

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
                    <CardTitle className="text-3xl font-bold">Online Admission Form</CardTitle>
                    <CardDescription className="text-blue-100">
                        Start your journey with us. apply online in just a few simple steps.
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

                        {/* Payment Section */}
                        {paymentConfig?.fee_enabled && (
                            <div className="border-t pt-6 mt-6">
                                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
                                    <div className="flex items-center gap-2 mb-2">
                                        <svg className="h-5 w-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                                        </svg>
                                        <h3 className="font-semibold text-blue-900">Application Fee</h3>
                                    </div>
                                    <p className="text-2xl font-bold text-blue-600">₹{paymentConfig.fee_amount}</p>
                                </div>

                                <div className="space-y-2">
                                    <Label>Payment Mode *</Label>
                                    <Select
                                        value={formData.payment_mode}
                                        onValueChange={(v) => setFormData({ ...formData, payment_mode: v })}
                                    >
                                        <SelectTrigger>
                                            <SelectValue />
                                        </SelectTrigger>
                                        <SelectContent>
                                            {paymentConfig.online_enabled && (
                                                <SelectItem value="ONLINE">
                                                    <div className="flex items-center gap-2">
                                                        <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
                                                        </svg>
                                                        <span>Online Payment</span>
                                                    </div>
                                                </SelectItem>
                                            )}
                                            {paymentConfig.offline_enabled && (
                                                <SelectItem value="OFFLINE">
                                                    <div className="flex items-center gap-2">
                                                        <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
                                                        </svg>
                                                        <span>Offline Payment (Pay at College)</span>
                                                    </div>
                                                </SelectItem>
                                            )}
                                        </SelectContent>
                                    </Select>
                                    <p className="text-xs text-gray-600">
                                        {formData.payment_mode === 'ONLINE'
                                            ? "You will be redirected to payment gateway after submission"
                                            : "You can pay at the college office and upload proof later"}
                                    </p>
                                </div>
                            </div>
                        )}

                        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                            <p className="text-sm text-blue-800">
                                <strong>What happens next?</strong><br />
                                {paymentConfig?.fee_enabled
                                    ? `After submission, complete the payment of ₹${paymentConfig.fee_amount}. You'll receive login credentials via email and SMS after payment confirmation.`
                                    : "After submission, you'll receive login credentials via email and SMS to access your student portal and complete the remaining application steps."}
                            </p>
                        </div>

                        <Button
                            type="submit"
                            className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold py-3 text-lg"
                            disabled={isSubmitting}
                        >
                            {isSubmitting ? "Submitting..." : paymentConfig?.fee_enabled && formData.payment_mode === 'ONLINE' ? "Proceed to Payment" : "Submit Application"}
                        </Button>
                    </form>
                </CardContent>
            </Card>
        </div>
    )
}
