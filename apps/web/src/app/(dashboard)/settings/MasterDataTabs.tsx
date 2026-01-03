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
