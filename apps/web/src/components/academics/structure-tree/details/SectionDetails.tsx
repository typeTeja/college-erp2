import React, { useEffect, useState } from 'react';
import { StructureNode } from '../types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Users, User, BookOpen } from 'lucide-react';
import { api } from '@/utils/api';
import { Skeleton } from '@/components/ui/skeleton';

interface SectionDetailsProps {
    node: StructureNode;
}

export function SectionDetails({ node }: SectionDetailsProps) {
    const section = node.data;
    const [stats, setStats] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    // Fetch live stats (e.g. subjects)
    useEffect(() => {
        const fetchDetails = async () => {
            try {
                // Fetch subjects for this semester (Context: section -> batch_semester)
                const subjectsRes = await api.get(`/academic/batch-subjects?batch_semester_id=${section.batch_semester_id}`);
                const theorySubjects = subjectsRes.data.filter((s: any) => s.subject_type === 'THEORY');
                
                // Fetch faculty info if we have an ID
                let faculty = null;
                if (section.faculty_id) {
                    // Assuming endpoint exists or we use the ID display
                    // faculty = await api.get(`/hr/faculty/${section.faculty_id}`);
                }

                setStats({
                    subjects: theorySubjects,
                    subjectCount: theorySubjects.length
                });
            } catch (e) {
                console.error(e);
            } finally {
                setLoading(false);
            }
        };
        fetchDetails();
    }, [section.id, section.batch_semester_id, section.faculty_id]);

    const utilization = Math.round((section.current_strength / section.max_strength) * 100);

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold tracking-tight text-slate-900">{section.name}</h2>
                    <p className="text-sm text-slate-500 font-mono mt-1">Code: {section.code}</p>
                </div>
                <Badge variant={section.is_active ? 'success' : 'secondary'}>
                    {section.is_active ? 'Active' : 'Inactive'}
                </Badge>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Class Strength</CardTitle>
                        <Users className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">
                            {section.current_strength} <span className="text-sm font-normal text-muted-foreground">/ {section.max_strength}</span>
                        </div>
                        <div className="w-full bg-slate-100 h-1.5 mt-2 rounded-full overflow-hidden">
                            <div 
                                className="bg-blue-600 h-full rounded-full" 
                                style={{ width: `${utilization}%` }} 
                            />
                        </div>
                        <p className="text-xs text-muted-foreground mt-1">{utilization}% Capacity</p>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Class Teacher</CardTitle>
                        <User className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                         <div className="text-lg font-medium">
                            {section.faculty_id ? `Faculty #${section.faculty_id}` : 'Unassigned'}
                         </div>
                         <p className="text-xs text-muted-foreground">ID: {section.faculty_id || 'N/A'}</p>
                    </CardContent>
                </Card>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <BookOpen className="h-4 w-4" />
                        Theory Subjects
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    {loading ? (
                        <div className="space-y-2">
                            <Skeleton className="h-10 w-full" />
                            <Skeleton className="h-10 w-full" />
                        </div>
                    ) : stats?.subjects.length > 0 ? (
                        <div className="space-y-2">
                            {stats.subjects.map((sub: any) => (
                                <div key={sub.id} className="flex items-center justify-between p-2 border rounded-md hover:bg-slate-50">
                                    <div className="flex items-center gap-3">
                                        <div className="h-8 w-8 rounded bg-blue-100 text-blue-700 flex items-center justify-center text-xs font-bold">
                                            TH
                                        </div>
                                        <div>
                                            {/* We need subject name. BatchSubject has subject_id, or maybe expanded data? 
                                                If the API for batch-subjects doesn't return joined subject name, we might show ID.
                                                Usually lists return joined data. Let's assume name exists or handle it.
                                            */}
                                            <p className="text-sm font-medium text-slate-900">
                                                {sub.subject?.name || `Subject #${sub.subject_id}`}
                                            </p>
                                            <p className="text-xs text-slate-500">{sub.subject?.code}</p>
                                        </div>
                                    </div>
                                    <Badge variant="outline">{sub.credits} Credits</Badge>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <p className="text-sm text-slate-500 italic">No theory subjects assigned to this semester.</p>
                    )}
                </CardContent>
            </Card>
        </div>
    );
}
