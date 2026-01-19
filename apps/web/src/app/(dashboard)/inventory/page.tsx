'use client'

import React, { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Skeleton } from '@/components/ui/skeleton'
import { Alert, AlertDescription } from '@/components/ui/alert'
import {
    Package, Plus, Search, Filter, AlertTriangle,
    ArrowUpRight, ArrowDownRight, History, Settings,
    QrCode, UserPlus, Boxes
} from 'lucide-react'
import { useAssets } from '@/hooks/use-inventory'
import { Asset, AssetCategory, AllocationStatus } from '@/types/inventory'

export default function InventoryPage() {
    const [searchQuery, setSearchQuery] = useState('')
    const [selectedCategory, setSelectedCategory] = useState<string>('')

    const { data: assets, isLoading, error } = useAssets({
        category: selectedCategory || undefined,
        query: searchQuery || undefined
    })

    const lowStockAssets = assets?.filter((a: Asset) => a.available_stock <= a.reorder_level) || []

    return (
        <div className="p-6 max-w-7xl mx-auto space-y-6">
            {/* Header */}
            <div className="flex justify-between items-end">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900">Inventory & Assets</h1>
                    <p className="text-slate-500 mt-1">Manage stock, allocations and audits</p>
                </div>
                <div className="flex gap-3">
                    <Button variant="outline" className="gap-2">
                        <History size={18} /> Audit History
                    </Button>
                    <Button className="gap-2">
                        <Plus size={18} /> Add New Asset
                    </Button>
                </div>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <Card className="bg-white border-slate-200 shadow-sm">
                    <CardContent className="pt-6">
                        <div className="flex justify-between items-start">
                            <div>
                                <p className="text-slate-500 text-sm font-medium uppercase tracking-wider">Total Items</p>
                                <h3 className="text-3xl font-bold mt-2 text-slate-900">{assets?.length || 0}</h3>
                            </div>
                            <div className="p-2 bg-blue-50 text-blue-600 rounded-lg">
                                <Package size={24} />
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="bg-white border-slate-200 shadow-sm">
                    <CardContent className="pt-6">
                        <div className="flex justify-between items-start">
                            <div>
                                <p className="text-slate-500 text-sm font-medium uppercase tracking-wider">Low Stock</p>
                                <h3 className="text-3xl font-bold mt-2 text-red-600">{lowStockAssets.length}</h3>
                            </div>
                            <div className="p-2 bg-red-50 text-red-600 rounded-lg">
                                <AlertTriangle size={24} />
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="bg-white border-slate-200 shadow-sm">
                    <CardContent className="pt-6">
                        <div className="flex justify-between items-start">
                            <div>
                                <p className="text-slate-500 text-sm font-medium uppercase tracking-wider">Value (Total)</p>
                                <h3 className="text-3xl font-bold mt-2 text-slate-900">
                                    ₹{assets?.reduce((acc: number, curr: Asset) => acc + (curr.total_stock * Number(curr.unit_price)), 0).toLocaleString()}
                                </h3>
                            </div>
                            <div className="p-2 bg-green-50 text-green-600 rounded-lg">
                                <ArrowUpRight size={24} />
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="bg-white border-slate-200 shadow-sm">
                    <CardContent className="pt-6">
                        <div className="flex justify-between items-start">
                            <div>
                                <p className="text-slate-500 text-sm font-medium uppercase tracking-wider">Active Allocations</p>
                                <h3 className="text-3xl font-bold mt-2 text-slate-900">--</h3>
                            </div>
                            <div className="p-2 bg-purple-50 text-purple-600 rounded-lg">
                                <UserPlus size={24} />
                            </div>
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Filters */}
            <Card className="border-slate-200">
                <CardContent className="p-4 flex flex-col md:flex-row gap-4">
                    <div className="flex-1 relative">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={18} />
                        <Input
                            placeholder="Search by asset name or QR code..."
                            className="pl-10"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                    </div>
                    <select
                        className="h-10 px-4 rounded-md border border-slate-200 bg-white text-sm focus:ring-2 focus:ring-blue-500 outline-none"
                        value={selectedCategory}
                        onChange={(e) => setSelectedCategory(e.target.value)}
                    >
                        <option value="">All Categories</option>
                        {Object.values(AssetCategory).map(cat => (
                            <option key={cat} value={cat}>{cat.replace('_', ' ')}</option>
                        ))}
                    </select>
                    <Button variant="outline" className="gap-2">
                        <Filter size={18} /> More Filters
                    </Button>
                </CardContent>
            </Card>

            {/* Main Table */}
            <Card className="border-slate-200 overflow-hidden shadow-sm">
                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="bg-slate-50 border-b border-slate-200">
                                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Item Details</th>
                                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Category</th>
                                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider text-center">In Stock</th>
                                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider text-center">Available</th>
                                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Price (Unit)</th>
                                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider">Status</th>
                                <th className="px-6 py-4 text-xs font-bold text-slate-500 uppercase tracking-wider text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                            {isLoading ? (
                                <tr>
                                    <td colSpan={7} className="px-6 py-12 text-center text-slate-400">Loading inventory records...</td>
                                </tr>
                            ) : assets?.length === 0 ? (
                                <tr>
                                    <td colSpan={7} className="px-6 py-12 text-center text-slate-400">No assets found matching your criteria.</td>
                                </tr>
                            ) : (
                                assets?.map((asset: Asset) => (
                                    <tr key={asset.id} className="hover:bg-slate-50/50 transition-colors group">
                                        <td className="px-6 py-4">
                                            <div className="flex items-center gap-3">
                                                <div className="p-2 bg-slate-100 rounded-lg text-slate-600 group-hover:bg-blue-50 group-hover:text-blue-600 transition-colors">
                                                    <Package size={20} />
                                                </div>
                                                <div>
                                                    <p className="font-bold text-slate-800">{asset.name}</p>
                                                    <p className="text-xs text-slate-400 font-mono">{asset.qr_code || 'No QR'}</p>
                                                </div>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4">
                                            <Badge variant="outline" className="bg-slate-50 text-slate-600 border-slate-200">
                                                {asset.category.replace('_', ' ')}
                                            </Badge>
                                        </td>
                                        <td className="px-6 py-4 text-center font-medium text-slate-700">
                                            {asset.total_stock} <span className="text-xs text-slate-400 font-normal">{asset.unit}</span>
                                        </td>
                                        <td className="px-6 py-4 text-center">
                                            <span className={`font-bold ${asset.available_stock <= asset.reorder_level ? 'text-red-600' : 'text-green-600'}`}>
                                                {asset.available_stock}
                                            </span>
                                            <span className="text-xs text-slate-400 ml-1">available</span>
                                        </td>
                                        <td className="px-6 py-4 font-medium text-slate-700">
                                            ₹{Number(asset.unit_price).toLocaleString()}
                                        </td>
                                        <td className="px-6 py-4">
                                            {asset.available_stock <= asset.reorder_level ? (
                                                <Badge className="bg-red-100 text-red-700 border-none">Low Stock</Badge>
                                            ) : (
                                                <Badge className="bg-green-100 text-green-700 border-none">Healthy</Badge>
                                            )}
                                        </td>
                                        <td className="px-6 py-4 text-right">
                                            <div className="flex justify-end gap-2">
                                                <Button variant="outline" size="sm" className="h-8 w-8 p-0" title="Allocate">
                                                    <UserPlus size={14} />
                                                </Button>
                                                <Button variant="outline" size="sm" className="h-8 w-8 p-0" title="QR Code">
                                                    <QrCode size={14} />
                                                </Button>
                                                <Button variant="outline" size="sm" className="h-8 w-8 p-0" title="Settings">
                                                    <Settings size={14} />
                                                </Button>
                                            </div>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </Card>

            {/* Low Stock Alerts */}
            {lowStockAssets.length > 0 && (
                <div className="bg-red-50 border border-red-100 rounded-xl p-4 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <AlertTriangle className="text-red-600" size={20} />
                        <div>
                            <p className="text-sm font-bold text-red-800">{lowStockAssets.length} items are below reorder level</p>
                            <p className="text-xs text-red-600">Review stock levels and initiate procurement if necessary.</p>
                        </div>
                    </div>
                    <Button size="sm" variant="outline" className="border-red-200 text-red-700 hover:bg-red-100">
                        View Alerts
                    </Button>
                </div>
            )}
        </div>
    )
}
