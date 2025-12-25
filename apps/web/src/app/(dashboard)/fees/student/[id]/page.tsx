'use client';

import { FeeDashboard } from '@/components/fees/FeeDashboard';
import { useParams } from 'next/navigation';

export default function StudentFeePage() {
    const params = useParams();
    const studentId = parseInt(params.id as string);

    return (
        <FeeDashboard studentId={studentId} />
    );
}
