'use client'

import { admissionsService } from '@/utils/admissions-service'
import { DocumentStatus } from '@/types/admissions'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Badge } from '@/components/ui/badge'
import { Textarea } from '@/components/ui/textarea'
import { useToast } from '@/hooks/use-toast'
import { CheckCircle, XCircle, FileText, Eye } from 'lucide-react'
import { useState } from 'react'

interface DocumentVerificationProps {
    applicationId: number
}

const DOCUMENT_TYPE_LABELS: Record<string, string> = {
    "PHOTO": "Passport Photo",
    "AADHAAR": "Aadhaar Card",
    "TENTH_MARKSHEET": "10th Marksheet",
    "TWELFTH_MARKSHEET": "12th Marksheet",
    "MIGRATION_CERTIFICATE": "Migration Certificate",
    "TRANSFER_CERTIFICATE": "Transfer Certificate",
    "CASTE_CERTIFICATE": "Caste Certificate",
    "INCOME_CERTIFICATE": "Income Certificate",
    "OTHER": "Other Document"
}

export default function DocumentVerification({ applicationId }: DocumentVerificationProps) {
    const { toast } = useToast()
    const [rejectionReasons, setRejectionReasons] = useState<Record<number, string>>({})

    const { data: documents, isLoading } = admissionsService.useDocuments(applicationId)
    const verifyMutation = admissionsService.useVerifyDocument()

    const handleVerify = async (docId: number, status: DocumentStatus) => {
        try {
            await verifyMutation.mutateAsync({
                docId,
                data: {
                    status,
                    rejection_reason: status === DocumentStatus.REJECTED ? rejectionReasons[docId] : undefined
                }
            })

            toast({
                title: "Success",
                description: `Document ${status === DocumentStatus.VERIFIED ? 'verified' : 'rejected'} successfully`
            })

            // Clear rejection reason
            if (status === DocumentStatus.REJECTED) {
                setRejectionReasons(prev => {
                    const newReasons = { ...prev }
                    delete newReasons[docId]
                    return newReasons
                })
            }
        } catch (error: any) {
            toast({
                title: "Error",
                description: error.response?.data?.detail || "Failed to update document status",
                variant: "destructive"
            })
        }
    }

    const getStatusColor = (status: DocumentStatus): "default" | "success" | "destructive" | "secondary" => {
        switch (status) {
            case DocumentStatus.VERIFIED:
                return "success"
            case DocumentStatus.REJECTED:
                return "destructive"
            case DocumentStatus.UPLOADED:
                return "secondary"
            default:
                return "default"
        }
    }

    const [viewingDoc, setViewingDoc] = useState<{ url: string, type: string, name: string } | null>(null)

    return (
        <>
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <FileText className="h-5 w-5" />
                        Document Verification
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    {isLoading ? (
                        <p className="text-center text-muted-foreground">Loading documents...</p>
                    ) : documents && documents.length > 0 ? (
                        <div className="space-y-4">
                            {documents.map((doc) => (
                                <div
                                    key={doc.id}
                                    className="p-4 border rounded-lg space-y-3"
                                >
                                    <div className="flex items-start justify-between">
                                        <div className="flex-1">
                                            <div className="flex items-center gap-2">
                                                <p className="font-medium">
                                                    {DOCUMENT_TYPE_LABELS[doc.document_type] || doc.document_type}
                                                </p>
                                                <Badge variant={getStatusColor(doc.status)}>
                                                    {doc.status}
                                                </Badge>
                                            </div>
                                            <p className="text-sm text-muted-foreground mt-1">
                                                {doc.file_name} • {(doc.file_size / 1024).toFixed(2)} KB
                                            </p>
                                            <p className="text-xs text-muted-foreground mt-1">
                                                Uploaded: {new Date(doc.uploaded_at).toLocaleString()}
                                            </p>
                                            {doc.file_url && (
                                                <Button
                                                    variant="link"
                                                    size="sm"
                                                    className="h-auto p-0 mt-1 text-blue-600"
                                                    onClick={() => setViewingDoc({
                                                        url: doc.file_url,
                                                        type: doc.file_name.toLowerCase().endsWith('.pdf') ? 'pdf' : 'image',
                                                        name: DOCUMENT_TYPE_LABELS[doc.document_type] || doc.document_type
                                                    })}
                                                >
                                                    <Eye className="h-3 w-3 mr-1" />
                                                    View Document
                                                </Button>
                                            )}
                                            {doc.verified_at && (
                                                <p className="text-xs text-muted-foreground">
                                                    Verified: {new Date(doc.verified_at).toLocaleString()}
                                                </p>
                                            )}
                                            {doc.rejection_reason && (
                                                <p className="text-sm text-red-600 mt-2">
                                                    <strong>Rejection Reason:</strong> {doc.rejection_reason}
                                                </p>
                                            )}
                                        </div>
                                    </div>

                                    {doc.status === DocumentStatus.UPLOADED && (
                                        <div className="space-y-3 pt-3 border-t">
                                            <Textarea
                                                placeholder="Rejection reason (if rejecting)..."
                                                value={rejectionReasons[doc.id] || ""}
                                                onChange={(e) => setRejectionReasons(prev => ({
                                                    ...prev,
                                                    [doc.id]: e.target.value
                                                }))}
                                                rows={2}
                                            />
                                            <div className="flex gap-2">
                                                <Button
                                                    size="sm"
                                                    variant="outline"
                                                    className="flex-1 text-green-600 border-green-600 hover:bg-green-50"
                                                    onClick={() => handleVerify(doc.id, DocumentStatus.VERIFIED)}
                                                    disabled={verifyMutation.isPending}
                                                >
                                                    <CheckCircle className="h-4 w-4 mr-2" />
                                                    Verify
                                                </Button>
                                                <Button
                                                    size="sm"
                                                    variant="outline"
                                                    className="flex-1 text-red-600 border-red-600 hover:bg-red-50"
                                                    onClick={() => handleVerify(doc.id, DocumentStatus.REJECTED)}
                                                    disabled={verifyMutation.isPending || !rejectionReasons[doc.id]}
                                                >
                                                    <XCircle className="h-4 w-4 mr-2" />
                                                    Reject
                                                </Button>
                                            </div>
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    ) : (
                        <p className="text-center text-muted-foreground py-8">
                            No documents uploaded yet
                        </p>
                    )}
                </CardContent>
            </Card>

            <Dialog open={!!viewingDoc} onOpenChange={(open) => !open && setViewingDoc(null)}>
                <DialogContent className="max-w-4xl h-[80vh]">
                    <DialogHeader>
                        <DialogTitle>{viewingDoc?.name}</DialogTitle>
                    </DialogHeader>
                    <div className="flex-1 h-full min-h-0 bg-slate-100 rounded-md overflow-hidden flex items-center justify-center relative">
                        {viewingDoc?.type === 'pdf' ? (
                            <iframe
                                src={viewingDoc.url}
                                className="w-full h-full"
                                title={viewingDoc.name}
                            />
                        ) : viewingDoc ? (
                            // eslint-disable-next-line @next/next/no-img-element
                            <img
                                src={viewingDoc.url}
                                alt={viewingDoc.name}
                                className="max-w-full max-h-full object-contain"
                            />
                        ) : null}
                    </div>
                </DialogContent>
            </Dialog>
        </>
    )
}
