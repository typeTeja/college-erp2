'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useForm, FormProvider, SubmitHandler } from 'react-hook-form'
import { admissionApi } from '@/services/admission-api'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { useToast } from '@/hooks/use-toast'
import { ArrowLeft, CheckCircle, Loader2, ChevronRight, ChevronLeft } from 'lucide-react'
import Link from 'next/link'
import { ApplicationCompleteSubmit, AddressType, EducationLevel, EducationBoard, ParentRelation } from '@/types/admissions'

// Components
import { PersonalDetailsForm } from './components/PersonalDetailsForm'
import { ParentDetailsForm } from './components/ParentDetailsForm'
import { AddressDetailsForm } from './components/AddressDetailsForm'
import { EducationDetailsForm } from './components/EducationDetailsForm'
import { BankHealthForm } from './components/BankHealthForm'
import { DocumentUploadSection } from './components/DocumentUploadSection'
import { DeclarationForm } from './components/DeclarationForm'

const STEPS = [
    { id: 'personal', title: 'Personal Details' },
    { id: 'parent', title: 'Parent Details' },
    { id: 'address', title: 'Address Details' },
    { id: 'education', title: 'Education' },
    { id: 'bank_health', title: 'Bank & Health' },
    { id: 'documents', title: 'Documents' },
    { id: 'declaration', title: 'Review & Submit' }
]

export default function CompleteApplicationPage() {
    const router = useRouter()
    const { toast } = useToast()
    const queryClient = useQueryClient()
    const [currentStep, setCurrentStep] = useState(0)

    // Fetch current application
    const { data: application, isLoading } = useQuery({
        queryKey: ['my-application'],
        queryFn: () => admissionApi.getMyApplication(),
    })

    // Initial Form State
    const methods = useForm<ApplicationCompleteSubmit>({
        mode: 'onChange',
        defaultValues: {
            parents: [],
            addresses: [
                { address_type: AddressType.PERMANENT, address_line1: '', city: '', state: '', district: '', pincode: '' },
                { address_type: AddressType.CURRENT, address_line1: '', city: '', state: '', district: '', pincode: '' }
            ],
            education: [],
            student_declaration_accepted: false,
            parent_declaration_accepted: false
        }
    })

    const { reset, trigger, handleSubmit, formState: { isSubmitting } } = methods

    // Populate form when data loads
    useEffect(() => {
        if (application) {
            // Transform application data to form structure if needed
            // Ideally, backend returns nulls/empty arrays if not filled.
            // We merge with defaults to ensure arrays exist.

            const defaultParents = application.parents && application.parents.length > 0
                ? application.parents
                : [{ relation: ParentRelation.FATHER, name: application.father_name || '', mobile: application.father_phone || '', is_primary_contact: true }]

            const defaultEducation = application.education && application.education.length > 0
                ? application.education
                : [{ level: EducationLevel.SSC, institution_name: '', percentage: 0, board: EducationBoard.STATE_BOARD }]

            reset({
                ...application, // Spread existing fields
                parents: defaultParents,
                addresses: application.addresses && application.addresses.length > 0 ? application.addresses : [
                    { address_type: AddressType.PERMANENT, address_line1: application.address || '', city: '', state: '', district: '', pincode: '' },
                    { address_type: AddressType.CURRENT, address_line1: '', city: '', state: '', district: '', pincode: '' }
                ],
                education: defaultEducation,
                bank_details: application.bank_details || {},
                health_details: application.health_details || {},
                // Maintain legacy mappings if new fields are empty
                aadhaar_number: application.aadhaar_number,
            } as any)
        }
    }, [application, reset])


    // Complete application mutation
    const completeMutation = useMutation({
        mutationFn: (data: ApplicationCompleteSubmit) => admissionApi.completeMyApplication(data),
        onSuccess: () => {
            toast({
                title: "Application Submitted!",
                description: "Your application is now under review.",
            })
            queryClient.invalidateQueries({ queryKey: ['my-application'] })
            router.push('/')
        },
        onError: (error: any) => {
            toast({
                title: "Submission Failed",
                description: error.response?.data?.detail || "Please check all fields and try again.",
                variant: "destructive"
            })
        }
    })

    const onSubmit: SubmitHandler<ApplicationCompleteSubmit> = (data) => {
        completeMutation.mutate(data)
    }

    const handleNext = async () => {
        let isValid = false

        // Validate current step fields
        switch (currentStep) {
            case 0: // Personal
                isValid = await trigger(['aadhaar_number', 'date_of_birth', 'gender', 'nationality', 'religion', 'caste_category'])
                break
            case 1: // Parent
                isValid = await trigger('parents')
                break
            case 2: // Address
                isValid = await trigger('addresses')
                break
            case 3: // Education
                isValid = await trigger('education')
                break
            case 4: // Bank/Health
                // Bank and Health are mostly optional, but check if needed
                isValid = true
                break
            case 5: // Docs
                // Docs upload is handled independently. We assume if they proceed, they are done. 
                // Could check required docs here if we had access to the list from the component state.
                // For now, allow proceed.
                isValid = true
                break
            case 6: // Declaration
                isValid = await trigger(['student_declaration_accepted', 'parent_declaration_accepted'])
                break
        }

        if (isValid) {
            setCurrentStep(prev => prev + 1)
            window.scrollTo(0, 0)
        }
    }

    const handleBack = () => {
        setCurrentStep(prev => prev - 1)
        window.scrollTo(0, 0)
    }

    // Render Steps
    const renderStepContent = () => {
        switch (currentStep) {
            case 0: return <PersonalDetailsForm />
            case 1: return <ParentDetailsForm />
            case 2: return <AddressDetailsForm />
            case 3: return <EducationDetailsForm />
            case 4: return <BankHealthForm />
            case 5: return <DocumentUploadSection applicationId={application?.id!} existingDocuments={application?.documents} />
            case 6: return <DeclarationForm />
            default: return null
        }
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

    // Already Completed Check
    if (['FORM_COMPLETED', 'UNDER_REVIEW', 'APPROVED', 'ADMITTED'].includes(application.status)) {
        return (
            <Card className="max-w-2xl mx-auto mt-8">
                <CardHeader className="text-center">
                    <CheckCircle className="h-16 w-16 text-green-600 mx-auto mb-4" />
                    <CardTitle>Application Submitted</CardTitle>
                    <CardDescription>
                        Your application {application.application_number} is under review.
                    </CardDescription>
                </CardHeader>
                <CardContent className="text-center">
                    <Link href="/">
                        <Button>Back to Dashboard</Button>
                    </Link>
                </CardContent>
            </Card>
        )
    }

    return (
        <div className="max-w-5xl mx-auto py-8 px-4">
            {/* Header */}
            <div className="flex items-center justify-between mb-8">
                <div>
                    <Link href="/">
                        <Button variant="ghost" className="mb-2 pl-0 hover:pl-0 hover:bg-transparent">
                            <ArrowLeft className="h-4 w-4 mr-2" />
                            Back to Dashboard
                        </Button>
                    </Link>
                    <h1 className="text-2xl font-bold text-gray-900">Application Form</h1>
                    <p className="text-gray-500">Application No: {application.application_number}</p>
                </div>
                <div className="text-right">
                    <div className="text-sm font-medium text-blue-600">Step {currentStep + 1} of {STEPS.length}</div>
                    <div className="text-gray-900 font-semibold">{STEPS[currentStep].title}</div>
                </div>
            </div>

            {/* Stepper Progress */}
            <div className="w-full bg-gray-200 h-2 rounded-full mb-8">
                <div
                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${((currentStep + 1) / STEPS.length) * 100}%` }}
                ></div>
            </div>

            <FormProvider {...methods}>
                <form onSubmit={handleSubmit(onSubmit)}>
                    <Card className="min-h-[400px]">
                        <CardContent className="pt-6">
                            {renderStepContent()}
                        </CardContent>
                    </Card>

                    {/* Navigation Buttons */}
                    <div className="flex justify-between mt-6">
                        <Button
                            type="button"
                            variant="outline"
                            onClick={handleBack}
                            disabled={currentStep === 0 || isSubmitting}
                        >
                            <ChevronLeft className="h-4 w-4 mr-2" />
                            Previous
                        </Button>

                        {currentStep < STEPS.length - 1 ? (
                            <Button
                                type="button"
                                onClick={handleNext}
                                className="bg-blue-600 hover:bg-blue-700"
                            >
                                Next
                                <ChevronRight className="h-4 w-4 ml-2" />
                            </Button>
                        ) : (
                            <Button
                                type="submit"
                                className="bg-green-600 hover:bg-green-700"
                                disabled={isSubmitting || completeMutation.isPending}
                            >
                                {completeMutation.isPending ? (
                                    <>
                                        <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                                        Submitting...
                                    </>
                                ) : (
                                    <>
                                        Submit Application
                                        <CheckCircle className="h-4 w-4 ml-2" />
                                    </>
                                )}
                            </Button>
                        )}
                    </div>
                </form>
            </FormProvider>
        </div>
    )
}
