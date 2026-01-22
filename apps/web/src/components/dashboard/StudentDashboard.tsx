'use client'

import React from 'react'
import { useAuthStore } from '@/store/use-auth-store'
import { Calendar, BookOpen, Clock, FileCheck, AlertCircle } from 'lucide-react'
import { KPICard } from '@/components/dashboard/KPICard'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useQuery } from '@tanstack/react-query'
import { admissionApi } from '@/services/admission-api'
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

    // Check if application is incomplete
    const isApplicationIncomplete = application &&
        (application.status === 'QUICK_APPLY_SUBMITTED' ||
            application.status === 'LOGGED_IN' ||
            application.status === 'FORM_IN_PROGRESS')

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-slate-900 text-2xl font-semibold mb-2">Student Dashboard</h1>
                <p className="text-slate-600">Welcome back, {user?.full_name}</p>
            </div>

            {/* Application Completion Alert */}
            {isApplicationIncomplete && (
                <Card className="border-orange-200 bg-orange-50">
                    <CardHeader className="pb-3">
                        <div className="flex items-start gap-3">
                            <AlertCircle className="h-5 w-5 text-orange-600 mt-0.5" />
                            <div className="flex-1">
                                <CardTitle className="text-lg text-orange-900">Complete Your Application</CardTitle>
                                <p className="text-sm text-orange-700 mt-1">
                                    Your application is incomplete. Please complete the remaining steps to proceed with the admission process.
                                </p>
                            </div>
                        </div>
                    </CardHeader>
                    <CardContent>
                        <div className="flex items-center justify-between">
                            <div className="text-sm text-orange-800">
                                <strong>Application Number:</strong> {application?.application_number}
                            </div>
                            <Link href="/dashboard/admissions/complete">
                                <Button className="bg-orange-600 hover:bg-orange-700 text-white">
                                    Complete Application
                                </Button>
                            </Link>
                        </div>
                    </CardContent>
                </Card>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <KPICard
                    title="My Attendance"
                    value="85%"
                    icon={<Calendar size={24} />}
                    trend={{ value: 'Above requirement', isPositive: true }}
                    color="blue"
                />
                <KPICard
                    title="Assignments"
                    value="3 Pending"
                    icon={<BookOpen size={24} />}
                    color="orange"
                />
                <KPICard
                    title="Next Class"
                    value="DBMS - Lab"
                    icon={<Clock size={24} />}
                    trend={{ value: 'In 10 mins', isPositive: true }}
                    color="green"
                />
                <KPICard
                    title="ODC Events"
                    value="2 New"
                    icon={<FileCheck size={24} />}
                    color="purple"
                />
            </div>

            {/* Timetable or Recent Activity could go here */}
            <div className="bg-white rounded-xl border border-slate-200 p-6">
                <h2 className="text-lg font-semibold mb-4">Today's Schedule</h2>
                <div className="text-slate-500 text-sm">No classes scheduled for today.</div>
            </div>
        </div>
    )
}
