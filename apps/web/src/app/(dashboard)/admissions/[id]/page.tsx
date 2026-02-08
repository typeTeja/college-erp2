'use client'

import { useParams } from 'next/navigation'
import { admissionsService } from '@/utils/admissions-service'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { ApplicationStatus, PaymentMode, AddressType, ParentRelation } from '@/types/admissions'
import DocumentUpload from '@/components/admissions/DocumentUpload'
import DocumentVerification from '@/components/admissions/DocumentVerification'
import ActivityTimeline from '@/components/admissions/ActivityTimeline'
import { useToast } from '@/hooks/use-toast'
import {
    CheckCircle, Clock, FileText, User, CreditCard,
    GraduationCap, MapPin, Phone, Mail, Calendar,
    Info, Building, ShieldCheck, HeartPulse, Briefcase,
    Globe, BookOpen, AlertCircle
} from 'lucide-react'

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

    const getStatusVariant = (status: ApplicationStatus): "default" | "success" | "destructive" | "secondary" | "outline" | "warning" => {
        switch (status) {
            case ApplicationStatus.ADMITTED:
            case ApplicationStatus.APPROVED:
                return "success"
            case ApplicationStatus.REJECTED:
            case ApplicationStatus.PAYMENT_FAILED:
                return "destructive"
            case ApplicationStatus.PENDING_PAYMENT:
            case ApplicationStatus.FORM_IN_PROGRESS:
                return "secondary"
            case ApplicationStatus.UNDER_REVIEW:
                return "default"
            default:
                return "outline"
        }
    }

    if (isLoading) {
        return (
            <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
                <p className="text-muted-foreground animate-pulse">Loading application data...</p>
            </div>
        )
    }

    if (!application) {
        return (
            <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
                <AlertCircle className="h-12 w-12 text-destructive" />
                <p className="text-xl font-semibold">Application Not Found</p>
                <Button variant="outline" onClick={() => window.history.back()}>Go Back</Button>
            </div>
        )
    }

    return (
        <div className="container mx-auto py-8 space-y-8 animate-in fade-in duration-500">
            {/* Header Section */}
            <header className="flex flex-col md:flex-row md:items-center justify-between gap-6 p-6 bg-card border rounded-2xl shadow-sm">
                <div className="flex items-center gap-5">
                    <div className="h-20 w-20 rounded-full bg-primary/10 flex items-center justify-center border-4 border-background shadow-inner">
                        <User className="h-10 w-10 text-primary" />
                    </div>
                    <div>
                        <div className="flex items-center gap-3">
                            <h1 className="text-3xl font-bold tracking-tight">{application.name}</h1>
                            <Badge variant={getStatusVariant(application.status)} className="capitalize px-3 py-1 text-sm font-semibold">
                                {application.status.toLowerCase().replace(/_/g, ' ')}
                            </Badge>
                        </div>
                        <div className="flex flex-wrap items-center gap-x-6 gap-y-1 mt-2 text-sm text-muted-foreground">
                            <div className="flex items-center gap-1.5">
                                <FileText className="h-4 w-4" />
                                <span className="font-mono">#{application.application_number}</span>
                            </div>
                            <div className="flex items-center gap-1.5">
                                <GraduationCap className="h-4 w-4" />
                                <span>{application.program?.name || 'Program Not Selected'}</span>
                            </div>
                            <div className="flex items-center gap-1.5">
                                <Clock className="h-4 w-4" />
                                <span>Applied {new Date(application.created_at).toLocaleDateString()}</span>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="flex gap-3">
                    {application.status === ApplicationStatus.APPROVED && (
                        <Button
                            onClick={handleConfirmAdmission}
                            disabled={confirmMutation.isPending}
                            className="bg-green-600 hover:bg-green-700 shadow-md transition-all hover:scale-105"
                        >
                            {confirmMutation.isPending ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <CheckCircle className="mr-2 h-4 w-4" />}
                            Confirm Admission
                        </Button>
                    )}
                    <Button variant="outline" className="shadow-sm">Export PDF</Button>
                </div>
            </header>

            {/* Overview Quick Stats */}
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <QuickStatCard
                    title="Contact"
                    icon={<Phone className="h-4 w-4 text-primary" />}
                    value={application.phone}
                    subValue={application.email}
                />
                <QuickStatCard
                    title="Payment Status"
                    icon={<CreditCard className="h-4 w-4 text-blue-500" />}
                    value={application.payment_status?.toUpperCase() || 'PENDING'}
                    subValue={application.fee_mode}
                    statusBadge={application.offline_payment_verified ? "Verified" : undefined}
                />
                <QuickStatCard
                    title="Documentation"
                    icon={<FileText className="h-4 w-4 text-purple-500" />}
                    value={`${application.documents?.length || 0} Files`}
                    subValue={application.documents_verified ? "All Verified ✓" : "Verification Pending"}
                />
                <QuickStatCard
                    title="Application Step"
                    icon={<Info className="h-4 w-4 text-orange-500" />}
                    value={`Step ${application.current_step || 1} of 7`}
                    subValue={`Last saved: ${application.last_saved_at ? new Date(application.last_saved_at).toLocaleDateString() : 'Never'}`}
                />
            </div>

            {/* Main Content Tabs */}
            <Tabs defaultValue="details" className="space-y-6">
                <TabsList className="bg-muted/50 p-1 rounded-xl glass-morphism border">
                    <TabsTrigger value="details" className="rounded-lg px-6 py-2">Full Details</TabsTrigger>
                    <TabsTrigger value="documents" className="rounded-lg px-6 py-2">Documents</TabsTrigger>
                    <TabsTrigger value="timeline" className="rounded-lg px-6 py-2">Activity Log</TabsTrigger>
                </TabsList>

                <TabsContent value="details" className="space-y-8">
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                        {/* Left Column - Core Info */}
                        <div className="lg:col-span-2 space-y-8">
                            {/* Personal Information */}
                            <Card className="border-none shadow-md overflow-hidden bg-gradient-to-br from-background to-muted/20">
                                <CardHeader className="border-b bg-muted/30 pb-4">
                                    <div className="flex items-center gap-2">
                                        <User className="h-5 w-5 text-primary" />
                                        <CardTitle className="text-lg">Personal Information</CardTitle>
                                    </div>
                                </CardHeader>
                                <CardContent className="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                    <DetailItem label="Full Name" value={application.name} />
                                    <DetailItem label="Gender" value={application.gender} />
                                    <DetailItem label="Date of Birth" value={application.date_of_birth ? new Date(application.date_of_birth).toLocaleDateString() : 'N/A'} />
                                    <DetailItem label="Blood Group" value={application.blood_group || 'N/A'} />
                                    <DetailItem label="Nationality" value={application.nationality || 'N/A'} />
                                    <DetailItem label="Religion" value={application.religion || 'N/A'} />
                                    <DetailItem label="Caste Category" value={application.caste_category || 'N/A'} />
                                    <DetailItem label="Mother Tongue" value={application.mother_tongue || 'N/A'} />
                                    <DetailItem label="Aadhaar Number" value={application.aadhaar_number} icon={<ShieldCheck className="h-3.5 w-3.5 text-green-600" />} />
                                </CardContent>
                            </Card>

                            {/* Addresses */}
                            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                {application.addresses?.map((addr, idx) => (
                                    <Card key={idx} className="border-none shadow-md">
                                        <CardHeader className="pb-3 flex flex-row items-center justify-between">
                                            <div className="flex items-center gap-2">
                                                <MapPin className="h-4 w-4 text-primary" />
                                                <CardTitle className="text-base">{addr.address_type.replace(/_/g, ' ')} Address</CardTitle>
                                            </div>
                                        </CardHeader>
                                        <CardContent className="text-sm space-y-1 text-muted-foreground">
                                            <p className="font-medium text-foreground">{addr.address_line}</p>
                                            <p>{addr.village_city}, {addr.district}</p>
                                            <p>{addr.state}, {addr.country}</p>
                                            <p className="pt-2 font-mono">PIN: {addr.pincode}</p>
                                        </CardContent>
                                    </Card>
                                ))}
                            </div>

                            {/* Education History */}
                            <Card className="border-none shadow-md">
                                <CardHeader className="border-b bg-muted/30 pb-4">
                                    <div className="flex items-center gap-2">
                                        <BookOpen className="h-5 w-5 text-primary" />
                                        <CardTitle className="text-lg">Academic Records</CardTitle>
                                    </div>
                                </CardHeader>
                                <CardContent className="p-0">
                                    <div className="overflow-x-auto">
                                        <table className="w-full text-sm">
                                            <thead className="bg-muted/50 text-muted-foreground uppercase text-[11px] tracking-wider">
                                                <tr>
                                                    <th className="px-6 py-3 text-left">Level</th>
                                                    <th className="px-6 py-3 text-left">Institution</th>
                                                    <th className="px-6 py-3 text-center">Year</th>
                                                    <th className="px-6 py-3 text-right">Result</th>
                                                </tr>
                                            </thead>
                                            <tbody className="divide-y">
                                                {application.education_history?.map((edu, idx) => (
                                                    <tr key={idx} className="hover:bg-muted/30 transition-colors">
                                                        <td className="px-6 py-4 font-semibold text-primary">{edu.level}</td>
                                                        <td className="px-6 py-4">
                                                            <div className="font-medium text-foreground">{edu.institution_name}</div>
                                                            <div className="text-[11px] text-muted-foreground">{edu.board}</div>
                                                        </td>
                                                        <td className="px-6 py-4 text-center">{edu.year_of_passing || 'N/A'}</td>
                                                        <td className="px-6 py-4 text-right">
                                                            <div className="font-bold text-foreground">
                                                                {edu.percentage ? `${edu.percentage}%` : edu.cgpa ? `${edu.cgpa} CGPA` : 'N/A'}
                                                            </div>
                                                        </td>
                                                    </tr>
                                                ))}
                                                {!application.education_history?.length && (
                                                    <tr>
                                                        <td colSpan={4} className="px-6 py-10 text-center text-muted-foreground italic">
                                                            No education records provided.
                                                        </td>
                                                    </tr>
                                                )}
                                            </tbody>
                                        </table>
                                    </div>
                                </CardContent>
                            </Card>
                        </div>

                        {/* Right Column - Parental & Details */}
                        <div className="space-y-8">
                            {/* Parent/Guardian Info */}
                            <Card className="border-none shadow-md">
                                <CardHeader className="border-b bg-muted/30 pb-4">
                                    <div className="flex items-center gap-2">
                                        <Building className="h-5 w-5 text-primary" />
                                        <CardTitle className="text-lg">Parent/Guardian Details</CardTitle>
                                    </div>
                                </CardHeader>
                                <CardContent className="p-6 space-y-6">
                                    {application.parents?.map((parent, idx) => (
                                        <div key={idx} className={`space-y-3 ${idx > 0 ? 'pt-6 border-t border-dashed' : ''}`}>
                                            <div className="flex items-center justify-between">
                                                <Badge variant="outline" className="bg-primary/5 text-primary border-primary/20">
                                                    {parent.relation}
                                                </Badge>
                                                {parent.is_primary_contact && <Badge className="bg-green-100 text-green-700 hover:bg-green-100 border-none px-2 py-0 text-[10px]">Primary</Badge>}
                                            </div>
                                            <p className="font-bold text-base">{parent.name}</p>
                                            <div className="grid grid-cols-1 gap-1 text-sm">
                                                <div className="flex items-center gap-2 text-muted-foreground">
                                                    <Phone className="h-3 w-3" />
                                                    <span>{parent.mobile}</span>
                                                </div>
                                                {parent.email && (
                                                    <div className="flex items-center gap-2 text-muted-foreground">
                                                        <Mail className="h-3 w-3" />
                                                        <span>{parent.email}</span>
                                                    </div>
                                                )}
                                                {parent.occupation && (
                                                    <div className="flex items-center gap-2 text-muted-foreground">
                                                        <Briefcase className="h-3 w-3" />
                                                        <span>{parent.occupation} {parent.annual_income ? `(₹${parent.annual_income.toLocaleString()})` : ''}</span>
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    ))}
                                    {!application.parents?.length && (
                                        <p className="text-center text-muted-foreground italic py-4">No parental info available.</p>
                                    )}
                                </CardContent>
                            </Card>

                            {/* Bank & Health */}
                            <div className="space-y-6">
                                {/* Bank */}
                                <Card className="border-none shadow-md bg-blue-50/50">
                                    <CardHeader className="pb-3 border-b flex flex-row items-center gap-2">
                                        <CreditCard className="h-4 w-4 text-blue-600" />
                                        <CardTitle className="text-base text-blue-900">Bank Details</CardTitle>
                                    </CardHeader>
                                    <CardContent className="pt-4 text-sm space-y-2">
                                        {application.bank_details ? (
                                            <>
                                                <p className="font-semibold text-blue-900">{application.bank_details.account_holder_name}</p>
                                                <p className="font-mono text-xs">{application.bank_details.account_number}</p>
                                                <p className="text-xs">{application.bank_details.bank_name}, {application.bank_details.branch_name}</p>
                                                <p className="font-mono text-xs font-bold pt-1">IFSC: {application.bank_details.ifsc_code}</p>
                                            </>
                                        ) : <p className="text-muted-foreground italic">No bank details provided.</p>}
                                    </CardContent>
                                </Card>

                                {/* Health */}
                                <Card className="border-none shadow-md bg-red-50/30">
                                    <CardHeader className="pb-3 border-b flex flex-row items-center gap-2">
                                        <HeartPulse className="h-4 w-4 text-red-600" />
                                        <CardTitle className="text-base text-red-900">Medical Info</CardTitle>
                                    </CardHeader>
                                    <CardContent className="pt-4 text-sm space-y-4">
                                        {application.health_info ? (
                                            <>
                                                <div className="flex items-center justify-between">
                                                    <span className="text-muted-foreground text-xs uppercase tracking-tight">Status</span>
                                                    <Badge variant={application.health_info.is_medically_fit ? "success" : "destructive"} className="text-[10px] px-1.5 py-0 h-4">
                                                        {application.health_info.is_medically_fit ? 'MEDICALLY FIT' : 'UNFIT'}
                                                    </Badge>
                                                </div>
                                                <div className="space-y-1">
                                                    <p className="text-xs text-muted-foreground">Certified By</p>
                                                    <p className="font-medium text-foreground">{application.health_info.practitioner_name || 'N/A'}</p>
                                                    <p className="text-[10px] opacity-70">Reg: {application.health_info.practitioner_registration_number || '-'}</p>
                                                </div>
                                            </>
                                        ) : <p className="text-muted-foreground italic">No medical info provided.</p>}
                                    </CardContent>
                                </Card>
                            </div>
                        </div>
                    </div>

                    {/* Admin Actions Bar */}
                    <Card className="border-none shadow-2xl bg-gradient-to-r from-primary/5 to-primary/10 border-t-4 border-primary p-2">
                        <CardContent className="flex flex-col md:flex-row items-center justify-between gap-6 p-6">
                            <div className="space-y-1 text-center md:text-left">
                                <h3 className="text-xl font-bold text-primary flex items-center justify-center md:justify-start gap-2">
                                    <ShieldCheck className="h-6 w-6" />
                                    Administrative Control
                                </h3>
                                <p className="text-sm text-muted-foreground">Finalize the admission process or manage account access for this student.</p>
                            </div>
                            <div className="flex items-center gap-4">
                                {application.status === ApplicationStatus.APPROVED && (
                                    <Button
                                        onClick={handleConfirmAdmission}
                                        disabled={confirmMutation.isPending}
                                        size="lg"
                                        className="bg-green-600 hover:bg-green-700 font-bold"
                                    >
                                        Confirm Admission
                                    </Button>
                                )}
                                {application.portal_user_id && (
                                    <ResendCredentialsButton applicationId={application.id} />
                                )}
                            </div>
                        </CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="documents">
                    <Card className="border-none shadow-lg">
                        <CardHeader>
                            <CardTitle>Documentation Manager</CardTitle>
                            <CardDescription>Review and verify applicant uploaded documents.</CardDescription>
                        </CardHeader>
                        <CardContent className="space-y-8">
                            <DocumentVerification applicationId={applicationId} />
                            <div className="pt-8 border-t border-dashed">
                                <h4 className="text-sm font-bold mb-4 flex items-center gap-2">
                                    <AlertCircle className="h-4 w-4 text-orange-500" />
                                    Manual Upload Override
                                </h4>
                                <DocumentUpload applicationId={applicationId} />
                            </div>
                        </CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="timeline">
                    <Card className="border-none shadow-lg">
                        <CardHeader>
                            <CardTitle>Activity Insights</CardTitle>
                            <CardDescription>Track the journey of this application.</CardDescription>
                        </CardHeader>
                        <CardContent>
                            <ActivityTimeline applicationId={applicationId} />
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>
        </div>
    )
}

function DetailItem({ label, value, icon }: { label: string, value: string | undefined | null, icon?: React.ReactNode }) {
    return (
        <div className="space-y-1 group">
            <p className="text-[11px] font-bold text-muted-foreground uppercase tracking-wider">{label}</p>
            <div className="flex items-center gap-2">
                {icon}
                <p className="font-semibold text-foreground group-hover:text-primary transition-colors truncate">{value || '—'}</p>
            </div>
        </div>
    )
}

function QuickStatCard({ title, icon, value, subValue, statusBadge }: { title: string, icon: React.ReactNode, value: string, subValue: string, statusBadge?: string }) {
    return (
        <Card className="border-none shadow-sm hover:shadow-md transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-[11px] font-bold text-muted-foreground uppercase">{title}</CardTitle>
                {icon}
            </CardHeader>
            <CardContent>
                <div className="flex items-center gap-2">
                    <div className="text-lg font-bold truncate">{value}</div>
                    {statusBadge && <Badge variant="outline" className="text-[9px] px-1 py-0 h-4 bg-green-50 text-green-700 border-green-200">{statusBadge}</Badge>}
                </div>
                <p className="text-xs text-muted-foreground truncate font-medium mt-0.5">{subValue}</p>
            </CardContent>
        </Card>
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
            className="border-blue-200 text-blue-700 hover:bg-blue-50"
        >
            {resendMutation.isPending ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <ShieldCheck className="mr-2 h-4 w-4" />}
            Reset Credentials
        </Button>
    )
}

const Loader2 = ({ className }: { className?: string }) => (
    <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className={className}
    >
        <path d="M21 12a9 9 0 1 1-6.219-8.56" />
    </svg>
)
