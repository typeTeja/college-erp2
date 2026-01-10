'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { BulkBatchSetupRequest } from '@/types/bulk-setup';
import { bulkSetupService } from '@/utils/bulk-setup-service';
import { Program } from '@/types/program';
import { Regulation } from '@/types/regulation';

interface BulkSetupWizardProps {
    programs: Program[];
    regulations: Regulation[];
}

type WizardStep = 'program' | 'regulation' | 'configuration' | 'review';

export function BulkSetupWizard({ programs, regulations }: BulkSetupWizardProps) {
    const router = useRouter();
    const [currentStep, setCurrentStep] = useState<WizardStep>('program');
    const [loading, setLoading] = useState(false);

    const [formData, setFormData] = useState<Partial<BulkBatchSetupRequest>>({
        sections_per_semester: 1,
        section_capacity: 60,
        labs_per_section: 0,
        lab_capacity: 20,
    });

    // Ensure labs_per_section is never null/undefined
    const ensureLabsValue = (value: number | undefined | null): number => {
        return value === null || value === undefined ? 0 : value;
    };

    const selectedProgram = programs.find(p => p.id === formData.program_id);
    const selectedRegulation = regulations.find(r => r.id === formData.regulation_id);
    // Show all regulations - backend will validate compatibility
    const filteredRegulations = regulations;

    const currentYear = new Date().getFullYear();

    // Calculate statistics
    const calculateStats = () => {
        if (!selectedProgram) return null;

        const years = selectedProgram.duration_years;
        // Always use semester system (2 semesters per year)
        const semesters = years * 2;
        const sections = semesters * (formData.sections_per_semester || 0);
        const labs = sections * ensureLabsValue(formData.labs_per_section);
        const totalSectionCapacity = sections * (formData.section_capacity || 0);
        const totalLabCapacity = labs * (formData.lab_capacity || 0);

        return {
            years,
            semesters,
            sections,
            labs,
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
            setCurrentStep('review');
        }
    };

    const handleBack = () => {
        if (currentStep === 'regulation') setCurrentStep('program');
        else if (currentStep === 'configuration') setCurrentStep('regulation');
        else if (currentStep === 'review') setCurrentStep('configuration');
    };

    const handleSubmit = async () => {
        if (!formData.program_id || !formData.joining_year || !formData.regulation_id) {
            toast.error('Missing required fields');
            return;
        }

        setLoading(true);
        try {
            // Ensure labs_per_section is a number, not null/undefined
            const payload = {
                ...formData,
                labs_per_section: ensureLabsValue(formData.labs_per_section),
            } as BulkBatchSetupRequest;

            const result = await bulkSetupService.createBulkBatch(payload);

            toast.success(
                <div>
                    <div className="font-semibold">{result.message}</div>
                    <div className="text-sm mt-1">
                        Created {result.years_created} years, {result.semesters_created} semesters,
                        {result.sections_created} sections, and {result.labs_created} labs
                    </div>
                </div>
            );

            router.push(`/academics/batches/${result.batch_id}`);
        } catch (error: any) {
            toast.error(error.response?.data?.detail || 'Failed to create batch');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto p-6">
            {/* Progress Steps */}
            <div className="mb-8">
                <div className="flex items-center justify-between">
                    {(['program', 'regulation', 'configuration', 'review'] as WizardStep[]).map((step, index) => (
                        <div key={step} className="flex items-center flex-1">
                            <div className="flex flex-col items-center flex-1">
                                <div
                                    className={`w-10 h-10 rounded-full flex items-center justify-center font-semibold transition-colors ${currentStep === step
                                        ? 'bg-blue-600 text-white'
                                        : index < (['program', 'regulation', 'configuration', 'review'] as WizardStep[]).indexOf(currentStep)
                                            ? 'bg-green-600 text-white'
                                            : 'bg-gray-200 text-gray-600'
                                        }`}
                                >
                                    {index + 1}
                                </div>
                                <div className="text-sm mt-2 font-medium capitalize">{step}</div>
                            </div>
                            {index < 3 && (
                                <div
                                    className={`h-1 flex-1 mx-2 transition-colors ${index < (['program', 'regulation', 'configuration', 'review'] as WizardStep[]).indexOf(currentStep)
                                        ? 'bg-green-600'
                                        : 'bg-gray-200'
                                        }`}
                                />
                            )}
                        </div>
                    ))}
                </div>
            </div>

            {/* Step Content */}
            <Card>
                <CardHeader>
                    <CardTitle>
                        {currentStep === 'program' && '1. Select Program & Year'}
                        {currentStep === 'regulation' && '2. Choose Regulation'}
                        {currentStep === 'configuration' && '3. Configure Structure'}
                        {currentStep === 'review' && '4. Review & Create'}
                    </CardTitle>
                    <CardDescription>
                        {currentStep === 'program' && 'Choose the program and joining year for this batch'}
                        {currentStep === 'regulation' && 'Select the regulation to bind to this batch'}
                        {currentStep === 'configuration' && 'Configure sections and lab groups'}
                        {currentStep === 'review' && 'Review your configuration before creating'}
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                    {/* Step 1: Program Selection */}
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
                                    {programs.map((program) => (
                                        <option key={program.id} value={program.id}>
                                            {program.name} ({program.code}) - {program.duration_years} years
                                        </option>
                                    ))}
                                </select>
                            </div>

                            <div>
                                <Label htmlFor="joining_year">Joining Year *</Label>
                                <Input
                                    id="joining_year"
                                    type="number"
                                    min={currentYear - 1}
                                    max={currentYear + 2}
                                    value={formData.joining_year || currentYear}
                                    onChange={(e) => setFormData({ ...formData, joining_year: parseInt(e.target.value) })}
                                />
                                <p className="text-sm text-gray-500 mt-1">
                                    Students joining in this year
                                </p>
                            </div>

                            {selectedProgram && formData.joining_year && (
                                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                                    <h4 className="font-semibold text-blue-900 mb-2">Batch Preview</h4>
                                    <p className="text-sm text-blue-800">
                                        Batch Code: <span className="font-mono font-semibold">
                                            {formData.joining_year}-{formData.joining_year + selectedProgram.duration_years}
                                        </span>
                                    </p>
                                    <p className="text-sm text-blue-800 mt-1">
                                        Duration: {selectedProgram.duration_years} years ({selectedProgram.duration_years * 2} semesters)
                                    </p>
                                </div>
                            )}
                        </div>
                    )}

                    {/* Step 2: Regulation Selection */}
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
                                    {filteredRegulations.map((regulation) => (
                                        <option key={regulation.id} value={regulation.id}>
                                            {regulation.regulation_name} ({regulation.regulation_code})
                                            {regulation.is_locked && ' 🔒'}
                                        </option>
                                    ))}
                                </select>
                                <p className="text-sm text-gray-500 mt-1">
                                    {filteredRegulations.length === 0
                                        ? 'No regulations available. Please create a regulation first.'
                                        : 'Select the regulation to bind to this batch'}
                                </p>
                            </div>

                            {selectedRegulation && (
                                <div className="bg-purple-50 border border-purple-200 rounded-lg p-4">
                                    <h4 className="font-semibold text-purple-900 mb-2">Regulation Details</h4>
                                    <p className="text-sm text-purple-800">
                                        Code: <span className="font-mono">{selectedRegulation.regulation_code}</span>
                                    </p>
                                    <p className="text-sm text-purple-800 mt-1">
                                        Name: {selectedRegulation.regulation_name}
                                    </p>
                                    {selectedRegulation.is_locked && (
                                        <p className="text-sm text-purple-800 mt-1">
                                            🔒 This regulation is locked (already in use)
                                        </p>
                                    )}
                                </div>
                            )}
                        </div>
                    )}

                    {/* Step 3: Configuration */}
                    {currentStep === 'configuration' && (
                        <div className="space-y-6">
                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <Label htmlFor="sections_per_semester">Sections per Semester *</Label>
                                    <Input
                                        id="sections_per_semester"
                                        type="number"
                                        min={1}
                                        max={10}
                                        value={formData.sections_per_semester}
                                        onChange={(e) => setFormData({ ...formData, sections_per_semester: parseInt(e.target.value) })}
                                    />
                                    <p className="text-sm text-gray-500 mt-1">e.g., 2 for Section A, B</p>
                                </div>

                                <div>
                                    <Label htmlFor="section_capacity">Section Capacity *</Label>
                                    <Input
                                        id="section_capacity"
                                        type="number"
                                        min={10}
                                        max={200}
                                        value={formData.section_capacity}
                                        onChange={(e) => setFormData({ ...formData, section_capacity: parseInt(e.target.value) })}
                                    />
                                    <p className="text-sm text-gray-500 mt-1">Max students per section</p>
                                </div>

                                <div>
                                    <Label htmlFor="labs_per_section">Lab Groups per Section</Label>
                                    <Input
                                        id="labs_per_section"
                                        type="number"
                                        min={0}
                                        max={5}
                                        value={formData.labs_per_section}
                                        onChange={(e) => setFormData({ ...formData, labs_per_section: parseInt(e.target.value) })}
                                    />
                                    <p className="text-sm text-gray-500 mt-1">0 for no labs</p>
                                </div>

                                <div>
                                    <Label htmlFor="lab_capacity">Lab Capacity</Label>
                                    <Input
                                        id="lab_capacity"
                                        type="number"
                                        min={5}
                                        max={50}
                                        value={formData.lab_capacity}
                                        onChange={(e) => setFormData({ ...formData, lab_capacity: parseInt(e.target.value) })}
                                        disabled={!formData.labs_per_section}
                                    />
                                    <p className="text-sm text-gray-500 mt-1">Max students per lab</p>
                                </div>
                            </div>

                            {stats && (
                                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                                    <h4 className="font-semibold text-green-900 mb-3">What Will Be Created</h4>
                                    <div className="grid grid-cols-2 gap-3 text-sm">
                                        <div className="flex justify-between">
                                            <span className="text-green-800">Program Years:</span>
                                            <span className="font-semibold text-green-900">{stats.years}</span>
                                        </div>
                                        <div className="flex justify-between">
                                            <span className="text-green-800">Semesters:</span>
                                            <span className="font-semibold text-green-900">{stats.semesters}</span>
                                        </div>
                                        <div className="flex justify-between">
                                            <span className="text-green-800">Sections:</span>
                                            <span className="font-semibold text-green-900">{stats.sections}</span>
                                        </div>
                                        <div className="flex justify-between">
                                            <span className="text-green-800">Lab Groups:</span>
                                            <span className="font-semibold text-green-900">{stats.labs}</span>
                                        </div>
                                        <div className="flex justify-between col-span-2 pt-2 border-t border-green-300">
                                            <span className="text-green-800">Total Section Capacity:</span>
                                            <span className="font-semibold text-green-900">{stats.totalSectionCapacity} students</span>
                                        </div>
                                        {stats.labs > 0 && (
                                            <div className="flex justify-between col-span-2">
                                                <span className="text-green-800">Total Lab Capacity:</span>
                                                <span className="font-semibold text-green-900">{stats.totalLabCapacity} students</span>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            )}
                        </div>
                    )}

                    {/* Step 4: Review */}
                    {currentStep === 'review' && (
                        <div className="space-y-4">
                            <div className="bg-gray-50 border border-gray-200 rounded-lg p-4 space-y-3">
                                <div>
                                    <h4 className="font-semibold text-gray-700 mb-1">Program</h4>
                                    <p className="text-gray-900">{selectedProgram?.name} ({selectedProgram?.code})</p>
                                </div>
                                <div>
                                    <h4 className="font-semibold text-gray-700 mb-1">Batch</h4>
                                    <p className="text-gray-900">
                                        {formData.joining_year}-{formData.joining_year! + selectedProgram!.duration_years}
                                    </p>
                                </div>
                                <div>
                                    <h4 className="font-semibold text-gray-700 mb-1">Regulation</h4>
                                    <p className="text-gray-900">{selectedRegulation?.regulation_name} ({selectedRegulation?.regulation_code})</p>
                                </div>
                                <div className="grid grid-cols-2 gap-3 pt-3 border-t border-gray-300">
                                    <div>
                                        <h4 className="font-semibold text-gray-700 mb-1">Sections/Semester</h4>
                                        <p className="text-gray-900">{formData.sections_per_semester}</p>
                                    </div>
                                    <div>
                                        <h4 className="font-semibold text-gray-700 mb-1">Section Capacity</h4>
                                        <p className="text-gray-900">{formData.section_capacity} students</p>
                                    </div>
                                    <div>
                                        <h4 className="font-semibold text-gray-700 mb-1">Labs/Section</h4>
                                        <p className="text-gray-900">{formData.labs_per_section || 'None'}</p>
                                    </div>
                                    {formData.labs_per_section! > 0 && (
                                        <div>
                                            <h4 className="font-semibold text-gray-700 mb-1">Lab Capacity</h4>
                                            <p className="text-gray-900">{formData.lab_capacity} students</p>
                                        </div>
                                    )}
                                </div>
                            </div>

                            {stats && (
                                <div className="bg-blue-50 border-2 border-blue-400 rounded-lg p-4">
                                    <h4 className="font-semibold text-blue-900 mb-2 flex items-center">
                                        <span className="text-2xl mr-2">🚀</span>
                                        Ready to Create
                                    </h4>
                                    <p className="text-blue-800 text-sm">
                                        This will create <span className="font-bold">{stats.years} years</span>,{' '}
                                        <span className="font-bold">{stats.semesters} semesters</span>,{' '}
                                        <span className="font-bold">{stats.sections} sections</span>, and{' '}
                                        <span className="font-bold">{stats.labs} lab groups</span> in a single operation.
                                    </p>
                                    <p className="text-blue-700 text-sm mt-2 font-medium">
                                        Total: {stats.years + stats.semesters + stats.sections + stats.labs} records will be created!
                                    </p>
                                </div>
                            )}
                        </div>
                    )}

                    {/* Navigation Buttons */}
                    <div className="flex justify-between pt-6 border-t">
                        <Button
                            variant="outline"
                            onClick={handleBack}
                            disabled={currentStep === 'program' || loading}
                        >
                            Back
                        </Button>

                        {currentStep !== 'review' ? (
                            <Button onClick={handleNext} className="bg-blue-600 hover:bg-blue-700">
                                Next
                            </Button>
                        ) : (
                            <Button
                                onClick={handleSubmit}
                                disabled={loading}
                                className="bg-green-600 hover:bg-green-700"
                            >
                                {loading ? 'Creating...' : 'Create Batch'}
                            </Button>
                        )}
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
