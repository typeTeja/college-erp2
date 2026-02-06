import React from 'react';
import { StructureNode } from '../types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Calendar, Users, BookOpen } from 'lucide-react';

interface SemesterDetailsProps {
    node: StructureNode;
}

export function SemesterDetails({ node }: SemesterDetailsProps) {
    const sem = node.data;
    const startDate = new Date(sem.start_date).toLocaleDateString();
    const endDate = new Date(sem.end_date).toLocaleDateString();

    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-2xl font-bold tracking-tight text-slate-900">{node.label}</h2>
                <div className="flex items-center gap-2 mt-2 text-slate-500 text-sm">
                    <Badge variant="outline">{sem.status}</Badge>
                    <span className="flex items-center gap-1">
                        <Calendar className="w-3.5 h-3.5" />
                        {startDate} - {endDate}
                    </span>
                </div>
            </div>

            <div className="grid gap-4 md:grid-cols-3">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Credits</CardTitle>
                        <BookOpen className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{sem.total_credits}</div>
                        <p className="text-xs text-muted-foreground">Min required: {sem.min_credits}</p>
                    </CardContent>
                </Card>
                {/* 
                  We could show interaction counts here if available in node.children 
                  but we don't have access to children here if they aren't passed.
                  Currently node is just the clicked node structure.
                */}
            </div>
            
            <Card>
                <CardHeader>
                    <CardTitle>Academic Plan</CardTitle>
                </CardHeader>
                <CardContent>
                    <p className="text-sm text-slate-500">
                        Select a Section or Lab Group from the tree to view specific roster and faculty details.
                    </p>
                </CardContent>
            </Card>
        </div>
    );
}
