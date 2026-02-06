import React from 'react';
import { StructureNode } from '../types';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface GenericDetailsProps {
    node: StructureNode;
}

export function GenericDetails({ node }: GenericDetailsProps) {
    return (
        <div className="space-y-6">
            <h2 className="text-2xl font-bold tracking-tight text-slate-900">{node.label}</h2>
            <Card>
                <CardHeader>
                    <CardTitle className="text-base text-slate-500">Details</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                        {Object.entries(node.data || {}).map(([key, value]) => {
                             if (typeof value === 'object' || key.endsWith('_id') || key === 'id') return null;
                             return (
                                 <div key={key} className="flex flex-col">
                                     <span className="text-slate-500 capitalize">{key.replace(/_/g, ' ')}</span>
                                     <span className="font-medium">{String(value)}</span>
                                 </div>
                             );
                        })}
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
