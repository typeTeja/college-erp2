'use client';

import React, { useState } from 'react';
import { 
    Table, TableBody, TableCell, TableHead, TableHeader, TableRow 
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { 
    Dialog, DialogContent, DialogDescription, DialogFooter, 
    DialogHeader, DialogTitle, DialogTrigger 
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Switch } from '@/components/ui/switch';
import { Plus, Edit, Trash2, Calendar, CheckCircle2 } from 'lucide-react';
import { academicYearService } from '@/utils/academic-year-service';
import { AcademicYear, AcademicYearCreateData, AcademicYearStatus } from '@/types/academic-base';
import { toast } from 'sonner';
import { format } from 'date-fns';

export function AcademicYearMaster() {
    const [isCreateOpen, setIsCreateOpen] = useState(false);
    const [editingYear, setEditingYear] = useState<AcademicYear | null>(null);

    const { data: years = [], isLoading } = academicYearService.useAcademicYears();
    const createMutation = academicYearService.useCreateAcademicYear();
    const updateMutation = academicYearService.useUpdateAcademicYear();
    const deleteMutation = academicYearService.useDeleteAcademicYear();

    const handleSave = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);
        
        const data: AcademicYearCreateData = {
            year: formData.get('year') as string,
            start_date: new Date(formData.get('start_date') as string).toISOString(),
            end_date: new Date(formData.get('end_date') as string).toISOString(),
            is_current: formData.get('is_current') === 'on',
            status: formData.get('status') as AcademicYearStatus || AcademicYearStatus.UPCOMING,
        };

        try {
            if (editingYear) {
                await updateMutation.mutateAsync({ id: editingYear.id, data });
                toast.success('Academic year updated successfully');
            } else {
                await createMutation.mutateAsync(data);
                toast.success('Academic year created successfully');
            }
            setIsCreateOpen(false);
            setEditingYear(null);
        } catch (error: any) {
            toast.error(error.response?.data?.detail || 'Failed to save academic year');
        }
    };

    const handleDelete = async (id: number) => {
        if (!confirm('Are you sure you want to delete this academic year?')) return;
        try {
            await deleteMutation.mutateAsync(id);
            toast.success('Academic year deleted successfully');
        } catch (error: any) {
            toast.error(error.response?.data?.detail || 'Failed to delete academic year');
        }
    };

    if (isLoading) {
        return <div className="p-8 text-center animate-pulse text-slate-500">Loading academic years...</div>;
    }

    return (
        <div className="space-y-4">
            <div className="flex justify-end bg-white p-4 rounded-lg border border-slate-200 shadow-sm">
                <Dialog open={isCreateOpen} onOpenChange={(open) => {
                    setIsCreateOpen(open);
                    if (!open) setEditingYear(null);
                }}>
                    <DialogTrigger asChild>
                        <Button className="bg-blue-600 hover:bg-blue-700">
                            <Plus className="h-4 w-4 mr-2" />
                            Add Academic Year
                        </Button>
                    </DialogTrigger>
                    <DialogContent className="sm:max-w-[425px]">
                        <form onSubmit={handleSave}>
                            <DialogHeader>
                                <DialogTitle>{editingYear ? 'Edit Academic Year' : 'Add New Academic Year'}</DialogTitle>
                                <DialogDescription>
                                    Define the start and end dates for a new academic year.
                                </DialogDescription>
                            </DialogHeader>
                            <div className="grid gap-4 py-4">
                                <div className="grid grid-cols-4 items-center gap-4">
                                    <Label htmlFor="year" className="text-right">Year Name</Label>
                                    <Input id="year" name="year" placeholder="e.g. 2024-25" defaultValue={editingYear?.year} className="col-span-3" required />
                                </div>
                                <div className="grid grid-cols-4 items-center gap-4">
                                    <Label htmlFor="start_date" className="text-right">Start Date</Label>
                                    <Input id="start_date" name="start_date" type="date" defaultValue={editingYear?.start_date ? format(new Date(editingYear.start_date), 'yyyy-MM-dd') : ''} className="col-span-3" required />
                                </div>
                                <div className="grid grid-cols-4 items-center gap-4">
                                    <Label htmlFor="end_date" className="text-right">End Date</Label>
                                    <Input id="end_date" name="end_date" type="date" defaultValue={editingYear?.end_date ? format(new Date(editingYear.end_date), 'yyyy-MM-dd') : ''} className="col-span-3" required />
                                </div>
                                <div className="grid grid-cols-4 items-center gap-4">
                                    <Label htmlFor="status" className="text-right">Status</Label>
                                    <select 
                                        id="status" 
                                        name="status" 
                                        defaultValue={editingYear?.status || AcademicYearStatus.UPCOMING}
                                        className="col-span-3 flex h-10 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    >
                                        {Object.values(AcademicYearStatus).map(s => (
                                            <option key={s} value={s}>{s}</option>
                                        ))}
                                    </select>
                                </div>
                                <div className="flex items-center space-x-2 ml-auto">
                                    <Switch id="is_current" name="is_current" defaultChecked={editingYear?.is_current} />
                                    <Label htmlFor="is_current">Set as Current Active Year</Label>
                                </div>
                            </div>
                            <DialogFooter>
                                <Button type="submit" disabled={createMutation.isPending || updateMutation.isPending}>
                                    {editingYear ? 'Update Year' : 'Create Year'}
                                </Button>
                            </DialogFooter>
                        </form>
                    </DialogContent>
                </Dialog>
            </div>

            <Card>
                <CardContent className="p-0">
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Academic Year</TableHead>
                                <TableHead>Start Date</TableHead>
                                <TableHead>End Date</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {years.length === 0 ? (
                                <TableRow>
                                    <TableCell colSpan={5} className="text-center py-12 text-slate-500">
                                        <div className="flex flex-col items-center">
                                            <Calendar className="h-10 w-10 text-slate-300 mb-2" />
                                            <p>No academic years defined.</p>
                                        </div>
                                    </TableCell>
                                </TableRow>
                            ) : (
                                years.map((year) => (
                                    <TableRow key={year.id} className={year.is_current ? "bg-blue-50/50" : ""}>
                                        <TableCell>
                                            <div className="flex items-center">
                                                <span className="font-semibold text-slate-900">{year.year}</span>
                                                {year.is_current && (
                                                    <Badge className="ml-2 bg-blue-600 hover:bg-blue-600">
                                                        <CheckCircle2 className="h-3 w-3 mr-1" />
                                                        Current
                                                    </Badge>
                                                )}
                                            </div>
                                        </TableCell>
                                        <TableCell>{format(new Date(year.start_date), 'dd MMM yyyy')}</TableCell>
                                        <TableCell>{format(new Date(year.end_date), 'dd MMM yyyy')}</TableCell>
                                        <TableCell>
                                            <Badge className={
                                                year.status === AcademicYearStatus.ACTIVE ? "bg-green-100 text-green-700" : 
                                                year.status === AcademicYearStatus.COMPLETED ? "bg-slate-100 text-slate-700" :
                                                "bg-blue-100 text-blue-700"
                                            }>
                                                {year.status}
                                            </Badge>
                                        </TableCell>
                                        <TableCell className="text-right">
                                            <Button 
                                                variant="ghost" 
                                                size="icon"
                                                onClick={() => {
                                                    setEditingYear(year);
                                                    setIsCreateOpen(true);
                                                }}
                                            >
                                                <Edit className="h-4 w-4 text-slate-500" />
                                            </Button>
                                            <Button 
                                                variant="ghost" 
                                                size="icon" 
                                                className="text-red-500 hover:text-red-600 hover:bg-red-50"
                                                onClick={() => handleDelete(year.id)}
                                            >
                                                <Trash2 className="h-4 w-4" />
                                            </Button>
                                        </TableCell>
                                    </TableRow>
                                ))
                            )}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>
        </div>
    );
}
