'use client'

import { useState } from 'react'
import Link from 'next/link'
import { ApplicationStatus } from '@/types/admissions'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow
} from '@/components/ui/table'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { Alert, AlertDescription } from '@/components/ui/alert'
import {
    Users,
    CreditCard,
    CheckCircle,
    FileText,
    Eye,
    Check,
    AlertCircle
} from 'lucide-react'
import { useToast } from '@/hooks/use-toast'
import { useAdmissions, useConfirmAdmission } from '@/hooks/use-admissions'
import admissionApi from '@/services/admission-api'
import AddOfflineApplicationDialog from '@/components/admissions/AddOfflineApplicationDialog'

export default function AdmissionsDashboard() {
    const { toast } = useToast()
    const [filterStatus, setFilterStatus] = useState<ApplicationStatus | undefined>()
    const [dialogOpen, setDialogOpen] = useState(false)

    // Form setup for inline adding (optional, or pass to dialog)
    // For now, we are keeping the existing structure but preparing for the dialog integration
    // The AddOfflineApplicationDialog should be the one using the schema mostly.

    const { data: applications, isLoading, error } = useAdmissions({
        status: filterStatus,
    })

    const confirmMutation = useConfirmAdmission()

    const stats = {
        total: applications?.length || 0,
        pending_payment: applications?.filter(a => a.status === ApplicationStatus.PENDING_PAYMENT).length || 0,
        paid: applications?.filter(a => a.status === ApplicationStatus.PAID).length || 0,
        completed: applications?.filter(a => a.status === ApplicationStatus.FORM_COMPLETED).length || 0,
        admitted: applications?.filter(a => a.status === ApplicationStatus.ADMITTED).length || 0,
    }

    const handleConfirm = async (id: number) => {
        try {
            await confirmMutation.mutateAsync(id)
            toast({
                title: "Admission Confirmed",
                description: "Student profile and user account have been created.",
            })
        } catch (error) {
            toast({
                title: "Error",
                description: "Failed to confirm admission.",
                variant: "destructive"
            })
        }
    }

    const handleVerifyPayment = async (id: number) => {
        if (!confirm("Are you sure you want to verify this offline payment? This will create a student account and send credentials.")) return;
        
        try {
            await admissionApi.verifyOfflinePayment(id, true)
            toast({
                title: "Payment Verified",
                description: "Payment marked as paid and credentials sent.",
            })
            // Ideally we should refetch data here. Assuming useAdmissions uses react-query and we can invalidate queries or just reload for now.
            window.location.reload() 
        } catch (error) {
            toast({
                title: "Error",
                description: "Failed to verify payment.",
                variant: "destructive"
            })
        }
    }

    const getStatusColor = (status: ApplicationStatus): "success" | "warning" | "danger" | "info" | "default" => {
        switch (status) {
            case ApplicationStatus.ADMITTED: return "success"
            case ApplicationStatus.PAID: return "info"
            case ApplicationStatus.PENDING_PAYMENT: return "warning"
            case ApplicationStatus.REJECTED: return "danger"
            default: return "default"
        }
    }

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-3xl font-bold">Admissions Dashboard</h1>
                <div className="space-x-2">
                    <Button variant="outline" size="sm">Export Data</Button>
                    <Button size="sm" onClick={() => setDialogOpen(true)}>Add Offline Application</Button>
                </div>
            </div>

            <AddOfflineApplicationDialog open={dialogOpen} onOpenChange={setDialogOpen} />

            {/* Summary Stats */}
            {isLoading ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    {[...Array(4)].map((_, i) => (
                        <Card key={i}>
                            <CardHeader className="pb-2">
                                <Skeleton className="h-4 w-24" />
                            </CardHeader>
                            <CardContent>
                                <Skeleton className="h-8 w-16" />
                            </CardContent>
                        </Card>
                    ))}
                </div>
            ) : error ? (
                <Alert variant="destructive">
                    <AlertCircle className="h-4 w-4" />
                    <AlertDescription>
                        Failed to load admissions data. Please try again later.
                    </AlertDescription>
                </Alert>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between pb-2">
                            <CardTitle className="text-sm font-medium">Total Apps</CardTitle>
                            <Users className="h-4 w-4 text-muted-foreground" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">{stats.total}</div>
                        </CardContent>
                    </Card>
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between pb-2">
                            <CardTitle className="text-sm font-medium">Paid (Leads)</CardTitle>
                            <CreditCard className="h-4 w-4 text-blue-600" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">{stats.paid}</div>
                        </CardContent>
                    </Card>
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between pb-2">
                            <CardTitle className="text-sm font-medium">Form Completed</CardTitle>
                            <FileText className="h-4 w-4 text-orange-600" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">{stats.completed}</div>
                        </CardContent>
                    </Card>
                    <Card>
                        <CardHeader className="flex flex-row items-center justify-between pb-2">
                            <CardTitle className="text-sm font-medium">Admitted</CardTitle>
                            <CheckCircle className="h-4 w-4 text-green-600" />
                        </CardHeader>
                        <CardContent>
                            <div className="text-2xl font-bold">{stats.admitted}</div>
                        </CardContent>
                    </Card>
                </div>
            )}

            {/* Applications Table */}
            <Card>
                <CardHeader>
                    <CardTitle>Recent Applications</CardTitle>
                </CardHeader>
                <CardContent>
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>App #</TableHead>
                                <TableHead>Name</TableHead>
                                <TableHead>Program</TableHead>
                                <TableHead>Date</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {isLoading ? (
                                <TableRow><TableCell colSpan={6} className="text-center">Loading...</TableCell></TableRow>
                            ) : applications?.length === 0 ? (
                                <TableRow><TableCell colSpan={6} className="text-center">No applications found.</TableCell></TableRow>
                            ) : (
                                applications?.map((app) => (
                                    <TableRow key={app.id}>
                                        <TableCell className="font-medium">{app.application_number}</TableCell>
                                        <TableCell>
                                            <div className="flex flex-col">
                                                <span>{app.name}</span>
                                                <span className="text-xs text-muted-foreground">{app.email}</span>
                                            </div>
                                        </TableCell>
                                        <TableCell>Program ID: {app.program_id}</TableCell>
                                        <TableCell>{new Date(app.created_at).toLocaleDateString()}</TableCell>
                                        <TableCell>
                                            <Badge variant={getStatusColor(app.status) as any}>
                                                {app.status.replace('_', ' ')}
                                            </Badge>
                                        </TableCell>
                                        <TableCell className="text-right space-x-2">
                                            <Link href={`/admissions/${app.id}`}>
                                                <Button variant="outline" size="sm" title="View Details" className="h-8 w-8 p-0">
                                                    <Eye className="h-4 w-4" />
                                                </Button>
                                            </Link>
                                            {app.status === ApplicationStatus.FORM_COMPLETED && (
                                                <Button
                                                    variant="outline"
                                                    size="sm"
                                                    className="text-green-600 h-8 w-8 p-0"
                                                    title="Confirm Admission"
                                                    onClick={() => handleConfirm(app.id)}
                                                    disabled={confirmMutation.isPending}
                                                >
                                                    <Check className="h-4 w-4" />
                                                </Button>
                                            )}
                                            {app.status === ApplicationStatus.PENDING_PAYMENT && (
                                                <Button
                                                    variant="outline"
                                                    size="sm"
                                                    className="text-blue-600 h-8 w-8 p-0"
                                                    title="Verify Payment (Offline)"
                                                    onClick={() => handleVerifyPayment(app.id)}
                                                >
                                                    <CreditCard className="h-4 w-4" />
                                                </Button>
                                            )}
                                        </TableCell>
                                    </TableRow>
                                ))
                            )}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    )
}
