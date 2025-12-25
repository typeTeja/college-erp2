'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import {
    BarChart3, Download, TrendingUp, Users,
    BookOpen, DollarSign, Package, Calendar,
    ArrowUpRight, ArrowDownRight, Filter
} from 'lucide-react'
import { reportService } from '@/utils/report-service'

export default function ReportsDashboard() {
    const { data: academicSyllabus } = reportService.useAcademicSyllabus()
    const { data: academicAttendance } = reportService.useAcademicAttendance()
    const { data: financialFees } = reportService.useFinancialFeeCollection()
    const { data: inventoryStock } = reportService.useInventoryStock()

    return (
        <div className="p-6 max-w-7xl mx-auto space-y-6">
            <div className="flex justify-between items-end">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900 flex items-center gap-3">
                        <BarChart3 className="text-blue-600" />
                        Reports & Analytics
                    </h1>
                    <p className="text-slate-500 mt-1">Institutional performance at a glance</p>
                </div>
                <div className="flex gap-3">
                    <Button variant="outline" className="gap-2">
                        <Filter size={18} /> Filters
                    </Button>
                    <Button className="gap-2 bg-blue-600 hover:bg-blue-700">
                        <Download size={18} /> Export PDF
                    </Button>
                </div>
            </div>

            {/* Top KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <Card className="border-slate-200 shadow-sm">
                    <CardContent className="pt-6">
                        <div className="flex justify-between items-start">
                            <div>
                                <p className="text-slate-500 text-sm font-medium uppercase tracking-wider">Academic Progress</p>
                                <h3 className="text-3xl font-bold mt-2 text-slate-900">
                                    {academicSyllabus?.completion_percentage?.toFixed(1) || 0}%
                                </h3>
                                <p className="text-xs text-green-600 flex items-center gap-1 mt-2">
                                    <TrendingUp size={12} /> +4.2% from last month
                                </p>
                            </div>
                            <div className="p-2 bg-blue-50 text-blue-600 rounded-lg">
                                <BookOpen size={24} />
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-slate-200 shadow-sm">
                    <CardContent className="pt-6">
                        <div className="flex justify-between items-start">
                            <div>
                                <p className="text-slate-500 text-sm font-medium uppercase tracking-wider">Avg. Attendance</p>
                                <h3 className="text-3xl font-bold mt-2 text-slate-900">
                                    {academicAttendance?.overall_percentage?.toFixed(1) || 0}%
                                </h3>
                                <p className="text-xs text-red-600 flex items-center gap-1 mt-2">
                                    <ArrowDownRight size={12} /> -1.5% from last month
                                </p>
                            </div>
                            <div className="p-2 bg-purple-50 text-purple-600 rounded-lg">
                                <Calendar size={24} />
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-slate-200 shadow-sm">
                    <CardContent className="pt-6">
                        <div className="flex justify-between items-start">
                            <div>
                                <p className="text-slate-500 text-sm font-medium uppercase tracking-wider">Fee Collection</p>
                                <h3 className="text-3xl font-bold mt-2 text-slate-900">
                                    ₹{financialFees?.total_collected?.toLocaleString() || 0}
                                </h3>
                                <p className="text-xs text-green-600 flex items-center gap-1 mt-2">
                                    <ArrowUpRight size={12} /> +12% from target
                                </p>
                            </div>
                            <div className="p-2 bg-green-50 text-green-600 rounded-lg">
                                <DollarSign size={24} />
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-slate-200 shadow-sm">
                    <CardContent className="pt-6">
                        <div className="flex justify-between items-start">
                            <div>
                                <p className="text-slate-500 text-sm font-medium uppercase tracking-wider">Inventory Value</p>
                                <h3 className="text-3xl font-bold mt-2 text-slate-900">
                                    ₹{inventoryStock?.total_valuation?.toLocaleString() || 0}
                                </h3>
                                <p className="text-xs text-amber-600 flex items-center gap-1 mt-2">
                                    {inventoryStock?.low_stock_items || 0} items low stock
                                </p>
                            </div>
                            <div className="p-2 bg-amber-50 text-amber-600 rounded-lg">
                                <Package size={24} />
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Detailed sections */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <Card className="border-slate-200">
                    <CardHeader>
                        <CardTitle className="text-lg">Recent Reports</CardTitle>
                        <CardDescription>Quick access to generated documents</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        {[
                            { name: 'Monthly Financial Audit - Dec', type: 'Finance', date: 'Dec 24, 2025' },
                            { name: 'Semester 1 Result Summary', type: 'Academic', date: 'Dec 22, 2025' },
                            { name: 'Asset Verification Report', type: 'Inventory', date: 'Dec 20, 2025' },
                            { name: 'Faculty Workload Matrix', type: 'HR', date: 'Dec 18, 2025' },
                        ].map((report, i) => (
                            <div key={i} className="flex items-center justify-between p-3 hover:bg-slate-50 rounded-lg border border-transparent hover:border-slate-100 transition-all cursor-pointer group">
                                <div className="flex items-center gap-3">
                                    <div className="p-2 bg-slate-100 rounded group-hover:bg-blue-100">
                                        <BarChart3 size={16} className="text-slate-600 group-hover:text-blue-600" />
                                    </div>
                                    <div>
                                        <p className="text-sm font-medium text-slate-900">{report.name}</p>
                                        <p className="text-xs text-slate-500">{report.type} • {report.date}</p>
                                    </div>
                                </div>
                                <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                                    <Download size={14} />
                                </Button>
                            </div>
                        ))}
                    </CardContent>
                </Card>

                <Card className="border-slate-200">
                    <CardHeader>
                        <CardTitle className="text-lg">Analytics Overview</CardTitle>
                        <CardDescription>Key trends and alerts</CardDescription>
                    </CardHeader>
                    <CardContent className="flex items-center justify-center p-12">
                        <div className="text-center space-y-3">
                            <div className="w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center mx-auto text-blue-600">
                                <TrendingUp size={32} />
                            </div>
                            <h4 className="font-semibold text-slate-800">Visual Analytics are being generated...</h4>
                            <p className="text-sm text-slate-500 max-w-xs">Integrating Chart.js/Recharts for student performance and collection projection graphs.</p>
                            <Button variant="outline" size="sm" className="mt-4">Refresh Data</Button>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    )
}
