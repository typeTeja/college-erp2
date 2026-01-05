'use client'

import { use } from 'react'
import Link from 'next/link'
import { programService } from '@/utils/program-service'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Loader2, ChevronLeft, BookOpen, Info } from 'lucide-react'

interface ManageStructurePageProps {
    params: Promise<{
        id: string
    }>
}

export default function ManageStructurePage({ params }: ManageStructurePageProps) {
    const { id: idString } = use(params)
    const id = parseInt(idString)
    const { data: program, isLoading } = programService.useProgram(id)

    if (isLoading) {
        return <div className="flex justify-center py-20"><Loader2 className="h-8 w-8 animate-spin" /></div>
    }

    if (!program) {
        return <div className="text-center py-20">Program not found</div>
    }

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div className="space-y-1">
                    <Link href="/programs" className="text-sm text-muted-foreground hover:underline flex items-center">
                        <ChevronLeft className="h-4 w-4 mr-1" /> Back to Programs
                    </Link>
                    <h1 className="text-3xl font-bold">{program.name}</h1>
                    <div className="flex items-center gap-2">
                        <Badge variant="outline">{program.code}</Badge>
                        <Badge variant="secondary">{program.program_type}</Badge>
                        <span className="text-sm text-muted-foreground ml-2">
                            {program.duration_years} Years • {program.total_credits} Credits
                        </span>
                    </div>
                </div>
            </div>

            <Card className="border-blue-200 bg-blue-50">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2 text-blue-800">
                        <Info className="h-5 w-5" />
                        Structure Management Update
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <p className="text-blue-700">
                        Program structure (semesters, credits, subjects) is now defined by <strong>Regulations</strong>.
                        Please associate a Regulation with this program to define its academic structure.
                    </p>
                </CardContent>
            </Card>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card>
                    <CardHeader>
                        <CardTitle>Program Details</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4 text-sm">
                        <div>
                            <span className="font-medium block text-muted-foreground">Department</span>
                            {program.department_name}
                        </div>
                        <div>
                            <span className="font-medium block text-muted-foreground">Created At</span>
                            {new Date().toLocaleDateString()}
                        </div>

                        <div className="pt-4 border-t">
                            {program.description && (
                                <div className="mb-2">
                                    <span className="font-semibold block mb-1">Description</span>
                                    <p className="text-muted-foreground">{program.description}</p>
                                </div>
                            )}
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
