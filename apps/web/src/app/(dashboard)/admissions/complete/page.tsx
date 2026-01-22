'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { admissionApi } from '@/services/admission-api'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Checkbox } from '@/components/ui/checkbox'
import { useToast } from '@/hooks/use-toast'
import { ArrowLeft, CheckCircle, Loader2 } from 'lucide-react'
import Link from 'next/link'

export default function CompleteApplicationPage() {
    const router = useRouter()
    const { toast } = useToast()
    const queryClient = useQueryClient()

    // Fetch current application
    const { data: application, isLoading } = useQuery({
        queryKey: ['my-application'],
        queryFn: () => admissionApi.getMyApplication(),
    })

    const [formData, setFormData] = useState({
        aadhaar_number: '',
        father_name: '',
        father_phone: '',
        address: '',
        previous_marks_percentage: '',
        applied_for_scholarship: false,
        hostel_required: false,
    })

    // Complete application mutation
    const completeMutation = useMutation({
        mutationFn: (data: any) => admissionApi.completeMyApplication(data),
        onSuccess: () => {
            toast({
                title: "Application Completed!",
                description: "Your application has been submitted successfully.",
            })
            queryClient.invalidateQueries({ queryKey: ['my-application'] })
            router.push('/dashboard')
        },
        onError: (error: any) => {
            toast({
                title: "Error",
                description: error.response?.data?.detail || "Failed to complete application",
                variant: "destructive"
            })
        }
    })

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()

        const submitData = {
            ...formData,
            previous_marks_percentage: formData.previous_marks_percentage
                ? parseFloat(formData.previous_marks_percentage)
                : undefined
        }

        completeMutation.mutate(submitData)
    }

    if (isLoading) {
        return (
            <div className="flex items-center justify-center min-h-[400px]">
                <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
            </div>
        )
    }

    if (!application) {
        return (
            <Card className="max-w-2xl mx-auto mt-8">
                <CardContent className="pt-6 text-center">
                    <p className="text-gray-600">No application found. Please submit a Quick Apply form first.</p>
                    <Link href="/apply">
                        <Button className="mt-4">Go to Quick Apply</Button>
                    </Link>
                </CardContent>
            </Card>
        )
    }

    // Check if already completed
    if (application.status === 'FORM_COMPLETED' || application.status === 'PENDING_PAYMENT') {
        return (
            <Card className="max-w-2xl mx-auto mt-8">
                <CardHeader className="text-center">
                    <CheckCircle className="h-16 w-16 text-green-600 mx-auto mb-4" />
                    <CardTitle>Application Already Completed</CardTitle>
                    <CardDescription>
                        Your application has been completed and is being processed.
                    </CardDescription>
                </CardHeader>
                <CardContent className="text-center">
                    <Link href="/dashboard">
                        <Button>Back to Dashboard</Button>
                    </Link>
                </CardContent>
            </Card>
        )
    }

    return (
        <div className="max-w-4xl mx-auto py-8 px-4">
            <Link href="/dashboard">
                <Button variant="ghost" className="mb-6">
                    <ArrowLeft className="h-4 w-4 mr-2" />
                    Back to Dashboard
                </Button>
            </Link>

            <Card>
                <CardHeader className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-t-lg">
                    <CardTitle className="text-2xl">Complete Your Application</CardTitle>
                    <CardDescription className="text-blue-100">
                        Application Number: <strong>{application.application_number}</strong>
                    </CardDescription>
                </CardHeader>
                <CardContent className="mt-6">
                    <form onSubmit={handleSubmit} className="space-y-6">
                        {/* Personal Details Section */}
                        <div className="space-y-4">
                            <h3 className="text-lg font-semibold text-gray-900 border-b pb-2">
                                Personal Details
                            </h3>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div className="space-y-2">
                                    <Label htmlFor="aadhaar">Aadhaar Number *</Label>
                                    <Input
                                        id="aadhaar"
                                        placeholder="XXXX XXXX XXXX"
                                        required
                                        value={formData.aadhaar_number}
                                        onChange={e => setFormData({ ...formData, aadhaar_number: e.target.value })}
                                        maxLength={12}
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="father_name">Father's Name *</Label>
                                    <Input
                                        id="father_name"
                                        placeholder="Father's full name"
                                        required
                                        value={formData.father_name}
                                        onChange={e => setFormData({ ...formData, father_name: e.target.value })}
                                    />
                                </div>
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="father_phone">Father's Phone Number *</Label>
                                <Input
                                    id="father_phone"
                                    placeholder="+91 98765 43210"
                                    required
                                    value={formData.father_phone}
                                    onChange={e => setFormData({ ...formData, father_phone: e.target.value })}
                                />
                            </div>

                            <div className="space-y-2">
                                <Label htmlFor="address">Permanent Address *</Label>
                                <textarea
                                    id="address"
                                    className="w-full min-h-[100px] px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    placeholder="Enter your complete address"
                                    required
                                    value={formData.address}
                                    onChange={e => setFormData({ ...formData, address: e.target.value })}
                                />
                            </div>
                        </div>

                        {/* Academic Details Section */}
                        <div className="space-y-4">
                            <h3 className="text-lg font-semibold text-gray-900 border-b pb-2">
                                Academic Details
                            </h3>

                            <div className="space-y-2">
                                <Label htmlFor="marks">Previous Marks Percentage</Label>
                                <Input
                                    id="marks"
                                    type="number"
                                    step="0.01"
                                    min="0"
                                    max="100"
                                    placeholder="85.5"
                                    value={formData.previous_marks_percentage}
                                    onChange={e => setFormData({ ...formData, previous_marks_percentage: e.target.value })}
                                />
                                <p className="text-xs text-gray-500">Enter your 10+2 or equivalent marks percentage</p>
                            </div>
                        </div>

                        {/* Additional Preferences Section */}
                        <div className="space-y-4">
                            <h3 className="text-lg font-semibold text-gray-900 border-b pb-2">
                                Additional Preferences
                            </h3>

                            <div className="space-y-3">
                                <div className="flex items-center space-x-2">
                                    <Checkbox
                                        id="scholarship"
                                        checked={formData.applied_for_scholarship}
                                        onCheckedChange={(checked) =>
                                            setFormData({ ...formData, applied_for_scholarship: checked as boolean })
                                        }
                                    />
                                    <Label htmlFor="scholarship" className="cursor-pointer">
                                        I want to apply for scholarship
                                    </Label>
                                </div>

                                <div className="flex items-center space-x-2">
                                    <Checkbox
                                        id="hostel"
                                        checked={formData.hostel_required}
                                        onCheckedChange={(checked) =>
                                            setFormData({ ...formData, hostel_required: checked as boolean })
                                        }
                                    />
                                    <Label htmlFor="hostel" className="cursor-pointer">
                                        I require hostel accommodation
                                    </Label>
                                </div>
                            </div>
                        </div>

                        {/* Information Box */}
                        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                            <p className="text-sm text-blue-800">
                                <strong>What happens next?</strong><br />
                                After submitting this form, you'll be directed to the payment page to complete your application fee payment.
                            </p>
                        </div>

                        {/* Submit Button */}
                        <div className="flex gap-4">
                            <Link href="/dashboard" className="flex-1">
                                <Button type="button" variant="outline" className="w-full">
                                    Save as Draft
                                </Button>
                            </Link>
                            <Button
                                type="submit"
                                className="flex-1 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700"
                                disabled={completeMutation.isPending}
                            >
                                {completeMutation.isPending ? (
                                    <>
                                        <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                                        Submitting...
                                    </>
                                ) : (
                                    'Submit Application'
                                )}
                            </Button>
                        </div>
                    </form>
                </CardContent>
            </Card>
        </div>
    )
}
