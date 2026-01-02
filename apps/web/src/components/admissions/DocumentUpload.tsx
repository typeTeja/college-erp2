'use client'

import { useState } from 'react'
import { admissionsService } from '@/utils/admissions-service'
import { DocumentType, DocumentStatus } from '@/types/admissions'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { useToast } from '@/hooks/use-toast'
import { Upload, FileText, CheckCircle, XCircle, Clock } from 'lucide-react'

interface DocumentUploadProps {
    applicationId: number
}

const DOCUMENT_TYPE_LABELS: Record<DocumentType, string> = {
    [DocumentType.PHOTO]: "Passport Photo",
    [DocumentType.AADHAAR]: "Aadhaar Card",
    [DocumentType.TENTH_MARKSHEET]: "10th Marksheet",
    [DocumentType.TWELFTH_MARKSHEET]: "12th Marksheet",
    [DocumentType.MIGRATION_CERTIFICATE]: "Migration Certificate",
    [DocumentType.TRANSFER_CERTIFICATE]: "Transfer Certificate",
    [DocumentType.CASTE_CERTIFICATE]: "Caste Certificate",
    [DocumentType.INCOME_CERTIFICATE]: "Income Certificate",
    [DocumentType.OTHER]: "Other Document"
}

export default function DocumentUpload({ applicationId }: DocumentUploadProps) {
    const { toast } = useToast()
    const [selectedType, setSelectedType] = useState<DocumentType | "">("")
    const [selectedFile, setSelectedFile] = useState<File | null>(null)

    const { data: documents, isLoading } = admissionsService.useDocuments(applicationId)
    const uploadMutation = admissionsService.useUploadDocument(applicationId)

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setSelectedFile(e.target.files[0])
        }
    }

    const handleUpload = async () => {
        if (!selectedType || !selectedFile) {
            toast({
                title: "Error",
                description: "Please select document type and file",
                variant: "destructive"
            })
            return
        }

        try {
            await uploadMutation.mutateAsync({
                documentType: selectedType as DocumentType,
                file: selectedFile
            })

            toast({
                title: "Success",
                description: "Document uploaded successfully"
            })

            // Reset form
            setSelectedType("")
            setSelectedFile(null)
            // Reset file input
            const fileInput = document.getElementById('file-input') as HTMLInputElement
            if (fileInput) fileInput.value = ''
        } catch (error: any) {
            toast({
                title: "Error",
                description: error.response?.data?.detail || "Failed to upload document",
                variant: "destructive"
            })
        }
    }

    const getStatusIcon = (status: DocumentStatus) => {
        switch (status) {
            case DocumentStatus.VERIFIED:
                return <CheckCircle className="h-4 w-4 text-green-600" />
            case DocumentStatus.REJECTED:
                return <XCircle className="h-4 w-4 text-red-600" />
            case DocumentStatus.UPLOADED:
                return <Clock className="h-4 w-4 text-yellow-600" />
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

    return (
        <div className="space-y-6">
            {/* Upload Form */}
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Upload className="h-5 w-5" />
                        Upload Document
                    </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="space-y-2">
                        <Label>Document Type</Label>
                        <Select value={selectedType} onValueChange={(v) => setSelectedType(v as DocumentType)}>
                            <SelectTrigger>
                                <SelectValue placeholder="Select document type" />
                            </SelectTrigger>
                            <SelectContent>
                                {Object.entries(DOCUMENT_TYPE_LABELS).map(([key, label]) => (
                                    <SelectItem key={key} value={key}>
                                        {label}
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>

                    <div className="space-y-2">
                        <Label htmlFor="file-input">Choose File</Label>
                        <Input
                            id="file-input"
                            type="file"
                            accept=".pdf,.jpg,.jpeg,.png,.doc,.docx"
                            onChange={handleFileChange}
                        />
                        {selectedFile && (
                            <p className="text-sm text-muted-foreground">
                                Selected: {selectedFile.name} ({(selectedFile.size / 1024).toFixed(2)} KB)
                            </p>
                        )}
                    </div>

                    <Button
                        onClick={handleUpload}
                        disabled={!selectedType || !selectedFile || uploadMutation.isPending}
                        className="w-full"
                    >
                        {uploadMutation.isPending ? "Uploading..." : "Upload Document"}
                    </Button>
                </CardContent>
            </Card>

            {/* Documents List */}
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <FileText className="h-5 w-5" />
                        Uploaded Documents
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    {isLoading ? (
                        <p className="text-center text-muted-foreground">Loading documents...</p>
                    ) : documents && documents.length > 0 ? (
                        <div className="space-y-3">
                            {documents.map((doc) => (
                                <div
                                    key={doc.id}
                                    className="flex items-center justify-between p-3 border rounded-lg"
                                >
                                    <div className="flex-1">
                                        <div className="flex items-center gap-2">
                                            {getStatusIcon(doc.status)}
                                            <p className="font-medium">
                                                {DOCUMENT_TYPE_LABELS[doc.document_type]}
                                            </p>
                                        </div>
                                        <p className="text-sm text-muted-foreground mt-1">
                                            {doc.file_name} • {(doc.file_size / 1024).toFixed(2)} KB
                                        </p>
                                        {doc.rejection_reason && (
                                            <p className="text-sm text-red-600 mt-1">
                                                Reason: {doc.rejection_reason}
                                            </p>
                                        )}
                                    </div>
                                    <Badge variant={getStatusColor(doc.status)}>
                                        {doc.status}
                                    </Badge>
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
        </div>
    )
}
