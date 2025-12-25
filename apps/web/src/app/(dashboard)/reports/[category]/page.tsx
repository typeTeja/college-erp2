'use client'

import React from 'react'
import { useParams } from 'next/navigation'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
    ArrowLeft, Download, Search, Filter,
    FileText, Calendar, User, Tag
} from 'lucide-react'
import Link from 'next/link'

export default function ReportCategoryPage() {
    const params = useParams()
    const category = params.category as string

    const categoryTitle = category.charAt(0).toUpperCase() + category.slice(1)

    return (
        <div className="p-6 max-w-7xl mx-auto space-y-6">
            <div className="flex items-center gap-4">
                <Link href="/reports">
                    <Button variant="outline" size="sm" className="h-9 w-9 p-0">
                        <ArrowLeft size={18} />
                    </Button>
                </Link>
                <div>
                    <h1 className="text-3xl font-bold text-slate-900">{categoryTitle} Reports</h1>
                    <p className="text-slate-500 mt-1">Detailed data breakdown and exports</p>
                </div>
                <div className="ml-auto flex gap-3">
                    <Button variant="outline" className="gap-2">
                        <Download size={18} /> Export CSV
                    </Button>
                </div>
            </div>

            <Card className="border-slate-200">
                <CardContent className="p-4 flex flex-col md:flex-row gap-4">
                    <div className="flex-1 relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                        <Input placeholder={`Search ${category} records...`} className="pl-10" />
                    </div>
                    <Button variant="outline" className="gap-2">
                        <Filter size={18} /> Date Range
                    </Button>
                </CardContent>
            </Card>

            <Card className="border-slate-200 overflow-hidden shadow-sm">
                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="bg-slate-50 border-b border-slate-200">
                                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">Parameter</th>
                                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">Value</th>
                                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase">Trend</th>
                                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase text-right">Last Updated</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100 italic text-slate-400">
                            <tr>
                                <td colSpan={4} className="px-6 py-12 text-center">
                                    Report data is being compiled. Please wait or try refreshing.
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </Card>
        </div>
    )
}
