'use client'

import { useFormContext } from 'react-hook-form'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Checkbox } from '@/components/ui/checkbox'
import { Textarea } from '@/components/ui/textarea' // Using textarea for details if implemented, else Input
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { ApplicationCompleteSubmit } from '@/types/admissions'

// Helper for conditional render
const TextAreaOrInput = (props: any) => <Input {...props} /> // Fallback if Textarea not available, but usually simple Input fine for now.

export function BankHealthForm() {
    const { register, formState: { errors } } = useFormContext<ApplicationCompleteSubmit>()

    return (
        <div className="space-y-6">
            {/* Bank Details */}
            <Card>
                <CardHeader>
                    <CardTitle className="text-base font-medium">Bank Account Details</CardTitle>
                </CardHeader>
                <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                        <Label>Account Holder Name</Label>
                        <Input
                            placeholder="Name as per Passbook"
                            {...register('bank_details.account_holder_name')}
                        />
                    </div>
                    <div className="space-y-2">
                        <Label>Bank Name</Label>
                        <Input
                            placeholder="e.g. SBI, HDFC"
                            {...register('bank_details.bank_name')}
                        />
                    </div>
                    <div className="space-y-2">
                        <Label>Branch Name</Label>
                        <Input
                            placeholder="e.g. Main Branch"
                            {...register('bank_details.branch_name')}
                        />
                    </div>
                    <div className="space-y-2">
                        <Label>IFSC Code</Label>
                        <Input
                            placeholder="SBIN0001234"
                            maxLength={11}
                            className="uppercase"
                            {...register('bank_details.ifsc_code')}
                        />
                    </div>
                    <div className="md:col-span-2 space-y-2">
                        <Label>Account Number</Label>
                        <Input
                            placeholder="Enter Account Number"
                            {...register('bank_details.account_number')}
                        />
                    </div>
                </CardContent>
            </Card>

            {/* Health Details */}
            <Card>
                <CardHeader>
                    <CardTitle className="text-base font-medium">Health & Medical Record</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label>Height (cm)</Label>
                            <Input
                                type="number"
                                placeholder="e.g. 175"
                                {...register('health_details.height_cm', { valueAsNumber: true })}
                            />
                        </div>
                        <div className="space-y-2">
                            <Label>Weight (kg)</Label>
                            <Input
                                type="number"
                                placeholder="e.g. 65"
                                {...register('health_details.weight_kg', { valueAsNumber: true })}
                            />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <Label>Allergies (if any)</Label>
                        <Input
                            placeholder="e.g. Peanuts, Penicillin"
                            {...register('health_details.allergies')}
                        />
                    </div>

                    <div className="space-y-2">
                        <Label>Chronic Illness / Medical History</Label>
                        <Input
                            placeholder="Describe any chronic conditions"
                            {...register('health_details.chronic_illness_details')}
                        />
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label>Family Doctor Name</Label>
                            <Input
                                placeholder="Dr. Name"
                                {...register('health_details.doctor_name')}
                            />
                        </div>
                        <div className="space-y-2">
                            <Label>Doctor's Phone</Label>
                            <Input
                                placeholder="Emergency Contact"
                                {...register('health_details.doctor_phone')}
                            />
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
