'use client';

import { FeeStructureForm } from '@/components/fees/FeeStructureForm';
import { useRouter } from 'next/navigation';
import { ArrowLeft } from 'lucide-react';
import { Button } from '@/components/ui/button';

export default function NewFeeStructurePage() {
    const router = useRouter();

    return (
        <div className="max-w-4xl mx-auto">
            {/* Header */}
            <div className="mb-6">
                <Button
                    variant="outline"
                    onClick={() => router.back()}
                    className="mb-4"
                >
                    <ArrowLeft className="w-4 h-4 mr-2" />
                    Back
                </Button>
                <h1 className="text-3xl font-bold text-gray-800">Create Fee Structure</h1>
                <p className="text-gray-600 mt-2">
                    Define a new fee structure for a program and academic year
                </p>
            </div>

            {/* Form */}
            <FeeStructureForm
                onSuccess={() => {
                    router.push('/fees');
                }}
            />
        </div>
    );
}
