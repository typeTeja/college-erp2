'use client';

import { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Checkbox } from '@/components/ui/checkbox';
import { Badge } from '@/components/ui/badge';
import { Copy, CheckCircle2, AlertCircle } from 'lucide-react';
import { toast } from 'sonner';
import { batchCloningService } from '@/utils/batch-cloning-service';
import type { BatchCloneRequest, BatchCloneResponse } from '@/types/batch-cloning';
import type { Regulation } from '@/types/regulation';

interface BatchCloneDialogProps {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    sourceBatchId: number;
    sourceBatchCode: string;
    sourceBatchName: string;
    programId: number;
    regulations: Regulation[];
    onSuccess?: () => void;
}

export function BatchCloneDialog({
    open,
    onOpenChange,
    sourceBatchId,
    sourceBatchCode,
    sourceBatchName,
    programId,
    regulations,
    onSuccess
}: BatchCloneDialogProps) {
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<BatchCloneResponse | null>(null);

    // Form state
    const [newJoiningYear, setNewJoiningYear] = useState(new Date().getFullYear() + 1);
    const [selectedRegulationId, setSelectedRegulationId] = useState<number | null>(null);
    const [cloneFaculty, setCloneFaculty] = useState(false);
    const [sectionMultiplier, setSectionMultiplier] = useState(1.0);
    const [labMultiplier, setLabMultiplier] = useState(1.0);
    const [customName, setCustomName] = useState('');

    // Filter regulations for this program
    const programRegulations = regulations.filter(r => r.program_id === programId);

    useEffect(() => {
        if (programRegulations.length > 0 && !selectedRegulationId) {
            setSelectedRegulationId(programRegulations[0].id);
        }
    }, [programRegulations]);

    const handleClone = async () => {
        if (!selectedRegulationId) {
            toast.error('Please select a regulation');
            return;
        }

        setLoading(true);
        try {
            const request: BatchCloneRequest = {
                new_joining_year: newJoiningYear,
                new_regulation_id: selectedRegulationId,
                clone_options: {
                    clone_faculty_assignments: cloneFaculty,
                    section_capacity_multiplier: sectionMultiplier,
                    lab_capacity_multiplier: labMultiplier,
                    custom_batch_name: customName || undefined
                }
            };

            const response = await batchCloningService.cloneBatch(sourceBatchId, request);
            setResult(response);

            toast.success(
                <div>
                    <div className="font-semibold">Batch Cloned Successfully!</div>
                    <div className="text-sm mt-1">{response.message}</div>
                </div>
            );

            if (onSuccess) {
                onSuccess();
            }
        } catch (error: any) {
            toast.error(error.response?.data?.detail || 'Failed to clone batch');
        } finally {
            setLoading(false);
        }
    };

    const handleClose = () => {
        setResult(null);
        onOpenChange(false);
    };

    return (
        <Dialog open={open} onOpenChange={handleClose}>
            <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                    <DialogTitle className="flex items-center gap-2">
                        <Copy className="h-5 w-5" />
                        Clone Batch Structure
                    </DialogTitle>
                    <DialogDescription>
                        Clone {sourceBatchName} ({sourceBatchCode}) for a new academic year
                    </DialogDescription>
                </DialogHeader>

                {!result ? (
                    <div className="space-y-6">
                        {/* Source Info */}
                        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                            <h4 className="font-semibold text-blue-900 mb-2">Source Batch</h4>
                            <p className="text-sm text-blue-700">
                                {sourceBatchName} ({sourceBatchCode})
                            </p>
                        </div>

                        {/* New Year */}
                        <div>
                            <Label htmlFor="year">New Joining Year *</Label>
                            <Input
                                id="year"
                                type="number"
                                min={2020}
                                max={2100}
                                value={newJoiningYear}
                                onChange={(e) => setNewJoiningYear(parseInt(e.target.value))}
                                className="mt-1"
                            />
                        </div>

                        {/* Regulation */}
                        <div>
                            <Label htmlFor="regulation">Regulation *</Label>
                            <select
                                id="regulation"
                                className="w-full mt-1 px-3 py-2 border border-gray-300 rounded-md"
                                value={selectedRegulationId || ''}
                                onChange={(e) => setSelectedRegulationId(parseInt(e.target.value))}
                            >
                                {programRegulations.map((reg) => (
                                    <option key={reg.id} value={reg.id}>
                                        {reg.name}
                                    </option>
                                ))}
                            </select>
                        </div>

                        {/* Custom Name */}
                        <div>
                            <Label htmlFor="customName">Custom Batch Name (Optional)</Label>
                            <Input
                                id="customName"
                                type="text"
                                placeholder="Leave empty for auto-generated name"
                                value={customName}
                                onChange={(e) => setCustomName(e.target.value)}
                                className="mt-1"
                            />
                        </div>

                        {/* Clone Options */}
                        <div className="space-y-4 border-t pt-4">
                            <h4 className="font-semibold">Clone Options</h4>

                            <div className="flex items-center space-x-2">
                                <Checkbox
                                    id="faculty"
                                    checked={cloneFaculty}
                                    onCheckedChange={(checked) => setCloneFaculty(checked as boolean)}
                                />
                                <Label htmlFor="faculty" className="cursor-pointer">
                                    Clone faculty assignments to sections
                                </Label>
                            </div>

                            <div>
                                <Label htmlFor="sectionMult">
                                    Section Capacity Multiplier: {sectionMultiplier}x
                                </Label>
                                <input
                                    id="sectionMult"
                                    type="range"
                                    min="0.5"
                                    max="2.0"
                                    step="0.1"
                                    value={sectionMultiplier}
                                    onChange={(e) => setSectionMultiplier(parseFloat(e.target.value))}
                                    className="w-full mt-1"
                                />
                                <p className="text-xs text-gray-500 mt-1">
                                    Adjust section capacities (0.5x to 2.0x)
                                </p>
                            </div>

                            <div>
                                <Label htmlFor="labMult">
                                    Lab Capacity Multiplier: {labMultiplier}x
                                </Label>
                                <input
                                    id="labMult"
                                    type="range"
                                    min="0.5"
                                    max="2.0"
                                    step="0.1"
                                    value={labMultiplier}
                                    onChange={(e) => setLabMultiplier(parseFloat(e.target.value))}
                                    className="w-full mt-1"
                                />
                                <p className="text-xs text-gray-500 mt-1">
                                    Adjust lab capacities (0.5x to 2.0x)
                                </p>
                            </div>
                        </div>

                        {/* Warning */}
                        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                            <div className="flex items-start gap-2">
                                <AlertCircle className="h-5 w-5 text-yellow-600 mt-0.5" />
                                <div className="text-sm text-yellow-800">
                                    <strong>Note:</strong> This will clone the structure only.
                                    Students, attendance, and grades will NOT be copied.
                                </div>
                            </div>
                        </div>

                        {/* Actions */}
                        <div className="flex justify-end gap-3 pt-4 border-t">
                            <Button variant="outline" onClick={handleClose}>
                                Cancel
                            </Button>
                            <Button
                                onClick={handleClone}
                                disabled={loading || !selectedRegulationId}
                                className="bg-blue-600 hover:bg-blue-700"
                            >
                                <Copy className="h-4 w-4 mr-2" />
                                {loading ? 'Cloning...' : 'Clone Batch'}
                            </Button>
                        </div>
                    </div>
                ) : (
                    /* Success Result */
                    <div className="space-y-4">
                        <div className="bg-green-50 border border-green-200 rounded-lg p-6 text-center">
                            <CheckCircle2 className="h-12 w-12 text-green-600 mx-auto mb-3" />
                            <h3 className="text-lg font-semibold text-green-900 mb-2">
                                Batch Cloned Successfully!
                            </h3>
                            <p className="text-green-700">{result.message}</p>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div className="bg-white border rounded-lg p-4">
                                <div className="text-2xl font-bold text-blue-600">
                                    {result.sections_created}
                                </div>
                                <div className="text-sm text-gray-600">Sections Created</div>
                            </div>
                            <div className="bg-white border rounded-lg p-4">
                                <div className="text-2xl font-bold text-purple-600">
                                    {result.labs_created}
                                </div>
                                <div className="text-sm text-gray-600">Labs Created</div>
                            </div>
                        </div>

                        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                            <h4 className="font-semibold text-blue-900 mb-2">New Batch</h4>
                            <p className="text-sm text-blue-700">
                                {result.batch_name} ({result.batch_code})
                            </p>
                        </div>

                        <div className="flex justify-end">
                            <Button onClick={handleClose}>
                                Done
                            </Button>
                        </div>
                    </div>
                )}
            </DialogContent>
        </Dialog>
    );
}
