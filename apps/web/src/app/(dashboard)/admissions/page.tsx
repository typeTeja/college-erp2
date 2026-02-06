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
    AlertCircle,
    CheckCircle2, // New import
    XCircle, // New import
    Clock // New import
} from 'lucide-react'
import { Switch } from '@/components/ui/switch'
import { Label } from '@/components/ui/label'
import { Trash2, RotateCcw } from 'lucide-react'
import { useToast } from '@/hooks/use-toast'
import { useAdmissions, useConfirmAdmission, useDeleteApplication, useRestoreApplication } from '@/hooks/use-admissions'
import admissionApi from '@/services/admission-api'
import AddOfflineApplicationDialog from '@/components/admissions/AddOfflineApplicationDialog'
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Input } from "@/components/ui/input"

export default function AdmissionsDashboard() {
    const { toast } = useToast()
    const [filterStatus, setFilterStatus] = useState<ApplicationStatus | undefined>()
    const [showDeleted, setShowDeleted] = useState(false)
    const [dialogOpen, setDialogOpen] = useState(false)

    // Verification Dialog State
    const [verifyDialogOpen, setVerifyDialogOpen] = useState(false)
    const [verifyingId, setVerifyingId] = useState<number | null>(null)
    const [verifyMode, setVerifyMode] = useState<'CASH' | 'ONLINE'>('CASH')
    const [verifyTxnId, setVerifyTxnId] = useState('')

    // Form setup for inline adding (optional, or pass to dialog)
    // For now, we are keeping the existing structure but preparing for the dialog integration
    // The AddOfflineApplicationDialog should be the one using the schema mostly.

    const { data: applications, isLoading, error } = useAdmissions({
        status: filterStatus,
        show_deleted: showDeleted
    })

    const confirmMutation = useConfirmAdmission()
    const deleteMutation = useDeleteApplication()
    const restoreMutation = useRestoreApplication()

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

    const handleDelete = async (id: number) => {
        if (!confirm("Are you sure you want to delete this application?")) return;
        try {
            await deleteMutation.mutateAsync({ id, reason: "Admin UI Deletion" })
            toast({
                title: "Application Deleted",
                description: "Application moved to trash.",
            })
        } catch (error) {
            toast({
                title: "Error",
                description: "Failed to delete application.",
                variant: "destructive"
            })
        }
    }

    const handleRestore = async (id: number) => {
        try {
            await restoreMutation.mutateAsync(id)
            toast({
                title: "Application Restored",
                description: "Application restored from trash.",
            })
        } catch (error) {
            toast({
                title: "Error",
                description: "Failed to restore application.",
                variant: "destructive"
            })
        }
    }

    const handleVerifyClick = (id: number) => {
        setVerifyingId(id)
        setVerifyMode('CASH')
        setVerifyTxnId('')
        setVerifyDialogOpen(true)
    }

    const handleConfirmVerify = async () => {
        if (!verifyingId) return;
        if (verifyMode === 'ONLINE' && !verifyTxnId) {
            toast({ title: "Error", description: "Transaction ID is required for online payment.", variant: "destructive" })
            return;
        }

        try {
            await admissionApi.verifyOfflinePayment(verifyingId, {
                verified: true,
                mode: verifyMode as any,
                transaction_id: verifyTxnId
            })
            toast({
                title: "Payment Verified",
                description: "Payment marked as paid and credentials sent.",
            })
            setVerifyDialogOpen(false)
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
                <div className="space-x-2 flex items-center">
                    <div className="flex items-center space-x-2 mr-4">
                        <Switch id="show-trash" checked={showDeleted} onCheckedChange={setShowDeleted} />
                        <Label htmlFor="show-trash">Show Trash</Label>
                    </div>
                    <Button variant="outline" size="sm">Export Data</Button>
                    <Button size="sm" onClick={() => setDialogOpen(true)}>Add Offline Application</Button>
                </div>
            </div>

            <AddOfflineApplicationDialog open={dialogOpen} onOpenChange={setDialogOpen} />

            <Dialog open={verifyDialogOpen} onOpenChange={setVerifyDialogOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>Verify Offline Payment</DialogTitle>
                        <DialogDescription>
                            Confirm receipt of payment. This will activate the student account.
                        </DialogDescription>
                    </DialogHeader>
                    <div className="grid gap-4 py-4">
                        <div className="space-y-2">
                            <Label>Payment Mode</Label>
                            <RadioGroup value={verifyMode} onValueChange={(v: any) => setVerifyMode(v)}>
                                <div className="flex items-center space-x-2">
                                    <RadioGroupItem value="CASH" id="mode-cash" />
                                    <Label htmlFor="mode-cash">Cash</Label>
                                </div>
                                <div className="flex items-center space-x-2">
                                    <RadioGroupItem value="ONLINE" id="mode-online" />
                                    <Label htmlFor="mode-online">Online Transfer (UPI/NEFT)</Label>
                                </div>
                            </RadioGroup>
                        </div>
                        {verifyMode === 'ONLINE' && (
                            <div className="space-y-2">
                                <Label htmlFor="txn-id">Transaction ID / Reference No</Label>
                                <Input
                                    id="txn-id"
                                    value={verifyTxnId}
                                    onChange={(e) => setVerifyTxnId(e.target.value)}
                                    placeholder="e.g. UTR123456789"
                                />
                            </div>
                        )}
                    </div>
                    <DialogFooter>
                        <Button variant="outline" onClick={() => setVerifyDialogOpen(false)}>Cancel</Button>
                        <Button onClick={handleConfirmVerify}>Verify Payment</Button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>

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
                    <CardTitle>{showDeleted ? "Deleted Applications (Trash)" : "Recent Applications"}</CardTitle>
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
                                <TableHead>Payment</TableHead>
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
                                                <span className="text-xs text-muted-foreground">{app.phone}</span>
                                            </div>
                                        </TableCell>
                                        <TableCell>{app.program?.name || `Program ID: ${app.program_id}`}</TableCell>
                                        <TableCell>{new Date(app.created_at).toLocaleDateString()}</TableCell>
                                        <TableCell>
                                            <Badge variant={getStatusColor(app.status) as any}>
                                                {app.status.replace('_', ' ')}
                                            </Badge>
                                        </TableCell>
                                        <TableCell>
                                            <Badge variant={app.payment_status === 'SUCCESS' || app.payment_status === 'success' ? 'success' : 'outline'}>
                                                {app.payment_status?.toUpperCase() || 'PENDING'}
                                            </Badge>
                                        </TableCell>
                                        <TableCell className="text-right space-x-2">
                                            {showDeleted ? (
                                                <Button
                                                    variant="outline"
                                                    size="sm"
                                                    className="text-green-600 h-8 w-8 p-0"
                                                    title="Restore"
                                                    onClick={() => handleRestore(app.id)}
                                                >
                                                    <RotateCcw className="h-4 w-4" />
                                                </Button>
                                            ) : (
                                                <>
                                                    <Link
                                                        href={`/admissions/${app.id}`}
                                                        className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 border border-input bg-background hover:bg-accent hover:text-accent-foreground h-8 w-8 p-0"
                                                        title="View Details"
                                                    >
                                                        <Eye className="h-4 w-4" />
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
                                                    {/* Verify Payment Button - Only for Offline Pending */}
                                                    {app.status === ApplicationStatus.PENDING_PAYMENT && app.fee_mode === 'OFFLINE' && !app.offline_payment_verified && (
                                                        <Button
                                                            variant="outline"
                                                            size="sm"
                                                            className="text-green-600 border-green-200 hover:bg-green-50"
                                                            title="Verify Payment (Offline)"
                                                            onClick={() => handleVerifyClick(app.id)}
                                                        >
                                                            <CheckCircle2 className="h-4 w-4 mr-2" />
                                                            Verify Payment
                                                        </Button>
                                                    )}
                                                    {/* Soft Delete for non-admitted/paid apps */}
                                                    {app.status !== ApplicationStatus.PAID && app.status !== ApplicationStatus.ADMITTED && (
                                                        <Button
                                                            variant="outline"
                                                            size="sm"
                                                            className="text-red-600 h-8 w-8 p-0"
                                                            title="Delete"
                                                            onClick={() => handleDelete(app.id)}
                                                        >
                                                            <Trash2 className="h-4 w-4" />
                                                        </Button>
                                                    )}
                                                </>
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
