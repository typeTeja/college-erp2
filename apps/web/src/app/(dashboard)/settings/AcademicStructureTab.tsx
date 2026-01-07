import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Info } from 'lucide-react';

export function AcademicStructureTab() {
    return (
        <Card>
            <CardHeader>
                <CardTitle className="flex items-center gap-2">
                    <Info className="h-5 w-5 text-blue-600" />
                    Academic Structure
                </CardTitle>
            </CardHeader>
            <CardContent>
                <p className="text-slate-600">
                    Academic Structure is now managed through <strong>Regulations</strong> and <strong>Academic Batches</strong>.
                    <br />
                    Please navigate to the Program Management or Batch Management sections to view details.
                </p>
            </CardContent>
        </Card>
    );
}
