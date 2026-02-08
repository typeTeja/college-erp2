'use client'

import { useFormContext, useWatch } from 'react-hook-form'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Checkbox } from '@/components/ui/checkbox'
import { Textarea } from '@/components/ui/textarea' // Assuming Textarea exists or use Input for line1? Textarea is better.
import { AddressType, ApplicationCompleteSubmit } from '@/types/admissions'
import { useEffect } from 'react'

export function AddressDetailsForm() {
    const { register, control, setValue, formState: { errors } } = useFormContext<ApplicationCompleteSubmit>()

    // Watch permanent address fields to sync if needed
    const permanentAddress = useWatch({ control, name: 'addresses.0' }) // Assuming index 0 is Permanent
    const isSameAsPermanent = useWatch({ control, name: 'addresses.1.is_same_as_permanent' }) // Assuming index 1 is Current

    useEffect(() => {
        if (isSameAsPermanent && permanentAddress) {
            setValue('addresses.1.address_line', permanentAddress.address_line)
            setValue('addresses.1.village_city', permanentAddress.village_city)
            setValue('addresses.1.state', permanentAddress.state)
            setValue('addresses.1.district', permanentAddress.district)
            setValue('addresses.1.pincode', permanentAddress.pincode)
            setValue('addresses.1.country', permanentAddress.country)
        }
    }, [isSameAsPermanent, permanentAddress, setValue])

    // Helper to render address fields
    const renderFields = (index: number, type: string, disabled: boolean = false) => (
        <div className={`grid grid-cols-1 md:grid-cols-2 gap-4 ${disabled ? 'opacity-70 pointer-events-none' : ''}`}>
            <div className="md:col-span-2 space-y-2">
                <Label>Address * (House No, Street, etc.)</Label>
                <Textarea
                    {...register(`addresses.${index}.address_line`, { required: 'Address is required' })}
                    placeholder="Enter full address"
                    disabled={disabled}
                    className="min-h-[80px]"
                />
                {errors.addresses?.[index]?.address_line && (
                    <p className="text-sm text-red-500">{errors.addresses[index].address_line.message as string}</p>
                )}
            </div>

            <div className="space-y-2">
                <Label>Village/City *</Label>
                <Input
                    {...register(`addresses.${index}.village_city`, { required: 'Village/City is required' })}
                    disabled={disabled}
                />
                {errors.addresses?.[index]?.village_city && (
                    <p className="text-sm text-red-500">{errors.addresses[index].village_city.message as string}</p>
                )}
            </div>

            <div className="space-y-2">
                <Label>District *</Label>
                <Input
                    {...register(`addresses.${index}.district`, { required: 'District is required' })}
                    disabled={disabled}
                />
            </div>

            <div className="space-y-2">
                <Label>State *</Label>
                <Input
                    {...register(`addresses.${index}.state`, { required: 'State is required' })}
                    disabled={disabled}
                />
                {errors.addresses?.[index]?.state && (
                    <p className="text-sm text-red-500">{errors.addresses[index].state.message as string}</p>
                )}
            </div>

            <div className="space-y-2">
                <Label>Pincode *</Label>
                <Input
                    {...register(`addresses.${index}.pincode`, {
                        required: 'Pincode is required',
                        pattern: { value: /^\d{6}$/, message: 'Must be 6 digits' }
                    })}
                    maxLength={6}
                    disabled={disabled}
                />
                {errors.addresses?.[index]?.pincode && (
                    <p className="text-sm text-red-500">{errors.addresses[index].pincode.message as string}</p>
                )}
            </div>

            <div className="space-y-2">
                <Label>Country *</Label>
                <Input
                    {...register(`addresses.${index}.country`, { required: 'Country is required' })}
                    disabled={disabled}
                    defaultValue="India"
                />
            </div>

            {/* Hidden Type Field */}
            <input type="hidden" {...register(`addresses.${index}.address_type`)} value={type} />
        </div>
    )

    return (
        <div className="space-y-8">
            <h3 className="text-lg font-semibold text-gray-900 border-b pb-2">
                Address Details
            </h3>

            {/* Permanent Address */}
            <div className="space-y-4">
                <h4 className="font-medium text-gray-700">Permanent Address</h4>
                {renderFields(0, AddressType.PERMANENT)}
            </div>

            {/* Current Address */}
            <div className="space-y-4">
                <div className="flex items-center justify-between">
                    <h4 className="font-medium text-gray-700">Current Address</h4>
                    <div className="flex items-center space-x-2">
                        <Checkbox
                            id="same-as-perm"
                            onCheckedChange={(checked) => setValue('addresses.1.is_same_as_permanent', checked === true)}
                            {...register('addresses.1.is_same_as_permanent')}
                        />
                        <Label htmlFor="same-as-perm" className="font-normal cursor-pointer">
                            Same as Permanent Address
                        </Label>
                    </div>
                </div>
                {renderFields(1, AddressType.PRESENT, isSameAsPermanent)}
            </div>
        </div>
    )
}
