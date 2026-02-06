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
import {
    Select, SelectContent, SelectItem, SelectTrigger, SelectValue
} from '@/components/ui/select';
import { Plus, Search, Layers, ExternalLink, Filter, RefreshCw } from 'lucide-react';
import { batchService } from '@/utils/batch-service';
import { programService } from '@/utils/program-service';
import { BatchStatus } from '@/types/academic-base';
import { toast } from 'sonner';

export function BatchMaster() {
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedProgramId, setSelectedProgramId] = useState<string>("all");

    const { data: programs = [] } = programService.usePrograms();
    const {
        data: batches = [],
        isLoading,
        refetch
    } = batchService.useBatches(selectedProgramId !== "all" ? parseInt(selectedProgramId) : undefined);

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
                            className="pl-9 h-10 border-slate-200 focus:border-blue-500 focus:ring-blue-500"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                    <div className="flex items-center gap-2">
                        <Filter className="h-4 w-4 text-slate-400" />
                        <Select value={selectedProgramId} onValueChange={setSelectedProgramId}>
                            <SelectTrigger className="w-64 h-10 border-slate-200 focus:border-blue-500 focus:ring-blue-500">
                                <SelectValue placeholder="All Programs" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="all">All Programs</SelectItem>
                                {programs.map(p => (
                                    <SelectItem key={p.id} value={p.id.toString()}>{p.name}</SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>
                </div>

                <div className="flex gap-2">
                    <Button
                        variant="outline"
                        size="icon"
                        onClick={() => refetch()}
                        className="h-10 w-10 border-slate-200 hover:bg-slate-50 hover:text-blue-600 transition-all active:scale-95"
                    >
                        <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
                    </Button>
                    <Link href="/setup/bulk-setup">
                        <Button className="h-10 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 shadow-md transition-all active:scale-95">
                            <Plus className="h-4 w-4 mr-2" />
                            Bulk Batch Setup
                        </Button>
                    </Link>
                </div>
            </div>

            <Card className="border-slate-200 shadow-sm overflow-hidden">
                <CardContent className="p-0">
                    <Table>
                        <TableHeader className="bg-slate-50">
                            <TableRow>
                                <TableHead className="font-semibold text-slate-700">Batch Name</TableHead>
                                <TableHead className="font-semibold text-slate-700">Program</TableHead>
                                <TableHead className="font-semibold text-slate-700">Academic Year</TableHead>
                                <TableHead className="font-semibold text-slate-700">Current Phase</TableHead>
                                <TableHead className="font-semibold text-slate-700">Students</TableHead>
                                <TableHead className="font-semibold text-slate-700">Status</TableHead>
                                <TableHead className="text-right font-semibold text-slate-700">Actions</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {filteredBatches.length === 0 ? (
                                <TableRow>
                                    <TableCell colSpan={7} className="text-center py-12 text-slate-500">
                                        <div className="flex flex-col items-center">
                                            <Layers className="h-10 w-10 text-slate-300 mb-2" />
                                            <p>No batches found.</p>
                                            <Link href="/setup/bulk-setup" className="text-blue-600 text-sm mt-2 hover:underline font-bold">
                                                Use Bulk Setup to create your first batch
                                            </Link>
                                        </div>
                                    </TableCell>
                                </TableRow>
                            ) : (
                                filteredBatches.map((batch) => (
                                    <TableRow key={batch.id} className="hover:bg-slate-50/50 transition-colors">
                                        <TableCell>
                                            <div className="flex flex-col">
                                                <span className="font-bold text-slate-900">{batch.batch_name}</span>
                                                <span className="text-xs font-mono text-slate-400">{batch.batch_code}</span>
                                            </div>
                                        </TableCell>
                                        <TableCell className="text-sm font-medium text-slate-600">
                                            {programs.find(p => p.id === batch.program_id)?.name || 'Unknown'}
                                        </TableCell>
                                        <TableCell className="text-sm font-medium text-slate-600">
                                            {batch.start_year} - {batch.end_year}
                                        </TableCell>
                                        <TableCell>
                                            <div className="flex gap-2 items-center">
                                                <Badge variant="outline" className="text-[10px] h-5 bg-white border-slate-200 text-slate-600">
                                                    Year {batch.current_year}
                                                </Badge>
                                                <Badge variant="outline" className="text-[10px] h-5 bg-blue-50 border-blue-100 text-blue-600 font-bold">
                                                    Sem {batch.current_semester}
                                                </Badge>
                                            </div>
                                        </TableCell>
                                        <TableCell className="text-sm">
                                            <div className="flex items-center gap-1.5">
                                                <div className="w-1.5 h-1.5 rounded-full bg-blue-500" />
                                                <span className="font-bold text-slate-700">{batch.total_students}</span>
                                            </div>
                                        </TableCell>
                                        <TableCell>
                                            <Badge
                                                className={
                                                    batch.status === BatchStatus.ACTIVE
                                                        ? "bg-green-100 text-green-700 hover:bg-green-100 border-none px-2 shadow-none"
                                                        : batch.status === BatchStatus.COMPLETED
                                                            ? "bg-blue-100 text-blue-700 hover:bg-blue-100 border-none px-2 shadow-none"
                                                            : "bg-slate-100 text-slate-600 hover:bg-slate-100 border-none px-2 shadow-none"
                                                }
                                            >
                                                {batch.status}
                                            </Badge>
                                        </TableCell>
                                        <TableCell className="text-right">
                                            <Link href={`/setup/batches/${batch.id}`}>
                                                <Button size="sm" className="h-8 bg-blue-50 text-blue-600 hover:bg-blue-100 hover:text-blue-700 border-none shadow-none font-bold text-[10px] uppercase tracking-wider">
                                                    Manage
                                                    <ExternalLink className="h-3 w-3 ml-1.5" />
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
