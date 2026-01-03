'use client';

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { toast } from 'sonner';
import {
    Plus, Edit2, Trash2, ChevronDown, ChevronRight, Users, Layers, BookOpen,
    Calendar, GraduationCap, Settings2, Wand2, FolderTree
} from 'lucide-react';
import {
    AcademicStructure, YearInfo, SemesterInfo, SectionInfo, PracticalBatchInfo,
    getAcademicStructure, generateAcademicStructure,
    ProgramFull, getPrograms,
    createProgramYear, updateProgramYear, deleteProgramYear,
    createSemester, updateSemester, deleteSemester,
    createSection, updateSection, deleteSection,
    createPracticalBatch, updatePracticalBatch, deletePracticalBatch
} from '@/utils/master-data-service';

// ============================================================================
// Academic Structure Tab Component
// ============================================================================

export function AcademicStructureTab() {
    const [structure, setStructure] = useState<AcademicStructure[]>([]);
    const [programs, setPrograms] = useState<ProgramFull[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedProgram, setSelectedProgram] = useState<number | null>(null);
    
    // Expanded states
    const [expandedPrograms, setExpandedPrograms] = useState<Set<number>>(new Set());
    const [expandedYears, setExpandedYears] = useState<Set<number>>(new Set());
    const [expandedSemesters, setExpandedSemesters] = useState<Set<number>>(new Set());
    const [expandedSections, setExpandedSections] = useState<Set<number>>(new Set());
    
    // Dialogs
    const [generateDialogOpen, setGenerateDialogOpen] = useState(false);
    const [editDialogOpen, setEditDialogOpen] = useState(false);
    const [editType, setEditType] = useState<'year' | 'semester' | 'section' | 'batch' | null>(null);
    const [editItem, setEditItem] = useState<any>(null);
    const [parentId, setParentId] = useState<number | null>(null);
    
    // Generate form
    const [generateForm, setGenerateForm] = useState({
        program_id: 0,
        sections_per_semester: 2,
        students_per_section: 60,
        batches_per_section: 2,
        students_per_batch: 30
    });
    
    // Edit form
    const [editForm, setEditForm] = useState({
        name: '',
        code: '',
        max_strength: 60,
        is_active: true,
        is_internship: false,
        is_project_semester: false
    });

    const fetchData = async () => {
        try {
            const [structureResult, programsResult] = await Promise.all([
                getAcademicStructure(selectedProgram || undefined),
                getPrograms(true)
            ]);
            setStructure(structureResult);
            setPrograms(programsResult);
        } catch (e) {
            toast.error('Failed to load academic structure');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => { fetchData(); }, [selectedProgram]);

    const toggleExpand = (type: 'program' | 'year' | 'semester' | 'section', id: number) => {
        const setters = {
            program: setExpandedPrograms,
            year: setExpandedYears,
            semester: setExpandedSemesters,
            section: setExpandedSections
        };
        setters[type](prev => {
            const newSet = new Set(prev);
            if (newSet.has(id)) {
                newSet.delete(id);
            } else {
                newSet.add(id);
            }
            return newSet;
        });
    };

    const handleGenerate = async () => {
        if (!generateForm.program_id) {
            toast.error('Please select a program');
            return;
        }
        try {
            const result = await generateAcademicStructure(generateForm);
            toast.success(result.message);
            setGenerateDialogOpen(false);
            fetchData();
        } catch (e: any) {
            toast.error(e?.response?.data?.detail || 'Generation failed');
        }
    };

    const openAddDialog = (type: 'year' | 'semester' | 'section' | 'batch', parentId: number) => {
        setEditType(type);
        setEditItem(null);
        setParentId(parentId);
        setEditForm({
            name: '',
            code: '',
            max_strength: type === 'section' ? 60 : type === 'batch' ? 30 : 0,
            is_active: true,
            is_internship: false,
            is_project_semester: false
        });
        setEditDialogOpen(true);
    };

    const openEditDialog = (type: 'year' | 'semester' | 'section' | 'batch', item: any) => {
        setEditType(type);
        setEditItem(item);
        setParentId(null);
        setEditForm({
            name: item.name,
            code: item.code || '',
            max_strength: item.max_strength || 60,
            is_active: item.is_active !== false,
            is_internship: item.is_internship || false,
            is_project_semester: item.is_project_semester || false
        });
        setEditDialogOpen(true);
    };

    const handleSaveEdit = async () => {
        try {
            if (editItem) {
                // Update
                switch (editType) {
                    case 'year':
                        await updateProgramYear(editItem.id, { name: editForm.name, is_active: editForm.is_active });
                        break;
                    case 'semester':
                        await updateSemester(editItem.id, { 
                            name: editForm.name, 
                            is_internship: editForm.is_internship,
                            is_project_semester: editForm.is_project_semester 
                        });
                        break;
                    case 'section':
                        await updateSection(editItem.id, { name: editForm.name, max_strength: editForm.max_strength, is_active: editForm.is_active });
                        break;
                    case 'batch':
                        await updatePracticalBatch(editItem.id, { name: editForm.name, max_strength: editForm.max_strength, is_active: editForm.is_active });
                        break;
                }
                toast.success('Updated successfully');
            } else {
                // Create
                switch (editType) {
                    case 'year':
                        // Find next year number
                        const program = structure.find(p => p.years.some(y => y.id === parentId) || p.id === parentId);
                        const maxYear = program ? Math.max(...program.years.map(y => y.year_number), 0) : 0;
                        await createProgramYear({ program_id: parentId!, year_number: maxYear + 1, name: editForm.name });
                        break;
                    case 'semester':
                        await createSemester({ program_year_id: parentId!, semester_number: 1, name: editForm.name });
                        break;
                    case 'section':
                        await createSection({ semester_id: parentId!, name: editForm.name, code: editForm.code, max_strength: editForm.max_strength });
                        break;
                    case 'batch':
                        await createPracticalBatch({ section_id: parentId!, name: editForm.name, code: editForm.code, max_strength: editForm.max_strength });
                        break;
                }
                toast.success('Created successfully');
            }
            setEditDialogOpen(false);
            fetchData();
        } catch (e: any) {
            toast.error(e?.response?.data?.detail || 'Operation failed');
        }
    };

    const handleDelete = async (type: 'year' | 'semester' | 'section' | 'batch', id: number, name: string) => {
        if (!confirm(`Delete "${name}" and all its children? This cannot be undone.`)) return;
        
        try {
            switch (type) {
                case 'year': await deleteProgramYear(id); break;
                case 'semester': await deleteSemester(id); break;
                case 'section': await deleteSection(id); break;
                case 'batch': await deletePracticalBatch(id); break;
            }
            toast.success('Deleted successfully');
            fetchData();
        } catch (e: any) {
            toast.error(e?.response?.data?.detail || 'Delete failed');
        }
    };

    return (
        <>
            <Card>
                <CardHeader className="flex flex-row items-center justify-between">
                    <CardTitle className="text-lg flex items-center gap-2">
                        <FolderTree className="h-5 w-5 text-indigo-600" />
                        Academic Structure
                    </CardTitle>
                    <div className="flex items-center gap-2">
                        <Select
                            value={selectedProgram?.toString() || "all"}
                            onValueChange={(v) => setSelectedProgram(v === "all" ? null : parseInt(v))}
                        >
                            <SelectTrigger className="w-48">
                                <SelectValue placeholder="All Programs" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="all">All Programs</SelectItem>
                                {programs.map(p => (
                                    <SelectItem key={p.id} value={p.id.toString()}>{p.code} - {p.name}</SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                        <Button onClick={() => setGenerateDialogOpen(true)} size="sm" variant="outline" className="gap-1">
                            <Wand2 className="h-4 w-4" /> Auto Generate
                        </Button>
                    </div>
                </CardHeader>
                <CardContent>
                    {loading ? (
                        <div className="flex justify-center py-8">
                            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
                        </div>
                    ) : structure.length === 0 ? (
                        <div className="text-center py-8 text-slate-500">
                            <FolderTree className="h-12 w-12 mx-auto mb-3 text-slate-300" />
                            <p>No academic structure found.</p>
                            <p className="text-sm mt-1">Click "Auto Generate" to create structure for a program.</p>
                        </div>
                    ) : (
                        <div className="space-y-2">
                            {/* Legend */}
                            <div className="flex gap-4 text-xs text-slate-500 mb-4 p-2 bg-slate-50 rounded">
                                <span className="flex items-center gap-1"><BookOpen className="h-3 w-3 text-purple-500" /> Course</span>
                                <span className="flex items-center gap-1"><Calendar className="h-3 w-3 text-blue-500" /> Year</span>
                                <span className="flex items-center gap-1"><Layers className="h-3 w-3 text-green-500" /> Semester</span>
                                <span className="flex items-center gap-1"><Users className="h-3 w-3 text-orange-500" /> Section (60 students)</span>
                                <span className="flex items-center gap-1"><GraduationCap className="h-3 w-3 text-red-500" /> Batch (30 students)</span>
                            </div>
                            
                            {/* Tree View */}
                            {structure.map((program) => (
                                <div key={program.id} className="border rounded-lg overflow-hidden">
                                    {/* Program Level */}
                                    <div 
                                        className="flex items-center justify-between p-3 bg-purple-50 cursor-pointer hover:bg-purple-100"
                                        onClick={() => toggleExpand('program', program.id)}
                                    >
                                        <div className="flex items-center gap-2">
                                            {expandedPrograms.has(program.id) ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
                                            <BookOpen className="h-4 w-4 text-purple-600" />
                                            <span className="font-medium">{program.code}</span>
                                            <span className="text-slate-600">- {program.name}</span>
                                            <Badge variant="outline" className="text-xs">{program.duration_years} Years</Badge>
                                            <Badge variant="secondary" className="text-xs">{program.semester_system ? 'Semester' : 'Year'} System</Badge>
                                        </div>
                                        <Button size="sm" variant="ghost" onClick={(e) => { e.stopPropagation(); openAddDialog('year', program.id); }}>
                                            <Plus className="h-4 w-4" />
                                        </Button>
                                    </div>
                                    
                                    {/* Years */}
                                    {expandedPrograms.has(program.id) && (
                                        <div className="pl-6 border-l-2 border-purple-200 ml-4">
                                            {program.years.length === 0 ? (
                                                <div className="p-3 text-sm text-slate-500 italic">No years configured. Click + to add or use Auto Generate.</div>
                                            ) : (
                                                program.years.map((year) => (
                                                    <div key={year.id} className="border-b last:border-b-0">
                                                        {/* Year Level */}
                                                        <div 
                                                            className="flex items-center justify-between p-2 bg-blue-50 cursor-pointer hover:bg-blue-100"
                                                            onClick={() => toggleExpand('year', year.id)}
                                                        >
                                                            <div className="flex items-center gap-2">
                                                                {expandedYears.has(year.id) ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
                                                                <Calendar className="h-4 w-4 text-blue-600" />
                                                                <span className="font-medium">{year.name}</span>
                                                                {!year.is_active && <Badge variant="secondary" className="text-xs">Inactive</Badge>}
                                                            </div>
                                                            <div className="flex gap-1">
                                                                <Button size="sm" variant="ghost" onClick={(e) => { e.stopPropagation(); openAddDialog('semester', year.id); }}>
                                                                    <Plus className="h-3 w-3" />
                                                                </Button>
                                                                <Button size="sm" variant="ghost" onClick={(e) => { e.stopPropagation(); openEditDialog('year', year); }}>
                                                                    <Edit2 className="h-3 w-3" />
                                                                </Button>
                                                                <Button size="sm" variant="ghost" onClick={(e) => { e.stopPropagation(); handleDelete('year', year.id, year.name); }}>
                                                                    <Trash2 className="h-3 w-3 text-red-500" />
                                                                </Button>
                                                            </div>
                                                        </div>
                                                        
                                                        {/* Semesters */}
                                                        {expandedYears.has(year.id) && (
                                                            <div className="pl-6 border-l-2 border-blue-200 ml-4">
                                                                {year.semesters.length === 0 ? (
                                                                    <div className="p-2 text-sm text-slate-500 italic">No semesters</div>
                                                                ) : (
                                                                    year.semesters.map((sem) => (
                                                                        <div key={sem.id} className="border-b last:border-b-0">
                                                                            {/* Semester Level */}
                                                                            <div 
                                                                                className="flex items-center justify-between p-2 bg-green-50 cursor-pointer hover:bg-green-100"
                                                                                onClick={() => toggleExpand('semester', sem.id)}
                                                                            >
                                                                                <div className="flex items-center gap-2">
                                                                                    {expandedSemesters.has(sem.id) ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
                                                                                    <Layers className="h-4 w-4 text-green-600" />
                                                                                    <span className="font-medium">{sem.name}</span>
                                                                                    {sem.is_internship && <Badge className="text-xs bg-yellow-100 text-yellow-800">Internship</Badge>}
                                                                                    {sem.is_project_semester && <Badge className="text-xs bg-cyan-100 text-cyan-800">Project</Badge>}
                                                                                </div>
                                                                                <div className="flex gap-1">
                                                                                    <Button size="sm" variant="ghost" onClick={(e) => { e.stopPropagation(); openAddDialog('section', sem.id); }}>
                                                                                        <Plus className="h-3 w-3" />
                                                                                    </Button>
                                                                                    <Button size="sm" variant="ghost" onClick={(e) => { e.stopPropagation(); openEditDialog('semester', sem); }}>
                                                                                        <Edit2 className="h-3 w-3" />
                                                                                    </Button>
                                                                                    <Button size="sm" variant="ghost" onClick={(e) => { e.stopPropagation(); handleDelete('semester', sem.id, sem.name); }}>
                                                                                        <Trash2 className="h-3 w-3 text-red-500" />
                                                                                    </Button>
                                                                                </div>
                                                                            </div>
                                                                            
                                                                            {/* Sections */}
                                                                            {expandedSemesters.has(sem.id) && (
                                                                                <div className="pl-6 border-l-2 border-green-200 ml-4">
                                                                                    {sem.sections.length === 0 ? (
                                                                                        <div className="p-2 text-sm text-slate-500 italic">No sections</div>
                                                                                    ) : (
                                                                                        sem.sections.map((section) => (
                                                                                            <div key={section.id} className="border-b last:border-b-0">
                                                                                                {/* Section Level */}
                                                                                                <div 
                                                                                                    className="flex items-center justify-between p-2 bg-orange-50 cursor-pointer hover:bg-orange-100"
                                                                                                    onClick={() => toggleExpand('section', section.id)}
                                                                                                >
                                                                                                    <div className="flex items-center gap-2">
                                                                                                        {expandedSections.has(section.id) ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
                                                                                                        <Users className="h-4 w-4 text-orange-600" />
                                                                                                        <span className="font-medium">{section.name}</span>
                                                                                                        <span className="text-xs text-slate-500">
                                                                                                            ({section.current_strength}/{section.max_strength} students)
                                                                                                        </span>
                                                                                                        {!section.is_active && <Badge variant="secondary" className="text-xs">Inactive</Badge>}
                                                                                                    </div>
                                                                                                    <div className="flex gap-1">
                                                                                                        <Button size="sm" variant="ghost" onClick={(e) => { e.stopPropagation(); openAddDialog('batch', section.id); }}>
                                                                                                            <Plus className="h-3 w-3" />
                                                                                                        </Button>
                                                                                                        <Button size="sm" variant="ghost" onClick={(e) => { e.stopPropagation(); openEditDialog('section', section); }}>
                                                                                                            <Edit2 className="h-3 w-3" />
                                                                                                        </Button>
                                                                                                        <Button size="sm" variant="ghost" onClick={(e) => { e.stopPropagation(); handleDelete('section', section.id, section.name); }}>
                                                                                                            <Trash2 className="h-3 w-3 text-red-500" />
                                                                                                        </Button>
                                                                                                    </div>
                                                                                                </div>
                                                                                                
                                                                                                {/* Practical Batches */}
                                                                                                {expandedSections.has(section.id) && (
                                                                                                    <div className="pl-6 border-l-2 border-orange-200 ml-4">
                                                                                                        {section.batches.length === 0 ? (
                                                                                                            <div className="p-2 text-sm text-slate-500 italic">No batches</div>
                                                                                                        ) : (
                                                                                                            section.batches.map((batch) => (
                                                                                                                <div 
                                                                                                                    key={batch.id} 
                                                                                                                    className="flex items-center justify-between p-2 bg-red-50 hover:bg-red-100"
                                                                                                                >
                                                                                                                    <div className="flex items-center gap-2">
                                                                                                                        <GraduationCap className="h-4 w-4 text-red-600" />
                                                                                                                        <span className="font-medium">{batch.name}</span>
                                                                                                                        <span className="text-xs text-slate-500">
                                                                                                                            ({batch.current_strength}/{batch.max_strength} students)
                                                                                                                        </span>
                                                                                                                        {!batch.is_active && <Badge variant="secondary" className="text-xs">Inactive</Badge>}
                                                                                                                    </div>
                                                                                                                    <div className="flex gap-1">
                                                                                                                        <Button size="sm" variant="ghost" onClick={() => openEditDialog('batch', batch)}>
                                                                                                                            <Edit2 className="h-3 w-3" />
                                                                                                                        </Button>
                                                                                                                        <Button size="sm" variant="ghost" onClick={() => handleDelete('batch', batch.id, batch.name)}>
                                                                                                                            <Trash2 className="h-3 w-3 text-red-500" />
                                                                                                                        </Button>
                                                                                                                    </div>
                                                                                                                </div>
                                                                                                            ))
                                                                                                        )}
                                                                                                    </div>
                                                                                                )}
                                                                                            </div>
                                                                                        ))
                                                                                    )}
                                                                                </div>
                                                                            )}
                                                                        </div>
                                                                    ))
                                                                )}
                                                            </div>
                                                        )}
                                                    </div>
                                                ))
                                            )}
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    )}
                </CardContent>
            </Card>

            {/* Generate Dialog */}
            <Dialog open={generateDialogOpen} onOpenChange={setGenerateDialogOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle className="flex items-center gap-2">
                            <Wand2 className="h-5 w-5" /> Auto Generate Academic Structure
                        </DialogTitle>
                    </DialogHeader>
                    <div className="space-y-4">
                        <div>
                            <Label>Select Program *</Label>
                            <Select 
                                value={generateForm.program_id?.toString() || ""} 
                                onValueChange={(v) => setGenerateForm({ ...generateForm, program_id: parseInt(v) })}
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
                        </div>
                        
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <Label>Sections per Semester</Label>
                                <Input 
                                    type="number" 
                                    value={generateForm.sections_per_semester} 
                                    onChange={(e) => setGenerateForm({ ...generateForm, sections_per_semester: parseInt(e.target.value) || 2 })}
                                    min={1}
                                />
                            </div>
                            <div>
                                <Label>Students per Section</Label>
                                <Input 
                                    type="number" 
                                    value={generateForm.students_per_section} 
                                    onChange={(e) => setGenerateForm({ ...generateForm, students_per_section: parseInt(e.target.value) || 60 })}
                                    min={1}
                                />
                            </div>
                            <div>
                                <Label>Batches per Section</Label>
                                <Input 
                                    type="number" 
                                    value={generateForm.batches_per_section} 
                                    onChange={(e) => setGenerateForm({ ...generateForm, batches_per_section: parseInt(e.target.value) || 2 })}
                                    min={1}
                                />
                            </div>
                            <div>
                                <Label>Students per Batch</Label>
                                <Input 
                                    type="number" 
                                    value={generateForm.students_per_batch} 
                                    onChange={(e) => setGenerateForm({ ...generateForm, students_per_batch: parseInt(e.target.value) || 30 })}
                                    min={1}
                                />
                            </div>
                        </div>
                        
                        <div className="bg-blue-50 p-3 rounded text-sm text-blue-800">
                            <strong>Preview:</strong> This will generate:
                            <ul className="mt-1 space-y-1 ml-4 list-disc">
                                <li>{programs.find(p => p.id === generateForm.program_id)?.duration_years || 0} Years</li>
                                <li>{(programs.find(p => p.id === generateForm.program_id)?.duration_years || 0) * 2} Semesters (2 per year)</li>
                                <li>{(programs.find(p => p.id === generateForm.program_id)?.duration_years || 0) * 2 * generateForm.sections_per_semester} Sections</li>
                                <li>{(programs.find(p => p.id === generateForm.program_id)?.duration_years || 0) * 2 * generateForm.sections_per_semester * generateForm.batches_per_section} Practical Batches</li>
                            </ul>
                        </div>
                        
                        <div className="flex justify-end gap-2">
                            <Button variant="outline" onClick={() => setGenerateDialogOpen(false)}>Cancel</Button>
                            <Button onClick={handleGenerate} className="bg-blue-600 hover:bg-blue-700">
                                <Wand2 className="h-4 w-4 mr-1" /> Generate
                            </Button>
                        </div>
                    </div>
                </DialogContent>
            </Dialog>

            {/* Edit/Add Dialog */}
            <Dialog open={editDialogOpen} onOpenChange={setEditDialogOpen}>
                <DialogContent>
                    <DialogHeader>
                        <DialogTitle>
                            {editItem ? `Edit ${editType}` : `Add ${editType}`}
                        </DialogTitle>
                    </DialogHeader>
                    <div className="space-y-4">
                        <div>
                            <Label>Name *</Label>
                            <Input 
                                value={editForm.name} 
                                onChange={(e) => setEditForm({ ...editForm, name: e.target.value })}
                                placeholder={editType === 'year' ? 'e.g., First Year' : editType === 'semester' ? 'e.g., Semester 1' : editType === 'section' ? 'e.g., Section A' : 'e.g., Batch A'}
                            />
                        </div>
                        
                        {(editType === 'section' || editType === 'batch') && !editItem && (
                            <div>
                                <Label>Code *</Label>
                                <Input 
                                    value={editForm.code} 
                                    onChange={(e) => setEditForm({ ...editForm, code: e.target.value.toUpperCase() })}
                                    placeholder="e.g., A, B, 1, 2"
                                />
                            </div>
                        )}
                        
                        {(editType === 'section' || editType === 'batch') && (
                            <div>
                                <Label>Max Strength</Label>
                                <Input 
                                    type="number" 
                                    value={editForm.max_strength} 
                                    onChange={(e) => setEditForm({ ...editForm, max_strength: parseInt(e.target.value) || 30 })}
                                    min={1}
                                />
                            </div>
                        )}
                        
                        {editType === 'semester' && (
                            <>
                                <div className="flex items-center gap-2">
                                    <Switch 
                                        checked={editForm.is_internship} 
                                        onCheckedChange={(v) => setEditForm({ ...editForm, is_internship: v })} 
                                    />
                                    <Label>Internship Semester</Label>
                                </div>
                                <div className="flex items-center gap-2">
                                    <Switch 
                                        checked={editForm.is_project_semester} 
                                        onCheckedChange={(v) => setEditForm({ ...editForm, is_project_semester: v })} 
                                    />
                                    <Label>Project Semester</Label>
                                </div>
                            </>
                        )}
                        
                        {(editType === 'year' || editType === 'section' || editType === 'batch') && (
                            <div className="flex items-center gap-2">
                                <Switch 
                                    checked={editForm.is_active} 
                                    onCheckedChange={(v) => setEditForm({ ...editForm, is_active: v })} 
                                />
                                <Label>Active</Label>
                            </div>
                        )}
                        
                        <div className="flex justify-end gap-2">
                            <Button variant="outline" onClick={() => setEditDialogOpen(false)}>Cancel</Button>
                            <Button onClick={handleSaveEdit} className="bg-blue-600 hover:bg-blue-700">Save</Button>
                        </div>
                    </div>
                </DialogContent>
            </Dialog>
        </>
    );
}
