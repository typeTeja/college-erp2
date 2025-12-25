'use client'

import React from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import {
    Search, Filter, ArrowLeft, ShoppingBag,
    CheckCircle2, CreditCard, User, Ruler
} from 'lucide-react'
import Link from 'next/link'

export default function UniformsPage() {
    return (
        <div className="p-6 max-w-7xl mx-auto space-y-6">
            <div className="flex items-center gap-4">
                <Link href="/inventory">
                    <Button variant="outline" size="sm" className="h-9 w-9 p-0">
                        <ArrowLeft size={18} />
                    </Button>
                </Link>
                <div>
                    <h1 className="text-3xl font-bold text-slate-900">Uniform Management</h1>
                    <p className="text-slate-500 mt-1">Track size allocations and student payments</p>
                </div>
                <div className="ml-auto flex gap-3">
                    <Button className="gap-2">
                        <ShoppingBag size={18} /> Bulk Issue
                    </Button>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card className="border-slate-200">
                    <CardHeader className="pb-2">
                        <CardTitle className="text-lg">Search Student</CardTitle>
                        <CardDescription>Enter Roll No or Name to manage uniforms</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="flex gap-2">
                            <Input placeholder="e.g. 2024-ST-001" />
                            <Button>Search</Button>
                        </div>
                    </CardContent>
                </Card>

                <Card className="border-slate-200 col-span-2">
                    <CardHeader className="pb-2">
                        <CardTitle className="text-lg">Quick Stats</CardTitle>
                    </CardHeader>
                    <CardContent className="flex gap-8">
                        <div>
                            <p className="text-xs text-slate-500 uppercase font-bold tracking-wider">Total Sets Issued</p>
                            <p className="text-2xl font-bold">124</p>
                        </div>
                        <div className="border-l border-slate-100 pl-8">
                            <p className="text-xs text-slate-500 uppercase font-bold tracking-wider">Payment Pending</p>
                            <p className="text-2xl font-bold text-amber-600">₹45,000</p>
                        </div>
                        <div className="border-l border-slate-100 pl-8">
                            <p className="text-xs text-slate-500 uppercase font-bold tracking-wider">OutOfStock Items</p>
                            <p className="text-2xl font-bold text-red-600">2</p>
                        </div>
                    </CardContent>
                </Card>
            </div>

            <Card className="border-slate-200 overflow-hidden shadow-sm">
                <div className="px-6 py-4 bg-slate-50 border-b border-slate-200 flex justify-between items-center">
                    <h3 className="font-bold text-slate-700 uppercase text-xs tracking-widest">Recent Issues</h3>
                    <Button variant="ghost" size="sm" className="text-xs text-blue-600 font-bold p-0 h-auto">View All</Button>
                </div>
                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="border-b border-slate-100">
                                <th className="px-6 py-3 text-xs font-bold text-slate-400">Student</th>
                                <th className="px-6 py-3 text-xs font-bold text-slate-400">Item</th>
                                <th className="px-6 py-3 text-xs font-bold text-slate-400">Size</th>
                                <th className="px-6 py-3 text-xs font-bold text-slate-400">Payment</th>
                                <th className="px-6 py-3 text-xs font-bold text-slate-400">Date Issued</th>
                                <th className="px-6 py-3 text-xs font-bold text-slate-400 text-right">Action</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                            <tr className="hover:bg-slate-50/50">
                                <td className="px-6 py-4">
                                    <div className="flex items-center gap-2">
                                        <div className="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-slate-500">
                                            <User size={14} />
                                        </div>
                                        <div>
                                            <p className="text-sm font-bold text-slate-800">Rahul Sharma</p>
                                            <p className="text-xs text-slate-400">24ADM042</p>
                                        </div>
                                    </div>
                                </td>
                                <td className="px-6 py-4 text-sm font-medium">Chef Coat (Executive)</td>
                                <td className="px-6 py-4">
                                    <Badge variant="outline" className="text-xs">XL</Badge>
                                </td>
                                <td className="px-6 py-4">
                                    <Badge className="bg-green-100 text-green-700 border-none px-2 py-0 text-xs">Paid</Badge>
                                </td>
                                <td className="px-6 py-4 text-sm text-slate-500">Dec 22, 2025</td>
                                <td className="px-6 py-4 text-right">
                                    <Button variant="outline" size="sm" className="h-8 text-xs">Receipt</Button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div className="p-4 bg-slate-50 text-center border-t border-slate-100">
                    <p className="text-xs text-slate-500">Showing last 10 issues. Perform a search to see specific records.</p>
                </div>
            </Card>
        </div>
    )
}
