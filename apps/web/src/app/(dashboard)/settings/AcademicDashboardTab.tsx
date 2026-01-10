'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { ChevronDown, ChevronRight, Users, BookOpen, FlaskConical, GraduationCap, Copy } from 'lucide-react';
import Link from 'next/link';
import { InlineEditableField } from '@/components/ui/InlineEditableField';
import { academicDashboardService } from '@/utils/academic-dashboard-service';
import { sectionService } from '@/utils/section-service';
import { BatchCloneDialog } from '@/components/academics/BatchCloneDialog';
import type { AcademicDashboardResponse, DashboardBatch, DashboardYear, DashboardSemester, DashboardSection } from '@/types/academic-dashboard';
import type { Regulation } from '@/types/regulation';
import { toast } from 'sonner';

export default function AcademicDashboardTab() {
    const [dashboard, setDashboard] = useState<AcademicDashboardResponse | null>(null);
    const [regulations, setRegulations] = useState<Regulation[]>([]);
    const [loading, setLoading] = useState(true);
    const [expandedBatches, setExpandedBatches] = useState<Set<number>>(new Set());
    const [cloneDialogOpen, setCloneDialogOpen] = useState(false);
    const [selectedBatch, setSelectedBatch] = useState<DashboardBatch | null>(null);
    const [expandedYears, setExpandedYears] = useState<Set<number>>(new Set());
    const [expandedSemesters, setExpandedSemesters] = useState<Set<number>>(new Set());
    const [expandedSections, setExpandedSections] = useState<Set<number>>(new Set());

    useEffect(() => {
        fetchDashboard();
    }, []);

    const fetchDashboard = async () => {
        try {
            const [dashboardData, regulationsData] = await Promise.all([
                academicDashboardService.getDashboard(),
                fetch('/api/v1/regulations/').then(r => r.json())
            ]);
            setDashboard(dashboardData);
            setRegulations(regulationsData);
            console.log('Dashboard data loaded:', dashboardData);
        } catch (error) {
            console.error('Failed to load dashboard:', error);
            toast.error('Failed to load academic dashboard');
        } finally {
            setLoading(false);
        }
    };

    const handleUpdateSectionCapacity = async (sectionId: number, newCapacity: number) => {
        try {
            await sectionService.updateSection(sectionId, { max_strength: newCapacity });
            toast.success('Section capacity updated');
            // Refresh data
            await fetchDashboard();
        } catch (error: any) {
            toast.error(error.response?.data?.detail || 'Failed to update capacity');
            throw error; // Re-throw to trigger InlineEditableField error handling
        }
    };

    const handleUpdateLabCapacity = async (labId: number, newCapacity: number) => {
        try {
            const response = await fetch(`/api/v1/master/practical-batches/${labId}`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ max_strength: newCapacity }),
            });
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to update');
            }
            toast.success('Lab capacity updated');
            // Refresh data
            await fetchDashboard();
        } catch (error: any) {
            toast.error(error.message || 'Failed to update capacity');
            throw error;
        }
    };

    const toggleExpand = (set: Set<number>, id: number) => {
        const newSet = new Set(set);
        if (newSet.has(id)) {
            newSet.delete(id);
        } else {
            newSet.add(id);
        }
        return newSet;
    };

    const toggleBatch = (batchId: number) => {
        setExpandedBatches(prev => {
            const next = new Set(prev);
            if (next.has(batchId)) {
                next.delete(batchId);
            } else {
                next.add(batchId);
            }
            return next;
        });
    };

    const handleCloneBatch = (batch: DashboardBatch) => {
        setSelectedBatch(batch);
        setCloneDialogOpen(true);
    };

    const handleCloneSuccess = () => {
        fetchDashboard();
        setCloneDialogOpen(false);
    };

    const getUtilizationColor = (percentage: number) => {
        if (percentage >= 90) return 'text-red-600 bg-red-50';
        if (percentage >= 70) return 'text-yellow-600 bg-yellow-50';
        if (percentage >= 50) return 'text-green-600 bg-green-50';
        return 'text-blue-600 bg-blue-50';
    };

    if (loading) {
        return (
            <div className="flex justify-center py-12">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
            </div>
        );
    }

    if (!dashboard || dashboard.batches.length === 0) {
        return (
            <Card>
                <CardContent className="py-12 text-center">
                    <GraduationCap className="h-16 w-16 text-slate-300 mx-auto mb-4" />
                    <h3 className="text-lg font-semibold text-slate-700 mb-2">
                        No academic batches found
                    </h3>
                    <p className="text-slate-500 mb-4">
                        Create your first batch using the Bulk Setup wizard
                    </p>
                    <Link
                        href="/academics/bulk-setup"
                        className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                    >
                        <GraduationCap className="h-4 w-4" />
                        Go to Bulk Setup Wizard
                    </Link>
                </CardContent>
            </Card>
        );
    }

    return (
        <div className="space-y-6">
            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
                <Card>
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-xs text-slate-500 uppercase font-medium">Batches</p>
                                <p className="text-2xl font-bold text-slate-900">{dashboard.summary.total_batches}</p>
                            </div>
                            <GraduationCap className="h-8 w-8 text-blue-500 opacity-20" />
                        </div>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-xs text-slate-500 uppercase font-medium">Students</p>
                                <p className="text-2xl font-bold text-slate-900">{dashboard.summary.total_students}</p>
                            </div>
                            <Users className="h-8 w-8 text-green-500 opacity-20" />
                        </div>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-xs text-slate-500 uppercase font-medium">Capacity</p>
                                <p className="text-2xl font-bold text-slate-900">{dashboard.summary.total_capacity}</p>
                            </div>
                            <BookOpen className="h-8 w-8 text-purple-500 opacity-20" />
                        </div>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-xs text-slate-500 uppercase font-medium">Sections</p>
                                <p className="text-2xl font-bold text-slate-900">{dashboard.summary.total_sections}</p>
                            </div>
                            <BookOpen className="h-8 w-8 text-orange-500 opacity-20" />
                        </div>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="pt-6">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-xs text-slate-500 uppercase font-medium">Labs</p>
                                <p className="text-2xl font-bold text-slate-900">{dashboard.summary.total_labs}</p>
                            </div>
                            <FlaskConical className="h-8 w-8 text-cyan-500 opacity-20" />
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Tree View */}
            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <BookOpen className="h-5 w-5 text-blue-600" />
                        Academic Structure
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="space-y-2">
                        {dashboard.batches.map((batch) => (
                            <div key={batch.id} className="border rounded-lg">
                                {/* Batch Level */}
                                <div
                                    className="flex items-center gap-2 p-3 hover:bg-slate-50 cursor-pointer"
                                    onClick={() => toggleBatch(batch.id)}
                                >
                                    {expandedBatches.has(batch.id) ? (
                                        <ChevronDown className="h-4 w-4 text-slate-400" />
                                    ) : (
                                        <ChevronRight className="h-4 w-4 text-slate-400" />
                                    )}
                                    <GraduationCap className="h-4 w-4 text-blue-600" />
                                    <div className="flex items-center justify-between flex-grow">
                                        <div>
                                            <h3 className="text-lg font-semibold">{batch.batch_name}</h3>
                                            <p className="text-sm text-gray-600">
                                                {batch.program_name} • {batch.regulation_name}
                                            </p>
                                        </div>
                                        <div className="flex items-center gap-2">
                                            <Button
                                                size="sm"
                                                variant="outline"
                                                onClick={(e) => { e.stopPropagation(); handleCloneBatch(batch); }}
                                                className="text-blue-600 hover:text-blue-700"
                                            >
                                                <Copy className="h-4 w-4 mr-1" />
                                                Clone
                                            </Button>
                                            <Badge variant={batch.status === 'active' ? 'default' : 'secondary'}>
                                                {batch.status}
                                            </Badge>
                                            <span className="text-slate-600 text-sm">
                                                {batch.total_students} / {batch.total_capacity} students
                                            </span>
                                            <Badge className={getUtilizationColor(batch.overall_utilization)}>
                                                {batch.overall_utilization}%
                                            </Badge>
                                        </div>
                                    </div>
                                </div>

                                {/* Years */}
                                {expandedBatches.has(batch.id) && (
                                    <div className="pl-8 pb-2">
                                        {batch.years.map((year) => (
                                            <div key={year.id} className="border-l-2 border-slate-200 ml-2">
                                                <div
                                                    className="flex items-center gap-2 p-2 hover:bg-slate-50 cursor-pointer"
                                                    onClick={() => setExpandedYears(toggleExpand(expandedYears, year.id))}
                                                >
                                                    {expandedYears.has(year.id) ? (
                                                        <ChevronDown className="h-4 w-4 text-slate-400 ml-2" />
                                                    ) : (
                                                        <ChevronRight className="h-4 w-4 text-slate-400 ml-2" />
                                                    )}
                                                    <BookOpen className="h-4 w-4 text-purple-600" />
                                                    <span className="font-medium text-slate-800">{year.year_name}</span>
                                                    <span className="text-sm text-slate-600 ml-auto">
                                                        {year.total_students} / {year.total_capacity}
                                                    </span>
                                                </div>

                                                {/* Semesters */}
                                                {expandedYears.has(year.id) && (
                                                    <div className="pl-8">
                                                        {year.semesters.map((semester) => (
                                                            <div key={semester.id} className="border-l-2 border-slate-200 ml-2">
                                                                <div
                                                                    className="flex items-center gap-2 p-2 hover:bg-slate-50 cursor-pointer"
                                                                    onClick={() => setExpandedSemesters(toggleExpand(expandedSemesters, semester.id))}
                                                                >
                                                                    {expandedSemesters.has(semester.id) ? (
                                                                        <ChevronDown className="h-4 w-4 text-slate-400 ml-2" />
                                                                    ) : (
                                                                        <ChevronRight className="h-4 w-4 text-slate-400 ml-2" />
                                                                    )}
                                                                    <BookOpen className="h-4 w-4 text-green-600" />
                                                                    <span className="text-sm font-medium text-slate-700">{semester.semester_name}</span>
                                                                    <Badge variant="outline" className="text-xs">{semester.total_credits} credits</Badge>
                                                                    <span className="text-sm text-slate-600 ml-auto">
                                                                        {semester.total_students} / {semester.total_capacity}
                                                                    </span>
                                                                </div>

                                                                {/* Sections */}
                                                                {expandedSemesters.has(semester.id) && (
                                                                    <div className="pl-8">
                                                                        {semester.sections.map((section) => (
                                                                            <div key={section.id} className="border-l-2 border-slate-200 ml-2">
                                                                                <div
                                                                                    className="flex items-center gap-2 p-2 hover:bg-slate-50 cursor-pointer"
                                                                                    onClick={() => setExpandedSections(toggleExpand(expandedSections, section.id))}
                                                                                >
                                                                                    {section.lab_groups.length > 0 && (
                                                                                        expandedSections.has(section.id) ? (
                                                                                            <ChevronDown className="h-4 w-4 text-slate-400 ml-2" />
                                                                                        ) : (
                                                                                            <ChevronRight className="h-4 w-4 text-slate-400 ml-2" />
                                                                                        )
                                                                                    )}
                                                                                    {section.lab_groups.length === 0 && <div className="w-4 ml-2" />}
                                                                                    <Users className="h-4 w-4 text-orange-600" />
                                                                                    <span className="text-sm text-slate-700">{section.name}</span>
                                                                                    {section.faculty_name && (
                                                                                        <Badge variant="secondary" className="text-xs">
                                                                                            {section.faculty_name}
                                                                                        </Badge>
                                                                                    )}
                                                                                    <span className="text-xs text-slate-600 ml-auto">
                                                                                        {section.current_strength} /
                                                                                    </span>
                                                                                    <InlineEditableField
                                                                                        value={section.max_strength}
                                                                                        type="number"
                                                                                        min={section.current_strength}
                                                                                        max={200}
                                                                                        onSave={(newValue) => handleUpdateSectionCapacity(section.id, newValue as number)}
                                                                                    />
                                                                                    <Badge className={`text-xs ${getUtilizationColor(section.utilization_percentage)}`}>
                                                                                        {section.utilization_percentage}%
                                                                                    </Badge>
                                                                                </div>

                                                                                {/* Labs */}
                                                                                {expandedSections.has(section.id) && section.lab_groups.length > 0 && (
                                                                                    <div className="pl-8">
                                                                                        {section.lab_groups.map((lab) => (
                                                                                            <div key={lab.id} className="flex items-center gap-2 p-2 border-l-2 border-slate-200 ml-2">
                                                                                                <FlaskConical className="h-3 w-3 text-cyan-600 ml-2" />
                                                                                                <span className="text-xs text-slate-600">{lab.name}</span>
                                                                                                <span className="text-xs text-slate-500 ml-auto">
                                                                                                    {lab.current_strength} /
                                                                                                </span>
                                                                                                <InlineEditableField
                                                                                                    value={lab.max_strength}
                                                                                                    type="number"
                                                                                                    min={lab.current_strength}
                                                                                                    max={100}
                                                                                                    onSave={(newValue) => handleUpdateLabCapacity(lab.id, newValue as number)}
                                                                                                />
                                                                                                <Badge className={`text-xs ${getUtilizationColor(lab.utilization_percentage)}`}>
                                                                                                    {lab.utilization_percentage}%
                                                                                                </Badge>
                                                                                            </div>
                                                                                        ))}
                                                                                    </div>
                                                                                )}
                                                                            </div>
                                                                        ))}
                                                                    </div>
                                                                )}
                                                            </div>
                                                        ))}
                                                    </div>
                                                )}
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>

            {/* Clone Dialog */}
            {selectedBatch && (
                <BatchCloneDialog
                    open={cloneDialogOpen}
                    onOpenChange={setCloneDialogOpen}
                    sourceBatchId={selectedBatch.id}
                    sourceBatchCode={selectedBatch.batch_code}
                    sourceBatchName={selectedBatch.batch_name}
                    programId={selectedBatch.program_id}
                    regulations={regulations}
                    onSuccess={handleCloneSuccess}
                />
            )}
        </div>
    );
}
