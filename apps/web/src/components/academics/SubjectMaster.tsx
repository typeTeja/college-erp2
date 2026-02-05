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
            short_name: formData.get('short_name') as string || null,
            subject_type: formData.get('subject_type') as SubjectType,
            evaluation_type: formData.get('evaluation_type') as EvaluationType,
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
                        <select 
                            className="flex h-10 w-48 rounded-md border border-slate-200 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                            value={selectedType}
                            onChange={(e) => setSelectedType(e.target.value as SubjectType | 'ALL')}
                        >
                            <option value="ALL">All Types</option>
                            {Object.values(SubjectType).map(type => (
                                <option key={type} value={type}>{type}</option>
                            ))}
                        </select>
                    </div>
                </div>
                
                <Dialog open={isCreateOpen} onOpenChange={(open) => {
                    setIsCreateOpen(open);
                    if (!open) setEditingSubject(null);
                }}>
                    <DialogTrigger asChild>
                        <Button className="bg-blue-600 hover:bg-blue-700">
                            <Plus className="h-4 w-4 mr-2" />
                            Add Subject
                        </Button>
                    </DialogTrigger>
                    <DialogContent className="sm:max-w-[425px]">
                        <form onSubmit={handleSave}>
                            <DialogHeader>
                                <DialogTitle>{editingSubject ? 'Edit Subject' : 'Add New Subject'}</DialogTitle>
                                <DialogDescription>
                                    Enter subject details for the central course catalog.
                                </DialogDescription>
                            </DialogHeader>
                            <div className="grid gap-4 py-4">
                                <div className="grid grid-cols-4 items-center gap-4">
                                    <Label htmlFor="name" className="text-right">Name</Label>
                                    <Input id="name" name="name" defaultValue={editingSubject?.name} className="col-span-3" required />
                                </div>
                                <div className="grid grid-cols-4 items-center gap-4">
                                    <Label htmlFor="code" className="text-right">Code</Label>
                                    <Input id="code" name="code" defaultValue={editingSubject?.code} className="col-span-3" required />
                                </div>
                                <div className="grid grid-cols-4 items-center gap-4">
                                    <Label htmlFor="subject_type" className="text-right">Type</Label>
                                    <select 
                                        id="subject_type" 
                                        name="subject_type" 
                                        defaultValue={editingSubject?.subject_type || SubjectType.THEORY}
                                        className="col-span-3 flex h-10 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    >
                                        {Object.values(SubjectType).map(type => (
                                            <option key={type} value={type}>{type}</option>
                                        ))}
                                    </select>
                                </div>
                                <div className="grid grid-cols-4 items-center gap-4">
                                    <Label htmlFor="evaluation_type" className="text-right">Evaluation</Label>
                                    <select 
                                        id="evaluation_type" 
                                        name="evaluation_type" 
                                        defaultValue={editingSubject?.evaluation_type || EvaluationType.THEORY_ONLY}
                                        className="col-span-3 flex h-10 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    >
                                        {Object.values(EvaluationType).map(type => (
                                            <option key={type} value={type}>{type.replace(/_/g, ' ')}</option>
                                        ))}
                                    </select>
                                </div>
                            </div>
                            <DialogFooter>
                                <Button type="submit" disabled={createMutation.isPending || updateMutation.isPending}>
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
