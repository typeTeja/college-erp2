'use client'

import { useState } from 'react'
import {
    Building2, Bed, Users, ShieldCheck,
    Plus, Search, Filter, AlertTriangle,
    Home, UserPlus, FileText, Settings
} from 'lucide-react'
import { hostelService } from '@/utils/hostel-service'
import { HostelType, RoomType, ComplaintStatus, HostelBlock, HostelRoom, HostelComplaint } from '@/types/hostel'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export default function HostelPage() {
    const [selectedBlock, setSelectedBlock] = useState<number | undefined>(undefined)

    const { data: blocks } = hostelService.useBlocks()
    const { data: rooms, isLoading: roomsLoading } = hostelService.useRooms(selectedBlock)
    const { data: complaints } = hostelService.useComplaints()

    const stats = [
        { label: 'Total Blocks', value: blocks?.length || 0, icon: <Building2 className="text-blue-600" /> },
        { label: 'Total Beds', value: rooms?.reduce((acc: number, r: HostelRoom) => acc + r.capacity, 0) || 0, icon: <Bed className="text-green-600" /> },
        { label: 'Occupied', value: rooms?.reduce((acc: number, r: HostelRoom) => acc + r.current_occupancy, 0) || 0, icon: <Users className="text-orange-600" /> },
        { label: 'Complaints', value: complaints?.filter((c: HostelComplaint) => c.status === ComplaintStatus.OPEN).length || 0, icon: <AlertTriangle className="text-red-600" /> },
    ]

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900 font-outfit">Hostel Management</h1>
                    <p className="text-slate-500 mt-1">Manage residency, allocations and facilities</p>
                </div>
                <div className="flex gap-2">
                    <Button variant="outline">
                        <Plus className="w-4 h-4 mr-2" />
                        New Block
                    </Button>
                    <Button>
                        <UserPlus className="w-4 h-4 mr-2" />
                        Allocate Bed
                    </Button>
                </div>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                {stats.map((stat, i) => (
                    <Card key={i}>
                        <CardContent className="p-6 flex items-center gap-4">
                            <div className="p-3 bg-slate-50 rounded-lg">
                                {stat.icon}
                            </div>
                            <div>
                                <p className="text-sm font-medium text-slate-500">{stat.label}</p>
                                <p className="text-2xl font-bold text-slate-900">{stat.value}</p>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Block Selector & Room List */}
                <div className="lg:col-span-2 space-y-6">
                    <Card>
                        <CardHeader className="border-b bg-slate-50/50">
                            <div className="flex items-center justify-between">
                                <CardTitle className="text-lg">Room Inventory</CardTitle>
                                <div className="flex gap-2">
                                    <select
                                        className="text-sm border rounded-md px-2 py-1"
                                        onChange={(e) => setSelectedBlock(Number(e.target.value) || undefined)}
                                    >
                                        <option value="">All Blocks</option>
                                        {blocks?.map((b: HostelBlock) => (
                                            <option key={b.id} value={b.id}>{b.name}</option>
                                        ))}
                                    </select>
                                </div>
                            </div>
                        </CardHeader>
                        <CardContent className="p-0">
                            <div className="overflow-x-auto">
                                <table className="w-full text-left">
                                    <thead>
                                        <tr className="bg-slate-50 border-b border-slate-200">
                                            <th className="px-6 py-3 text-xs font-semibold text-slate-600 uppercase">Room</th>
                                            <th className="px-6 py-3 text-xs font-semibold text-slate-600 uppercase">Type</th>
                                            <th className="px-6 py-3 text-xs font-semibold text-slate-600 uppercase">Capacity</th>
                                            <th className="px-6 py-3 text-xs font-semibold text-slate-600 uppercase">Occupancy</th>
                                            <th className="px-6 py-3 text-xs font-semibold text-slate-600 uppercase text-right">Rent</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-slate-200">
                                        {roomsLoading ? (
                                            <tr><td colSpan={5} className="px-6 py-4 text-center">Loading...</td></tr>
                                        ) : rooms?.map((room: HostelRoom) => (
                                            <tr key={room.id} className="hover:bg-slate-50 transition-colors">
                                                <td className="px-6 py-4 font-medium text-slate-900">{room.room_number}</td>
                                                <td className="px-6 py-4">
                                                    <Badge variant="info">{room.room_type}</Badge>
                                                </td>
                                                <td className="px-6 py-4 text-slate-600">{room.capacity} Beds</td>
                                                <td className="px-6 py-4">
                                                    <div className="w-full bg-slate-100 rounded-full h-2 max-w-[100px]">
                                                        <div
                                                            className={`h-2 rounded-full ${room.current_occupancy === room.capacity ? 'bg-red-500' : 'bg-blue-600'}`}
                                                            style={{ width: `${(room.current_occupancy / room.capacity) * 100}%` }}
                                                        />
                                                    </div>
                                                    <span className="text-xs text-slate-500 mt-1">{room.current_occupancy}/{room.capacity} filled</span>
                                                </td>
                                                <td className="px-6 py-4 text-right font-semibold text-slate-700">₹{room.monthly_rent}</td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </CardContent>
                    </Card>
                </div>

                {/* Sidebar: Recent Complaints & Gatepasses */}
                <div className="space-y-6">
                    <Card>
                        <CardHeader className="border-b">
                            <CardTitle className="text-lg flex items-center gap-2">
                                <AlertTriangle className="w-5 h-5 text-orange-500" />
                                Active Complaints
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="p-4 space-y-4">
                            {complaints?.filter((c: HostelComplaint) => c.status !== ComplaintStatus.RESOLVED).map((complaint: HostelComplaint) => (
                                <div key={complaint.id} className="p-3 border rounded-lg hover:border-blue-200 transition-colors cursor-pointer">
                                    <div className="flex justify-between items-start mb-1">
                                        <span className="text-sm font-semibold text-slate-900">{complaint.category}</span>
                                        <Badge variant={complaint.priority === 'HIGH' ? 'danger' : 'warning'} className="text-[10px] scale-90">
                                            {complaint.priority}
                                        </Badge>
                                    </div>
                                    <p className="text-xs text-slate-500 line-clamp-2">{complaint.description}</p>
                                    <div className="mt-2 flex items-center justify-between">
                                        <span className="text-[10px] text-slate-400">Date: {new Date(complaint.created_at).toLocaleDateString()}</span>
                                        <span className="text-[10px] font-medium text-blue-600 uppercase">{complaint.status}</span>
                                    </div>
                                </div>
                            ))}
                            <Button variant="secondary" className="w-full text-xs text-slate-500">View All Complaints</Button>
                        </CardContent>
                    </Card>

                    <Card>
                        <CardHeader className="border-b">
                            <CardTitle className="text-lg flex items-center gap-2">
                                <FileText className="w-5 h-5 text-blue-500" />
                                Gatepass Stats
                            </CardTitle>
                        </CardHeader>
                        <CardContent className="p-6">
                            <div className="space-y-4 text-center">
                                <div className="text-3xl font-bold text-slate-900">12</div>
                                <p className="text-sm text-slate-500">Pending Approvals</p>
                                <Button className="w-full">Review Requests</Button>
                            </div>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    )
}
