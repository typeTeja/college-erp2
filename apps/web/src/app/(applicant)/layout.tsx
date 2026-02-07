'use client';

import { ApplicantLayout } from '@/components/layout/ApplicantLayout';

export default function Layout({ children }: { children: React.ReactNode }) {
    return <ApplicantLayout>{children}</ApplicantLayout>;
}
