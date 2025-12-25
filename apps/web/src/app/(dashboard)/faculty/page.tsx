'use client'

import { useState } from 'react'
import {
    Users, Plus, Search, Filter, GraduationCap,
    Mail, Phone, BookOpen, Clock, MoreVertical,
    FileText, UserPlus
} from 'lucide-react'
import { facultyService } from '@/utils/faculty-service'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Faculty } from '@/types/faculty'

export default function FacultyPage() {
    const [searchTerm, setSearchTerm] = useState('')
    const [selectedDept, setSelectedDept] = useState<string>('')

    const { data: faculties, isLoading } = facultyService.useFaculties(selectedDept || undefined)

    const filteredFaculties = faculties?.filter(f =>
        f.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        f.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        f.department?.toLowerCase().includes(searchTerm.toLowerCase())
    )

    const departments = Array.from(new Set(faculties?.map(f => f.department).filter(Boolean)))

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-slate-900 font-outfit">Faculty Directory</h1>
                    <p className="text-slate-500 mt-1">Manage teaching staff and academic assignments</p>
                </div>
                <div className="flex gap-2">
                    <Button variant="outline">
                        <FileText className="w-4 h-4 mr-2" />
                        Export
                    </Button>
                    <Button>
                        <UserPlus className="w-4 h-4 mr-2" />
                        Add Faculty
                    </Button>
                </div>
            </div>

            {/* Quick Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <Card>
                    <CardContent className="p-6 flex items-center gap-4">
                        <div className="p-3 bg-blue-50 text-blue-600 rounded-lg">
                            <Users size={24} />
                        </div>
                        <div>
                            <p className="text-sm font-medium text-slate-500">Total Faculty</p>
                            <p className="text-2xl font-bold text-slate-900">{faculties?.length || 0}</p>
                        </div>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6 flex items-center gap-4">
                        <div className="p-3 bg-green-50 text-green-600 rounded-lg">
                            <GraduationCap size={24} />
                        </div>
                        <div>
                            <p className="text-sm font-medium text-slate-500">PhD Holders</p>
                            <p className="text-2xl font-bold text-slate-900">
                                {faculties?.filter(f => f.qualification?.toLowerCase().includes('phd')).length || 0}
                            </p>
                        </div>
                    </CardContent>
                </Card>
                <Card>
                    <CardContent className="p-6 flex items-center gap-4">
                        <div className="p-3 bg-orange-50 text-orange-600 rounded-lg">
                            <Clock size={24} />
                        </div>
                        <div>
                            <p className="text-sm font-medium text-slate-500">Avg. Workload</p>
                            <p className="text-2xl font-bold text-slate-900">18h / week</p>
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Filters */}
            <div className="flex flex-col md:flex-row gap-4 bg-white p-4 rounded-xl border border-slate-200">
                <div className="flex-1 relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 w-4 h-4" />
                    <input
                        type="text"
                        placeholder="Search by name, email or department..."
                        className="w-full pl-10 pr-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
                <div className="flex gap-2">
                    <select
                        className="border rounded-lg px-3 py-2 text-sm outline-none bg-white"
                        value={selectedDept}
                        onChange={(e) => setSelectedDept(e.target.value)}
                    >
                        <option value="">All Departments</option>
                        {departments.map(dept => (
                            <option key={dept} value={dept || ''}>{dept}</option>
                        ))}
                    </select>
                    <Button variant="outline" size="sm">
                        <Filter className="w-4 h-4 mr-2" />
                        More Filters
                    </Button>
                </div>
            </div>

            {/* Faculty List */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {isLoading ? (
                    [1, 2, 3].map(i => (
                        <div key={i} className="h-48 bg-slate-50 animate-pulse rounded-xl border border-slate-100" />
                    ))
                ) : filteredFaculties?.map((faculty: Faculty) => (
                    <Card key={faculty.id} className="hover:border-blue-200 transition-all group">
                        <CardHeader className="flex flex-row items-start justify-between space-y-0 pb-2">
                            <div className="flex items-center gap-3">
                                <div className="w-12 h-12 bg-slate-100 rounded-full flex items-center justify-center text-blue-600 font-bold text-lg">
                                    {faculty.name.split(' ').map(n => n[0]).join('')}
                                </div>
                                <div>
                                    <h3 className="font-semibold text-slate-900">{faculty.name}</h3>
                                    <p className="text-xs text-slate-500">{faculty.designation || 'Lecturer'}</p>
                                </div>
                            </div>
                            <button className="p-1 hover:bg-slate-50 rounded text-slate-400">
                                <MoreVertical size={16} />
                            </button>
                        </CardHeader>
                        <CardContent className="space-y-4 pt-4">
                            <div className="flex flex-wrap gap-2">
                                <Badge variant="info" className="text-[10px]">{faculty.department}</Badge>
                                <Badge variant="secondary" className="text-[10px] bg-slate-100">{faculty.qualification || 'Masters'}</Badge>
                            </div>

                            <div className="space-y-2">
                                <div className="flex items-center gap-2 text-xs text-slate-600">
                                    <Mail size={12} className="text-slate-400" />
                                    <span>{faculty.email || 'N/A'}</span>
                                </div>
                                <div className="flex items-center gap-2 text-xs text-slate-600">
                                    <Phone size={12} className="text-slate-400" />
                                    <span>{faculty.phone || 'N/A'}</span>
                                </div>
                            </div>

                            <div className="pt-4 border-t flex justify-between items-center text-xs">
                                <div className="flex flex-col">
                                    <span className="text-slate-400">Weekly Load</span>
                                    <span className="font-semibold text-slate-700">{faculty.max_weekly_hours} Hours</span>
                                </div>
                                <Button variant="secondary" size="sm" className="h-8 text-[10px] text-blue-600 hover:text-blue-700 hover:bg-blue-50">
                                    View Schedule
                                </Button>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>

            {!isLoading && filteredFaculties?.length === 0 && (
                <div className="text-center py-20 bg-slate-50 rounded-2xl border-2 border-dashed border-slate-200">
                    <GraduationCap className="mx-auto h-12 w-12 text-slate-300 mb-4" />
                    <h3 className="text-lg font-medium text-slate-900">No faculty found</h3>
                    <p className="text-slate-500">Try adjusting your search or filters</p>
                </div>
            )}
        </div>
    )
}
