'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { toast } from 'sonner';
import {
    Plus, Edit2, Trash2, Calendar, DollarSign, GraduationCap, Building, Users, Briefcase,
    BookOpen, MapPin, Phone, Mail, Globe, Award, Percent, Clock, X, Check, Search
} from 'lucide-react';
import {
    AcademicYear, getAcademicYears, createAcademicYear, updateAcademicYear, deleteAcademicYear,
    AcademicBatch, getAcademicBatches, createAcademicBatch, updateAcademicBatch, deleteAcademicBatch,
    ProgramInfo, getProgramsList,
    ProgramFull, getPrograms, createProgram, updateProgram, deleteProgram,
    DepartmentInfo, getDepartmentsList, createDepartment, updateDepartment, deleteDepartment,
    FeeHead, getFeeHeads, createFeeHead, updateFeeHead, deleteFeeHead,
    InstallmentPlan, getInstallmentPlans, createInstallmentPlan, updateInstallmentPlan, deleteInstallmentPlan,
    ScholarshipSlab, getScholarshipSlabs, createScholarshipSlab, updateScholarshipSlab, deleteScholarshipSlab,
    Board, getBoards, createBoard, updateBoard, deleteBoard,
    PreviousQualification, getQualifications, createQualification, updateQualification, deleteQualification,
    StudyGroup, getStudyGroups, createStudyGroup, updateStudyGroup, deleteStudyGroup,
    ReservationCategory, getReservationCategories, createReservationCategory, updateReservationCategory, deleteReservationCategory,
    LeadSource, getLeadSources, createLeadSource, updateLeadSource, deleteLeadSource,
    Designation, getDesignations, createDesignation, updateDesignation, deleteDesignation,
    Classroom, getClassrooms, createClassroom, updateClassroom, deleteClassroom,
    PlacementCompany, getPlacementCompanies, createPlacementCompany, updatePlacementCompany, deletePlacementCompany,
} from '@/utils/master-data-service';
import { getRegulations } from '@/utils/regulation-service'; // Import Regulation Service
import { Regulation } from '@/types/regulation'; // Import Regulation Type

// ============================================================================
// Generic Data Table Component
// ============================================================================

interface Column<T> {
    key: keyof T | string;
    label: string;
    render?: (item: T) => React.ReactNode;
}

interface DataTableProps<T> {
    title: string;
    icon: React.ReactNode;
    data: T[];
    columns: Column<T>[];
    onAdd: () => void;
    onEdit: (item: T) => void;
    onDelete: (item: T) => void;
    loading?: boolean;
}

function DataTable<T extends { id: number }>({
    title, icon, data, columns, onAdd, onEdit, onDelete, loading
}: DataTableProps<T>) {
    const [search, setSearch] = useState('');

    const filteredData = data.filter(item =>
        JSON.stringify(item).toLowerCase().includes(search.toLowerCase())
    );

    return (
        <Card>
            <CardHeader className="flex flex-row items-center justify-between">
                <CardTitle className="text-lg flex items-center gap-2">
                    {icon}
                    {title}
                </CardTitle>
                <div className="flex items-center gap-2">
                    <div className="relative">
                        <Search className="absolute left-2 top-2.5 h-4 w-4 text-slate-400" />
                        <Input
                            placeholder="Search..."
                            value={search}
                            onChange={(e) => setSearch(e.target.value)}
                            className="pl-8 w-48"
                        />
                    </div>
                    <Button onClick={onAdd} size="sm" className="bg-blue-600 hover:bg-blue-700">
                        <Plus className="h-4 w-4 mr-1" /> Add
                    </Button>
                </div>
            </CardHeader>
            <CardContent>
                {loading ? (
                    <div className="flex justify-center py-8">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
                    </div>
                ) : filteredData.length === 0 ? (
                    <div className="text-center py-8 text-slate-500">
                        No data found. Click "Add" to create a new entry.
                    </div>
                ) : (
                    <div className="overflow-x-auto">
                        <table className="w-full text-sm">
                            <thead>
                                <tr className="border-b bg-slate-50">
                                    {columns.map((col) => (
                                        <th key={String(col.key)} className="px-4 py-3 text-left font-medium text-slate-600">
                                            {col.label}
                                        </th>
                                    ))}
                                    <th className="px-4 py-3 text-right font-medium text-slate-600">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {filteredData.map((item) => (
                                    <tr key={item.id} className="border-b hover:bg-slate-50">
                                        {columns.map((col) => (
                                            <td key={String(col.key)} className="px-4 py-3">
                                                {col.render ? col.render(item) : String((item as any)[col.key] ?? '-')}
                                            </td>
                                        ))}
                                        <td className="px-4 py-3">
                                            <div className="flex justify-end gap-1">
                                                <Button variant="ghost" size="sm" onClick={() => onEdit(item)}>
                                                    <Edit2 className="h-4 w-4 text-blue-600" />
                                                </Button>
                                                <Button variant="ghost" size="sm" onClick={() => onDelete(item)}>
                                                    <Trash2 className="h-4 w-4 text-red-600" />
                                                </Button>
                                            </div>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </CardContent>
        </Card>
    );
}

// ============================================================================
// Academic Year Tab
// ============================================================================

export function AcademicYearTab() {
    const [data, setData] = useState<AcademicYear[]>([]);
    const [loading, setLoading] = useState(true);
    const [dialogOpen, setDialogOpen] = useState(false);
    const [editItem, setEditItem] = useState<AcademicYear | null>(null);
    const [formData, setFormData] = useState<{
        name: string;
        start_date: string;
        end_date: string;
        status: 'UPCOMING' | 'ACTIVE' | 'COMPLETED';
        is_current: boolean;
    }>({
        name: '', start_date: '', end_date: '', status: 'UPCOMING', is_current: false
    });

    const fetchData = async () => {
        try {
            const result = await getAcademicYears();
            setData(result);
        } catch (e) {
            toast.error('Failed to load academic years');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { fetchData(); }, []);

    const handleSubmit = async () => {
        try {
            if (editItem) {
                await updateAcademicYear(editItem.id, formData);
                toast.success('Academic year updated');
            } else {
                await createAcademicYear(formData);
                toast.success('Academic year created');
            }
            setDialogOpen(false);
            setEditItem(null);
            fetchData();
        } catch (e) {
            toast.error('Operation failed');
        }
    };

    const handleDelete = async (item: AcademicYear) => {
        if (confirm('Are you sure you want to delete this academic year?')) {
            try {
                await deleteAcademicYear(item.id);
                toast.success('Academic year deleted');
                fetchData();
            } catch (e) {
                toast.error('Failed to delete');
            }
        }
    };

    const openAdd = () => {
        setEditItem(null);
        setFormData({ name: '', start_date: '', end_date: '', status: 'UPCOMING', is_current: false });
        setDialogOpen(true);
    };

    const openEdit = (item: AcademicYear) => {
        setEditItem(item);
        setFormData({
            name: item.name,
            start_date: item.start_date,
            end_date: item.end_date,
            status: item.status,
            is_current: item.is_current
        });
        setDialogOpen(true);
    };

    return (
        <>
            <DataTable
                title="Academic Years"
                icon={<Calendar className="h-5 w-5 text-blue-600" />}
                data={data}
                loading={loading}
                columns={[
                    { key: 'name', label: 'Year' },
                    { key: 'start_date', label: 'Start Date' },
                    { key: 'end_date', label: 'End Date' },
                    {
                        key: 'status', label: 'Status', render: (item) => (
                            <Badge variant={item.status === 'ACTIVE' ? 'default' : item.status === 'COMPLETED' ? 'secondary' : 'outline'}>
                                {item.status}
                            </Badge>
                        )
                    },
                    {
                        key: 'is_current', label: 'Current', render: (item) =>
                            item.is_current ? <Check className="h-4 w-4 text-green-600" /> : <X className="h-4 w-4 text-slate-300" />
                    },
                ]}
                onAdd={openAdd}
                onEdit={openEdit}
                onDelete={handleDelete}
            />

            <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>{editItem ? 'Edit Academic Year' : 'Add Academic Year'}</DialogTitle>
                    </DialogHeader>
                    <div className="space-y-4">
                        <div>
                            <Label>Year Name (e.g., 2024-2025)</Label>
                            <Input value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} />
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <Label>Start Date</Label>
                                <Input type="date" value={formData.start_date} onChange={(e) => setFormData({ ...formData, start_date: e.target.value })} />
                            </div>
                            <div>
                                <Label>End Date</Label>
                                <Input type="date" value={formData.end_date} onChange={(e) => setFormData({ ...formData, end_date: e.target.value })} />
                            </div>
                        </div>
                        <div>
                            <Label>Status</Label>
                            <Select value={formData.status} onValueChange={(v: 'UPCOMING' | 'ACTIVE' | 'COMPLETED') => setFormData({ ...formData, status: v })}>
                                <SelectTrigger><SelectValue /></SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="UPCOMING">Upcoming</SelectItem>
                                    <SelectItem value="ACTIVE">Active</SelectItem>
                                    <SelectItem value="COMPLETED">Completed</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                        <div className="flex items-center gap-2">
                            <Switch checked={formData.is_current} onCheckedChange={(v) => setFormData({ ...formData, is_current: v })} />
                            <Label>Set as Current Academic Year</Label>
                        </div>
                        <div className="flex justify-end gap-2">
                            <Button variant="outline" onClick={() => setDialogOpen(false)}>Cancel</Button>
                            <Button onClick={handleSubmit} className="bg-blue-600 hover:bg-blue-700">Save</Button>
                        </div>
                    </div>
                </DialogContent>
            </Dialog>
        </>
    );
}

// ============================================================================
// Departments Tab
// ============================================================================

export function DepartmentsTab() {
    const [data, setData] = useState<DepartmentInfo[]>([]);
    const [loading, setLoading] = useState(true);
    const [dialogOpen, setDialogOpen] = useState(false);
    const [editItem, setEditItem] = useState<DepartmentInfo | null>(null);
    const [formData, setFormData] = useState({
        name: '',
        code: '',
        description: '',
        is_active: true
    });

    const fetchData = async () => {
        try {
            const result = await getDepartmentsList();
            setData(result);
        } catch (e) {
            toast.error('Failed to load departments');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { fetchData(); }, []);

    const handleSubmit = async () => {
        try {
            if (editItem) {
                await updateDepartment(editItem.id, formData);
                toast.success('Department updated');
            } else {
                await createDepartment(formData);
                toast.success('Department created');
            }
            setDialogOpen(false);
            setEditItem(null);
            fetchData();
        } catch (e: any) {
            toast.error(e?.response?.data?.detail || 'Operation failed');
        }
    };

    const handleDelete = async (item: DepartmentInfo) => {
        if (confirm(`Delete department "${item.name}"?`)) {
            try {
                await deleteDepartment(item.id);
                toast.success('Department deleted');
                fetchData();
            } catch (e: any) {
                toast.error(e?.response?.data?.detail || 'Failed to delete');
            }
        }
    };

    const openAdd = () => {
        setEditItem(null);
        setFormData({ name: '', code: '', description: '', is_active: true });
        setDialogOpen(true);
    };

    const openEdit = (item: DepartmentInfo) => {
        setEditItem(item);
        setFormData({
            name: item.name,
            code: item.code,
            description: '', // Desc not in info, might need separate get? ignoring for now as list is simple
            is_active: true
        });
        setDialogOpen(true);
    };

    return (
        <>
            <DataTable
                title="Departments"
                icon={<BookOpen className="h-5 w-5 text-blue-600" />}
                data={data}
                loading={loading}
                columns={[
                    { key: 'name', label: 'Department Name' },
                    { key: 'code', label: 'Code' },
                ]}
                onAdd={openAdd}
                onEdit={openEdit}
                onDelete={handleDelete}
            />

            <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>{editItem ? 'Edit Department' : 'Add Department'}</DialogTitle>
                    </DialogHeader>
                    <div className="space-y-4">
                        <div>
                            <Label>Department Name (e.g., Computer Science)</Label>
                            <Input value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} />
                        </div>
                        <div>
                            <Label>Department Code (e.g., CSE)</Label>
                            <Input value={formData.code} onChange={(e) => setFormData({ ...formData, code: e.target.value.toUpperCase() })} />
                        </div>
                        <div className="flex justify-end gap-2">
                            <Button variant="outline" onClick={() => setDialogOpen(false)}>Cancel</Button>
                            <Button onClick={handleSubmit} className="bg-blue-600 hover:bg-blue-700">Save</Button>
                        </div>
                    </div>
                </DialogContent>
            </Dialog>
        </>
    );
}

// ============================================================================
// Programs/Courses Tab - Add Course Management
// ============================================================================

export function ProgramsTab() {
    const [data, setData] = useState<ProgramFull[]>([]);
    const [departments, setDepartments] = useState<DepartmentInfo[]>([]);
    const [loading, setLoading] = useState(true);
    const [dialogOpen, setDialogOpen] = useState(false);
    const [editItem, setEditItem] = useState<ProgramFull | null>(null);

    const currentYear = new Date().getFullYear();

    const [formData, setFormData] = useState({
        code: '',
        short_name: '',
        name: '',
        program_type: 'UG' as 'UG' | 'PG' | 'DIPLOMA' | 'CERTIFICATE' | 'PHD',
        duration_years: 3,
        description: '',
        semester_system: true,
        rnet_required: true,
        allow_installments: true,
        department_id: 0,
        is_active: true
    });

    const fetchData = async () => {
        try {
            const [programsResult, deptsResult] = await Promise.all([
                getPrograms(),
                getDepartmentsList()
            ]);
            setData(programsResult);
            setDepartments(deptsResult);
        } catch (e) {
            toast.error('Failed to load programs');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { fetchData(); }, []);

    const handleSubmit = async () => {
        if (!formData.code || !formData.name || !formData.department_id) {
            toast.error('Please fill all required fields');
            return;
        }

        try {
            if (editItem) {
                await updateProgram(editItem.id, formData);
                toast.success('Course updated successfully');
            } else {
                await createProgram(formData);
                toast.success('Course added successfully');
            }
            setDialogOpen(false);
            setEditItem(null);
            resetForm();
            fetchData();
        } catch (e: any) {
            toast.error(e?.response?.data?.detail || 'Operation failed');
        }
    };

    const handleDelete = async (item: ProgramFull) => {
        if (confirm(`Delete course "${item.name}"? This cannot be undone if there are no enrolled students.`)) {
            try {
                await deleteProgram(item.id);
                toast.success('Course deleted');
                fetchData();
            } catch (e: any) {
                toast.error(e?.response?.data?.detail || 'Failed to delete');
            }
        }
    };

    const resetForm = () => {
        setFormData({
            code: '',
            short_name: '',
            name: '',
            program_type: 'UG',
            duration_years: 3,
            description: '',
            semester_system: true,
            rnet_required: true,
            allow_installments: true,
            department_id: departments[0]?.id || 0,
            is_active: true
        });
    };

    const openAdd = () => {
        setEditItem(null);
        resetForm();
        setDialogOpen(true);
    };

    const openEdit = (item: ProgramFull) => {
        setEditItem(item);
        setFormData({
            code: item.code,
            short_name: item.short_name || item.code,
            name: item.name,
            program_type: item.program_type,
            duration_years: item.duration_years,
            description: item.description || '',
            semester_system: item.semester_system,
            rnet_required: item.rnet_required,
            allow_installments: item.allow_installments,
            department_id: item.department_id,
            is_active: item.is_active
        });
        setDialogOpen(true);
    };

    // Calculate batch example based on duration
    const batchExample = `${currentYear}-${currentYear + formData.duration_years}`;

    return (
        <>
            <Card>
                <CardHeader className="flex flex-row items-center justify-between">
                    <CardTitle className="text-lg flex items-center gap-2">
                        <BookOpen className="h-5 w-5 text-purple-600" />
                        Programs / Courses
                    </CardTitle>
                    <Button onClick={openAdd} size="sm" className="bg-blue-600 hover:bg-blue-700">
                        <Plus className="h-4 w-4 mr-1" /> Add Course
                    </Button>
                </CardHeader>
                <CardContent>
                    {loading ? (
                        <div className="flex justify-center py-8">
                            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
                        </div>
                    ) : data.length === 0 ? (
                        <div className="text-center py-8 text-slate-500">
                            No courses found. Click "Add Course" to create a new one.
                        </div>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full text-sm">
                                <thead>
                                    <tr className="border-b bg-slate-50">
                                        <th className="px-4 py-3 text-left font-medium text-slate-600">Code</th>
                                        <th className="px-4 py-3 text-left font-medium text-slate-600">Course Name</th>
                                        <th className="px-4 py-3 text-left font-medium text-slate-600">Type</th>
                                        <th className="px-4 py-3 text-left font-medium text-slate-600">Duration</th>
                                        <th className="px-4 py-3 text-left font-medium text-slate-600">System</th>
                                        <th className="px-4 py-3 text-left font-medium text-slate-600">Status</th>
                                        <th className="px-4 py-3 text-right font-medium text-slate-600">Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {data.map((item) => (
                                        <tr key={item.id} className="border-b hover:bg-slate-50">
                                            <td className="px-4 py-3">
                                                <div className="font-medium">{item.code}</div>
                                                <div className="text-xs text-slate-500">{item.short_name}</div>
                                            </td>
                                            <td className="px-4 py-3">
                                                <div>{item.name}</div>
                                                <div className="text-xs text-slate-500">{item.department_name}</div>
                                            </td>
                                            <td className="px-4 py-3">
                                                <Badge variant="outline">{item.program_type}</Badge>
                                            </td>
                                            <td className="px-4 py-3">{item.duration_years} Years</td>
                                            <td className="px-4 py-3">
                                                <Badge variant={item.semester_system ? 'default' : 'secondary'}>
                                                    {item.semester_system ? 'Semester' : 'Year'}
                                                </Badge>
                                            </td>
                                            <td className="px-4 py-3">
                                                <Badge variant={item.is_active ? 'default' : 'secondary'}>
                                                    {item.is_active ? 'Active' : 'Inactive'}
                                                </Badge>
                                            </td>
                                            <td className="px-4 py-3">
                                                <div className="flex justify-end gap-1">
                                                    <Button variant="ghost" size="sm" onClick={() => openEdit(item)}>
                                                        <Edit2 className="h-4 w-4 text-blue-600" />
                                                    </Button>
                                                    <Button variant="ghost" size="sm" onClick={() => handleDelete(item)}>
                                                        <Trash2 className="h-4 w-4 text-red-600" />
                                                    </Button>
                                                </div>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </CardContent>
            </Card>

            <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
                <DialogContent className="max-w-lg">
                    <DialogHeader>
                        <DialogTitle>{editItem ? 'Edit Course' : 'Add Course'}</DialogTitle>
                    </DialogHeader>
                    <div className="space-y-4 max-h-[70vh] overflow-y-auto">
                        {/* Program Code */}
                        <div>
                            <Label>Program Code *</Label>
                            <Input
                                value={formData.code}
                                onChange={(e) => setFormData({ ...formData, code: e.target.value.toUpperCase() })}
                                placeholder="e.g., BHM"
                                disabled={!!editItem}
                            />
                        </div>

                        {/* Short Name */}
                        <div>
                            <Label>Short Name *</Label>
                            <Input
                                value={formData.short_name}
                                onChange={(e) => setFormData({ ...formData, short_name: e.target.value })}
                                placeholder="e.g., BHM"
                            />
                        </div>

                        {/* Course Name */}
                        <div>
                            <Label>Course Name *</Label>
                            <Input
                                value={formData.name}
                                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                placeholder="e.g., Bachelor of Hotel Management"
                            />
                        </div>

                        {/* Department */}
                        <div>
                            <Label>Department *</Label>
                            <Select
                                value={formData.department_id?.toString() || ""}
                                onValueChange={(v) => setFormData({ ...formData, department_id: parseInt(v) })}
                            >
                                <SelectTrigger>
                                    <SelectValue placeholder="Select Department" />
                                </SelectTrigger>
                                <SelectContent>
                                    {departments.map(d => (
                                        <SelectItem key={d.id} value={d.id.toString()}>{d.name}</SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </div>

                        {/* Program Type */}
                        <div>
                            <Label>Program Type</Label>
                            <Select
                                value={formData.program_type}
                                onValueChange={(v: 'UG' | 'PG' | 'DIPLOMA' | 'CERTIFICATE' | 'PHD') => setFormData({ ...formData, program_type: v })}
                            >
                                <SelectTrigger>
                                    <SelectValue />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="UG">Undergraduate (UG)</SelectItem>
                                    <SelectItem value="PG">Postgraduate (PG)</SelectItem>
                                    <SelectItem value="DIPLOMA">Diploma</SelectItem>
                                    <SelectItem value="CERTIFICATE">Certificate</SelectItem>
                                    <SelectItem value="PHD">Ph.D</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>

                        {/* Duration */}
                        <div>
                            <Label>Duration (Years) *</Label>
                            <Input
                                type="number"
                                value={formData.duration_years}
                                onChange={(e) => setFormData({ ...formData, duration_years: parseInt(e.target.value) || 3 })}
                                min={1}
                                max={10}
                            />
                            <p className="text-xs text-slate-500 mt-1">
                                This is used to calculate academic batches. Example: {formData.duration_years}-year course starting {currentYear} = Batch {batchExample}
                            </p>
                        </div>

                        {/* Academic System Toggle */}
                        <div className="bg-slate-50 rounded-lg p-4 space-y-3">
                            <Label className="font-medium">Academic System</Label>
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-2">
                                    <div className={`w-2 h-2 rounded-full ${formData.semester_system ? 'bg-green-500' : 'bg-slate-300'}`} />
                                    <span className={formData.semester_system ? 'text-slate-900 font-medium' : 'text-slate-500'}>
                                        Semester System
                                    </span>
                                </div>
                                <Switch
                                    checked={formData.semester_system}
                                    onCheckedChange={(v) => setFormData({ ...formData, semester_system: v })}
                                />
                            </div>
                            <p className="text-xs text-slate-500">
                                {formData.semester_system
                                    ? '✓ Semester system - Academic year divided into semesters'
                                    : '✗ Year system - Continuous classes throughout the academic year'}
                            </p>
                        </div>

                        {/* RNET Toggle */}
                        <div className="bg-slate-50 rounded-lg p-4 space-y-3">
                            <div className="flex items-center justify-between">
                                <div>
                                    <Label className="font-medium">RNET Required</Label>
                                    <p className="text-xs text-slate-500 mt-1">
                                        {formData.rnet_required
                                            ? 'Students must pass entrance test before admission'
                                            : 'If unchecked, students skip entrance test and go directly to admission offer'}
                                    </p>
                                </div>
                                <Switch
                                    checked={formData.rnet_required}
                                    onCheckedChange={(v) => setFormData({ ...formData, rnet_required: v })}
                                />
                            </div>
                        </div>

                        {/* Installments Toggle */}
                        <div className="bg-slate-50 rounded-lg p-4 space-y-3">
                            <div className="flex items-center justify-between">
                                <div>
                                    <Label className="font-medium">Allow Installments</Label>
                                    <p className="text-xs text-slate-500 mt-1">
                                        Students can pay annual fee in multiple installments
                                    </p>
                                </div>
                                <Switch
                                    checked={formData.allow_installments}
                                    onCheckedChange={(v) => setFormData({ ...formData, allow_installments: v })}
                                />
                            </div>
                        </div>

                        {/* Active Status */}
                        <div className="flex items-center gap-2">
                            <Switch
                                checked={formData.is_active}
                                onCheckedChange={(v) => setFormData({ ...formData, is_active: v })}
                            />
                            <Label>Active</Label>
                        </div>

                        {/* Actions */}
                        <div className="flex justify-end gap-2 pt-4">
                            <Button variant="outline" onClick={() => setDialogOpen(false)}>Cancel</Button>
                            <Button
                                onClick={handleSubmit}
                                className="bg-blue-600 hover:bg-blue-700"
                            >
                                {editItem ? 'Update Course' : 'Add Course'}
                            </Button>
                        </div>
                    </div>
                </DialogContent>
            </Dialog>
        </>
    );
}

// ============================================================================
// Academic Batch Tab - Program-wise batch management
// ============================================================================

export function AcademicBatchTab() {
    const [data, setData] = useState<AcademicBatch[]>([]);
    const [programs, setPrograms] = useState<ProgramInfo[]>([]);
    const [academicYears, setAcademicYears] = useState<AcademicYear[]>([]);
    // New state for regulations
    const [regulations, setRegulations] = useState<Regulation[]>([]);

    const [loading, setLoading] = useState(true);
    const [dialogOpen, setDialogOpen] = useState(false);
    const [editItem, setEditItem] = useState<AcademicBatch | null>(null);
    const [selectedProgram, setSelectedProgram] = useState<ProgramInfo | null>(null);
    const [filterProgramId, setFilterProgramId] = useState<number | null>(null);

    const currentYear = new Date().getFullYear();

    const [formData, setFormData] = useState({
        program_id: 0,
        regulation_id: 0, // Add regulation_id
        academic_year_id: 0,
        admission_year: currentYear,
        max_strength: 60,
        is_active: true
    });

    // Auto-calculate batch name and graduation year based on program selection
    const calculateBatchDetails = (programId: number, admissionYear: number) => {
        const program = programs.find(p => p.id === programId);
        if (program) {
            const graduationYear = admissionYear + program.duration_years;
            const batchName = `${program.code} ${admissionYear}-${graduationYear}`;
            const batchCode = `${program.code}${admissionYear}`;
            return { batchName, batchCode, graduationYear, program };
        }
        return null;
    };

    const fetchData = async () => {
        try {
            const [batchesResult, programsResult, yearsResult] = await Promise.all([
                getAcademicBatches(filterProgramId || undefined),
                getProgramsList(),
                getAcademicYears()
            ]);
            setData(batchesResult);
            setPrograms(programsResult);
            setAcademicYears(yearsResult);
        } catch (e) {
            toast.error('Failed to load data');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { fetchData(); }, [filterProgramId]);

    // Handle program change to fetch regulations
    const handleProgramChange = async (programId: number) => {
        const program = programs.find(p => p.id === programId);
        setSelectedProgram(program || null);
        setFormData(prev => ({ ...prev, program_id: programId, regulation_id: 0 })); // Reset regulation

        // Fetch regulations for this program
        if (programId) {
            try {
                // Fetch ALL regulations for the program, regardless of lock status
                const regs = await getRegulations(programId);
                console.log(`Fetched regulations for program ${programId}:`, regs);
                setRegulations(regs);

                if (regs.length === 0) {
                    toast.warning("No regulations found. Please create a Regulation first.");
                }
            } catch (e) {
                console.error("Failed to load regulations", e);
                toast.error("Failed to load regulations");
                setRegulations([]);
            }
        } else {
            setRegulations([]);
        }
    };

    const handleSubmit = async () => {
        try {
            const details = calculateBatchDetails(formData.program_id, formData.admission_year);
            if (!details) {
                toast.error('Please select a program');
                return;
            }
            if (!formData.regulation_id) {
                toast.error('Please select a regulation');
                return;
            }
            if (!formData.admission_year) {
                toast.error('Please Select Admission Year');
                return;
            }

            const payload = {
                name: details.batchName,
                code: details.batchCode,
                program_id: formData.program_id,
                regulation_id: formData.regulation_id, // Include regulation_id
                academic_year_id: formData.academic_year_id || academicYears.find(y => y.is_current)?.id || academicYears[0]?.id,
                joining_year: formData.admission_year, // Backend expects joining_year
                total_students: formData.max_strength, // Backend expects total_students
                is_active: formData.is_active
            };

            if (editItem) {
                await updateAcademicBatch(editItem.id, payload);
                toast.success('Academic batch updated');
            } else {
                await createAcademicBatch(payload);
                toast.success('Academic batch created');
            }
            setDialogOpen(false);
            setEditItem(null);
            setSelectedProgram(null);
            fetchData();
        } catch (e: any) {
            toast.error(e?.response?.data?.detail || 'Operation failed');
        }
    };

    const handleDelete = async (item: AcademicBatch) => {
        if (confirm(`Delete batch "${item.name}"? This may affect student records.`)) {
            try {
                await deleteAcademicBatch(item.id);
                toast.success('Academic batch deleted');
                fetchData();
            } catch (e) {
                toast.error('Failed to delete');
            }
        }
    };

    const openAdd = () => {
        setEditItem(null);
        setSelectedProgram(null);
        setRegulations([]); // Reset regulations for new entry
        setFormData({
            program_id: 0,
            regulation_id: 0,
            academic_year_id: academicYears.find(y => y.is_current)?.id || 0,
            admission_year: currentYear,
            max_strength: 60,
            is_active: true
        });
        setDialogOpen(true);
    };

    const openEdit = (item: AcademicBatch) => {
        setEditItem(item);
        const program = programs.find(p => p.id === item.program_id);
        setSelectedProgram(program || null);
        // We need to fetch regulations for the program to populate the dropdown
        if (item.program_id) {
            getRegulations(item.program_id).then(regs => setRegulations(regs));
        }

        setFormData({
            program_id: item.program_id,
            regulation_id: item.regulation_id || 0,
            academic_year_id: item.academic_year_id || 0, // Fallback
            admission_year: item.joining_year,
            max_strength: item.total_students,
            is_active: item.is_active
        });
        setDialogOpen(true);
    };

    // Preview calculation
    const previewDetails = formData.program_id ? calculateBatchDetails(formData.program_id, formData.admission_year) : null;

    return (
        <>
            <Card>
                <CardHeader className="flex flex-row items-center justify-between">
                    <CardTitle className="text-lg flex items-center gap-2">
                        <GraduationCap className="h-5 w-5 text-indigo-600" />
                        Academic Batches
                    </CardTitle>
                    <div className="flex items-center gap-2">
                        <Select
                            value={filterProgramId?.toString() || "all"}
                            onValueChange={(v) => setFilterProgramId(v === "all" ? null : parseInt(v))}
                        >
                            <SelectTrigger className="w-48">
                                <SelectValue placeholder="Filter by Program" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="all">All Programs</SelectItem>
                                {programs.map(p => (
                                    <SelectItem key={p.id} value={p.id.toString()}>{p.code} - {p.name}</SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                        <Button onClick={openAdd} size="sm" className="bg-blue-600 hover:bg-blue-700">
                            <Plus className="h-4 w-4 mr-1" /> Create Batch
                        </Button>
                    </div>
                </CardHeader>
                <CardContent>
                    {loading ? (
                        <div className="flex justify-center py-8">
                            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
                        </div>
                    ) : data.length === 0 ? (
                        <div className="text-center py-8 text-slate-500">
                            No batches found. Click "Create Batch" to add a new one.
                        </div>
                    ) : (
                        <div className="overflow-x-auto">
                            <table className="w-full text-sm">
                                <thead>
                                    <tr className="border-b bg-slate-50">
                                        <th className="px-4 py-3 text-left font-medium text-slate-600">Batch Name</th>
                                        <th className="px-4 py-3 text-left font-medium text-slate-600">Program</th>
                                        <th className="px-4 py-3 text-left font-medium text-slate-600">Admission Year</th>
                                        <th className="px-4 py-3 text-left font-medium text-slate-600">Graduation Year</th>
                                        <th className="px-4 py-3 text-left font-medium text-slate-600">Strength</th>
                                        <th className="px-4 py-3 text-left font-medium text-slate-600">Status</th>
                                        <th className="px-4 py-3 text-right font-medium text-slate-600">Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {data.map((item) => {
                                        // Lookup program details
                                        const program = programs.find(p => p.id === item.program_id);
                                        return (
                                            <tr key={item.id} className="border-b hover:bg-slate-50">
                                                <td className="px-4 py-3">
                                                    <div className="font-medium">{item.name || (item as any).batch_name}</div>
                                                    <div className="text-xs text-slate-500">{item.code || (item as any).batch_code}</div>
                                                </td>
                                                <td className="px-4 py-3">
                                                    <Badge variant="outline">{program ? program.code : (item.program_code || item.program_name || '-')}</Badge>
                                                </td>
                                                <td className="px-4 py-3">{item.admission_year || (item as any).joining_year}</td>
                                                <td className="px-4 py-3">{item.graduation_year || (item as any).end_year}</td>
                                                <td className="px-4 py-3">
                                                    <span className="text-blue-600 font-medium">{item.current_strength || 0}</span>
                                                    <span className="text-slate-400"> / {item.max_strength || (item as any).total_students}</span>
                                                </td>
                                                <td className="px-4 py-3">
                                                    <Badge variant={item.is_active ? 'default' : 'secondary'}>
                                                        {item.is_active ? 'Active' : 'Inactive'}
                                                    </Badge>
                                                </td>
                                                <td className="px-4 py-3">
                                                    <div className="flex justify-end gap-1">
                                                        <Button variant="ghost" size="sm" onClick={() => openEdit(item)}>
                                                            <Edit2 className="h-4 w-4 text-blue-600" />
                                                        </Button>
                                                        <Button variant="ghost" size="sm" onClick={() => handleDelete(item)}>
                                                            <Trash2 className="h-4 w-4 text-red-600" />
                                                        </Button>
                                                    </div>
                                                </td>
                                            </tr>
                                        );
                                    })}
                                </tbody>
                            </table>
                        </div>
                    )}
                </CardContent>
            </Card>

            <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
                <DialogContent className="max-w-lg">
                    <DialogHeader>
                        <DialogTitle>{editItem ? 'Edit Academic Batch' : 'Create Academic Batch'}</DialogTitle>
                    </DialogHeader>
                    <div className="space-y-4">
                        {/* Program Selection */}
                        <div>
                            <Label>Program *</Label>
                            <Select
                                value={formData.program_id?.toString() || ""}
                                onValueChange={(v) => handleProgramChange(parseInt(v))}
                            >
                                <SelectTrigger>
                                    <SelectValue placeholder="Select Program" />
                                </SelectTrigger>
                                <SelectContent>
                                    {programs.map(p => (
                                        <SelectItem key={p.id} value={p.id.toString()}>
                                            {p.code} - {p.name} ({p.duration_years} years)
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                            {selectedProgram && (
                                <p className="text-xs text-slate-500 mt-1">
                                    Duration: {selectedProgram.duration_years} years | Type: {selectedProgram.program_type}
                                </p>
                            )}
                        </div>

                        {/* Admission Year */}
                        <div>
                            <Label>Regulation *</Label>
                            <Select
                                value={formData.regulation_id?.toString() || "0"}
                                onValueChange={(v) => setFormData(prev => ({ ...prev, regulation_id: parseInt(v) }))}
                                disabled={!formData.program_id}
                            >
                                <SelectTrigger>
                                    <SelectValue placeholder={formData.program_id ? "Select Regulation" : "Select Program First"} />
                                </SelectTrigger>
                                <SelectContent>
                                    {regulations.map(r => (
                                        <SelectItem key={r.id} value={r.id.toString()}>
                                            {r.regulation_name} ({r.regulation_code}) {r.is_active ? '' : '(Inactive)'}
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                            {formData.program_id && regulations.length === 0 && (
                                <p className="text-xs text-red-600 mt-1">No regulations found. Go to Regulations tab to create one.</p>
                            )}
                        </div>

                        {/* Admission Year */}
                        <div>
                            <Label>Joining Year (Admission Year) *</Label>
                            <Select
                                value={formData.admission_year.toString()}
                                onValueChange={(v) => setFormData({ ...formData, admission_year: parseInt(v) })}
                            >
                                <SelectTrigger>
                                    <SelectValue />
                                </SelectTrigger>
                                <SelectContent>
                                    {Array.from({ length: 10 }, (_, i) => currentYear - 5 + i).map(year => (
                                        <SelectItem key={year} value={year.toString()}>{year}</SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </div>

                        {/* Auto-calculated Preview */}
                        {previewDetails && (
                            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 space-y-2">
                                <h4 className="font-medium text-blue-800 flex items-center gap-2">
                                    <Check className="h-4 w-4" /> Batch Preview
                                </h4>
                                <div className="grid grid-cols-2 gap-2 text-sm">
                                    <div>
                                        <span className="text-slate-600">Batch Name:</span>
                                        <div className="font-medium text-blue-900">{previewDetails.batchName}</div>
                                    </div>
                                    <div>
                                        <span className="text-slate-600">Batch Code:</span>
                                        <div className="font-medium text-blue-900">{previewDetails.batchCode}</div>
                                    </div>
                                    <div>
                                        <span className="text-slate-600">Start Year:</span>
                                        <div className="font-medium">{formData.admission_year + 1}</div>
                                    </div>
                                    <div>
                                        <span className="text-slate-600">Graduation Year:</span>
                                        <div className="font-medium">{previewDetails.graduationYear}</div>
                                    </div>
                                </div>
                            </div>
                        )}

                        {/* Max Strength */}
                        <div>
                            <Label>Maximum Strength</Label>
                            <Input
                                type="number"
                                value={formData.max_strength}
                                onChange={(e) => setFormData({ ...formData, max_strength: parseInt(e.target.value) || 60 })}
                                min={1}
                            />
                        </div>

                        {/* Active Status */}
                        <div className="flex items-center gap-2">
                            <Switch
                                checked={formData.is_active}
                                onCheckedChange={(v) => setFormData({ ...formData, is_active: v })}
                            />
                            <Label>Active</Label>
                        </div>

                        {/* Actions */}
                        <div className="flex justify-end gap-2 pt-4">
                            <Button variant="outline" onClick={() => setDialogOpen(false)}>Cancel</Button>
                            <Button
                                onClick={handleSubmit}
                                className="bg-blue-600 hover:bg-blue-700"
                                disabled={!formData.program_id}
                            >
                                {editItem ? 'Update Batch' : 'Create Batch'}
                            </Button>
                        </div>
                    </div>
                </DialogContent>
            </Dialog>
        </>
    );
}

// ============================================================================
// Fee Head Tab
// ============================================================================

export function FeeHeadTab() {
    const [data, setData] = useState<FeeHead[]>([]);
    const [loading, setLoading] = useState(true);
    const [dialogOpen, setDialogOpen] = useState(false);
    const [editItem, setEditItem] = useState<FeeHead | null>(null);
    const [formData, setFormData] = useState({
        name: '', code: '', description: '', is_refundable: false, is_recurring: true, is_mandatory: true, display_order: 0, is_active: true
    });

    const fetchData = async () => {
        try {
            const result = await getFeeHeads();
            setData(result);
        } catch (e) {
            toast.error('Failed to load fee heads');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { fetchData(); }, []);

    const handleSubmit = async () => {
        try {
            if (editItem) {
                await updateFeeHead(editItem.id, formData);
                toast.success('Fee head updated');
            } else {
                await createFeeHead(formData);
                toast.success('Fee head created');
            }
            setDialogOpen(false);
            fetchData();
        } catch (e) {
            toast.error('Operation failed');
        }
    };

    const handleDelete = async (item: FeeHead) => {
        if (confirm('Delete this fee head?')) {
            try {
                await deleteFeeHead(item.id);
                toast.success('Fee head deleted');
                fetchData();
            } catch (e) {
                toast.error('Failed to delete');
            }
        }
    };

    return (
        <>
            <DataTable
                title="Fee Heads"
                icon={<DollarSign className="h-5 w-5 text-green-600" />}
                data={data}
                loading={loading}
                columns={[
                    { key: 'name', label: 'Name' },
                    { key: 'code', label: 'Code' },
                    { key: 'is_refundable', label: 'Refundable', render: (item) => item.is_refundable ? 'Yes' : 'No' },
                    { key: 'is_mandatory', label: 'Mandatory', render: (item) => item.is_mandatory ? 'Yes' : 'No' },
                    { key: 'is_active', label: 'Status', render: (item) => <Badge variant={item.is_active ? 'default' : 'secondary'}>{item.is_active ? 'Active' : 'Inactive'}</Badge> },
                ]}
                onAdd={() => {
                    setEditItem(null);
                    setFormData({ name: '', code: '', description: '', is_refundable: false, is_recurring: true, is_mandatory: true, display_order: 0, is_active: true });
                    setDialogOpen(true);
                }}
                onEdit={(item) => {
                    setEditItem(item);
                    setFormData(item as any);
                    setDialogOpen(true);
                }}
                onDelete={handleDelete}
            />

            <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>{editItem ? 'Edit Fee Head' : 'Add Fee Head'}</DialogTitle>
                    </DialogHeader>
                    <div className="space-y-4">
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <Label>Name</Label>
                                <Input value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} placeholder="e.g., Tuition Fee" />
                            </div>
                            <div>
                                <Label>Code</Label>
                                <Input value={formData.code} onChange={(e) => setFormData({ ...formData, code: e.target.value.toUpperCase() })} placeholder="e.g., TF" />
                            </div>
                        </div>
                        <div>
                            <Label>Description</Label>
                            <Textarea value={formData.description} onChange={(e) => setFormData({ ...formData, description: e.target.value })} />
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="flex items-center gap-2">
                                <Switch checked={formData.is_refundable} onCheckedChange={(v) => setFormData({ ...formData, is_refundable: v })} />
                                <Label>Refundable</Label>
                            </div>
                            <div className="flex items-center gap-2">
                                <Switch checked={formData.is_mandatory} onCheckedChange={(v) => setFormData({ ...formData, is_mandatory: v })} />
                                <Label>Mandatory</Label>
                            </div>
                            <div className="flex items-center gap-2">
                                <Switch checked={formData.is_recurring} onCheckedChange={(v) => setFormData({ ...formData, is_recurring: v })} />
                                <Label>Recurring</Label>
                            </div>
                            <div className="flex items-center gap-2">
                                <Switch checked={formData.is_active} onCheckedChange={(v) => setFormData({ ...formData, is_active: v })} />
                                <Label>Active</Label>
                            </div>
                        </div>
                        <div className="flex justify-end gap-2">
                            <Button variant="outline" onClick={() => setDialogOpen(false)}>Cancel</Button>
                            <Button onClick={handleSubmit} className="bg-blue-600 hover:bg-blue-700">Save</Button>
                        </div>
                    </div>
                </DialogContent>
            </Dialog>
        </>
    );
}

// ============================================================================
// Board Tab
// ============================================================================

export function BoardTab() {
    const [data, setData] = useState<Board[]>([]);
    const [loading, setLoading] = useState(true);
    const [dialogOpen, setDialogOpen] = useState(false);
    const [editItem, setEditItem] = useState<Board | null>(null);
    const [formData, setFormData] = useState({
        name: '', code: '', full_name: '', state: '', country: 'India', is_active: true, display_order: 0
    });

    const fetchData = async () => {
        try {
            const result = await getBoards();
            setData(result);
        } catch (e) {
            toast.error('Failed to load boards');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { fetchData(); }, []);

    const handleSubmit = async () => {
        try {
            if (editItem) {
                await updateBoard(editItem.id, formData);
                toast.success('Board updated');
            } else {
                await createBoard(formData);
                toast.success('Board created');
            }
            setDialogOpen(false);
            fetchData();
        } catch (e) {
            toast.error('Operation failed');
        }
    };

    const handleDelete = async (item: Board) => {
        if (confirm('Delete this board?')) {
            try {
                await deleteBoard(item.id);
                toast.success('Board deleted');
                fetchData();
            } catch (e) {
                toast.error('Failed to delete');
            }
        }
    };

    return (
        <>
            <DataTable
                title="Boards / Universities"
                icon={<BookOpen className="h-5 w-5 text-purple-600" />}
                data={data}
                loading={loading}
                columns={[
                    { key: 'name', label: 'Name' },
                    { key: 'code', label: 'Code' },
                    { key: 'state', label: 'State' },
                    { key: 'country', label: 'Country' },
                    { key: 'is_active', label: 'Status', render: (item) => <Badge variant={item.is_active ? 'default' : 'secondary'}>{item.is_active ? 'Active' : 'Inactive'}</Badge> },
                ]}
                onAdd={() => {
                    setEditItem(null);
                    setFormData({ name: '', code: '', full_name: '', state: '', country: 'India', is_active: true, display_order: 0 });
                    setDialogOpen(true);
                }}
                onEdit={(item) => {
                    setEditItem(item);
                    setFormData(item as any);
                    setDialogOpen(true);
                }}
                onDelete={handleDelete}
            />

            <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>{editItem ? 'Edit Board' : 'Add Board'}</DialogTitle>
                    </DialogHeader>
                    <div className="space-y-4">
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <Label>Name</Label>
                                <Input value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} placeholder="e.g., CBSE" />
                            </div>
                            <div>
                                <Label>Code</Label>
                                <Input value={formData.code} onChange={(e) => setFormData({ ...formData, code: e.target.value.toUpperCase() })} placeholder="e.g., CBSE" />
                            </div>
                        </div>
                        <div>
                            <Label>Full Name</Label>
                            <Input value={formData.full_name} onChange={(e) => setFormData({ ...formData, full_name: e.target.value })} placeholder="e.g., Central Board of Secondary Education" />
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <Label>State</Label>
                                <Input value={formData.state} onChange={(e) => setFormData({ ...formData, state: e.target.value })} placeholder="e.g., Telangana" />
                            </div>
                            <div>
                                <Label>Country</Label>
                                <Input value={formData.country} onChange={(e) => setFormData({ ...formData, country: e.target.value })} />
                            </div>
                        </div>
                        <div className="flex items-center gap-2">
                            <Switch checked={formData.is_active} onCheckedChange={(v) => setFormData({ ...formData, is_active: v })} />
                            <Label>Active</Label>
                        </div>
                        <div className="flex justify-end gap-2">
                            <Button variant="outline" onClick={() => setDialogOpen(false)}>Cancel</Button>
                            <Button onClick={handleSubmit} className="bg-blue-600 hover:bg-blue-700">Save</Button>
                        </div>
                    </div>
                </DialogContent>
            </Dialog>
        </>
    );
}

// ============================================================================
// Reservation Category Tab
// ============================================================================

export function ReservationCategoryTab() {
    const [data, setData] = useState<ReservationCategory[]>([]);
    const [loading, setLoading] = useState(true);
    const [dialogOpen, setDialogOpen] = useState(false);
    const [editItem, setEditItem] = useState<ReservationCategory | null>(null);
    const [formData, setFormData] = useState({
        name: '', code: '', full_name: '', reservation_percentage: 0, fee_concession_percentage: 0,
        requires_certificate: true, certificate_issuing_authority: '', is_active: true, display_order: 0
    });

    const fetchData = async () => {
        try {
            const result = await getReservationCategories();
            setData(result);
        } catch (e) {
            toast.error('Failed to load categories');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { fetchData(); }, []);

    const handleSubmit = async () => {
        try {
            if (editItem) {
                await updateReservationCategory(editItem.id, formData);
                toast.success('Category updated');
            } else {
                await createReservationCategory(formData);
                toast.success('Category created');
            }
            setDialogOpen(false);
            fetchData();
        } catch (e) {
            toast.error('Operation failed');
        }
    };

    const handleDelete = async (item: ReservationCategory) => {
        if (confirm('Delete this category?')) {
            try {
                await deleteReservationCategory(item.id);
                toast.success('Category deleted');
                fetchData();
            } catch (e) {
                toast.error('Failed to delete');
            }
        }
    };

    return (
        <>
            <DataTable
                title="Reservation Categories"
                icon={<Award className="h-5 w-5 text-orange-600" />}
                data={data}
                loading={loading}
                columns={[
                    { key: 'name', label: 'Name' },
                    { key: 'code', label: 'Code' },
                    { key: 'reservation_percentage', label: 'Reservation %', render: (item) => `${item.reservation_percentage}%` },
                    { key: 'fee_concession_percentage', label: 'Fee Concession %', render: (item) => `${item.fee_concession_percentage}%` },
                    { key: 'is_active', label: 'Status', render: (item) => <Badge variant={item.is_active ? 'default' : 'secondary'}>{item.is_active ? 'Active' : 'Inactive'}</Badge> },
                ]}
                onAdd={() => {
                    setEditItem(null);
                    setFormData({ name: '', code: '', full_name: '', reservation_percentage: 0, fee_concession_percentage: 0, requires_certificate: true, certificate_issuing_authority: '', is_active: true, display_order: 0 });
                    setDialogOpen(true);
                }}
                onEdit={(item) => {
                    setEditItem(item);
                    setFormData(item as any);
                    setDialogOpen(true);
                }}
                onDelete={handleDelete}
            />

            <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>{editItem ? 'Edit Category' : 'Add Category'}</DialogTitle>
                    </DialogHeader>
                    <div className="space-y-4">
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <Label>Name</Label>
                                <Input value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} placeholder="e.g., SC" />
                            </div>
                            <div>
                                <Label>Code</Label>
                                <Input value={formData.code} onChange={(e) => setFormData({ ...formData, code: e.target.value.toUpperCase() })} />
                            </div>
                        </div>
                        <div>
                            <Label>Full Name</Label>
                            <Input value={formData.full_name} onChange={(e) => setFormData({ ...formData, full_name: e.target.value })} placeholder="e.g., Scheduled Caste" />
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <Label>Reservation %</Label>
                                <Input type="number" value={formData.reservation_percentage} onChange={(e) => setFormData({ ...formData, reservation_percentage: parseFloat(e.target.value) })} />
                            </div>
                            <div>
                                <Label>Fee Concession %</Label>
                                <Input type="number" value={formData.fee_concession_percentage} onChange={(e) => setFormData({ ...formData, fee_concession_percentage: parseFloat(e.target.value) })} />
                            </div>
                        </div>
                        <div>
                            <Label>Certificate Issuing Authority</Label>
                            <Input value={formData.certificate_issuing_authority} onChange={(e) => setFormData({ ...formData, certificate_issuing_authority: e.target.value })} />
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="flex items-center gap-2">
                                <Switch checked={formData.requires_certificate} onCheckedChange={(v) => setFormData({ ...formData, requires_certificate: v })} />
                                <Label>Requires Certificate</Label>
                            </div>
                            <div className="flex items-center gap-2">
                                <Switch checked={formData.is_active} onCheckedChange={(v) => setFormData({ ...formData, is_active: v })} />
                                <Label>Active</Label>
                            </div>
                        </div>
                        <div className="flex justify-end gap-2">
                            <Button variant="outline" onClick={() => setDialogOpen(false)}>Cancel</Button>
                            <Button onClick={handleSubmit} className="bg-blue-600 hover:bg-blue-700">Save</Button>
                        </div>
                    </div>
                </DialogContent>
            </Dialog>
        </>
    );
}

// ============================================================================
// Lead Source Tab
// ============================================================================

export function LeadSourceTab() {
    const [data, setData] = useState<LeadSource[]>([]);
    const [loading, setLoading] = useState(true);
    const [dialogOpen, setDialogOpen] = useState(false);
    const [editItem, setEditItem] = useState<LeadSource | null>(null);
    const [formData, setFormData] = useState<{
        name: string;
        code: string;
        description: string;
        category: 'DIGITAL' | 'OFFLINE' | 'REFERRAL' | 'OTHER';
        is_active: boolean;
        display_order: number;
    }>({
        name: '', code: '', description: '', category: 'DIGITAL', is_active: true, display_order: 0
    });

    const fetchData = async () => {
        try {
            const result = await getLeadSources();
            setData(result);
        } catch (e) {
            toast.error('Failed to load lead sources');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { fetchData(); }, []);

    const handleSubmit = async () => {
        try {
            if (editItem) {
                await updateLeadSource(editItem.id, formData);
                toast.success('Lead source updated');
            } else {
                await createLeadSource(formData);
                toast.success('Lead source created');
            }
            setDialogOpen(false);
            fetchData();
        } catch (e) {
            toast.error('Operation failed');
        }
    };

    const handleDelete = async (item: LeadSource) => {
        if (confirm('Delete this lead source?')) {
            try {
                await deleteLeadSource(item.id);
                toast.success('Lead source deleted');
                fetchData();
            } catch (e) {
                toast.error('Failed to delete');
            }
        }
    };

    return (
        <>
            <DataTable
                title="Lead Sources"
                icon={<Users className="h-5 w-5 text-cyan-600" />}
                data={data}
                loading={loading}
                columns={[
                    { key: 'name', label: 'Name' },
                    { key: 'code', label: 'Code' },
                    { key: 'category', label: 'Category', render: (item) => <Badge variant="outline">{item.category}</Badge> },
                    { key: 'is_active', label: 'Status', render: (item) => <Badge variant={item.is_active ? 'default' : 'secondary'}>{item.is_active ? 'Active' : 'Inactive'}</Badge> },
                ]}
                onAdd={() => {
                    setEditItem(null);
                    setFormData({ name: '', code: '', description: '', category: 'DIGITAL', is_active: true, display_order: 0 });
                    setDialogOpen(true);
                }}
                onEdit={(item) => {
                    setEditItem(item);
                    setFormData(item as any);
                    setDialogOpen(true);
                }}
                onDelete={handleDelete}
            />

            <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>{editItem ? 'Edit Lead Source' : 'Add Lead Source'}</DialogTitle>
                    </DialogHeader>
                    <div className="space-y-4">
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <Label>Name</Label>
                                <Input value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} placeholder="e.g., Website" />
                            </div>
                            <div>
                                <Label>Code</Label>
                                <Input value={formData.code} onChange={(e) => setFormData({ ...formData, code: e.target.value.toUpperCase() })} />
                            </div>
                        </div>
                        <div>
                            <Label>Description</Label>
                            <Textarea value={formData.description} onChange={(e) => setFormData({ ...formData, description: e.target.value })} />
                        </div>
                        <div>
                            <Label>Category</Label>
                            <Select value={formData.category} onValueChange={(v: 'DIGITAL' | 'OFFLINE' | 'REFERRAL' | 'OTHER') => setFormData({ ...formData, category: v })}>
                                <SelectTrigger><SelectValue /></SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="DIGITAL">Digital</SelectItem>
                                    <SelectItem value="OFFLINE">Offline</SelectItem>
                                    <SelectItem value="REFERRAL">Referral</SelectItem>
                                    <SelectItem value="OTHER">Other</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                        <div className="flex items-center gap-2">
                            <Switch checked={formData.is_active} onCheckedChange={(v) => setFormData({ ...formData, is_active: v })} />
                            <Label>Active</Label>
                        </div>
                        <div className="flex justify-end gap-2">
                            <Button variant="outline" onClick={() => setDialogOpen(false)}>Cancel</Button>
                            <Button onClick={handleSubmit} className="bg-blue-600 hover:bg-blue-700">Save</Button>
                        </div>
                    </div>
                </DialogContent>
            </Dialog>
        </>
    );
}

// ============================================================================
// Designation Tab
// ============================================================================

export function DesignationTab() {
    const [data, setData] = useState<Designation[]>([]);
    const [loading, setLoading] = useState(true);
    const [dialogOpen, setDialogOpen] = useState(false);
    const [editItem, setEditItem] = useState<Designation | null>(null);
    const [formData, setFormData] = useState({
        name: '', code: '', level: 1, min_experience_years: 0, min_qualification: '', is_teaching: true, is_active: true, display_order: 0
    });

    const fetchData = async () => {
        try {
            const result = await getDesignations();
            setData(result);
        } catch (e) {
            toast.error('Failed to load designations');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { fetchData(); }, []);

    const handleSubmit = async () => {
        try {
            if (editItem) {
                await updateDesignation(editItem.id, formData);
                toast.success('Designation updated');
            } else {
                await createDesignation(formData);
                toast.success('Designation created');
            }
            setDialogOpen(false);
            fetchData();
        } catch (e) {
            toast.error('Operation failed');
        }
    };

    const handleDelete = async (item: Designation) => {
        if (confirm('Delete this designation?')) {
            try {
                await deleteDesignation(item.id);
                toast.success('Designation deleted');
                fetchData();
            } catch (e) {
                toast.error('Failed to delete');
            }
        }
    };

    return (
        <>
            <DataTable
                title="Designations"
                icon={<Briefcase className="h-5 w-5 text-indigo-600" />}
                data={data}
                loading={loading}
                columns={[
                    { key: 'name', label: 'Name' },
                    { key: 'code', label: 'Code' },
                    { key: 'level', label: 'Level' },
                    { key: 'is_teaching', label: 'Teaching', render: (item) => item.is_teaching ? 'Yes' : 'No' },
                    { key: 'is_active', label: 'Status', render: (item) => <Badge variant={item.is_active ? 'default' : 'secondary'}>{item.is_active ? 'Active' : 'Inactive'}</Badge> },
                ]}
                onAdd={() => {
                    setEditItem(null);
                    setFormData({ name: '', code: '', level: 1, min_experience_years: 0, min_qualification: '', is_teaching: true, is_active: true, display_order: 0 });
                    setDialogOpen(true);
                }}
                onEdit={(item) => {
                    setEditItem(item);
                    setFormData(item as any);
                    setDialogOpen(true);
                }}
                onDelete={handleDelete}
            />

            <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>{editItem ? 'Edit Designation' : 'Add Designation'}</DialogTitle>
                    </DialogHeader>
                    <div className="space-y-4">
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <Label>Name</Label>
                                <Input value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} placeholder="e.g., Professor" />
                            </div>
                            <div>
                                <Label>Code</Label>
                                <Input value={formData.code} onChange={(e) => setFormData({ ...formData, code: e.target.value.toUpperCase() })} />
                            </div>
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <Label>Level (Hierarchy)</Label>
                                <Input type="number" value={formData.level} onChange={(e) => setFormData({ ...formData, level: parseInt(e.target.value) })} />
                            </div>
                            <div>
                                <Label>Min Experience (Years)</Label>
                                <Input type="number" value={formData.min_experience_years} onChange={(e) => setFormData({ ...formData, min_experience_years: parseInt(e.target.value) })} />
                            </div>
                        </div>
                        <div>
                            <Label>Min Qualification</Label>
                            <Input value={formData.min_qualification} onChange={(e) => setFormData({ ...formData, min_qualification: e.target.value })} placeholder="e.g., Ph.D" />
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="flex items-center gap-2">
                                <Switch checked={formData.is_teaching} onCheckedChange={(v) => setFormData({ ...formData, is_teaching: v })} />
                                <Label>Teaching Position</Label>
                            </div>
                            <div className="flex items-center gap-2">
                                <Switch checked={formData.is_active} onCheckedChange={(v) => setFormData({ ...formData, is_active: v })} />
                                <Label>Active</Label>
                            </div>
                        </div>
                        <div className="flex justify-end gap-2">
                            <Button variant="outline" onClick={() => setDialogOpen(false)}>Cancel</Button>
                            <Button onClick={handleSubmit} className="bg-blue-600 hover:bg-blue-700">Save</Button>
                        </div>
                    </div>
                </DialogContent>
            </Dialog>
        </>
    );
}

// ============================================================================
// Placement Company Tab
// ============================================================================

export function PlacementCompanyTab() {
    const [data, setData] = useState<PlacementCompany[]>([]);
    const [loading, setLoading] = useState(true);
    const [dialogOpen, setDialogOpen] = useState(false);
    const [editItem, setEditItem] = useState<PlacementCompany | null>(null);
    const [formData, setFormData] = useState<{
        name: string;
        code: string;
        company_type: 'HOTEL' | 'RESTAURANT' | 'CRUISE' | 'OTHER';
        contact_person: string;
        contact_email: string;
        contact_phone: string;
        address: string;
        city: string;
        state: string;
        country: string;
        website: string;
        is_partner: boolean;
        is_active: boolean;
    }>({
        name: '', code: '', company_type: 'HOTEL', contact_person: '', contact_email: '', contact_phone: '',
        address: '', city: '', state: '', country: 'India', website: '', is_partner: false, is_active: true
    });

    const fetchData = async () => {
        try {
            const result = await getPlacementCompanies();
            setData(result);
        } catch (e) {
            toast.error('Failed to load companies');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { fetchData(); }, []);

    const handleSubmit = async () => {
        try {
            if (editItem) {
                await updatePlacementCompany(editItem.id, formData);
                toast.success('Company updated');
            } else {
                await createPlacementCompany(formData);
                toast.success('Company created');
            }
            setDialogOpen(false);
            fetchData();
        } catch (e) {
            toast.error('Operation failed');
        }
    };

    const handleDelete = async (item: PlacementCompany) => {
        if (confirm('Delete this company?')) {
            try {
                await deletePlacementCompany(item.id);
                toast.success('Company deleted');
                fetchData();
            } catch (e) {
                toast.error('Failed to delete');
            }
        }
    };

    return (
        <>
            <DataTable
                title="Placement Companies / Hotels"
                icon={<Building className="h-5 w-5 text-teal-600" />}
                data={data}
                loading={loading}
                columns={[
                    { key: 'name', label: 'Name' },
                    { key: 'company_type', label: 'Type', render: (item) => <Badge variant="outline">{item.company_type}</Badge> },
                    { key: 'city', label: 'City' },
                    { key: 'is_partner', label: 'Partner', render: (item) => item.is_partner ? <Badge className="bg-green-100 text-green-800">Partner</Badge> : '-' },
                    { key: 'students_placed', label: 'Students Placed' },
                    { key: 'is_active', label: 'Status', render: (item) => <Badge variant={item.is_active ? 'default' : 'secondary'}>{item.is_active ? 'Active' : 'Inactive'}</Badge> },
                ]}
                onAdd={() => {
                    setEditItem(null);
                    setFormData({
                        name: '', code: '', company_type: 'HOTEL', contact_person: '', contact_email: '', contact_phone: '',
                        address: '', city: '', state: '', country: 'India', website: '', is_partner: false, is_active: true
                    });
                    setDialogOpen(true);
                }}
                onEdit={(item) => {
                    setEditItem(item);
                    setFormData(item as any);
                    setDialogOpen(true);
                }}
                onDelete={handleDelete}
            />

            <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
                <DialogContent className="max-w-2xl">
                    <DialogHeader>
                        <DialogTitle>{editItem ? 'Edit Company' : 'Add Company'}</DialogTitle>
                    </DialogHeader>
                    <div className="space-y-4 max-h-[70vh] overflow-y-auto">
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <Label>Company Name</Label>
                                <Input value={formData.name} onChange={(e) => setFormData({ ...formData, name: e.target.value })} placeholder="e.g., Taj Hotels" />
                            </div>
                            <div>
                                <Label>Code</Label>
                                <Input value={formData.code} onChange={(e) => setFormData({ ...formData, code: e.target.value.toUpperCase() })} />
                            </div>
                        </div>
                        <div>
                            <Label>Company Type</Label>
                            <Select value={formData.company_type} onValueChange={(v: 'HOTEL' | 'RESTAURANT' | 'CRUISE' | 'OTHER') => setFormData({ ...formData, company_type: v })}>
                                <SelectTrigger><SelectValue /></SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="HOTEL">Hotel</SelectItem>
                                    <SelectItem value="RESTAURANT">Restaurant</SelectItem>
                                    <SelectItem value="CRUISE">Cruise Line</SelectItem>
                                    <SelectItem value="OTHER">Other</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                        <div className="grid grid-cols-3 gap-4">
                            <div>
                                <Label>Contact Person</Label>
                                <Input value={formData.contact_person} onChange={(e) => setFormData({ ...formData, contact_person: e.target.value })} />
                            </div>
                            <div>
                                <Label>Email</Label>
                                <Input type="email" value={formData.contact_email} onChange={(e) => setFormData({ ...formData, contact_email: e.target.value })} />
                            </div>
                            <div>
                                <Label>Phone</Label>
                                <Input value={formData.contact_phone} onChange={(e) => setFormData({ ...formData, contact_phone: e.target.value })} />
                            </div>
                        </div>
                        <div>
                            <Label>Address</Label>
                            <Textarea value={formData.address} onChange={(e) => setFormData({ ...formData, address: e.target.value })} />
                        </div>
                        <div className="grid grid-cols-3 gap-4">
                            <div>
                                <Label>City</Label>
                                <Input value={formData.city} onChange={(e) => setFormData({ ...formData, city: e.target.value })} />
                            </div>
                            <div>
                                <Label>State</Label>
                                <Input value={formData.state} onChange={(e) => setFormData({ ...formData, state: e.target.value })} />
                            </div>
                            <div>
                                <Label>Country</Label>
                                <Input value={formData.country} onChange={(e) => setFormData({ ...formData, country: e.target.value })} />
                            </div>
                        </div>
                        <div>
                            <Label>Website</Label>
                            <Input value={formData.website} onChange={(e) => setFormData({ ...formData, website: e.target.value })} placeholder="https://" />
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="flex items-center gap-2">
                                <Switch checked={formData.is_partner} onCheckedChange={(v) => setFormData({ ...formData, is_partner: v })} />
                                <Label>Partnership Company</Label>
                            </div>
                            <div className="flex items-center gap-2">
                                <Switch checked={formData.is_active} onCheckedChange={(v) => setFormData({ ...formData, is_active: v })} />
                                <Label>Active</Label>
                            </div>
                        </div>
                        <div className="flex justify-end gap-2">
                            <Button variant="outline" onClick={() => setDialogOpen(false)}>Cancel</Button>
                            <Button onClick={handleSubmit} className="bg-blue-600 hover:bg-blue-700">Save</Button>
                        </div>
                    </div>
                </DialogContent>
            </Dialog>
        </>
    );
}

// ============================================================================
// Export All Tabs
// ============================================================================

export {
    DataTable
};
