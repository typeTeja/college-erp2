'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { 
    Table, TableBody, TableCell, TableHead, TableHeader, TableRow 
} from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Plus, Search, Layers, ExternalLink, Filter } from 'lucide-react';
import { batchService } from '@/utils/batch-service';
import { programService } from '@/utils/program-service';
import { BatchStatus } from '@/types/academic-base';
import { toast } from 'sonner';

export function BatchMaster() {
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedProgramId, setSelectedProgramId] = useState<number | undefined>(undefined);

    const { data: programs = [] } = programService.usePrograms();
    const { data: batches = [], isLoading } = batchService.useBatches(selectedProgramId);

    const filteredBatches = batches.filter(b => 
        b.batch_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        b.batch_code.toLowerCase().includes(searchTerm.toLowerCase())
    );

    if (isLoading) {
        return <div className="p-8 text-center animate-pulse text-slate-500">Loading batches...</div>;
    }

    return (
        <div className="space-y-4">
            <div className="flex flex-col md:flex-row justify-between gap-4 bg-white p-4 rounded-lg border border-slate-200 shadow-sm">
                <div className="flex flex-1 gap-4">
                    <div className="relative w-64">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
                        <Input 
                            placeholder="Search batches..." 
                            className="pl-9"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                    <div className="flex items-center gap-2">
                        <Filter className="h-4 w-4 text-slate-400" />
                        <select 
                            className="flex h-10 w-64 rounded-md border border-slate-200 bg-white px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                            value={selectedProgramId || ''}
                            onChange={(e) => setSelectedProgramId(e.target.value ? parseInt(e.target.value) : undefined)}
                        >
                            <option value="">All Programs</option>
                            {programs.map(p => (
                                <option key={p.id} value={p.id}>{p.name}</option>
                            ))}
                        </select>
                    </div>
                </div>
                
                <div className="flex gap-2">
                    <Link href="/setup/bulk-setup">
                        <Button className="bg-blue-600 hover:bg-blue-700">
                            <Plus className="h-4 w-4 mr-2" />
                            Bulk Batch Setup
                        </Button>
                    </Link>
                </div>
            </div>

            <Card>
                <CardContent className="p-0">
                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Batch Name</TableHead>
                                <TableHead>Program</TableHead>
                                <TableHead>Academic Year</TableHead>
                                <TableHead>Current Phase</TableHead>
                                <TableHead>Students</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead className="text-right">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {filteredBatches.length === 0 ? (
                                <TableRow>
                                    <TableCell colSpan={7} className="text-center py-12 text-slate-500">
                                        <div className="flex flex-col items-center">
                                            <Layers className="h-10 w-10 text-slate-300 mb-2" />
                                            <p>No batches found.</p>
                                            <Link href="/setup/bulk-setup" className="text-blue-600 text-sm mt-2 hover:underline">
                                                Use Bulk Setup to create your first batch
                                            </Link>
                                        </div>
                                    </TableCell>
                                </TableRow>
                            ) : (
                                filteredBatches.map((batch) => (
                                    <TableRow key={batch.id}>
                                        <TableCell>
                                            <div className="flex flex-col">
                                                <span className="font-medium text-slate-900">{batch.batch_name}</span>
                                                <span className="text-xs font-mono text-slate-400">{batch.batch_code}</span>
                                            </div>
                                        </TableCell>
                                        <TableCell className="text-sm">
                                            {programs.find(p => p.id === batch.program_id)?.name || 'Unknown'}
                                        </TableCell>
                                        <TableCell className="text-sm">
                                            {batch.start_year} - {batch.end_year}
                                        </TableCell>
                                        <TableCell>
                                            <div className="flex gap-2 items-center">
                                                <Badge variant="outline" className="text-[10px] h-5">
                                                    Year {batch.current_year}
                                                </Badge>
                                                <Badge variant="outline" className="text-[10px] h-5 bg-blue-50">
                                                    Sem {batch.current_semester}
                                                </Badge>
                                            </div>
                                        </TableCell>
                                        <TableCell className="text-sm font-medium">
                                            {batch.total_students}
                                        </TableCell>
                                        <TableCell>
                                            <Badge className={
                                                batch.status === BatchStatus.ACTIVE ? "bg-green-100 text-green-700" : 
                                                batch.status === BatchStatus.COMPLETED ? "bg-blue-100 text-blue-700" :
                                                "bg-slate-100 text-slate-700"
                                            }>
                                                {batch.status}
                                            </Badge>
                                        </TableCell>
                                        <TableCell className="text-right">
                                            <Link href={`/setup/batches/${batch.id}`}>
                                                <Button variant="ghost" size="sm" className="text-blue-600 hover:text-blue-700 hover:bg-blue-50">
                                                    Manage
                                                    <ExternalLink className="h-3 w-3 ml-1" />
                                                </Button>
                                            </Link>
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
