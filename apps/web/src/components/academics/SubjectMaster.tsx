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
import {
    Select, SelectContent, SelectItem, SelectTrigger, SelectValue
} from '@/components/ui/select';
import { Plus, Edit, Trash2, Search, BookOpen, Filter } from 'lucide-react';
import { subjectService } from '@/utils/subject-service';
import { Subject, SubjectCreateData } from '@/types/subject';
import { SubjectType, EvaluationType } from '@/types/academic-base';
import { toast } from 'sonner';

export function SubjectMaster() {
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedType, setSelectedType] = useState<SubjectType | 'ALL'>('ALL');
    const [isCreateOpen, setIsCreateOpen] = useState(false);
    const [editingSubject, setEditingSubject] = useState<Subject | null>(null);

    // Form state for Select components
    const [subjectType, setSubjectType] = useState<SubjectType>(SubjectType.THEORY);
    const [evaluationType, setEvaluationType] = useState<EvaluationType>(EvaluationType.THEORY_ONLY);

    const { data: subjects = [], isLoading } = subjectService.useSubjects();
    const createMutation = subjectService.useCreateSubject();
    const updateMutation = subjectService.useUpdateSubject();
    const deleteMutation = subjectService.useDeleteSubject();

    const filteredSubjects = subjects.filter(s => {
        const matchesSearch = s.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            s.code.toLowerCase().includes(searchTerm.toLowerCase());
        const matchesType = selectedType === 'ALL' || s.subject_type === selectedType;
        return matchesSearch && matchesType;
    });

    const handleSave = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);

        const data: SubjectCreateData = {
            name: formData.get('name') as string,
            code: formData.get('code') as string,
            short_name: (formData.get('short_name') as string) || null,
            subject_type: subjectType,
            evaluation_type: evaluationType,
        };

        try {
            if (editingSubject) {
                await updateMutation.mutateAsync({ id: editingSubject.id, data });
                toast.success('Subject updated successfully');
            } else {
                await createMutation.mutateAsync(data);
                toast.success('Subject created successfully');
            }
            setIsCreateOpen(false);
            setEditingSubject(null);
        } catch (error: any) {
            toast.error(error.response?.data?.detail || 'Failed to save subject');
        }
    };

    const handleDelete = async (id: number) => {
        if (!confirm('Are you sure you want to delete this subject?')) return;
        try {
            await deleteMutation.mutateAsync(id);
            toast.success('Subject deleted successfully');
        } catch (error: any) {
            toast.error(error.response?.data?.detail || 'Failed to delete subject');
        }
    };

    if (isLoading) {
        return <div className="p-8 text-center animate-pulse text-slate-500">Loading subjects...</div>;
    }

    return (
        <div className="space-y-4">
            <div className="flex flex-col md:flex-row justify-between gap-4 bg-white p-4 rounded-lg border border-slate-200 shadow-sm">
                <div className="flex flex-1 gap-4">
                    <div className="relative w-64">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                        <Input
                            placeholder="Search subjects..."
                            className="pl-9"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                    <div className="flex items-center gap-2">
                        <Filter className="h-4 w-4 text-slate-400" />
                        <Select
                            value={selectedType}
                            onValueChange={(v) => setSelectedType(v as SubjectType | 'ALL')}
                        >
                            <SelectTrigger className="w-48">
                                <SelectValue placeholder="All Types" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="ALL">All Types</SelectItem>
                                {Object.values(SubjectType).map(type => (
                                    <SelectItem key={type} value={type}>{type}</SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>
                </div>

                <Dialog open={isCreateOpen} onOpenChange={(open) => {
                    setIsCreateOpen(open);
                    if (!open) setEditingSubject(null);
                    if (open && editingSubject) {
                        setSubjectType(editingSubject.subject_type);
                        setEvaluationType(editingSubject.evaluation_type);
                    } else if (open) {
                        setSubjectType(SubjectType.THEORY);
                        setEvaluationType(EvaluationType.THEORY_ONLY);
                    }
                }}>
                    <DialogTrigger asChild>
                        <Button className="bg-blue-600 hover:bg-blue-700 shadow-sm transition-all active:scale-95">
                            <Plus className="h-4 w-4 mr-2" />
                            Add Subject
                        </Button>
                    </DialogTrigger>
                    <DialogContent className="sm:max-w-[425px] border-none shadow-2xl bg-white/95 backdrop-blur-sm">
                        <form onSubmit={handleSave}>
                            <DialogHeader>
                                <DialogTitle className="text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                                    {editingSubject ? 'Edit Subject' : 'Add New Subject'}
                                </DialogTitle>
                                <DialogDescription className="text-slate-500">
                                    Define academic details for the central course catalog.
                                </DialogDescription>
                            </DialogHeader>
                            <div className="flex flex-col gap-5 py-6">
                                <div className="space-y-2">
                                    <Label htmlFor="name" className="text-slate-700 font-semibold">Subject Name</Label>
                                    <Input
                                        id="name"
                                        name="name"
                                        placeholder="e.g. Data Structures & Algorithms"
                                        defaultValue={editingSubject?.name}
                                        className="border-slate-200 focus:border-blue-500 focus:ring-blue-500 transition-all"
                                        required
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="code" className="text-slate-700 font-semibold">Subject Code</Label>
                                    <Input
                                        id="code"
                                        name="code"
                                        placeholder="e.g. CS301"
                                        defaultValue={editingSubject?.code}
                                        className="font-mono border-slate-200 focus:border-blue-500 focus:ring-blue-500 transition-all"
                                        required
                                    />
                                    <p className="text-[10px] text-slate-400">Unique identifier used for mapping and result generation.</p>
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div className="space-y-2">
                                        <Label htmlFor="subject_type" className="text-slate-700 font-semibold">Type</Label>
                                        <Select value={subjectType} onValueChange={(v) => setSubjectType(v as SubjectType)}>
                                            <SelectTrigger className="border-slate-200 focus:border-blue-500 focus:ring-blue-500">
                                                <SelectValue placeholder="Select type" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                {Object.values(SubjectType).map(type => (
                                                    <SelectItem key={type} value={type}>{type}</SelectItem>
                                                ))}
                                            </SelectContent>
                                        </Select>
                                    </div>
                                    <div className="space-y-2">
                                        <Label htmlFor="evaluation_type" className="text-slate-700 font-semibold">Evaluation</Label>
                                        <Select value={evaluationType} onValueChange={(v) => setEvaluationType(v as EvaluationType)}>
                                            <SelectTrigger className="border-slate-200 focus:border-blue-500 focus:ring-blue-500 text-xs">
                                                <SelectValue placeholder="Select eval" />
                                            </SelectTrigger>
                                            <SelectContent>
                                                {Object.values(EvaluationType).map(type => (
                                                    <SelectItem key={type} value={type}>{type.replace(/_/g, ' ')}</SelectItem>
                                                ))}
                                            </SelectContent>
                                        </Select>
                                    </div>
                                </div>
                            </div>
                            <DialogFooter>
                                <Button
                                    type="submit"
                                    className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 shadow-md transition-all active:scale-95"
                                    disabled={createMutation.isPending || updateMutation.isPending}
                                >
                                    {editingSubject ? 'Update Subject' : 'Create Subject'}
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
                                <TableHead>Subject Name</TableHead>
                                <TableHead>Code</TableHead>
                                <TableHead>Type</TableHead>
                                <TableHead>Evaluation</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {filteredSubjects.length === 0 ? (
                                <TableRow>
                                    <TableCell colSpan={5} className="text-center py-12 text-slate-500">
                                        <div className="flex flex-col items-center">
                                            <BookOpen className="h-10 w-10 text-slate-300 mb-2" />
                                            <p>No subjects found.</p>
                                        </div>
                                    </TableCell>
                                </TableRow>
                            ) : (
                                filteredSubjects.map((sub) => (
                                    <TableRow key={sub.id}>
                                        <TableCell className="font-medium text-slate-900">{sub.name}</TableCell>
                                        <TableCell className="font-mono text-xs">{sub.code}</TableCell>
                                        <TableCell>
                                            <Badge variant="outline" className="bg-slate-50">
                                                {sub.subject_type}
                                            </Badge>
                                        </TableCell>
                                        <TableCell className="text-xs text-slate-600">
                                            {sub.evaluation_type.replace(/_/g, ' ')}
                                        </TableCell>
                                        <TableCell className="text-right">
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                onClick={() => {
                                                    setEditingSubject(sub);
                                                    setIsCreateOpen(true);
                                                }}
                                            >
                                                <Edit className="h-4 w-4 text-slate-500" />
                                            </Button>
                                            <Button
                                                variant="ghost"
                                                size="icon"
                                                className="text-red-500 hover:text-red-600 hover:bg-red-50"
                                                onClick={() => handleDelete(sub.id)}
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
