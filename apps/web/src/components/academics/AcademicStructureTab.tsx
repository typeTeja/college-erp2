"use client";

import React, { useState, useEffect } from 'react';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
    DialogFooter
} from '@/components/ui/dialog';
import { Badge } from '@/components/ui/badge';
import { useToast } from '@/hooks/use-toast';
import {
    Plus,
    Edit2,
    BookOpen,
    Lock,
    History,
    Search,
    Loader2,
    CheckCircle2,
    XCircle
} from 'lucide-react';
import { api } from '@/utils/api';

export default function AcademicStructureTab() {
    const { toast } = useToast();
    const [regulations, setRegulations] = useState<any[]>([]);
    const [programs, setPrograms] = useState<any[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isDialogOpen, setIsDialogOpen] = useState(false);
    const [selectedProgram, setSelectedProgram] = useState<string>('all');

    const fetchData = async () => {
        try {
            setIsLoading(true);
            const [regRes, progRes] = await Promise.all([
                api.get('/academic/regulations'),
                api.get('/academic/programs')
            ]);
            setRegulations(regRes.data);
            setPrograms(progRes.data);
        } catch (error) {
            console.error('Error fetching data:', error);
            toast({
                title: 'Error',
                description: 'Failed to load academic data',
                variant: 'destructive',
            });
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const filteredRegulations = regulations.filter(reg =>
        selectedProgram === 'all' || reg.program_id.toString() === selectedProgram
    );

    return (
        <Card className="border-none shadow-none">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4 px-0">
                <CardTitle className="text-xl font-bold">Academic Regulations</CardTitle>
                <div className="flex items-center gap-4">
                    <select
                        className="h-9 w-[200px] rounded-md border border-input bg-transparent px-3 py-1 text-sm shadow-sm"
                        value={selectedProgram}
                        onChange={(e) => setSelectedProgram(e.target.value)}
                    >
                        <option value="all">All Programs</option>
                        {programs.map(p => (
                            <option key={p.id} value={p.id}>{p.code}</option>
                        ))}
                    </select>
                    <Button className="bg-primary hover:bg-primary/90">
                        <Plus className="mr-2 h-4 w-4" /> New Regulation
                    </Button>
                </div>
            </CardHeader>
            <CardContent className="px-0">
                {isLoading ? (
                    <div className="flex items-center justify-center p-12">
                        <Loader2 className="h-8 w-8 animate-spin text-primary" />
                    </div>
                ) : (
                    <div className="rounded-md border">
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Code</TableHead>
                                    <TableHead>Program</TableHead>
                                    <TableHead>Version</TableHead>
                                    <TableHead>Effective From</TableHead>
                                    <TableHead>Status</TableHead>
                                    <TableHead className="text-right">Actions</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {filteredRegulations.length === 0 ? (
                                    <TableRow>
                                        <TableCell colSpan={6} className="h-24 text-center text-muted-foreground">
                                            No regulations found. Start by creating a new template.
                                        </TableCell>
                                    </TableRow>
                                ) : (
                                    filteredRegulations.map((reg) => (
                                        <TableRow key={reg.id}>
                                            <TableCell className="font-bold">{reg.name}</TableCell>
                                            <TableCell>{programs.find(p => p.id === reg.program_id)?.code || 'N/A'}</TableCell>
                                            <TableCell>
                                                <Badge variant="outline">{reg.regulation_version || 'v1'}</Badge>
                                            </TableCell>
                                            <TableCell>{reg.effective_from_year || 'Any'}</TableCell>
                                            <TableCell>
                                                {reg.is_locked ? (
                                                    <div className="flex items-center text-green-600 gap-1 text-sm">
                                                        <Lock className="h-3 w-3" /> Locked
                                                    </div>
                                                ) : (
                                                    <div className="flex items-center text-amber-600 gap-1 text-sm">
                                                        <Edit2 className="h-3 w-3" /> Draft
                                                    </div>
                                                )}
                                            </TableCell>
                                            <TableCell className="text-right">
                                                <div className="flex justify-end gap-2">
                                                    <Button variant="ghost" size="sm" className="h-8">
                                                        <BookOpen className="h-3.5 w-3.5 mr-1" /> View Rules
                                                    </Button>
                                                    {!reg.is_locked && (
                                                        <Button variant="ghost" size="sm" className="h-8 text-amber-600">
                                                            <Edit2 className="h-3.5 w-3.5 mr-1" /> Edit
                                                        </Button>
                                                    )}
                                                </div>
                                            </TableCell>
                                        </TableRow>
                                    ))
                                )}
                            </TableBody>
                        </Table>
                    </div>
                )}
            </CardContent>

            <div className="mt-6">
                <div className="bg-slate-50 p-4 rounded-lg border border-slate-200 flex items-start gap-3">
                    <History className="h-5 w-5 text-slate-500 mt-0.5" />
                    <div>
                        <h4 className="text-sm font-semibold text-slate-700">Hardening Notice</h4>
                        <p className="text-xs text-slate-500 mt-1 max-w-2xl">
                            Regulations are immutable templates. Once a regulation is used to create a batch, the rules are frozen into the batch independently. Use **Regulation Versioning** (v1, v1.1) for updates to existing frameworks.
                        </p>
                    </div>
                </div>
            </div>
        </Card>
    );
}
