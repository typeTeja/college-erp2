import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ChevronRight, ChevronDown, Layers, Users, Beaker, BookOpen, UserPlus, Settings2, GraduationCap } from 'lucide-react';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { getAcademicBatches, getProgramYears, getBatchSemesters, getBatchSubjects } from '@/utils/master-data-service';
import { BatchSubject } from '@/types/academic-batch';
import { toast } from 'sonner';
import { SemesterSettingsDialog } from './SemesterSettingsDialog';
import LabAllocationManager from './LabAllocationManager';

interface StructureNode {
    id: string;
    label: string;
    type: 'BATCH' | 'YEAR' | 'SEMESTER' | 'SECTION' | 'LAB';
    children?: StructureNode[];
    details?: string;
    meta?: any;
    isActive?: boolean;
}

export function AcademicStructureTab() {
    const [batches, setBatches] = useState<any[]>([]);
    const [selectedBatch, setSelectedBatch] = useState<string>("");
    const [structure, setStructure] = useState<StructureNode[]>([]);
    const [expanded, setExpanded] = useState<Record<string, boolean>>({});

    // Allocation Modal State
    const [allocationOpen, setAllocationOpen] = useState(false);
    const [selectedLab, setSelectedLab] = useState<any>(null);
    const [semesterSubjects, setSemesterSubjects] = useState<BatchSubject[]>([]);

    // Semester Settings Modal State
    const [settingsOpen, setSettingsOpen] = useState(false);
    const [selectedSemester, setSelectedSemester] = useState<any>(null);

    useEffect(() => {
        loadBatches();
    }, []);

    const loadBatches = async () => {
        try {
            const data = await getAcademicBatches(undefined, true);
            setBatches(data);
        } catch (e) {
            toast.error("Failed to load batches");
        }
    };

    const loadStructure = async (batchId: string) => {
        if (!batchId) return;
        try {
            // Fetch program years and semesters
            const [programYears, allSemesters] = await Promise.all([
                getProgramYears(parseInt(batchId)),
                getBatchSemesters(parseInt(batchId))
            ]);

            // Group semesters by program_year_id
            const semestersByYear = allSemesters.reduce((acc: any, sem: any) => {
                if (!acc[sem.program_year_id]) {
                    acc[sem.program_year_id] = [];
                }
                acc[sem.program_year_id].push(sem);
                return acc;
            }, {});

            // Build year nodes with nested semesters
            const nodes: StructureNode[] = programYears.map((year: any) => {
                const yearSemesters = semestersByYear[year.id] || [];

                return {
                    id: `year-${year.id}`,
                    label: year.year_name,
                    type: 'YEAR',
                    details: `${yearSemesters.length} semester${yearSemesters.length !== 1 ? 's' : ''}`,
                    meta: year,
                    children: yearSemesters.map((sem: any) => ({
                        id: `sem-${sem.id}`,
                        label: sem.semester_name,
                        type: 'SEMESTER',
                        details: sem.start_date ? `${sem.start_date} - ${sem.end_date}` : 'Set dates',
                        isActive: sem.is_active,
                        meta: sem,
                        children: [
                            {
                                id: `sem-${sem.id}-sections`,
                                label: 'Theory Sections',
                                type: 'SECTION',
                                children: (sem.sections || []).map((sec: any) => ({
                                    id: `sec-${sec.id}`,
                                    label: `${sec.name} (${sec.code})`,
                                    type: 'SECTION',
                                    details: `${sec.current_strength}/${sec.max_strength} students`
                                }))
                            },
                            {
                                id: `sem-${sem.id}-labs`,
                                label: 'Practical Lab Batches',
                                type: 'LAB',
                                children: (sem.practical_batches || []).map((lab: any) => ({
                                    id: `lab-${lab.id}`,
                                    label: `${lab.name} (${lab.code})`,
                                    type: 'LAB',
                                    details: `${lab.current_strength}/${lab.max_strength} students`,
                                    meta: {
                                        ...lab,
                                        batch_id: parseInt(batchId),
                                        batch_semester_id: sem.id,
                                        semester_no: sem.semester_no
                                    }
                                }))
                            }
                        ]
                    }))
                };
            });

            setStructure(nodes);
            // Auto expand root nodes (years) and their semester children
            const newExpanded = { ...expanded };
            nodes.forEach(yearNode => {
                newExpanded[yearNode.id] = true; // Expand years
                yearNode.children?.forEach(semesterNode => {
                    newExpanded[semesterNode.id] = true; // Expand semesters
                    semesterNode.children?.forEach(containerNode => {
                        // Auto-expand "Theory Sections" and "Practical Lab Batches" containers
                        newExpanded[containerNode.id] = true;
                    });
                });
            });
            setExpanded(newExpanded);

        } catch (e: any) {
            console.error('Failed to load structure:', e);
            toast.error(e?.message || "Failed to load structure. Please try again.");
        }
    };

    const toggleExpand = (id: string) => {
        setExpanded(prev => ({ ...prev, [id]: !prev[id] }));
    };

    const handleOpenAllocation = async (labMeta: any) => {
        try {
            // Fetch subjects for this semester (to filter for Practicals inside modal)
            const subjects = await getBatchSubjects(labMeta.batch_id, labMeta.semester_no);
            setSemesterSubjects(subjects);
            setSelectedLab(labMeta);
            setAllocationOpen(true);
        } catch (e) {
            console.error(e);
            toast.error("Failed to load semester subjects");
        }
    };

    const renderTree = (nodes: StructureNode[]) => {
        return (
            <div className="pl-4 border-l border-slate-200 ml-2 space-y-1">
                {nodes.map(node => (
                    <div key={node.id}>
                        <div
                            className={`flex items-center justify-between p-2 rounded-md transition-colors hover:bg-slate-50 cursor-pointer group ${node.type === 'SEMESTER' ? 'font-medium text-slate-900' : 'text-slate-600'}`}
                            onClick={() => toggleExpand(node.id)}
                        >
                            <div className="flex items-center gap-2">
                                {node.children && node.children.length > 0 ? (
                                    expanded[node.id] ? <ChevronDown className="h-4 w-4 text-slate-400" /> : <ChevronRight className="h-4 w-4 text-slate-400" />
                                ) : <span className="w-4" />}

                                {node.type === 'YEAR' && <GraduationCap className="h-4 w-4 text-purple-600" />}
                                {node.type === 'SEMESTER' && <Layers className="h-4 w-4 text-indigo-600" />}
                                {node.type === 'SECTION' && <Users className="h-4 w-4 text-blue-600" />}
                                {node.type === 'LAB' && <Beaker className="h-4 w-4 text-emerald-600" />}

                                <span>{node.label}</span>
                                {node.details && <span className="text-xs text-slate-400 ml-2">{node.details}</span>}
                            </div>

                            {/* Action Buttons for Leaf Nodes */}
                            {node.type === 'LAB' && node.meta && (
                                <div className="opacity-0 group-hover:opacity-100 transition-opacity">
                                    <Button
                                        size="sm"
                                        variant="outline"
                                        className="h-7 text-xs"
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            handleOpenAllocation(node.meta);
                                        }}
                                    >
                                        <Settings2 className="h-3 w-3 mr-1" />
                                        Manage
                                    </Button>
                                </div>
                            )}

                            {node.type === 'SEMESTER' && node.meta && (
                                <div className="opacity-0 group-hover:opacity-100 transition-opacity ml-auto mr-2">
                                    <Button
                                        size="sm"
                                        variant="ghost"
                                        className="h-7 w-7 p-0"
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            setSelectedSemester(node.meta);
                                            setSettingsOpen(true);
                                        }}
                                        title="Edit Semester Dates"
                                    >
                                        <Settings2 className="h-4 w-4 text-slate-500" />
                                    </Button>
                                </div>
                            )}
                        </div>

                        {expanded[node.id] && node.children && (
                            renderTree(node.children)
                        )}
                    </div>
                ))}
            </div>
        );
    };

    return (
        <>
            <Card className="min-h-[600px]">
                <CardHeader>
                    <CardTitle className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <Layers className="h-5 w-5 text-indigo-600" />
                            Academic Structure Viewer
                        </div>
                        <div className="w-[300px]">
                            <Select value={selectedBatch} onValueChange={(v) => { setSelectedBatch(v); loadStructure(v); }}>
                                <SelectTrigger>
                                    <SelectValue placeholder="Select Batch to View" />
                                </SelectTrigger>
                                <SelectContent>
                                    {batches.map((b: any) => (
                                        <SelectItem key={b.id} value={b.id.toString()}>
                                            {b.batch_name} ({b.batch_code})
                                        </SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </div>
                    </CardTitle>
                </CardHeader>
                <CardContent>
                    {selectedBatch ? (
                        structure.length > 0 ? (
                            renderTree(structure)
                        ) : (
                            <div className="text-center py-12 text-slate-500">
                                Loading structure or no structure found...
                            </div>
                        )
                    ) : (
                        <div className="text-center py-12 text-slate-500">
                            <BookOpen className="h-12 w-12 mx-auto text-slate-300 mb-2" />
                            <p>Select an academic batch to view its structure hierarchy</p>
                        </div>
                    )}
                </CardContent>
            </Card>

            {selectedLab && (
                <LabAllocationManager
                    open={allocationOpen}
                    onClose={() => setAllocationOpen(false)}
                    labBatch={selectedLab}
                    subjects={semesterSubjects}
                />
            )}

            {selectedSemester && (
                <SemesterSettingsDialog
                    open={settingsOpen}
                    onClose={() => setSettingsOpen(false)}
                    batchId={selectedSemester.batch_id}
                    semesterId={selectedSemester.id}
                    semesterName={selectedSemester.semester_name}
                    currentStartDate={selectedSemester.start_date}
                    currentEndDate={selectedSemester.end_date}
                    currentIsActive={selectedSemester.is_active}
                    onUpdate={() => selectedBatch && loadStructure(selectedBatch)}
                />
            )}
        </>
    );
}
