import React from 'react';
import { StructureNode } from './types';
import { Card, CardContent } from '@/components/ui/card';
import { SemesterDetails } from './details/SemesterDetails';
import { SectionDetails } from './details/SectionDetails';
import { LabDetails } from './details/LabDetails';
import { GenericDetails } from './details/GenericDetails';

interface DetailPanelProps {
    node: StructureNode;
}

export function DetailPanel({ node }: DetailPanelProps) {
    // Dispatch mapping
    switch (node.type) {
        case 'SEMESTER':
            return <SemesterDetails node={node} />;
        case 'SECTION':
            return <SectionDetails node={node} />;
        case 'LAB':
            return <LabDetails node={node} />;
        case 'SECTION_GROUP':
        case 'LAB_GROUP':
             // Just show generic info or a summary for the group
             return (
                 <div className="flex flex-col items-center justify-center h-full text-slate-400">
                     <p>Select a specific {node.type === 'SECTION_GROUP' ? 'section' : 'lab'} to view details.</p>
                 </div>
             );
        default:
            return <GenericDetails node={node} />;
    }
}
