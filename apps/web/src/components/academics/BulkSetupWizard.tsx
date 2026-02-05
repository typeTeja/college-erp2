'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { BulkBatchSetupRequest } from '@/types/bulk-setup';
import { Program } from '@/types/program';
import { Regulation } from '@/types/regulation';
import { academicYearService } from '@/utils/academic-year-service';
import { institutionalService } from '@/utils/institutional-service';
import { api } from '@/utils/api';
import { Lock, AlertCircle, ShieldCheck } from 'lucide-react';
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow
} from '@/components/ui/table';

interface BulkSetupWizardProps {
    programs: Program[];
    regulations: Regulation[];
}

type WizardStep = 'program' | 'regulation' | 'configuration' | 'freeze' | 'review';

export function BulkSetupWizard({ programs, regulations }: BulkSetupWizardProps) {
    const router = useRouter();
    const [currentStep, setCurrentStep] = useState<WizardStep>('program');
    const [loading, setLoading] = useState(false);
    const [creationStep, setCreationStep] = useState<string>('');

    const currentYear = new Date().getFullYear();

    const { data: academicYears = [] } = academicYearService.useAcademicYears();
    const { data: departments = [] } = institutionalService.useDepartments();

    const [formData, setFormData] = useState<Partial<BulkBatchSetupRequest>>({
        joining_year: currentYear,
        sections_per_semester: 1,
        section_capacity: 60,
        labs_per_semester: 0,
        lab_capacity: 40,
    });

    const selectedProgram = programs.find(p => p.id === formData.program_id);
    const selectedRegulation = regulations.find(r => r.id === formData.regulation_id);
    const filteredRegulations = regulations.filter(r => !formData.program_id || r.program_id === formData.program_id);

    // Calculate statistics
    const calculateStats = () => {
        if (!selectedProgram) return null;

        const years = selectedProgram.duration_years;
        const semesters = selectedProgram.number_of_semesters || years * 2;
        const sectionsPerSemester = formData.sections_per_semester || 0;
        const totalSections = semesters * sectionsPerSemester;
        const labsPerSemester = formData.labs_per_semester || 0;
        const totalLabs = semesters * labsPerSemester;

        const batchIntakeCapacity = sectionsPerSemester * (formData.section_capacity || 0);
        const labIntakeCapacity = labsPerSemester * (formData.lab_capacity || 0);

        const totalSectionCapacity = totalSections * (formData.section_capacity || 0);
        const totalLabCapacity = totalLabs * (formData.lab_capacity || 0);

        return {
            years,
            semesters,
            sectionsPerSemester,
            totalSections,
            labsPerSemester,
            totalLabs,
            batchIntakeCapacity,
            labIntakeCapacity,
            totalSectionCapacity,
            totalLabCapacity,
        };
    };

    const stats = calculateStats();

    const handleNext = () => {
        if (currentStep === 'program') {
            if (!formData.program_id || !formData.joining_year) {
                toast.error('Please select a program and joining year');
                return;
            }
            setCurrentStep('regulation');
        } else if (currentStep === 'regulation') {
            if (!formData.regulation_id) {
                toast.error('Please select a regulation');
                return;
            }
            setCurrentStep('configuration');
        } else if (currentStep === 'configuration') {
            if (!formData.sections_per_semester || !formData.section_capacity) {
                toast.error('Please configure sections');
                return;
            }
            setCurrentStep('freeze');
        } else if (currentStep === 'freeze') {
            setCurrentStep('review');
        }
    };

    const handleBack = () => {
        if (currentStep === 'regulation') setCurrentStep('program');
        else if (currentStep === 'freeze') setCurrentStep('configuration');
        else if (currentStep === 'review') setCurrentStep('freeze');
    };

    const handleSubmit = async () => {
        if (!formData.program_id || !formData.joining_year || !formData.regulation_id) {
            toast.error('Missing required fields');
            return;
        }

        setLoading(true);
        setCreationStep('Initializing setup...');

        try {
            // 1. Create the Batch
            setCreationStep('Creating batch...');
            const batchName = `${formData.joining_year}-${formData.joining_year + (selectedProgram?.duration_years || 0)} ${selectedProgram?.code}`;
            const batchCode = `${selectedProgram?.code}-${formData.joining_year}`;

            const admissionYear = academicYears.find(ay => ay.year.includes(formData.joining_year!.toString()));
            if (!admissionYear) {
                throw new Error(`Academic year record for ${formData.joining_year} not found. Please setup academic years first.`);
            }

            const batchResponse = await api.post<any>('/academic/batches', {
                batch_name: batchName,
                batch_code: batchCode,
                program_id: formData.program_id,
                regulation_id: formData.regulation_id,
                joining_year: formData.joining_year,
                start_year: formData.joining_year,
                end_year: formData.joining_year + (selectedProgram?.duration_years || 0)
            });
            const batch = batchResponse.data;

            // 2. Create Semesters
            const totalSemesters = selectedProgram?.number_of_semesters || 8;
            setCreationStep(`Creating ${totalSemesters} semesters...`);

            for (let i = 1; i <= totalSemesters; i++) {
                const yearOffset = Math.floor((i - 1) / 2);
                const targetYear = formData.joining_year! + yearOffset;
                const semYear = academicYears.find(ay => ay.year.includes(targetYear.toString()));

                if (!semYear) {
                    throw new Error(`Academic year for semester ${i} (${targetYear}) not found.`);
                }

                setCreationStep(`Creating Semester ${i}...`);
                const semResponse = await api.post<any>('/academic/batch-semesters', {
                    batch_id: batch.id,
                    semester_number: i,
                    academic_year_id: semYear.id,
                    start_date: new Date(targetYear, i % 2 !== 0 ? 6 : 0, 1).toISOString(),
                    end_date: new Date(targetYear + (i % 2 === 0 ? 0 : 1), i % 2 !== 0 ? 11 : 5, 30).toISOString()
                });
                const semester = semResponse.data;

                // 3. Create Sections
                if (formData.sections_per_semester) {
                    setCreationStep(`Creating sections for Sem ${i}...`);
                    for (let s = 1; s <= formData.sections_per_semester; s++) {
                        const sectionName = `Section ${String.fromCharCode(64 + s)}`;
                        await api.post('/academic/sections', {
                            name: sectionName,
                            batch_id: batch.id,
                            semester_no: i,
                            capacity: formData.section_capacity || 60
                        });
                    }
                }

                // 4. Create Practical Batches
                if (formData.labs_per_semester) {
                    setCreationStep(`Creating labs for Sem ${i}...`);
                    for (let l = 1; l <= formData.labs_per_semester; l++) {
                        const labName = `L${l}`;
                        await api.post('/academic/practical-batches', {
                            name: labName,
                            batch_id: batch.id,
                            batch_semester_id: semester.id,
                            capacity: formData.lab_capacity || 30,
                            code: `${batchCode}-S${i}-L${l}`
                        });
                    }
                }
            }

            // 5. Hardened Rule Freeze (NEW)
            setCreationStep('Calculating rule checksum & freezing rules...');
            await api.post(`/academic/batches/${batch.id}/freeze`);

            toast.success('Sequential batch setup completed successfully');
            router.push('/setup/batches');
        } catch (error: any) {
            console.error('Batch setup sequence failed:', error);
            const detail = error.response?.data?.detail;
            toast.error(typeof detail === 'string' ? detail : error.message || 'Failed to complete sequential setup');
        } finally {
            setLoading(false);
            setCreationStep('');
        }
    };

    return (
        <div className="max-w-4xl mx-auto p-6">
            <div className="mb-8">
                <div className="flex items-center justify-between">
                    {(['program', 'regulation', 'configuration', 'freeze', 'review'] as WizardStep[]).map((step, index) => (
                        <div key={step} className="flex items-center flex-1">
                            <div className="flex flex-col items-center flex-1">
                                <div
                                    className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold transition-colors ${currentStep === step ? 'bg-blue-600 text-white' :
                                        index < (['program', 'regulation', 'configuration', 'freeze', 'review'] as WizardStep[]).indexOf(currentStep) ? 'bg-green-600 text-white' :
                                            'bg-gray-200 text-gray-600'
                                        }`}
                                >
                                    {index + 1}
                                </div>
                                <div className="text-sm mt-2 font-medium capitalize">{step}</div>
                            </div>
                            {index < 4 && (
                                <div className={`h-1 flex-1 mx-2 transition-colors ${index < (['program', 'regulation', 'configuration', 'review'] as WizardStep[]).indexOf(currentStep) ? 'bg-green-600' : 'bg-gray-200'
                                    }`} />
                            )}
                        </div>
                    ))}
                </div>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle>
                        {currentStep === 'program' && '1. Select Program & Year'}
                        {currentStep === 'regulation' && '2. Choose Regulation'}
                        {currentStep === 'configuration' && '3. Configure Structure'}
                        {currentStep === 'freeze' && '4. Regulation Freeze Preview'}
                        {currentStep === 'review' && '5. Review & Create'}
                    </CardTitle>
                    <CardDescription>
                        {currentStep === 'program' && 'Choose the program and joining year for this batch'}
                        {currentStep === 'regulation' && 'Select the regulation to bind to this batch'}
                        {currentStep === 'configuration' && 'Configure sections and lab groups'}
                        {currentStep === 'freeze' && 'Mandatory review of immutable academic rules'}
                        {currentStep === 'review' && 'Review your configuration before creating'}
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                    {currentStep === 'program' && (
                        <div className="space-y-4">
                            <div>
                                <Label htmlFor="program">Program *</Label>
                                <select
                                    id="program"
                                    className="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    value={formData.program_id || ''}
                                    onChange={(e) => setFormData({ ...formData, program_id: parseInt(e.target.value), regulation_id: undefined })}
                                >
                                    <option value="">Select a program</option>
                                    {programs.map((p) => {
                                        const deptName = departments.find(d => d.id === p.department_id)?.department_name;
                                        return (
                                            <option key={p.id} value={p.id}>
                                                {p.name} ({p.code}) {deptName ? `- ${deptName}` : ''}
                                            </option>
                                        );
                                    })}
                                </select>
                            </div>
                            <div>
                                <Label htmlFor="joining_year">Joining Year *</Label>
                                <Input
                                    id="joining_year"
                                    type="number"
                                    value={formData.joining_year}
                                    onChange={(e) => setFormData({ ...formData, joining_year: parseInt(e.target.value) })}
                                />
                            </div>
                        </div>
                    )}

                    {currentStep === 'regulation' && (
                        <div className="space-y-4">
                            <div>
                                <Label htmlFor="regulation">Regulation *</Label>
                                <select
                                    id="regulation"
                                    className="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    value={formData.regulation_id || ''}
                                    onChange={(e) => setFormData({ ...formData, regulation_id: parseInt(e.target.value) })}
                                >
                                    <option value="">Select a regulation</option>
                                    {filteredRegulations.map((r) => (
                                        <option key={r.id} value={r.id}>{r.name}</option>
                                    ))}
                                </select>
                            </div>
                        </div>
                    )}

                    {currentStep === 'configuration' && (
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <Label htmlFor="sections">Sections per Semester</Label>
                                <Input
                                    id="sections"
                                    type="number"
                                    value={formData.sections_per_semester}
                                    onChange={(e) => setFormData({ ...formData, sections_per_semester: parseInt(e.target.value) })}
                                />
                            </div>
                            <div>
                                <Label htmlFor="capacity">Section Capacity</Label>
                                <Input
                                    id="capacity"
                                    type="number"
                                    value={formData.section_capacity}
                                    onChange={(e) => setFormData({ ...formData, section_capacity: parseInt(e.target.value) })}
                                />
                            </div>
                            <div>
                                <Label htmlFor="labs">Lab Groups per Semester</Label>
                                <Input
                                    id="labs"
                                    type="number"
                                    value={formData.labs_per_semester === 0 ? 0 : (formData.labs_per_semester || '')}
                                    onChange={(e) => setFormData({ ...formData, labs_per_semester: parseInt(e.target.value) || 0 })}
                                />
                            </div>
                            <div>
                                <Label htmlFor="lab_capacity">Lab Capacity</Label>
                                <Input
                                    id="lab_capacity"
                                    type="number"
                                    value={formData.lab_capacity}
                                    onChange={(e) => setFormData({ ...formData, lab_capacity: parseInt(e.target.value) })}
                                    disabled={!formData.labs_per_semester}
                                />
                            </div>
                        </div>
                    )}

                    {currentStep === 'freeze' && (
                        <div className="space-y-4">
                            <div className="bg-amber-50 border border-amber-200 p-4 rounded-lg">
                                <h4 className="text-amber-800 font-semibold flex items-center gap-2">
                                    <Lock className="h-4 w-4" /> Immutable Rule Freeze
                                </h4>
                                <p className="text-xs text-amber-700 mt-1">
                                    Continuing will create a **one-way commit** of the following rules from Regulation <strong>{selectedRegulation?.name}</strong>. Once frozen, these rules cannot be changed even if the global regulation is updated.
                                </p>
                            </div>

                            <div className="border rounded-lg overflow-hidden">
                                <Table>
                                    <TableHeader className="bg-slate-50">
                                        <TableRow>
                                            <TableHead>Category</TableHead>
                                            <TableHead>Details</TableHead>
                                        </TableRow>
                                    </TableHeader>
                                    <TableBody>
                                        <TableRow>
                                            <TableCell className="font-medium">Total Credits</TableCell>
                                            <TableCell>{selectedRegulation?.total_credits || 'N/A'}</TableCell>
                                        </TableRow>
                                        <TableRow>
                                            <TableCell className="font-medium">Subjects</TableCell>
                                            <TableCell>{(selectedRegulation as any)?.subjects?.length || 0} subjects will be snapshotted</TableCell>
                                        </TableRow>
                                        <TableRow>
                                            <TableCell className="font-medium">Promotion Rules</TableCell>
                                            <TableCell>Credit-based detention will be enforced</TableCell>
                                        </TableRow>
                                    </TableBody>
                                </Table>
                            </div>

                            <div className="flex items-center space-x-2 p-2">
                                <input type="checkbox" id="confirm-freeze" className="rounded border-gray-300" />
                                <Label htmlFor="confirm-freeze" className="text-xs text-slate-600">
                                    I understand that these academic rules will be frozen and immutable for this cohort.
                                </Label>
                            </div>
                        </div>
                    )}

                    {currentStep === 'review' && stats && (
                        <div className="space-y-4">
                            <div className="bg-gray-50 p-4 rounded-lg space-y-2 text-sm">
                                <div className="flex justify-between"><span>Program:</span><span className="font-medium">{selectedProgram?.name}</span></div>
                                <div className="flex justify-between"><span>Regulation:</span><span className="font-medium">{selectedRegulation?.name}</span></div>
                                <div className="flex justify-between"><span>Batch Year:</span><span className="font-medium">{formData.joining_year}</span></div>
                                <div className="flex justify-between border-t pt-2"><span>Total Semesters:</span><span className="font-medium">{stats.semesters}</span></div>
                                <div className="flex justify-between"><span>Sections/Sem:</span><span className="font-medium">{stats.sectionsPerSemester}</span></div>
                                <div className="flex justify-between"><span>Total Sections:</span><span className="font-medium">{stats.totalSections}</span></div>
                            </div>
                            <div className="bg-blue-50 p-4 border border-blue-200 rounded-lg">
                                <h4 className="font-semibold text-blue-900 mb-1 flex items-center">🚀 Atomic Creation Summary</h4>
                                <p className="text-xs text-blue-800">Sequential execution will create {stats.semesters} semesters and {stats.totalSections} sections + {stats.totalLabs} lab groups.</p>
                            </div>
                        </div>
                    )}

                    <div className="flex justify-between pt-6 border-t">
                        <Button variant="outline" onClick={handleBack} disabled={currentStep === 'program' || loading}>Back</Button>
                        {currentStep !== 'review' ? (
                            <Button onClick={handleNext}>Next</Button>
                        ) : (
                            <Button onClick={handleSubmit} disabled={loading} className="bg-green-600 hover:bg-green-700 min-w-[120px]">
                                {loading ? (
                                    <div className="flex items-center">
                                        <div className="animate-spin mr-2 h-4 w-4 border-2 border-white border-t-transparent rounded-full" />
                                        Creating...
                                    </div>
                                ) : 'Create Batch'}
                            </Button>
                        )}
                    </div>

                    {loading && creationStep && (
                        <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded animate-pulse text-center">
                            <p className="text-sm text-blue-700 font-medium">{creationStep}</p>
                        </div>
                    )}
                </CardContent>
            </Card>
        </div>
    );
}
