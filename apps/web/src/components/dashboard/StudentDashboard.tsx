'use client'

import React from 'react'
import { useAuthStore } from '@/store/use-auth-store'
import { Calendar, BookOpen, Clock, FileCheck, AlertCircle } from 'lucide-react'
import { KPICard } from '@/components/dashboard/KPICard'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useQuery } from '@tanstack/react-query'
import { admissionApi } from '@/services/admission-api'
import { ApplicationStatus } from '@/types/admissions'
import { useRouter } from 'next/navigation'
import Link from 'next/link'

export function StudentDashboard() {
    const { user } = useAuthStore()
    const router = useRouter()

    // Fetch student's application if exists
    const { data: application, isLoading } = useQuery({
        queryKey: ['my-application'],
        queryFn: () => admissionApi.getMyApplication(),
        retry: false,
        // Don't throw error if no application found
        meta: {
            errorMessage: null
        }
    })

    // Helper statuses
    const isOnlinePaid = application?.payment_status === 'SUCCESS' || application?.payment_status === 'PAID'
    const isOfflinePaid = application?.fee_mode === 'OFFLINE' && application?.offline_payment_verified
    const isPaid = isOnlinePaid || isOfflinePaid || application?.status === ApplicationStatus.PAID || application?.status === ApplicationStatus.FORM_COMPLETED || application?.status === ApplicationStatus.ADMITTED || application?.status === ApplicationStatus.APPROVED

    const isFormCompleted = application?.status === ApplicationStatus.FORM_COMPLETED || application?.status === ApplicationStatus.UNDER_REVIEW || application?.status === ApplicationStatus.APPROVED || application?.status === ApplicationStatus.ADMITTED
    
    // Verification is complex: incomplete if just form submitted.
    // We assume verification is done if status is APPROVED or ADMITTED, or documents_verified is explicitly true
    const isVerified = application?.status === ApplicationStatus.APPROVED || application?.status === ApplicationStatus.ADMITTED || application?.documents_verified

    const isAdmitted = application?.status === ApplicationStatus.ADMITTED

    // Define timeline steps based on status
    const getSteps = () => {
        const steps = [
            { label: 'Quick Apply', status: 'completed' },
            { label: 'Payment', status: 'pending' },
            { label: 'Application Form', status: 'pending' },
            { label: 'Verification', status: 'pending' },
            { label: 'Admission Confirmed', status: 'pending' }
        ]

        if (!application) return steps

        // Step 1: Payment
        if (isPaid) {
            steps[1].status = 'completed'
        } else {
             // If we are here, we are not paid.
             // If Quick Apply submitted, we are at Payment step
             steps[1].status = 'current'
             return steps // Stop here, next steps are pending
        }

        // Step 2: Form
        if (isFormCompleted) {
             steps[2].status = 'completed'
        } else {
             steps[2].status = 'current'
             return steps
        }

        // Step 3: Verification
        if (isVerified) {
             steps[3].status = 'completed'
        } else {
             steps[3].status = 'current'
             return steps
        }

        // Step 4: Admission
        if (isAdmitted) {
             steps[4].status = 'completed'
        } else {
             // If verified but not admitted, we are waiting for admission logic (or just show verification completed and waiting)
             steps[4].status = 'current'
        }

        return steps
    }

    const steps = getSteps()

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-slate-900 text-2xl font-semibold mb-2">Student Dashboard</h1>
                <p className="text-slate-600">Welcome back, {user?.full_name}</p>
            </div>

            {/* Application Info Card */}
            {application && (
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {/* Card 1: Application Info */}
                    <Card>
                        <CardHeader className="pb-2">
                             <CardTitle className="text-sm font-medium text-slate-500">Application Number</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">{application.application_number}</div>
                            <div className="text-xs text-slate-500 mt-1">
                                {application.program?.name || 'N/A'}
                            </div>
                        </CardContent>
                    </Card>

                    {/* Card 2: Current Stage */}
                     <Card>
                        <CardHeader className="pb-2">
                             <CardTitle className="text-sm font-medium text-slate-500">Current Status</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold capitalize">{application.status?.replace(/_/g, ' ') || 'Unknown'}</div>
                            <div className="text-xs text-slate-500 mt-1">
                                Last updated: {application.updated_at ? new Date(application.updated_at).toLocaleDateString() : 'N/A'}
                            </div>
                        </CardContent>
                    </Card>

                    {/* Card 3: Payment Details */}
                     <Card>
                        <CardHeader className="pb-2">
                             <CardTitle className="text-sm font-medium text-slate-500">Payment Status</CardTitle>
                        </CardHeader>
                        <CardContent>
                             <div className={`text-2xl font-bold ${isPaid ? 'text-green-600' : 'text-orange-600'}`}>
                                {isPaid ? 'Paid' : 'Pending'}
                            </div>
                             <div className="text-xs text-slate-500 mt-1 flex flex-col">
                                <span>Amount: ₹{application.application_fee}</span>
                                <span className="uppercase font-semibold mt-0.5 text-[10px] tracking-wide text-slate-600">
                                    {application.fee_mode} MODE
                                    {application.fee_mode === 'OFFLINE' && !isOfflinePaid && ' (Verification Pending)'}
                                </span>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            )}

            {/* Application Completion Alert */}
            {/* Show alert if: Not Paid OR (Paid but Form Not Completed) */}
            {(!isPaid || (isPaid && !isFormCompleted)) && (
                <Card className="border-orange-200 bg-orange-50">
                    <CardHeader className="pb-3">
                        <div className="flex items-start gap-3">
                            <AlertCircle className="h-5 w-5 text-orange-600 mt-0.5" />
                            <div className="flex-1">
                                <CardTitle className="text-lg text-orange-900">Action Required</CardTitle>
                                <p className="text-sm text-orange-700 mt-1">
                                    {!isPaid 
                                        ? "Your application fee payment is pending. Please complete the payment to proceed." 
                                        : "Your application payment is confirmed. Please complete the full application form."}
                                </p>
                            </div>
                        </div>
                    </CardHeader>
                    <CardContent>
                        <div className="flex items-center justify-end">
                            <Link href={!isPaid ? "/admissions/payment" : "/admissions/complete"}>
                                {/* Note: /admissions/payment page might need to be created if not exists, falling back to complete which handles checks */}
                                <Button className="bg-orange-600 hover:bg-orange-700 text-white">
                                    {!isPaid ? "Pay Application Fee" : "Complete Application Form"}
                                </Button>
                            </Link>
                        </div>
                    </CardContent>
                </Card>
            )}

            {/* Application Timeline */}
            <Card>
                <CardHeader>
                    <CardTitle>Admission Progress</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="relative flex items-center justify-between w-full max-w-4xl mx-auto py-8">
                         {/* Connecting Line */}
                         <div className="absolute top-1/2 left-0 w-full h-1 bg-gray-200 -z-0 -translate-y-1/2" />
                        
                        {steps.map((step, index) => (
                            <div key={index} className="flex flex-col items-center relative z-10 bg-white px-2">
                                <div className={`w-10 h-10 rounded-full flex items-center justify-center border-4 transition-colors ${
                                    step.status === 'completed' ? 'bg-green-100 border-green-500 text-green-600' :
                                    step.status === 'current' ? 'bg-blue-100 border-blue-500 text-blue-600' :
                                    'bg-gray-100 border-gray-300 text-gray-400'
                                }`}>
                                    {step.status === 'completed' ? (
                                        <FileCheck size={20} />
                                    ) : (
                                        <span className="font-semibold">{index + 1}</span>
                                    )}
                                </div>
                                <span className={`mt-2 text-sm font-medium ${
                                    step.status === 'completed' ? 'text-green-600' :
                                    step.status === 'current' ? 'text-blue-600' :
                                    'text-gray-500'
                                }`}>
                                    {step.label}
                                </span>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>

            {/* Show message if waiting for verification */}
            {application?.status === ApplicationStatus.FORM_COMPLETED && (
                 <div className="bg-blue-50 border border-blue-200 rounded-xl p-6 text-center">
                    <h3 className="text-lg font-semibold text-blue-900">Application Under Review</h3>
                    <p className="text-blue-700 mt-2">
                        You have successfully submitted your application. Our admissions team is currently reviewing your documents.
                        Please check back later for updates.
                    </p>
                </div>
            )}
        </div>
    )
}
