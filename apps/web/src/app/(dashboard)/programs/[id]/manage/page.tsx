'use client'

import { useState, useEffect, use } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { programService } from '@/utils/program-service'
import { Program, ProgramYear, Semester } from '@/types/program'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Switch } from '@/components/ui/switch'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { useToast } from '@/hooks/use-toast'
import { ChevronLeft, Save, Loader2, Calendar, BookOpen } from 'lucide-react'
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion'

interface ManageStructurePageProps {
    params: Promise<{
        id: string
    }>
}

export default function ManageStructurePage({ params }: ManageStructurePageProps) {
    const { id: idString } = use(params)
    const id = parseInt(idString)
    const router = useRouter()
    const { toast } = useToast()
    const { data: program, isLoading, refetch } = programService.useProgram(id)
    const updateMutation = programService.useUpdateStructure()

    const [structure, setStructure] = useState<ProgramYear[]>([])
    const [isDirty, setIsDirty] = useState(false)

    // Sync local state with fetched data
    useEffect(() => {
        if (program?.years) {
            setStructure(JSON.parse(JSON.stringify(program.years))) // Deep copy
        }
    }, [program])

    const handleSemesterChange = (yearIndex: number, semIndex: number, field: keyof Semester, value: any) => {
        const newStructure = [...structure]
        newStructure[yearIndex].semesters[semIndex] = {
            ...newStructure[yearIndex].semesters[semIndex],
            [field]: value
        }
        setStructure(newStructure)
        setIsDirty(true)
    }

    const handleSave = async () => {
        try {
            await updateMutation.mutateAsync({
                id,
                data: {
                    years: structure
                }
            })
            toast({ title: "Structure updated successfully!" })
            setIsDirty(false)
            refetch()
        } catch (error: any) {
            toast({
                title: "Failed to update structure",
                description: error.response?.data?.detail || "Something went wrong",
                variant: "destructive"
            })
        }
    }

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
                <Button onClick={handleSave} disabled={!isDirty || updateMutation.isPending}>
                    {updateMutation.isPending ? <Loader2 className="mr-2 h-4 w-4 animate-spin" /> : <Save className="mr-2 h-4 w-4" />}
                    Save Changes
                </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="md:col-span-2 space-y-6">
                    <Card>
                        <CardHeader>
                            <CardTitle>Program Structure</CardTitle>
                            <CardDescription>
                                Customize the names and settings for each semester.
                                Mark internships or final projects here.
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <Accordion type="multiple" defaultValue={structure.map(y => `year-${y.id}`)} className="w-full">
                                {structure.map((year, yearIndex) => (
                                    <AccordionItem key={year.id} value={`year-${year.id}`}>
                                        <AccordionTrigger className="hover:no-underline">
                                            <div className="flex items-center gap-2">
                                                <Calendar className="h-4 w-4 text-muted-foreground" />
                                                <span className="font-semibold">{year.name}</span>
                                                <Badge variant="outline" className="ml-2 text-xs font-normal">
                                                    Year {year.year_number}
                                                </Badge>
                                            </div>
                                        </AccordionTrigger>
                                        <AccordionContent className="pt-4 space-y-4">
                                            {year.semesters.map((sem, semIndex) => (
                                                <div key={sem.id} className="border rounded-md p-4 bg-muted/20">
                                                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 items-end">
                                                        <div className="space-y-2">
                                                            <Label>Semester Name</Label>
                                                            <Input
                                                                value={sem.name}
                                                                onChange={(e) => handleSemesterChange(yearIndex, semIndex, 'name', e.target.value)}
                                                            />
                                                        </div>
                                                        <div className="flex items-center gap-4 border p-2 rounded-md bg-background">
                                                            <div className="flex items-center space-x-2">
                                                                <Switch
                                                                    id={`intern-${sem.id}`}
                                                                    checked={sem.is_internship}
                                                                    onCheckedChange={(checked) => handleSemesterChange(yearIndex, semIndex, 'is_internship', checked)}
                                                                />
                                                                <Label htmlFor={`intern-${sem.id}`} className="cursor-pointer">Internship</Label>
                                                            </div>
                                                            <div className="flex items-center space-x-2">
                                                                <Switch
                                                                    id={`project-${sem.id}`}
                                                                    checked={sem.is_project_semester}
                                                                    onCheckedChange={(checked) => handleSemesterChange(yearIndex, semIndex, 'is_project_semester', checked)}
                                                                />
                                                                <Label htmlFor={`project-${sem.id}`} className="cursor-pointer">Project</Label>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            ))}
                                        </AccordionContent>
                                    </AccordionItem>
                                ))}
                            </Accordion>
                        </CardContent>
                    </Card>
                </div>

                <div className="space-y-6">
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
                                {new Date().toLocaleDateString()} {/* Placeholder for real date */}
                            </div>

                            <div className="pt-4 border-t">
                                <span className="font-medium block text-muted-foreground mb-2">Metadata</span>
                                {program.eligibility_criteria && (
                                    <div className="mb-2">
                                        <span className="text-xs font-semibold">Eligibility:</span>
                                        <p className="text-xs text-muted-foreground line-clamp-2">{program.eligibility_criteria}</p>
                                    </div>
                                )}
                                {program.program_outcomes && (
                                    <div>
                                        <span className="text-xs font-semibold">Outcomes:</span>
                                        <p className="text-xs text-muted-foreground line-clamp-2">{program.program_outcomes}</p>
                                    </div>
                                )}
                            </div>
                        </CardContent>
                    </Card>

                    <Card className="bg-blue-50 border-blue-100">
                        <CardHeader className="pb-2">
                            <CardTitle className="text-sm text-blue-800 flex items-center gap-2">
                                <BookOpen className="h-4 w-4" />
                                Quick Status
                            </CardTitle>
                        </CardHeader>
                        <CardContent>
                            <p className="text-xs text-blue-600 mb-2">
                                Marking a semester as "Internship" may trigger specific workflows in the future (e.g., hiding subject inputs, changing fee structures).
                            </p>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    )
}
