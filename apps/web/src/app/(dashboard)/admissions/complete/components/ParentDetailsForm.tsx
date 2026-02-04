'use client'

import { useFormContext, useFieldArray, Controller } from 'react-hook-form'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from '@/components/ui/select'
import { ParentRelation, Gender, ApplicationCompleteSubmit } from '@/types/admissions'
import { Trash2, Plus } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export function ParentDetailsForm() {
    const { register, control, formState: { errors } } = useFormContext<ApplicationCompleteSubmit>()

    const { fields, append, remove } = useFieldArray({
        control,
        name: "parents"
    })

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center border-b pb-2">
                <h3 className="text-lg font-semibold text-gray-900">
                    Parent / Guardian Details
                </h3>
                <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    onClick={() => append({
                        relation: ParentRelation.FATHER,
                        name: '',
                        mobile: '',
                        is_primary_contact: false
                    })}
                >
                    <Plus className="h-4 w-4 mr-2" />
                    Add Guardian
                </Button>
            </div>

            <div className="space-y-4">
                {fields.map((field, index) => (
                    <Card key={field.id} className="relative">
                        <CardHeader className="pb-2">
                            <div className="flex justify-between items-center">
                                <CardTitle className="text-base font-medium">
                                    Parent/Guardian #{index + 1}
                                </CardTitle>
                                {index > 0 && ( // Prevent removing the first one if we want to enforce at least one? Or allow all.
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
                            {/* Relation */}
                            <div className="space-y-2">
                                <Label>Relation *</Label>
                                <Controller
                                    control={control}
                                    name={`parents.${index}.relation`}
                                    rules={{ required: 'Relation is required' }}
                                    render={({ field }) => (
                                        <Select onValueChange={field.onChange} defaultValue={field.value}>
                                            <SelectTrigger>
                                                <SelectValue placeholder="Select Relation" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                {Object.values(ParentRelation).map((r) => (
                                                    <SelectItem key={r} value={r}>{r}</SelectItem>
                                                ))}
                                            </SelectContent>
                                        </Select>
                                    )}
                                />
                                {errors.parents?.[index]?.relation && (
                                    <p className="text-sm text-red-500">{errors.parents[index].relation.message as string}</p>
                                )}
                            </div>

                            {/* Name */}
                            <div className="space-y-2">
                                <Label>Full Name *</Label>
                                <Input
                                    placeholder="Enter full name"
                                    {...register(`parents.${index}.name`, { required: 'Name is required' })}
                                />
                                {errors.parents?.[index]?.name && (
                                    <p className="text-sm text-red-500">{errors.parents[index].name.message as string}</p>
                                )}
                            </div>

                            {/* Gender - Optional but helpful */}
                            <div className="space-y-2">
                                <Label>Gender</Label>
                                <Controller
                                    control={control}
                                    name={`parents.${index}.gender`}
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
                            </div>

                            {/* Mobile */}
                            <div className="space-y-2">
                                <Label>Mobile Number *</Label>
                                <Input
                                    placeholder="10 digit mobile"
                                    maxLength={10}
                                    {...register(`parents.${index}.mobile`, {
                                        required: 'Mobile is required',
                                        pattern: { value: /^\d{10}$/, message: 'Must be 10 digits' }
                                    })}
                                />
                                {errors.parents?.[index]?.mobile && (
                                    <p className="text-sm text-red-500">{errors.parents[index].mobile.message as string}</p>
                                )}
                            </div>

                            {/* Email */}
                            <div className="space-y-2">
                                <Label>Email</Label>
                                <Input
                                    placeholder="email@example.com"
                                    type="email"
                                    {...register(`parents.${index}.email`, {
                                        pattern: { value: /^\S+@\S+$/i, message: "Invalid email address" }
                                    })}
                                />
                            </div>

                            {/* Occupation */}
                            <div className="space-y-2">
                                <Label>Occupation</Label>
                                <Input
                                    placeholder="e.g. Engineer, Farmer"
                                    {...register(`parents.${index}.occupation`)}
                                />
                            </div>

                            {/* Annual Income */}
                            <div className="space-y-2">
                                <Label>Annual Income</Label>
                                <Input
                                    type="number"
                                    placeholder="e.g. 500000"
                                    {...register(`parents.${index}.annual_income`, { valueAsNumber: true })}
                                />
                            </div>

                            {/* Primary Contact Checkbox - Spanning 2 cols or just 1 */}
                            <div className="flex items-center space-x-2 md:col-span-2 mt-2">
                                <Controller
                                    control={control}
                                    name={`parents.${index}.is_primary_contact`}
                                    render={({ field }) => (
                                        <Checkbox
                                            id={`primary-${index}`}
                                            checked={field.value}
                                            onCheckedChange={field.onChange}
                                        />
                                    )}
                                />
                                <Label htmlFor={`primary-${index}`} className="cursor-pointer font-normal">
                                    This person is the primary contact for all communications
                                </Label>
                            </div>

                        </CardContent>
                    </Card>
                ))}
            </div>

            {fields.length === 0 && (
                <div className="text-center p-8 border-2 border-dashed rounded-lg text-gray-500">
                    No parents added. Please add at least one parent/guardian.
                </div>
            )}
        </div>
    )
}
