import React from 'react';
import { StructureNode } from '../types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { FlaskConical, Users } from 'lucide-react';

interface LabDetailsProps {
    node: StructureNode;
}

export function LabDetails({ node }: LabDetailsProps) {
    const lab = node.data;
    const utilization = Math.round((lab.current_strength / lab.max_strength) * 100);

    return (
        <div className="space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold tracking-tight text-slate-900">{lab.name}</h2>
                    <p className="text-sm text-slate-500 font-mono mt-1">Code: {lab.code}</p>
                </div>
                <Badge variant={lab.is_active ? 'success' : 'secondary'}>
                    {lab.is_active ? 'Active' : 'Inactive'}
                </Badge>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Batch Capacity</CardTitle>
                        <Users className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">
                            {lab.current_strength} <span className="text-sm font-normal text-muted-foreground">/ {lab.max_strength}</span>
                        </div>
                        <div className="w-full bg-slate-100 h-1.5 mt-2 rounded-full overflow-hidden">
                            <div 
                                className="bg-green-600 h-full rounded-full" 
                                style={{ width: `${utilization}%` }} 
                            />
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Type</CardTitle>
                        <FlaskConical className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                         <div className="text-lg font-medium">Practical Group</div>
                         <p className="text-xs text-muted-foreground">For Laboratory Sessions</p>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
