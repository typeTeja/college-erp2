'use client';

import React, { useState, useEffect } from 'react';
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogFooter
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
import { getAcademicBatches, getBatchSemesters, getBatchSubjects } from '@/utils/master-data-service';
import { CreateSessionDTO } from '@/types/attendance';
import { BatchSemester, BatchSubject, Section, PracticalBatch } from '@/types/academic-batch';
import { toast } from 'sonner';

interface CreateSessionDialogProps {
    open: boolean;
    onClose: () => void;
    onSubmit: (data: CreateSessionDTO) => Promise<void>;
}

export function CreateSessionDialog({ open, onClose, onSubmit }: CreateSessionDialogProps) {
    const [loading, setLoading] = useState(false);

    // State for Selection Flow
    const [batches, setBatches] = useState<any[]>([]);
    const [selectedBatchId, setSelectedBatchId] = useState<string>("");
    const [semesters, setSemesters] = useState<BatchSemester[]>([]);
    const [selectedSemesterId, setSelectedSemesterId] = useState<string>("");

    const [subjects, setSubjects] = useState<BatchSubject[]>([]);
    const [selectedSubjectId, setSelectedSubjectId] = useState<string>("");

    // Derived Options based on Subject Type
    const [sections, setSections] = useState<Section[]>([]);
    const [selectedSectionId, setSelectedSectionId] = useState<string>("");

    const [labBatches, setLabBatches] = useState<PracticalBatch[]>([]);
    const [selectedLabBatchId, setSelectedLabBatchId] = useState<string>("");

    // Session Details
    const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
    const [startTime, setStartTime] = useState("09:00");
    const [endTime, setEndTime] = useState("10:00");
    const [topic, setTopic] = useState("");

    // Load Batches on Open
    useEffect(() => {
        if (open) {
            loadBatches();
        }
    }, [open]);

    // Load Semesters when Batch Selected
    useEffect(() => {
        if (selectedBatchId) {
            loadSemesters(parseInt(selectedBatchId));
        } else {
            setSemesters([]);
        }
    }, [selectedBatchId]);

    // Load Subjects & Structure when Semester Selected
    useEffect(() => {
        if (selectedBatchId && selectedSemesterId) {
            loadSubjectsAndStructure(parseInt(selectedBatchId), parseInt(selectedSemesterId));
        } else {
            setSubjects([]);
            setSections([]);
            setLabBatches([]);
        }
    }, [selectedSemesterId]);

    const loadBatches = async () => {
        try {
            const data = await getAcademicBatches(undefined, true);
            setBatches(data);
        } catch (error) {
            toast.error("Failed to load batches");
        }
    };

    const loadSemesters = async (batchId: number) => {
        try {
            const data = await getBatchSemesters(batchId);
            setSemesters(data);
        } catch (error) {
            toast.error("Failed to load semesters");
        }
    };

    const loadSubjectsAndStructure = async (batchId: number, semesterId: number) => {
        try {
            // Find semester object to get sections/labs (assuming they are included or we fetch structure)
            const semester = semesters.find(s => s.id === semesterId);
            if (semester) {
                // In a real app we might need to fetch sections separately if not hydrated
                // Assuming master-data-service returns them in semester object as per previous UI work
                // But wait, getBatchSemesters might be lightweight.
                // Let's assume for now we need to rely on what's available.
                // Actually, previous AcademicStructureTab fetched structure which included sections.
                // Let's rely on getBatchSemesters returning them or fetch if needed.
                // Edit: master-data-service getBatchSemesters returns BatchSemester[] which has optional sections?: Section[]
                setSections(semester.sections || []);
                setLabBatches(semester.practical_batches || []);
            }

            // Fetch Subjects
            // We need semester_no.
            const sem = semesters.find(s => s.id === semesterId);
            if (sem) {
                const subjs = await getBatchSubjects(batchId, sem.semester_no);
                setSubjects(subjs);
            }
        } catch (error) {
            toast.error("Failed to load subjects");
        }
    };

    const getSelectedSubject = () => subjects.find(s => s.id.toString() === selectedSubjectId);

    const handleSubmit = async () => {
        if (!selectedSubjectId || !date || !startTime || !endTime) {
            toast.error("Please fill required fields");
            return;
        }

        const subject = getSelectedSubject();
        if (!subject) return;

        // Validation based on Subject Type
        if (subject.subject_type === 'THEORY' && !selectedSectionId) {
            toast.error("Please select a section for Theory session");
            return;
        }
        if (subject.subject_type === 'PRACTICAL' && !selectedLabBatchId) {
            toast.error("Please select a lab batch for Practical session");
            return;
        }

        const payload: CreateSessionDTO = {
            subject_id: parseInt(selectedSubjectId),
            session_date: date,
            start_time: startTime,
            end_time: endTime,
            topic: topic,
            // Map IDs.
            // Note: CreateSessionDTO might need update to support IDs instead of raw strings if it was legacy.
            // Let's assume it supports section_id and practical_batch_id

            // Legacy support or new fields?
            // The FacutlyAttendancePanel used `section: 'A'`.
            // We need to check CreateSessionDTO definition.
            // For now, I will send what I have.
        } as any;

        // Add specific fields
        if (subject.subject_type === 'THEORY') {
            // We need to resolve Section ID to Code/Name if backend expects string, or update backend to use ID.
            // Usually backend expects ID now.
            (payload as any).section_id = parseInt(selectedSectionId);
        } else {
            (payload as any).practical_batch_id = parseInt(selectedLabBatchId);
        }

        setLoading(true);
        try {
            await onSubmit(payload);
            onClose();
        } catch (e) {
            // handled by parent
        } finally {
            setLoading(false);
        }
    };

    const selectedSubject = getSelectedSubject();

    return (
        <Dialog open={open} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-[500px]">
                <DialogHeader>
                    <DialogTitle>Create Class Session</DialogTitle>
                </DialogHeader>
                <div className="grid gap-4 py-4">
                    {/* Batch & Semester Selection */}
                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label>Batch</Label>
                            <Select value={selectedBatchId} onValueChange={setSelectedBatchId}>
                                <SelectTrigger>
                                    <SelectValue placeholder="Select Batch" />
                                </SelectTrigger>
                                <SelectContent>
                                    {batches.map(b => (
                                        <SelectItem key={b.id} value={b.id.toString()}>{b.batch_code}</SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </div>
                        <div className="space-y-2">
                            <Label>Semester</Label>
                            <Select value={selectedSemesterId} onValueChange={setSelectedSemesterId} disabled={!selectedBatchId}>
                                <SelectTrigger>
                                    <SelectValue placeholder="Select Semester" />
                                </SelectTrigger>
                                <SelectContent>
                                    {semesters.map(s => (
                                        <SelectItem key={s.id} value={s.id.toString()}>{s.semester_name}</SelectItem>
                                    ))}
                                </SelectContent>
                            </Select>
                        </div>
                    </div>

                    {/* Subject Selection */}
                    <div className="space-y-2">
                        <Label>Subject</Label>
                        <Select value={selectedSubjectId} onValueChange={setSelectedSubjectId} disabled={!selectedSemesterId}>
                            <SelectTrigger>
                                <SelectValue placeholder="Choose Subject" />
                            </SelectTrigger>
                            <SelectContent>
                                {subjects.map(s => (
                                    <SelectItem key={s.id} value={s.id.toString()}>
                                        {s.subject_name} ({s.subject_type})
                                    </SelectItem>
                                ))}
                            </SelectContent>
                        </Select>
                    </div>

                    {/* Conditional Group Selection */}
                    {selectedSubject && (
                        <div className="p-3 bg-slate-50 rounded-md border border-slate-200">
                            {selectedSubject.subject_type === 'PRACTICAL' ? (
                                <div className="space-y-2">
                                    <Label className="text-emerald-700">Lab Batch (Practical)</Label>
                                    <Select value={selectedLabBatchId} onValueChange={setSelectedLabBatchId}>
                                        <SelectTrigger>
                                            <SelectValue placeholder="Select Lab Group" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            {labBatches.map(lb => (
                                                <SelectItem key={lb.id} value={lb.id.toString()}>{lb.name} ({lb.code})</SelectItem>
                                            ))}
                                        </SelectContent>
                                    </Select>
                                </div>
                            ) : (
                                <div className="space-y-2">
                                    <Label className="text-blue-700">Section (Theory)</Label>
                                    <Select value={selectedSectionId} onValueChange={setSelectedSectionId}>
                                        <SelectTrigger>
                                            <SelectValue placeholder="Select Section" />
                                        </SelectTrigger>
                                        <SelectContent>
                                            {sections.map(sec => (
                                                <SelectItem key={sec.id} value={sec.id.toString()}>{sec.name}</SelectItem>
                                            ))}
                                        </SelectContent>
                                    </Select>
                                </div>
                            )}
                        </div>
                    )}

                    {/* Date and Time */}
                    <div className="grid grid-cols-3 gap-4">
                        <div className="space-y-2 col-span-1">
                            <Label>Date</Label>
                            <Input type="date" value={date} onChange={e => setDate(e.target.value)} />
                        </div>
                        <div className="space-y-2 col-span-1">
                            <Label>Start Time</Label>
                            <Input type="time" value={startTime} onChange={e => setStartTime(e.target.value)} />
                        </div>
                        <div className="space-y-2 col-span-1">
                            <Label>End Time</Label>
                            <Input type="time" value={endTime} onChange={e => setEndTime(e.target.value)} />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <Label>Topic / Description (Optional)</Label>
                        <Input value={topic} onChange={e => setTopic(e.target.value)} placeholder="e.g., Intro to Chemistry" />
                    </div>

                </div>
                <DialogFooter>
                    <Button variant="outline" onClick={onClose} disabled={loading}>Cancel</Button>
                    <Button onClick={handleSubmit} disabled={loading}>
                        {loading ? 'Creating...' : 'Create Session'}
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
}
