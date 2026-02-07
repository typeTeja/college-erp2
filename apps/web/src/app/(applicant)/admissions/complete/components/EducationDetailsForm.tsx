'use client'

import { useFormContext, useFieldArray, Controller } from 'react-hook-form'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select'
import { EducationLevel, EducationBoard, ApplicationCompleteSubmit } from '@/types/admissions'
import { Trash2, Plus } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export function EducationDetailsForm() {
    const { register, control, formState: { errors } } = useFormContext<ApplicationCompleteSubmit>()

    const { fields, append, remove } = useFieldArray({
        control,
        name: "education"
    })

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center border-b pb-2">
                <h3 className="text-lg font-semibold text-gray-900">
                    Education Details
                </h3>
                <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    onClick={() => append({
                        level: EducationLevel.DEGREE,
                        institution_name: '',
                        percentage: 0,
                        board: EducationBoard.STATE_BOARD
                    })}
                >
                    <Plus className="h-4 w-4 mr-2" />
                    Add Qualification
                </Button>
            </div>

            <div className="space-y-4">
                {fields.map((field, index) => (
                    <Card key={field.id} className="relative">
                        <CardHeader className="pb-2">
                            <div className="flex justify-between items-center">
                                <CardTitle className="text-base font-medium">
                                    Qualification #{index + 1}
                                </CardTitle>
                                {index > 1 && ( // Assume first 2 are mandatory (SSC, Inter)? Or let user manage. Let's allowing removing any beyond 1.
                                    <Button
                                        type="button"
                                        variant="ghost"
                                        size="icon"
                                        className="text-red-500 hover:text-red-700 hover:bg-red-50"
                                        onClick={() => remove(index)}
                                    >
                                        <Trash2 className="h-4 w-4" />
                                    </Button>
                                )}
                            </div>
                        </CardHeader>
                        <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {/* Level */}
                            <div className="space-y-2">
                                <Label>Level of Education *</Label>
                                <Controller
                                    control={control}
                                    name={`education.${index}.level`}
                                    rules={{ required: 'Level is required' }}
                                    render={({ field }) => (
                                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                                            <SelectTrigger>
                                                <SelectValue placeholder="Select Level" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                {Object.values(EducationLevel).map((l) => (
                                                    <SelectItem key={l} value={l}>{l.replace('_', ' ')}</SelectItem>
                                                ))}
                                            </SelectContent>
                                        </Select>
                                    )}
                                />
                                {errors.education?.[index]?.level && (
                                    <p className="text-sm text-red-500">{errors.education[index].level.message as string}</p>
                                )}
                            </div>

                            {/* Institution Name */}
                            <div className="space-y-2">
                                <Label>Institution Name *</Label>
                                <Input
                                    placeholder="School / College Name"
                                    {...register(`education.${index}.institution_name`, { required: 'Institution name is required' })}
                                />
                                {errors.education?.[index]?.institution_name && (
                                    <p className="text-sm text-red-500">{errors.education[index].institution_name.message as string}</p>
                                )}
                            </div>

                            {/* Board */}
                            <div className="space-y-2">
                                <Label>Board / University *</Label>
                                <Controller
                                    control={control}
                                    name={`education.${index}.board`}
                                    rules={{ required: 'Board is required' }}
                                    render={({ field }) => (
                                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                                            <SelectTrigger>
                                                <SelectValue placeholder="Select Board" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                {Object.values(EducationBoard).map((b) => (
                                                    <SelectItem key={b} value={b}>{b.replace('_', ' ')}</SelectItem>
                                                ))}
                                            </SelectContent>
                                        </Select>
                                    )}
                                />
                            </div>

                            {/* Hall Ticket */}
                            <div className="space-y-2">
                                <Label>Hall Ticket / Roll No.</Label>
                                <Input
                                    placeholder="Roll Number"
                                    {...register(`education.${index}.hall_ticket_number`)}
                                />
                            </div>

                            {/* Year of Passing */}
                            <div className="space-y-2">
                                <Label>Year of Passing *</Label>
                                <Input
                                    type="number"
                                    placeholder="YYYY"
                                    {...register(`education.${index}.year_of_passing`, {
                                        required: 'Year is required',
                                        min: { value: 1990, message: "Invalid year" },
                                        max: { value: new Date().getFullYear(), message: "Invalid year" }
                                    })}
                                />
                                {errors.education?.[index]?.year_of_passing && (
                                    <p className="text-sm text-red-500">{errors.education[index].year_of_passing.message as string}</p>
                                )}
                            </div>

                            {/* Percentage */}
                            <div className="space-y-2">
                                <Label>Percentage / CGPA *</Label>
                                <Input
                                    type="number"
                                    step="0.01"
                                    placeholder="e.g. 85.5"
                                    {...register(`education.${index}.percentage`, {
                                        required: 'Percentage is required',
                                        min: 0,
                                        max: 100,
                                        valueAsNumber: true
                                    })}
                                />
                                {errors.education?.[index]?.percentage && (
                                    <p className="text-sm text-red-500">{errors.education[index].percentage.message as string}</p>
                                )}
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>

            {fields.length === 0 && (
                <div className="text-center p-8 border-2 border-dashed rounded-lg text-gray-500">
                    No education details added.
                </div>
            )}
        </div>
    )
}
