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
            const detail = error.response?.data?.detail;
            const message = Array.isArray(detail) 
                ? detail.map((d: any) => d.msg).join(", ") 
                : typeof detail === 'string' ? detail : 'Failed to save academic year';
            toast.error(message);
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
        return <div className="p-8 text-center animate-pulse text-slate-500 font-medium tracking-tight">Loading academic years...</div>;
    }

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                <div>
                    <h3 className="text-lg font-bold text-slate-900">Academic Calendar</h3>
                    <p className="text-sm text-slate-500">Manage institutional academic periods and current active year.</p>
                </div>
                <Dialog open={isCreateOpen} onOpenChange={(open) => {
                    setIsCreateOpen(open);
                    if (!open) setEditingYear(null);
                }}>
                    <DialogTrigger asChild>
                        <Button className="bg-blue-600 hover:bg-blue-700 h-11 px-6 shadow-md transition-all active:scale-95">
                            <Plus className="h-4 w-4 mr-2" />
                            Add Academic Year
                        </Button>
                    </DialogTrigger>
                    <DialogContent className="sm:max-w-[600px] gap-0 p-0 overflow-hidden">
                        <form onSubmit={handleSave}>
                            <DialogHeader className="p-6 bg-slate-50 border-b border-slate-200">
                                <DialogTitle className="text-xl font-bold text-slate-900">
                                    {editingYear ? 'Update Academic Year' : 'New Academic Year'}
                                </DialogTitle>
                                <DialogDescription className="text-slate-500">
                                    Define the duration and current status of this academic period.
                                </DialogDescription>
                            </DialogHeader>

                            <div className="p-6 grid grid-cols-2 gap-x-8 gap-y-6">
                                {/* Row 1: Year Name (Full Width) */}
                                <div className="col-span-2 space-y-2">
                                    <Label htmlFor="year" className="text-sm font-semibold text-slate-700">Year Name <span className="text-red-500">*</span></Label>
                                    <Input 
                                        id="year" 
                                        name="year" 
                                        placeholder="e.g. 2024-25" 
                                        defaultValue={editingYear?.year} 
                                        required 
                                        className="h-11 border-slate-200 focus:ring-blue-500" 
                                    />
                                    <p className="text-[11px] text-slate-400 italic">Unique identifier for this period (e.g. 2025-26)</p>
                                </div>

                                {/* Row 2: Start & End Dates */}
                                <div className="space-y-2">
                                    <Label htmlFor="start_date" className="text-sm font-semibold text-slate-700">Start Date <span className="text-red-500">*</span></Label>
                                    <div className="relative">
                                        <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                                        <Input 
                                            id="start_date" 
                                            name="start_date" 
                                            type="date" 
                                            defaultValue={editingYear?.start_date ? format(new Date(editingYear.start_date), 'yyyy-MM-dd') : ''} 
                                            required 
                                            className="h-11 pl-10 border-slate-200 focus:ring-blue-500" 
                                        />
                                    </div>
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="end_date" className="text-sm font-semibold text-slate-700">End Date <span className="text-red-500">*</span></Label>
                                    <div className="relative">
                                        <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                                        <Input 
                                            id="end_date" 
                                            name="end_date" 
                                            type="date" 
                                            defaultValue={editingYear?.end_date ? format(new Date(editingYear.end_date), 'yyyy-MM-dd') : ''} 
                                            required 
                                            className="h-11 pl-10 border-slate-200 focus:ring-blue-500" 
                                        />
                                    </div>
                                </div>

                                {/* Row 3: Status & Logic */}
                                <div className="space-y-2">
                                    <Label htmlFor="status" className="text-sm font-semibold text-slate-700">Phase Status</Label>
                                    <select 
                                        id="status" 
                                        name="status" 
                                        defaultValue={editingYear?.status || AcademicYearStatus.UPCOMING}
                                        className="w-full h-11 rounded-md border border-slate-200 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    >
                                        {Object.values(AcademicYearStatus).map(s => (
                                            <option key={s} value={s}>{s}</option>
                                        ))}
                                    </select>
                                </div>

                                <div className="bg-slate-50 p-4 rounded-lg border border-slate-200 flex items-center justify-between">
                                    <div className="space-y-0.5">
                                        <Label htmlFor="is_current" className="text-xs font-bold text-slate-900">Active Year</Label>
                                        <p className="text-[10px] text-slate-500 leading-tight">Set as default for dashboard & sessions</p>
                                    </div>
                                    <Switch 
                                        id="is_current" 
                                        name="is_current" 
                                        defaultChecked={editingYear?.is_current}
                                        className="data-[state=checked]:bg-blue-600"
                                    />
                                </div>
                            </div>

                            <DialogFooter className="p-6 bg-slate-50 border-t border-slate-200">
                                <Button 
                                    type="button" 
                                    variant="outline" 
                                    onClick={() => {
                                        setIsCreateOpen(false);
                                        setEditingYear(null);
                                    }}
                                    className="border-slate-300 h-11"
                                >
                                    Cancel
                                </Button>
                                <Button 
                                    type="submit" 
                                    disabled={createMutation.isPending || updateMutation.isPending}
                                    className="bg-blue-600 hover:bg-blue-700 h-11 min-w-[140px]"
                                >
                                    {editingYear ? 'Update Academic Year' : 'Create Year'}
                                </Button>
                            </DialogFooter>
                        </form>
                    </DialogContent>
                </Dialog>
            </div>

            <Card className="rounded-xl overflow-hidden shadow-sm border-slate-200">
                <CardContent className="p-0">
                    <Table>
                        <TableHeader className="bg-slate-50">
                            <TableRow>
                                <TableHead className="font-bold py-4 pl-6">Academic Period</TableHead>
                                <TableHead className="font-bold py-4">Timeline</TableHead>
                                <TableHead className="font-bold py-4">Status</TableHead>
                                <TableHead className="text-right py-4 pr-6">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {years.length === 0 ? (
                                <TableRow>
                                    <TableCell colSpan={4} className="text-center py-20 text-slate-400 font-medium">
                                        <Calendar className="h-10 w-10 mx-auto text-slate-200 mb-2" />
                                        No academic years defined yet.
                                    </TableCell>
                                </TableRow>
                            ) : (
                                years.map((year) => (
                                    <TableRow key={year.id} className={`hover:bg-slate-50/50 transition-colors ${year.is_current ? "bg-blue-50/30" : ""}`}>
                                        <TableCell className="py-4 pl-6">
                                            <div className="flex items-center gap-3">
                                                <div className={`p-2 rounded-lg ${year.is_current ? 'bg-blue-100 text-blue-600' : 'bg-slate-100 text-slate-500'}`}>
                                                    <Calendar className="h-5 w-5" />
                                                </div>
                                                <div className="flex flex-col">
                                                    <span className="font-bold text-slate-900 text-base">{year.year}</span>
                                                    {year.is_current && (
                                                        <span className="text-[10px] uppercase font-bold text-blue-600 tracking-wider">Default Global Year</span>
                                                    )}
                                                </div>
                                            </div>
                                        </TableCell>
                                        <TableCell>
                                            <div className="flex flex-col gap-0.5">
                                                <span className="text-sm font-medium text-slate-700">
                                                    {format(new Date(year.start_date), 'MMM dd, yyyy')} – {format(new Date(year.end_date), 'MMM dd, yyyy')}
                                                </span>
                                                <span className="text-[10px] text-slate-500">12 Month Duration</span>
                                            </div>
                                        </TableCell>
                                        <TableCell>
                                            <Badge variant="secondary" className={`font-bold text-[10px] px-2.5 py-0.5 ${
                                                year.status === AcademicYearStatus.ACTIVE ? "bg-green-100 text-green-700 border-green-200" : 
                                                year.status === AcademicYearStatus.COMPLETED ? "bg-slate-100 text-slate-700 border-slate-200" :
                                                "bg-blue-50 text-blue-700 border-blue-100"
                                            }`}>
                                                {year.status}
                                            </Badge>
                                        </TableCell>
                                        <TableCell className="text-right pr-6">
                                            <div className="flex justify-end gap-1">
                                                <Button 
                                                    variant="ghost" 
                                                    size="icon"
                                                    className="h-8 w-8 hover:bg-blue-50 hover:text-blue-600"
                                                    onClick={() => {
                                                        setEditingYear(year);
                                                        setIsCreateOpen(true);
                                                    }}
                                                >
                                                    <Edit className="h-4 w-4" />
                                                </Button>
                                                <Button 
                                                    variant="ghost" 
                                                    size="icon" 
                                                    className="h-8 w-8 text-slate-400 hover:text-red-500 hover:bg-red-50"
                                                    onClick={() => handleDelete(year.id)}
                                                >
                                                    <Trash2 className="h-4 w-4" />
                                                </Button>
                                            </div>
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
