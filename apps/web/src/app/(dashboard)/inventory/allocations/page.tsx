'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import {
    Search, Filter, ArrowLeft, Download,
    CheckCircle2, AlertCircle, Clock, RotateCcw
} from 'lucide-react'
import Link from 'next/link'
import { AllocationStatus } from '@/types/inventory'

export default function AllocationsPage() {
    return (
        <div className="p-6 max-w-7xl mx-auto space-y-6">
            <div className="flex items-center gap-4">
                <Link href="/inventory">
                    <Button variant="outline" size="sm" className="h-9 w-9 p-0">
                        <ArrowLeft size={18} />
                    </Button>
                </Link>
                <div>
                    <h1 className="text-3xl font-bold text-slate-900">Allocations Tracking</h1>
                    <p className="text-slate-500 mt-1">Monitor issued assets and return schedules</p>
                </div>
                <div className="ml-auto flex gap-3">
                    <Button variant="outline" className="gap-2">
                        <Download size={18} /> Export List
                    </Button>
                </div>
            </div>

            <Card className="border-slate-200">
                <CardContent className="p-4 flex flex-col md:flex-row gap-4">
                    <div className="flex-1 relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                        <Input placeholder="Search by student name, faculty or ID..." className="pl-10" />
                    </div>
                    <select className="h-10 px-4 rounded-md border border-slate-200 bg-white text-sm outline-none">
                        <option value="">All Statuses</option>
                        {Object.values(AllocationStatus).map(status => (
                            <option key={status} value={status}>{status}</option>
                        ))}
                    </select>
                    <Button variant="outline" className="gap-2">
                        <Filter size={18} /> Filters
                    </Button>
                </CardContent>
            </Card>

            <Card className="border-slate-200 overflow-hidden shadow-sm">
                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="bg-slate-50 border-b border-slate-200">
                                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">Asset</th>
                                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">Allocated To</th>
                                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">Qty</th>
                                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">Date</th>
                                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">Due Date</th>
                                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">Status</th>
                                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100 italic text-slate-400">
                            <tr>
                                <td colSpan={7} className="px-6 py-12 text-center">
                                    No active allocations found. Start by issuing assets from the inventory dashboard.
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </Card>
        </div>
    )
}
