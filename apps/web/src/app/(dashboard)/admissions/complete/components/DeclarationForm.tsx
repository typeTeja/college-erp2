'use client'

import { useFormContext, Controller } from 'react-hook-form'
import { Label } from '@/components/ui/label'
import { Checkbox } from '@/components/ui/checkbox'
import { Card, CardContent } from '@/components/ui/card'
import { ApplicationCompleteSubmit } from '@/types/admissions'

export function DeclarationForm() {
    const { control, formState: { errors } } = useFormContext<ApplicationCompleteSubmit>()

    return (
        <div className="space-y-6">
            <h3 className="text-lg font-semibold text-gray-900 border-b pb-2">
                Declarations
            </h3>

            <Card>
                <CardContent className="p-6 space-y-6">
                    {/* Student Declaration */}
                    <div className="space-y-3">
                        <Label className="text-base font-medium">Student Declaration</Label>
                        <div className="p-4 bg-gray-50 rounded-md text-sm text-gray-700 leading-relaxed border">
                            I declare that the information provided in this application is true and correct to the best of my knowledge and belief.
                            I understand that any misrepresentation or omission of facts will justify the denial of admission, the cancellation of admission, or expulsion.
                            I agree to abide by the rules and regulations of the institute.
                        </div>
                        <div className="flex items-start space-x-2">
                            <Controller
                                control={control}
                                name="student_declaration_accepted"
                                rules={{ required: "You must accept the declaration" }}
                                render={({ field }) => (
                                    <Checkbox
                                        id="student_decl"
                                        checked={field.value}
                                        onCheckedChange={field.onChange}
                                    />
                                )}
                            />
                            <div className="grid gap-1.5 leading-none">
                                <Label htmlFor="student_decl" className="cursor-pointer font-normal">
                                    I accept the student declaration
                                </Label>
                                {errors.student_declaration_accepted && (
                                    <p className="text-sm text-red-500">{errors.student_declaration_accepted.message as string}</p>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* Parent Declaration */}
                    <div className="space-y-3 pt-4 border-t">
                        <Label className="text-base font-medium">Parent / Guardian Declaration</Label>
                        <div className="p-4 bg-gray-50 rounded-md text-sm text-gray-700 leading-relaxed border">
                            I undertake the responsibility for the conduct and behavior of my ward.
                            I also declare that I will pay the fees and other charges as per the schedule.
                            I am aware that ragging is strictly prohibited and my ward is liable for punishment if found guilty.
                        </div>
                        <div className="flex items-start space-x-2">
                            <Controller
                                control={control}
                                name="parent_declaration_accepted"
                                rules={{ required: "Parent/Guardian must accept the declaration" }}
                                render={({ field }) => (
                                    <Checkbox
                                        id="parent_decl"
                                        checked={field.value}
                                        onCheckedChange={field.onChange}
                                    />
                                )}
                            />
                            <div className="grid gap-1.5 leading-none">
                                <Label htmlFor="parent_decl" className="cursor-pointer font-normal">
                                    I accept the parent/guardian declaration
                                </Label>
                                {errors.parent_declaration_accepted && (
                                    <p className="text-sm text-red-500">{errors.parent_declaration_accepted.message as string}</p>
                                )}
                            </div>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
