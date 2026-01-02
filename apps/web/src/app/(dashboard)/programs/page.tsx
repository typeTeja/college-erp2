'use client'

import { useState } from 'react'
import Link from 'next/link'
import { programService } from '@/utils/program-service'
import { ProgramType, ProgramStatus, Program } from '@/types/program'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { Plus, Search, BookOpen, Layers, Edit, Trash2, Settings } from 'lucide-react'
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table'
import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
    AlertDialogTrigger,
} from "@/components/ui/alert-dialog"

export default function ProgramsPage() {
    const [search, setSearch] = useState('')
    const [typeFilter, setTypeFilter] = useState<ProgramType | 'ALL'>('ALL')
    const [statusFilter, setStatusFilter] = useState<ProgramStatus | 'ALL'>('ALL')

    // Convert 'ALL' to undefined for API call
    const queryType = typeFilter === 'ALL' ? undefined : typeFilter
    const queryStatus = statusFilter === 'ALL' ? undefined : statusFilter

    const { data: programs, isLoading } = programService.usePrograms(queryType, queryStatus)
    const deleteMutation = programService.useDeleteProgram()

    const filteredPrograms = programs?.filter(p =>
        p.name.toLowerCase().includes(search.toLowerCase()) ||
        p.code.toLowerCase().includes(search.toLowerCase())
    )

    const handleDelete = async (id: number) => {
        try {
            await deleteMutation.mutateAsync(id)
        } catch (error) {
            console.error("Failed to delete program", error)
            alert("Failed to delete program. It might have enrolled students.")
        }
    }

    const getStatusColor = (status: ProgramStatus) => {
        switch (status) {
            case ProgramStatus.ACTIVE: return "default" // Black/Primary
            case ProgramStatus.DRAFT: return "secondary" // Gray
            case ProgramStatus.ARCHIVED: return "destructive" // Red-ish/Orange
            default: return "outline"
        }
    }

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h2 className="text-3xl font-bold tracking-tight">Programs</h2>
                    <p className="text-muted-foreground">
                        Manage academic programs, departments, and course structures.
                    </p>
                </div>
                <Link href="/programs/create">
                    <Button>
                        <Plus className="mr-2 h-4 w-4" />
                        Create Program
                    </Button>
                </Link>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>All Programs</CardTitle>
                    <CardDescription>
                        List of all academic programs offered by the institute.
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="flex flex-col md:flex-row gap-4 mb-6">
                        <div className="relative flex-1">
                            <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
                            <Input
                                placeholder="Search programs by name or code..."
                                className="pl-8"
                                value={search}
                                onChange={(e) => setSearch(e.target.value)}
                            />
                        </div>
                        <Select
                            value={typeFilter}
                            onValueChange={(val) => setTypeFilter(val as ProgramType | 'ALL')}
                        >
                            <SelectTrigger className="w-[180px]">
                                <SelectValue placeholder="Filter by Type" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="ALL">All Types</SelectItem>
                                {Object.values(ProgramType).map((t) => (
                                    <SelectItem key={t} value={t}>{t}</SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                        <Select
                            value={statusFilter}
                            onValueChange={(val) => setStatusFilter(val as ProgramStatus | 'ALL')}
                        >
                            <SelectTrigger className="w-[180px]">
                                <SelectValue placeholder="Filter by Status" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="ALL">All Statuses</SelectItem>
                                {Object.values(ProgramStatus).map((s) => (
                                    <SelectItem key={s} value={s}>{s}</SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>

                    <div className="rounded-md border">
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Code</TableHead>
                                    <TableHead>Name</TableHead>
                                    <TableHead>Type</TableHead>
                                    <TableHead>Department</TableHead>
                                    <TableHead>Duration</TableHead>
                                    <TableHead>Status</TableHead>
                                    <TableHead className="text-right">Actions</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {isLoading ? (
                                    <TableRow>
                                        <TableCell colSpan={7} className="h-24 text-center">
                                            Loading programs...
                                        </TableCell>
                                    </TableRow>
                                ) : filteredPrograms?.length === 0 ? (
                                    <TableRow>
                                        <TableCell colSpan={7} className="h-24 text-center">
                                            No programs found.
                                        </TableCell>
                                    </TableRow>
                                ) : (
                                    filteredPrograms?.map((program) => (
                                        <TableRow key={program.id}>
                                            <TableCell className="font-medium">{program.code}</TableCell>
                                            <TableCell>
                                                <div className="flex flex-col">
                                                    <span className="font-medium">{program.name}</span>
                                                    <span className="text-xs text-muted-foreground truncate max-w-[200px]">
                                                        {program.description}
                                                    </span>
                                                </div>
                                            </TableCell>
                                            <TableCell>
                                                <Badge variant="outline">{program.program_type}</Badge>
                                            </TableCell>
                                            <TableCell>{program.department_name}</TableCell>
                                            <TableCell>{program.duration_years} Years</TableCell>
                                            <TableCell>
                                                <Badge variant={getStatusColor(program.status)}>
                                                    {program.status}
                                                </Badge>
                                            </TableCell>
                                            <TableCell className="text-right">
                                                <div className="flex justify-end gap-2">
                                                    <Link href={`/programs/${program.id}/manage`}>
                                                        <Button variant="ghost" size="icon" title="Manage Structure">
                                                            <Settings className="h-4 w-4" />
                                                        </Button>
                                                    </Link>
                                                    <AlertDialog>
                                                        <AlertDialogTrigger asChild>
                                                            <Button variant="ghost" size="icon" className="text-destructive hover:text-destructive">
                                                                <Trash2 className="h-4 w-4" />
                                                            </Button>
                                                        </AlertDialogTrigger>
                                                        <AlertDialogContent>
                                                            <AlertDialogHeader>
                                                                <AlertDialogTitle>Delete Program?</AlertDialogTitle>
                                                                <AlertDialogDescription>
                                                                    Are you sure you want to delete <strong>{program.name}</strong>?
                                                                    This action cannot be undone. You cannot delete programs with enrolled students.
                                                                </AlertDialogDescription>
                                                            </AlertDialogHeader>
                                                            <AlertDialogFooter>
                                                                <AlertDialogCancel>Cancel</AlertDialogCancel>
                                                                <AlertDialogAction onClick={() => handleDelete(program.id)} className="bg-destructive text-destructive-foreground hover:bg-destructive/90">
                                                                    Delete
                                                                </AlertDialogAction>
                                                            </AlertDialogFooter>
                                                        </AlertDialogContent>
                                                    </AlertDialog>
                                                </div>
                                            </TableCell>
                                        </TableRow>
                                    ))
                                )}
                            </TableBody>
                        </Table>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
