'use client';

import { useEffect, useState } from 'react';
import { BulkSetupWizard } from '@/components/academics/BulkSetupWizard';
import { Program } from '@/types/program';
import { Regulation } from '@/types/regulation';
import { api } from '@/utils/api';
import { toast } from 'sonner';

export default function BulkSetupPage() {
    const [programs, setPrograms] = useState<Program[]>([]);
    const [regulations, setRegulations] = useState<Regulation[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [programsRes, regulationsRes] = await Promise.all([
                    api.get<Program[]>('/master/programs-list'),
                    api.get<Regulation[]>('/regulations/'),
                ]);

                setPrograms(programsRes.data);
                setRegulations(regulationsRes.data);
            } catch (error) {
                toast.error('Failed to load programs and regulations');
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                    <p className="mt-4 text-gray-600">Loading...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-6xl mx-auto px-4">
                <div className="mb-8">
                    <h1 className="text-3xl font-bold text-gray-900">One-Click Batch Setup</h1>
                    <p className="text-gray-600 mt-2">
                        Create an entire academic structure in minutes. Set up years, semesters, sections, and lab groups all at once.
                    </p>
                </div>

                <BulkSetupWizard programs={programs} regulations={regulations} />
            </div>
        </div>
    );
}
