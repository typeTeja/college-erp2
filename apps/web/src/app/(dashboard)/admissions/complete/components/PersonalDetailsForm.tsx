'use client'

import { useFormContext, Controller } from 'react-hook-form'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select'
import { BloodGroup, Religion, CasteCategory, Gender, ApplicationCompleteSubmit } from '@/types/admissions'

export function PersonalDetailsForm() {
    const { register, control, formState: { errors } } = useFormContext<ApplicationCompleteSubmit>()

    return (
        <div className="space-y-6">
            <h3 className="text-lg font-semibold text-gray-900 border-b pb-2">
                Personal Details
            </h3>

            {/* Row 1: Aadhaar & DOB */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                    <Label htmlFor="aadhaar_number">Aadhaar Number *</Label>
                    <Input
                        id="aadhaar_number"
                        placeholder="XXXX XXXX XXXX"
                        maxLength={12}
                        {...register('aadhaar_number', { required: 'Aadhaar number is required', pattern: { value: /^\d{12}$/, message: 'Must be 12 digits' } })}
                    />
                    {errors.aadhaar_number && (
                        <p className="text-sm text-red-500">{errors.aadhaar_number.message as string}</p>
                    )}
                </div>

                <div className="space-y-2">
                    <Label htmlFor="date_of_birth">Date of Birth *</Label>
                    <Input
                        id="date_of_birth"
                        type="date"
                        {...register('date_of_birth', { required: 'Date of birth is required' })}
                    />
                    {errors.date_of_birth && (
                        <p className="text-sm text-red-500">{errors.date_of_birth.message as string}</p>
                    )}
                </div>
            </div>

            {/* Row 2: Gender & Blood Group */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                    <Label htmlFor="gender">Gender *</Label>
                    <Controller
                        control={control}
                        name="gender"
                        rules={{ required: 'Gender is required' }}
                        render={({ field }) => (
                            <Select onValueChange={field.onChange} defaultValue={field.value}>
                                <SelectTrigger>
                                    <SelectValue placeholder="Select Gender" />
                                </SelectTrigger>
                                <SelectContent>
                                    {Object.values(Gender).map((g) => (
                                        <SelectItem key={g} value={g}>{g}</SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        )}
                    />
                    {errors.gender && (
                        <p className="text-sm text-red-500">{errors.gender.message as string}</p>
                    )}
                </div>

                <div className="space-y-2">
                    <Label htmlFor="blood_group">Blood Group</Label>
                    <Controller
                        control={control}
                        name="blood_group"
                        render={({ field }) => (
                            <Select onValueChange={field.onChange} defaultValue={field.value}>
                                <SelectTrigger>
                                    <SelectValue placeholder="Select Blood Group" />
                                </SelectTrigger>
                                <SelectContent>
                                    {Object.values(BloodGroup).map((bg) => (
                                        <SelectItem key={bg} value={bg}>{bg.replace('_', ' ')}</SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        )}
                    />
                </div>
            </div>

            {/* Row 3: Religion & Caste */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                    <Label htmlFor="religion">Religion</Label>
                    <Controller
                        control={control}
                        name="religion"
                        render={({ field }) => (
                            <Select onValueChange={field.onChange} defaultValue={field.value}>
                                <SelectTrigger>
                                    <SelectValue placeholder="Select Religion" />
                                </SelectTrigger>
                                <SelectContent>
                                    {Object.values(Religion).map((r) => (
                                        <SelectItem key={r} value={r}>{r.replace(/_/g, ' ')}</SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        )}
                    />
                </div>

                <div className="space-y-2">
                    <Label htmlFor="caste_category">Caste Category</Label>
                    <Controller
                        control={control}
                        name="caste_category"
                        render={({ field }) => (
                            <Select onValueChange={field.onChange} defaultValue={field.value}>
                                <SelectTrigger>
                                    <SelectValue placeholder="Select Category" />
                                </SelectTrigger>
                                <SelectContent>
                                    {Object.values(CasteCategory).map((c) => (
                                        <SelectItem key={c} value={c}>{c.replace(/_/g, ' ')}</SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        )}
                    />
                </div>
            </div>

            {/* Row 4: Nationality & Mother Tongue */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                    <Label htmlFor="nationality">Nationality *</Label>
                    <Input
                        id="nationality"
                        placeholder="Indian"
                        {...register('nationality', { required: 'Nationality is required' })}
                    />
                    {errors.nationality && (
                        <p className="text-sm text-red-500">{errors.nationality.message as string}</p>
                    )}
                </div>
                <div className="space-y-2">
                    <Label htmlFor="mother_tongue">Mother Tongue</Label>
                    <Input
                        id="mother_tongue"
                        placeholder="e.g. English, Hindi"
                        {...register('mother_tongue')}
                    />
                </div>
            </div>

            {/* Row 5: Identification Marks */}
            <div className="space-y-4">
                <div className="space-y-2">
                    <Label htmlFor="identification_mark_1">Identification Mark 1</Label>
                    <Input
                        id="identification_mark_1"
                        placeholder="e.g. Mole on right cheek"
                        {...register('identification_mark_1')}
                    />
                </div>
                <div className="space-y-2">
                    <Label htmlFor="identification_mark_2">Identification Mark 2</Label>
                    <Input
                        id="identification_mark_2"
                        placeholder="e.g. Scar on forehead"
                        {...register('identification_mark_2')}
                    />
                </div>
            </div>
        </div>
    )
}
