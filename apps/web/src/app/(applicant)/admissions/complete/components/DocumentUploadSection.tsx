'use client'

import { useState } from 'react'
import { useFormContext, useWatch } from 'react-hook-form'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { admissionApi } from '@/services/admission-api'
import { DocumentType, CasteCategory } from '@/types/admissions'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import { Card, CardContent } from '@/components/ui/card'
import { Loader2, UploadCloud, CheckCircle, FileText, XCircle } from 'lucide-react'
import { useToast } from '@/hooks/use-toast'

interface DocumentUploadSectionProps {
    applicationId: number;
    existingDocuments?: any[];
}

export function DocumentUploadSection({ applicationId, existingDocuments = [] }: DocumentUploadSectionProps) {
    const { control } = useFormContext()
    const { toast } = useToast()
    const queryClient = useQueryClient()
    const casteCategory = useWatch({ control, name: 'caste_category' })

    // Define required documents based on rules
    const requiredDocs = [
        { type: DocumentType.PHOTO, label: 'Candidate Photo', required: true },
        { type: DocumentType.AADHAAR, label: 'Aadhaar Card', required: true },
        { type: DocumentType.TENTH_MARKSHEET, label: 'SSC / 10th Marksheet', required: true },
        { type: DocumentType.TWELFTH_MARKSHEET, label: 'Intermediate / 12th Marksheet', required: true },
        { type: DocumentType.TRANSFER_CERTIFICATE, label: 'Transfer Certificate', required: true },
        { type: DocumentType.CONDUCT_CERTIFICATE, label: 'Conduct Certificate', required: true },
    ]

    // Add Caste Certificate if not General/OC
    if (casteCategory && casteCategory !== CasteCategory.GENERAL && casteCategory !== CasteCategory.OC) {
        requiredDocs.push({ type: DocumentType.CASTE_CERTIFICATE, label: 'Caste Certificate', required: true })
    }

    // Include other optional docs
    requiredDocs.push({ type: DocumentType.INCOME_CERTIFICATE, label: 'Income Certificate', required: false })
    requiredDocs.push({ type: DocumentType.MIGRATION_CERTIFICATE, label: 'Migration Certificate (if applicable)', required: false })

    const uploadMutation = useMutation({
        mutationFn: ({ file, type }: { file: File, type: DocumentType }) =>
            admissionApi.uploadDocument(applicationId, file, type),
        onSuccess: () => {
            toast({ title: "Upload Successful", description: "Document uploaded successfully." })
            queryClient.invalidateQueries({ queryKey: ['my-application'] })
        },
        onError: (err: any) => {
            toast({
                title: "Upload Failed",
                description: err.response?.data?.detail || "Failed to upload document",
                variant: "destructive"
            })
        }
    })

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>, type: DocumentType) => {
        const file = e.target.files?.[0]
        if (!file) return

        // Validate size (e.g. 5MB)
        if (file.size > 5 * 1024 * 1024) {
            toast({ title: "File too large", description: "Max file size is 5MB", variant: "destructive" })
            return
        }

        uploadMutation.mutate({ file, type })
    }

    const getDocStatus = (type: DocumentType) => {
        const doc = existingDocuments.find(d => d.document_type === type)
        return doc
    }

    return (
        <div className="space-y-6">
            <h3 className="text-lg font-semibold text-gray-900 border-b pb-2">
                Document Uploads
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {requiredDocs.map((docConfig) => {
                    const existingDoc = getDocStatus(docConfig.type)
                    const isUploading = uploadMutation.isPending && uploadMutation.variables?.type === docConfig.type

                    return (
                        <Card key={docConfig.type} className={existingDoc ? "bg-green-50 border-green-200" : ""}>
                            <CardContent className="p-4">
                                <div className="flex justify-between items-start mb-2">
                                    <Label className="text-base font-medium">
                                        {docConfig.label} {docConfig.required && <span className="text-red-500">*</span>}
                                    </Label>
                                    {existingDoc ? (
                                        <CheckCircle className="h-5 w-5 text-green-600" />
                                    ) : (
                                        <FileText className="h-5 w-5 text-gray-400" />
                                    )}
                                </div>

                                {existingDoc ? (
                                    <div className="text-sm text-green-700 mb-2">
                                        <span className="font-medium">Uploaded:</span> {existingDoc.file_name}
                                        <br />
                                        <a href={existingDoc.file_url} target="_blank" rel="noopener noreferrer" className="underline hover:text-green-900">
                                            View Document
                                        </a>
                                    </div>
                                ) : (
                                    <p className="text-xs text-gray-500 mb-2">Supported: JPG, PNG, PDF (Max 5MB)</p>
                                )}

                                <div className="mt-2">
                                    <Label htmlFor={`file-${docConfig.type}`} className="cursor-pointer">
                                        <div className="flex items-center justify-center w-full h-10 px-4 py-2 bg-white border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50">
                                            {isUploading ? (
                                                <Loader2 className="h-4 w-4 animate-spin mr-2" />
                                            ) : (
                                                <UploadCloud className="h-4 w-4 mr-2" />
                                            )}
                                            {existingDoc ? "Replace File" : "Upload File"}
                                        </div>
                                    </Label>
                                    <Input
                                        id={`file-${docConfig.type}`}
                                        type="file"
                                        accept=".jpg,.jpeg,.png,.pdf"
                                        className="hidden"
                                        onChange={(e) => handleFileChange(e, docConfig.type)}
                                        disabled={isUploading}
                                    />
                                </div>
                            </CardContent>
                        </Card>
                    )
                })}
            </div>
        </div>
    )
}
