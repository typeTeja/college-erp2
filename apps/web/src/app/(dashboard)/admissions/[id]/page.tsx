'use client'

import { useParams } from 'next/navigation'
import { admissionsService } from '@/utils/admissions-service'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { ApplicationStatus, PaymentMode } from '@/types/admissions'
import DocumentUpload from '@/components/admissions/DocumentUpload'
import DocumentVerification from '@/components/admissions/DocumentVerification'
import ActivityTimeline from '@/components/admissions/ActivityTimeline'
import { useToast } from '@/hooks/use-toast'
import { CheckCircle, Clock, FileText, User, CreditCard, GraduationCap } from 'lucide-react'

export default function ApplicationDetailPage() {
    const params = useParams()
    const applicationId = parseInt(params.id as string)
    const { toast } = useToast()

    const { data: application, isLoading } = admissionsService.useApplication(applicationId)
    const confirmMutation = admissionsService.useConfirmAdmission()

    const handleConfirmAdmission = async () => {
        try {
            await confirmMutation.mutateAsync(applicationId)
            toast({
                title: "Success",
                description: "Admission confirmed successfully. Student account created."
            })
        } catch (error: any) {
            toast({
                title: "Error",
                description: error.response?.data?.detail || "Failed to confirm admission",
                variant: "destructive"
            })
        }
    }

    const getStatusColor = (status: ApplicationStatus): "default" | "success" | "destructive" | "secondary" => {
        switch (status) {
            case ApplicationStatus.ADMITTED:
                return "success"
            case ApplicationStatus.REJECTED:
            case ApplicationStatus.PAYMENT_FAILED:
                return "destructive"
            case ApplicationStatus.PENDING_PAYMENT:
                return "secondary"
            default:
                return "default"
        }
    }

    if (isLoading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <p className="text-muted-foreground">Loading application...</p>
            </div>
        )
    }

    if (!application) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <p className="text-muted-foreground">Application not found</p>
            </div>
        )
    }

    return (
        <div className="container mx-auto py-8 space-y-6">
            {/* Header */}
            <div className="flex items-start justify-between">
                <div>
                    <h1 className="text-3xl font-bold">{application.name}</h1>
                    <div className="flex flex-col gap-1 mt-1">
                        <p className="text-muted-foreground">Application #{application.application_number}</p>
                        {application.program && <Badge variant="outline" className="w-fit">{application.program.name}</Badge>}
                    </div>
                </div>
                <Badge variant={getStatusColor(application.status)} className="text-lg px-4 py-2">
                    {application.status.replace(/_/g, ' ')}
                </Badge>
            </div>

            {/* Overview Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Contact</CardTitle>
                        <User className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-sm">
                            <p className="font-medium">{application.email}</p>
                            <p className="text-muted-foreground">{application.phone}</p>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Payment</CardTitle>
                        <CreditCard className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-sm">
                            <p className="font-medium">{application.fee_mode}</p>
                            {application.fee_mode === PaymentMode.OFFLINE && (
                                <p className="text-muted-foreground">
                                    {application.offline_payment_verified ? 'Verified ✓' : 'Pending'}
                                </p>
                            )}
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Documents</CardTitle>
                        <FileText className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">
                            {application.documents?.length || 0}
                        </div>
                        <p className="text-xs text-muted-foreground">
                            Uploaded
                        </p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Created</CardTitle>
                        <Clock className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-sm">
                            <p className="font-medium">
                                {new Date(application.created_at).toLocaleDateString()}
                            </p>
                            <p className="text-muted-foreground">
                                {new Date(application.created_at).toLocaleTimeString()}
                            </p>
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Main Content Tabs */}
            <Tabs defaultValue="details" className="space-y-4">
                <TabsList>
                    <TabsTrigger value="details">Details</TabsTrigger>
                    <TabsTrigger value="documents">Documents</TabsTrigger>
                    <TabsTrigger value="timeline">Timeline</TabsTrigger>
                </TabsList>

                <TabsContent value="details" className="space-y-4">
                    {/* Personal Information */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Personal Information</CardTitle>
                        </CardHeader>
                        <CardContent className="grid grid-cols-2 gap-4">
                            <div>
                                <p className="text-sm text-muted-foreground">Full Name</p>
                                <p className="font-medium">{application.name}</p>
                            </div>
                            <div>
                                <p className="text-sm text-muted-foreground">Gender</p>
                                <p className="font-medium">{application.gender}</p>
                            </div>
                            <div>
                                <p className="text-sm text-muted-foreground">Email</p>
                                <p className="font-medium">{application.email}</p>
                            </div>
                            <div>
                                <p className="text-sm text-muted-foreground">Phone</p>
                                <p className="font-medium">{application.phone}</p>
                            </div>
                            {application.aadhaar_number && (
                                <div>
                                    <p className="text-sm text-muted-foreground">Aadhaar Number</p>
                                    <p className="font-medium">{application.aadhaar_number}</p>
                                </div>
                            )}
                            {application.father_name && (
                                <>
                                    <div>
                                        <p className="text-sm text-muted-foreground">Father's Name</p>
                                        <p className="font-medium">{application.father_name}</p>
                                    </div>
                                    <div>
                                        <p className="text-sm text-muted-foreground">Father's Phone</p>
                                        <p className="font-medium">{application.father_phone}</p>
                                    </div>
                                </>
                            )}
                            {application.address && (
                                <div className="col-span-2">
                                    <p className="text-sm text-muted-foreground">Address</p>
                                    <p className="font-medium">{application.address}</p>
                                </div>
                            )}
                        </CardContent>
                    </Card>

                    {/* Academic Information */}
                    <Card>
                        <CardHeader>
                            <CardTitle>Academic Information</CardTitle>
                        </CardHeader>
                        <CardContent className="grid grid-cols-2 gap-4">
                            <div>
                                <p className="text-sm text-muted-foreground">State</p>
                                <p className="font-medium">{application.state}</p>
                            </div>
                            <div>
                                <p className="text-sm text-muted-foreground">Board</p>
                                <p className="font-medium">{application.board}</p>
                            </div>
                            <div>
                                <p className="text-sm text-muted-foreground">Group of Study</p>
                                <p className="font-medium">{application.group_of_study}</p>
                            </div>
                            {application.previous_marks_percentage && (
                                <div>
                                    <p className="text-sm text-muted-foreground">Previous Marks %</p>
                                    <p className="font-medium">{application.previous_marks_percentage}%</p>
                                </div>
                            )}
                            <div>
                                <p className="text-sm text-muted-foreground">Scholarship</p>
                                <p className="font-medium">{application.applied_for_scholarship ? 'Yes' : 'No'}</p>
                            </div>
                            <div>
                                <p className="text-sm text-muted-foreground">Hostel Required</p>
                                <p className="font-medium">{application.hostel_required ? 'Yes' : 'No'}</p>
                            </div>
                        </CardContent>
                    </Card>

                    {/* Admin Actions */}
                    {application.status === ApplicationStatus.APPROVED && (
                        <Card className="border-green-200 bg-green-50">
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2">
                                    <GraduationCap className="h-5 w-5" />
                                    Confirm Admission
                                </CardTitle>
                            </CardHeader>
                            <CardContent>
                                <p className="text-sm text-muted-foreground mb-4">
                                    This application is ready for admission confirmation. This will create a student account and send a password setup email.
                                </p>
                                <Button
                                    onClick={handleConfirmAdmission}
                                    disabled={confirmMutation.isPending}
                                    className="bg-green-600 hover:bg-green-700"
                                >
                                    {confirmMutation.isPending ? "Confirming..." : "Confirm Admission"}
                                </Button>
                            </CardContent>
                        </Card>
                    )}

                    {/* Resend Credentials Action */}
                    {application.payment_status === 'SUCCESS' && application.portal_user_id && (
                        <Card className="border-blue-200 bg-blue-50">
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2">
                                    <User className="h-5 w-5" />
                                    Resend Login Credentials
                                </CardTitle>
                            </CardHeader>
                            <CardContent>
                                <p className="text-sm text-muted-foreground mb-4">
                                    Student account exists. Verify that the student has paid the application fee.
                                    Clicking this will generate a <strong>NEW</strong> password and send it via Email and SMS.
                                    The old password will stop working immediately.
                                </p>
                                <ResendCredentialsButton applicationId={application.id} />
                            </CardContent>
                        </Card>
                    )}
                </TabsContent>

                <TabsContent value="documents">
                    <div className="space-y-6">
                        <DocumentUpload applicationId={applicationId} />
                        <DocumentVerification applicationId={applicationId} />
                    </div>
                </TabsContent>

                <TabsContent value="timeline">
                    <ActivityTimeline applicationId={applicationId} />
                </TabsContent>
            </Tabs>


        </div>
    )
}

function ResendCredentialsButton({ applicationId }: { applicationId: number }) {
    const { toast } = useToast()
    const resendMutation = admissionsService.useResendCredentials()

    const handleResend = async () => {
        if (!confirm("Are you sure? This will reset the student's password.")) return

        try {
            await resendMutation.mutateAsync(applicationId)
            toast({
                title: "Success",
                description: "New credentials sent to student via Email/SMS."
            })
        } catch (error: any) {
            toast({
                title: "Error",
                description: error.response?.data?.detail || "Failed to resend credentials",
                variant: "destructive"
            })
        }
    }

    return (
        <Button
            onClick={handleResend}
            disabled={resendMutation.isPending}
            variant="outline"
            className="bg-white hover:bg-blue-100 text-blue-700 border-blue-300"
        >
            {resendMutation.isPending ? "Sending..." : "Resend Credentials"}
        </Button>
    )
}
