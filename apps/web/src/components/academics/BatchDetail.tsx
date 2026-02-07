'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import {
    ChevronLeft,
    Users,
    Layers,
    Settings,
    Calendar,
    BookOpen,
    CheckCircle2,
    ArrowRight,
    Search,
    Filter,
    Plus,
    ExternalLink,
    FileText
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Progress } from '@/components/ui/progress';
import {
    Table, TableBody, TableCell, TableHead, TableHeader, TableRow
} from '@/components/ui/table';
import { Input } from '@/components/ui/input';
import { batchService } from '@/utils/batch-service';
import { programService } from '@/utils/program-service';
import { BatchStatus } from '@/types/academic-base';
import { toast } from 'sonner';

interface BatchDetailProps {
    batchId: number;
}

export function BatchDetail({ batchId }: BatchDetailProps) {
    const router = useRouter();
    const [activeTab, setActiveTab] = useState('overview');
    const [studentSearch, setStudentSearch] = useState('');

    const { data: batch, isLoading: isBatchLoading } = batchService.useBatch(batchId);
    const { data: semesters = [], isLoading: isSemLoading } = batchService.useBatchSemesters(batchId);
    const { data: programs = [] } = programService.usePrograms();

    if (isBatchLoading || isSemLoading) {
        return <div className="p-8 text-center animate-pulse text-slate-500">Loading batch details...</div>;
    }

    if (!batch) {
        return (
            <div className="p-12 text-center">
                <h3 className="text-lg font-bold text-slate-800">Batch not found</h3>
                <Button variant="link" onClick={() => router.push('/setup/batches')}>
                    Go back to batches
                </Button>
            </div>
        );
    }

    const program = programs.find(p => p.id === batch.program_id);
    const currentSemester = semesters.find(s => s.semester_number === batch.current_semester);

    return (
        <div className="space-y-6">
            {/* Header / Breadcrumbs */}
            <div className="flex items-center gap-4">
                <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => router.back()}
                    className="h-9 w-9 bg-white border border-slate-200 shadow-sm hover:bg-slate-50"
                >
                    <ChevronLeft className="h-5 w-5" />
                </Button>
                <div>
                    <div className="flex items-center gap-2">
                        <h1 className="text-2xl font-bold text-slate-900">{batch.batch_name}</h1>
                        <Badge variant="outline" className="font-mono text-xs px-2 bg-slate-50">
                            {batch.batch_code}
                        </Badge>
                        <Badge className={
                            batch.status === BatchStatus.ACTIVE ? "bg-green-100 text-green-700 hover:bg-green-100" :
                                batch.status === BatchStatus.COMPLETED ? "bg-blue-100 text-blue-700 hover:bg-blue-100" :
                                    "bg-slate-100 text-slate-700"
                        }>
                            {batch.status}
                        </Badge>
                    </div>
                    <p className="text-sm text-slate-500 mt-0.5">
                        {program?.name} • {batch.start_year} - {batch.end_year}
                    </p>
                </div>
            </div>

            {/* Quick Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <Card className="border-none bg-blue-600 text-white shadow-lg overflow-hidden relative">
                    <CardContent className="pt-6">
                        <div className="flex justify-between items-start opacity-20 absolute -right-4 -bottom-4">
                            <Users size={80} />
                        </div>
                        <p className="text-blue-100 text-xs font-bold uppercase tracking-wider">Total Students</p>
                        <h3 className="text-4xl font-bold mt-2">{batch.total_students}</h3>
                        <p className="text-blue-200 text-[10px] mt-2 flex items-center gap-1">
                            <CheckCircle2 size={10} /> Active roster verified
                        </p>
                    </CardContent>
                </Card>

                <Card className="border-none bg-indigo-600 text-white shadow-lg overflow-hidden relative">
                    <CardContent className="pt-6">
                        <div className="flex justify-between items-start opacity-20 absolute -right-4 -bottom-4">
                            <Layers size={80} />
                        </div>
                        <p className="text-indigo-100 text-xs font-bold uppercase tracking-wider">Current Phase</p>
                        <h3 className="text-4xl font-bold mt-2">Sem {batch.current_semester}</h3>
                        <p className="text-indigo-200 text-[10px] mt-2 flex items-center gap-1">
                            <Calendar size={10} /> Year {batch.current_year}
                        </p>
                    </CardContent>
                </Card>

                <Card className="shadow-sm border-slate-200">
                    <CardContent className="pt-6">
                        <p className="text-slate-500 text-xs font-bold uppercase tracking-wider">Attendance Avg</p>
                        <h3 className="text-4xl font-bold mt-2 text-slate-800">84%</h3>
                        <div className="mt-4">
                            <Progress value={84} className="h-1.5" />
                        </div>
                    </CardContent>
                </Card>

                <Card className="shadow-sm border-slate-200">
                    <CardContent className="pt-6">
                        <p className="text-slate-500 text-xs font-bold uppercase tracking-wider">Pending Tasks</p>
                        <h3 className="text-4xl font-bold mt-2 text-slate-800">3</h3>
                        <p className="text-red-500 text-[10px] mt-2 font-bold uppercase">Actions Required</p>
                    </CardContent>
                </Card>
            </div>

            <Tabs value={activeTab} onValueChange={setActiveTab} className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                <div className="px-6 border-b border-slate-100 pt-2">
                    <TabsList className="bg-transparent gap-6 h-12">
                        <TabsTrigger
                            value="overview"
                            className="text-xs font-bold uppercase tracking-widest text-slate-400 data-[state=active]:text-blue-600 data-[state=active]:border-b-2 data-[state=active]:border-blue-600 rounded-none bg-transparent"
                        >
                            Overview
                        </TabsTrigger>
                        <TabsTrigger
                            value="structure"
                            className="text-xs font-bold uppercase tracking-widest text-slate-400 data-[state=active]:text-blue-600 data-[state=active]:border-b-2 data-[state=active]:border-blue-600 rounded-none bg-transparent"
                        >
                            Academic Structure
                        </TabsTrigger>
                        <TabsTrigger
                            value="students"
                            className="text-xs font-bold uppercase tracking-widest text-slate-400 data-[state=active]:text-blue-600 data-[state=active]:border-b-2 data-[state=active]:border-blue-600 rounded-none bg-transparent"
                        >
                            Students
                        </TabsTrigger>
                        <TabsTrigger
                            value="settings"
                            className="text-xs font-bold uppercase tracking-widest text-slate-400 data-[state=active]:text-blue-600 data-[state=active]:border-b-2 data-[state=active]:border-blue-600 rounded-none bg-transparent"
                        >
                            Control Panel
                        </TabsTrigger>
                    </TabsList>
                </div>

                <TabsContent value="overview" className="p-6">
                    <div className="grid md:grid-cols-2 gap-8">
                        <div>
                            <h3 className="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
                                <CheckCircle2 className="text-green-500 h-5 w-5" />
                                Current Progress
                            </h3>
                            <div className="space-y-6">
                                <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
                                    <div className="flex justify-between items-center mb-2">
                                        <span className="text-sm font-bold text-slate-700">Syllabus Completion</span>
                                        <span className="text-blue-600 font-bold">65%</span>
                                    </div>
                                    <Progress value={65} className="h-2 bg-slate-200" />
                                </div>

                                <div className="space-y-4">
                                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-widest">Upcoming Milestones</h4>
                                    {[
                                        { title: 'Mid-Term Examinations', date: 'March 15, 2026', type: 'EXAM' },
                                        { title: 'Internal Marks Submission', date: 'March 20, 2026', type: 'ADMIN' },
                                        { title: 'Promotion Eligibility Freeze', date: 'April 05, 2026', type: 'SYSTEM' }
                                    ].map((m, i) => (
                                        <div key={i} className="flex items-center justify-between p-3 rounded-lg border border-slate-100 hover:border-slate-200 transition-colors">
                                            <div className="flex items-center gap-3">
                                                <div className="w-2 h-2 rounded-full bg-blue-500" />
                                                <div>
                                                    <p className="text-sm font-bold text-slate-800">{m.title}</p>
                                                    <p className="text-[10px] text-slate-500">{m.date}</p>
                                                </div>
                                            </div>
                                            <Badge variant="outline" className="text-[10px]">{m.type}</Badge>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>

                        <div className="space-y-6">
                            <Card className="border-dashed border-2 bg-slate-50/50">
                                <CardContent className="pt-6">
                                    <h3 className="font-bold text-slate-800 flex items-center gap-2">
                                        <BookOpen className="text-blue-500 h-5 w-5" />
                                        Batch Regulation
                                    </h3>
                                    <p className="text-xs text-slate-500 mt-1">
                                        This batch is operating under the <strong>R24 Regulation</strong> framework.
                                    </p>
                                    <Button variant="outline" size="sm" className="mt-4 w-full h-9 text-xs font-bold">
                                        View Regulation Template
                                    </Button>
                                </CardContent>
                            </Card>

                            <div className="bg-amber-50 border border-amber-200 p-4 rounded-xl flex items-start gap-3">
                                <Settings className="text-amber-600 h-5 w-5 mt-0.5" />
                                <div>
                                    <h4 className="text-sm font-bold text-amber-800">Batch Locked</h4>
                                    <p className="text-xs text-amber-700/80 mt-1 leading-relaxed">
                                        Major structural changes are disabled for active batches. To override, contact system administrator.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </TabsContent>

                <TabsContent value="structure" className="p-0">
                    <Table>
                        <TableHeader className="bg-slate-50">
                            <TableRow>
                                <TableHead className="w-[100px]">Sem</TableHead>
                                <TableHead>Period</TableHead>
                                <TableHead>Subjects</TableHead>
                                <TableHead>Total Credits</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {semesters.map((sem) => (
                                <TableRow key={sem.id}>
                                    <TableCell className="font-bold">Semester {sem.semester_number}</TableCell>
                                    <TableCell className="text-sm">
                                        {sem.start_date || '--'} to {sem.end_date || '--'}
                                    </TableCell>
                                    <TableCell>
                                        <div className="flex gap-1 flex-wrap">
                                            <Badge variant="secondary" className="text-[10px] font-medium bg-slate-100">8 Theory</Badge>
                                            <Badge variant="secondary" className="text-[10px] font-medium bg-slate-100">4 Practical</Badge>
                                        </div>
                                    </TableCell>
                                    <TableCell className="font-bold text-slate-700">22</TableCell>
                                    <TableCell>
                                        <Badge variant={sem.is_current ? "default" : "outline"} className={sem.is_current ? "bg-blue-600" : ""}>
                                            {sem.is_current ? 'Current' : 'Completed'}
                                        </Badge>
                                    </TableCell>
                                    <TableCell className="text-right">
                                        <Button variant="ghost" size="sm" className="text-xs font-bold text-blue-600">
                                            Details <ArrowRight className="h-3 w-3 ml-1" />
                                        </Button>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TabsContent>

                <TabsContent value="students" className="p-6">
                    <div className="flex justify-between items-center mb-6">
                        <div className="relative w-64">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                            <Input
                                placeholder="Search by name or ID..."
                                className="pl-9 h-9"
                                value={studentSearch}
                                onChange={(e) => setStudentSearch(e.target.value)}
                            />
                        </div>
                        <div className="flex gap-2">
                            <Button variant="outline" size="sm" className="h-9">
                                <Plus className="h-4 w-4 mr-2" /> Assign Student
                            </Button>
                        </div>
                    </div>

                    <div className="rounded-xl border border-slate-100 overflow-hidden">
                        <Table>
                            <TableHeader className="bg-slate-50/50">
                                <TableRow>
                                    <TableHead>Student</TableHead>
                                    <TableHead>Enrollment No</TableHead>
                                    <TableHead>Section</TableHead>
                                    <TableHead>Progress</TableHead>
                                    <TableHead className="text-right">Actions</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                <TableRow>
                                    <TableCell colSpan={5} className="text-center py-12 text-slate-400">
                                        <div className="flex flex-col items-center">
                                            <Users className="h-10 w-10 opacity-20 mb-2" />
                                            <p className="text-sm">Connect a student roster to this batch.</p>
                                            <Button variant="link" size="sm" className="text-blue-600">
                                                Start Assignment Wizard
                                            </Button>
                                        </div>
                                    </TableCell>
                                </TableRow>
                            </TableBody>
                        </Table>
                    </div>
                </TabsContent>

                <TabsContent value="settings" className="p-6">
                    <div className="grid md:grid-cols-3 gap-6">
                        {[
                            { title: 'Promotion Engine', desc: 'Promote batch to next semester/year', icon: ArrowRight, color: 'text-blue-600', action: 'Launch Engine' },
                            { title: 'Regulation Swap', desc: 'Update academic framework (R-series)', icon: Layers, color: 'text-indigo-600', action: 'Configure' },
                            { title: 'Freeze Roster', desc: 'Prevent any further student changes', icon: Lock, color: 'text-amber-600', action: 'Lock Now' },
                            { title: 'Bulk Grading', desc: 'Batch update marks and results', icon: CheckCircle2, color: 'text-green-600', action: 'Open Portal' },
                            { title: 'Report Center', desc: 'Generate consolidated batch analytics', icon: FileText, color: 'text-slate-600', action: 'Download' },
                            { title: 'Batch Metadata', desc: 'Edit basic info and dates', icon: Settings, color: 'text-slate-600', action: 'Edit Info' }
                        ].map((item, i) => (
                            <Card key={i} className="hover:border-blue-200 transition-all cursor-pointer group">
                                <CardContent className="pt-6">
                                    <div className={`p-2 rounded-lg bg-slate-50 w-fit mb-4 group-hover:scale-110 transition-transform ${item.color}`}>
                                        <item.icon size={20} />
                                    </div>
                                    <h4 className="font-bold text-slate-800">{item.title}</h4>
                                    <p className="text-[10px] text-slate-500 mt-1 uppercase tracking-wider">{item.desc}</p>
                                    <Button variant="ghost" size="sm" className="mt-4 w-full h-8 text-[10px] font-bold group-hover:bg-slate-50">
                                        {item.action}
                                    </Button>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </TabsContent>
            </Tabs>
        </div>
    );
}

// Internal icons needed
function Lock(props: any) {
    return (
        <svg
            {...props}
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
        >
            <rect width="18" height="11" x="3" y="11" rx="2" ry="2" />
            <path d="M7 11V7a5 5 0 0 1 10 0v4" />
        </svg>
    )
}
