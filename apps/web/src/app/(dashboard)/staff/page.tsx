"use client"

import React, { useState } from 'react';
import { DashboardShell } from '@/components/dashboard/DashboardShell';
import { WidgetCard } from '@/components/dashboard/widgets/WidgetCard';
import { Card, CardContent } from '@/components/ui/card';
import { useAuthStore } from '@/store/use-auth-store';
import { 
    BookOpen, Home, DollarSign, Phone,
    AlertCircle, TrendingUp, Users, Clock 
} from 'lucide-react';

/**
 * Staff Dashboard
 * 
 * Purpose: Role-specific operational widgets (Staff view)
 * Audience: Non-teaching staff (Librarian, Warden, Accounts, SSE)
 * Time Horizon: Today / This Week
 * 
 * Configurable Widgets Based on Role:
 * - Librarian: Books, Returns, Stock
 * - Warden: Occupancy, Gate Passes, Complaints
 * - Accounts: Collections, Dues, Payments
 * - SSE: Attendance Risks, Calls, Follow-ups
 * 
 * Mental Model: Operational Dashboard, not Admin Panel
 */
export default function StaffDashboard() {
    const { user, hasHydrated } = useAuthStore();
    const [selectedRole, setSelectedRole] = useState<'librarian' | 'warden' | 'accounts' | 'sse'>('librarian');

    // Check if user is staff
    const isStaff = !!user?.roles.some(r => 
        ['LIBRARIAN', 'WARDEN', 'ACCOUNTS', 'SSE', 'STAFF'].includes(r)
    );

    if (!hasHydrated) {
        return <div className="p-6 bg-slate-50 animate-pulse h-screen rounded-xl" />;
    }

    if (!isStaff) {
        return (
            <div className="p-6">
                <Card>
                    <CardContent className="pt-6">
                        <p className="text-sm text-slate-500">
                            You do not have permission to view the Staff Dashboard.
                        </p>
                    </CardContent>
                </Card>
            </div>
        );
    }

    return (
        <DashboardShell
            title="Staff Dashboard"
            subtitle="Manage your daily operations and tasks"
            role="Staff"
        >
            {/* Role Selector */}
            <Card className="mb-6">
                <CardContent className="pt-6">
                    <div className="flex items-center gap-4">
                        <span className="text-sm font-medium text-slate-700">View as:</span>
                        <div className="flex gap-2">
                            <RoleButton 
                                role="librarian" 
                                label="Librarian" 
                                icon={<BookOpen className="h-4 w-4" />}
                                active={selectedRole === 'librarian'}
                                onClick={() => setSelectedRole('librarian')}
                            />
                            <RoleButton 
                                role="warden" 
                                label="Warden" 
                                icon={<Home className="h-4 w-4" />}
                                active={selectedRole === 'warden'}
                                onClick={() => setSelectedRole('warden')}
                            />
                            <RoleButton 
                                role="accounts" 
                                label="Accounts" 
                                icon={<DollarSign className="h-4 w-4" />}
                                active={selectedRole === 'accounts'}
                                onClick={() => setSelectedRole('accounts')}
                            />
                            <RoleButton 
                                role="sse" 
                                label="SSE" 
                                icon={<Phone className="h-4 w-4" />}
                                active={selectedRole === 'sse'}
                                onClick={() => setSelectedRole('sse')}
                            />
                        </div>
                    </div>
                </CardContent>
            </Card>

            {/* Render role-specific widgets */}
            {selectedRole === 'librarian' && <LibrarianWidgets />}
            {selectedRole === 'warden' && <WardenWidgets />}
            {selectedRole === 'accounts' && <AccountsWidgets />}
            {selectedRole === 'sse' && <SSEWidgets />}
        </DashboardShell>
    );
}

// Librarian Widgets
function LibrarianWidgets() {
    return (
        <>
            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <MetricCard title="Books Issued Today" value="24" color="blue" />
                <MetricCard title="Overdue Books" value="15" color="red" />
                <MetricCard title="New Arrivals" value="8" color="green" />
                <MetricCard title="Pending Returns" value="32" color="yellow" />
            </div>

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <WidgetCard title="Overdue Books" description="Books pending return">
                    <div className="space-y-2">
                        <OverdueItem student="Rajesh Kumar" book="Data Structures" daysOverdue={5} />
                        <OverdueItem student="Priya Sharma" book="Operating Systems" daysOverdue={12} />
                        <OverdueItem student="Amit Patel" book="Computer Networks" daysOverdue={3} />
                    </div>
                </WidgetCard>

                <WidgetCard title="Stock Alerts" description="Low stock items">
                    <div className="space-y-2">
                        <StockItem book="Introduction to Algorithms" current={2} minimum={5} />
                        <StockItem book="Database Systems" current={1} minimum={5} />
                        <StockItem book="Computer Architecture" current={3} minimum={5} />
                    </div>
                </WidgetCard>
            </div>
        </>
    );
}

// Warden Widgets
function WardenWidgets() {
    return (
        <>
            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <MetricCard title="Hostel Occupancy" value="92%" color="blue" />
                <MetricCard title="Gate Passes Today" value="18" color="green" />
                <MetricCard title="Pending Fines" value="₹12,500" color="red" />
                <MetricCard title="Open Complaints" value="5" color="yellow" />
            </div>

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <WidgetCard title="Occupancy Chart" description="Room-wise occupancy">
                    <div className="space-y-3">
                        <OccupancyBar block="Block A" occupied={45} total={50} />
                        <OccupancyBar block="Block B" occupied={48} total={50} />
                        <OccupancyBar block="Block C" occupied={42} total={50} />
                    </div>
                </WidgetCard>

                <WidgetCard title="Gate Pass Requests" description="Today's requests">
                    <div className="space-y-2">
                        <GatePassItem student="Rajesh Kumar" time="6:00 PM" reason="Medical" status="approved" />
                        <GatePassItem student="Priya Sharma" time="5:30 PM" reason="Family" status="pending" />
                        <GatePassItem student="Amit Patel" time="7:00 PM" reason="Personal" status="approved" />
                    </div>
                </WidgetCard>
            </div>
        </>
    );
}

// Accounts Widgets
function AccountsWidgets() {
    return (
        <>
            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <MetricCard title="Collections Today" value="₹2.5L" color="green" />
                <MetricCard title="Pending Dues" value="₹8.2L" color="red" />
                <MetricCard title="Failed Payments" value="12" color="yellow" />
                <MetricCard title="Concession Requests" value="8" color="blue" />
            </div>

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <WidgetCard title="Collection Summary" description="Today's fee collections">
                    <div className="space-y-3">
                        <CollectionBar category="Tuition Fee" amount={150000} total={200000} />
                        <CollectionBar category="Hostel Fee" amount={80000} total={100000} />
                        <CollectionBar category="Exam Fee" amount={20000} total={50000} />
                    </div>
                </WidgetCard>

                <WidgetCard title="Pending Dues" description="Students with outstanding payments">
                    <div className="space-y-2">
                        <DuesItem student="Rajesh Kumar" amount={25000} dueDate="10 Feb 2026" />
                        <DuesItem student="Priya Sharma" amount={15000} dueDate="5 Feb 2026" />
                        <DuesItem student="Amit Patel" amount={30000} dueDate="15 Feb 2026" />
                    </div>
                </WidgetCard>
            </div>
        </>
    );
}

// SSE Widgets
function SSEWidgets() {
    return (
        <>
            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <MetricCard title="Attendance Risks" value="23" color="red" />
                <MetricCard title="Calls Pending" value="15" color="yellow" />
                <MetricCard title="Follow-ups Due" value="8" color="blue" />
                <MetricCard title="Issues Raised" value="5" color="green" />
            </div>

            {/* Main Content Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <WidgetCard title="Attendance Risk List" description="Students below 75% attendance">
                    <div className="space-y-2">
                        <RiskItem student="Rajesh Kumar" attendance={72} lastContact="2 days ago" />
                        <RiskItem student="Priya Sharma" attendance={68} lastContact="5 days ago" />
                        <RiskItem student="Amit Patel" attendance={71} lastContact="1 day ago" />
                    </div>
                </WidgetCard>

                <WidgetCard title="Calls Pending" description="Parent calls to be made">
                    <div className="space-y-2">
                        <CallItem student="Rajesh Kumar" reason="Low Attendance" priority="high" />
                        <CallItem student="Priya Sharma" reason="Fee Pending" priority="medium" />
                        <CallItem student="Amit Patel" reason="Disciplinary" priority="high" />
                    </div>
                </WidgetCard>
            </div>
        </>
    );
}

// Helper Components

function RoleButton({ role, label, icon, active, onClick }: {
    role: string;
    label: string;
    icon: React.ReactNode;
    active: boolean;
    onClick: () => void;
}) {
    return (
        <button
            onClick={onClick}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                active 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}
        >
            {icon}
            {label}
        </button>
    );
}

function MetricCard({ title, value, color }: {
    title: string;
    value: string;
    color: 'blue' | 'yellow' | 'red' | 'green';
}) {
    const colors = {
        blue: 'text-blue-600',
        yellow: 'text-yellow-600',
        red: 'text-red-600',
        green: 'text-green-600'
    };
    
    return (
        <Card>
            <CardContent className="pt-6">
                <p className="text-sm text-slate-600">{title}</p>
                <p className={`text-2xl font-bold mt-1 ${colors[color]}`}>{value}</p>
            </CardContent>
        </Card>
    );
}

function OverdueItem({ student, book, daysOverdue }: {
    student: string;
    book: string;
    daysOverdue: number;
}) {
    return (
        <div className="flex items-center justify-between py-2 border-b last:border-0">
            <div>
                <p className="text-sm font-medium text-slate-900">{student}</p>
                <p className="text-xs text-slate-500">{book}</p>
            </div>
            <span className="text-xs px-2 py-1 rounded-full bg-red-100 text-red-700">
                {daysOverdue} days overdue
            </span>
        </div>
    );
}

function StockItem({ book, current, minimum }: {
    book: string;
    current: number;
    minimum: number;
}) {
    return (
        <div className="flex items-center justify-between py-2 border-b last:border-0">
            <p className="text-sm font-medium text-slate-900">{book}</p>
            <div className="text-right">
                <p className="text-sm font-semibold text-red-600">{current} / {minimum}</p>
                <p className="text-xs text-slate-500">In stock</p>
            </div>
        </div>
    );
}

function OccupancyBar({ block, occupied, total }: {
    block: string;
    occupied: number;
    total: number;
}) {
    const percentage = (occupied / total) * 100;
    
    return (
        <div>
            <div className="flex justify-between text-sm mb-1">
                <span className="text-slate-700">{block}</span>
                <span className="font-medium">{occupied}/{total} rooms</span>
            </div>
            <div className="w-full bg-slate-200 rounded-full h-2">
                <div 
                    className="bg-blue-600 h-2 rounded-full" 
                    style={{ width: `${percentage}%` }} 
                />
            </div>
        </div>
    );
}

function GatePassItem({ student, time, reason, status }: {
    student: string;
    time: string;
    reason: string;
    status: 'approved' | 'pending' | 'rejected';
}) {
    const colors = {
        approved: 'bg-green-100 text-green-700',
        pending: 'bg-yellow-100 text-yellow-700',
        rejected: 'bg-red-100 text-red-700'
    };
    
    return (
        <div className="flex items-center justify-between py-2 border-b last:border-0">
            <div>
                <p className="text-sm font-medium text-slate-900">{student}</p>
                <p className="text-xs text-slate-500">{time} • {reason}</p>
            </div>
            <span className={`text-xs px-2 py-1 rounded-full ${colors[status]}`}>
                {status.charAt(0).toUpperCase() + status.slice(1)}
            </span>
        </div>
    );
}

function CollectionBar({ category, amount, total }: {
    category: string;
    amount: number;
    total: number;
}) {
    const percentage = (amount / total) * 100;
    
    return (
        <div>
            <div className="flex justify-between text-sm mb-1">
                <span className="text-slate-700">{category}</span>
                <span className="font-medium">₹{(amount/1000).toFixed(0)}K / ₹{(total/1000).toFixed(0)}K</span>
            </div>
            <div className="w-full bg-slate-200 rounded-full h-2">
                <div 
                    className="bg-green-600 h-2 rounded-full" 
                    style={{ width: `${percentage}%` }} 
                />
            </div>
        </div>
    );
}

function DuesItem({ student, amount, dueDate }: {
    student: string;
    amount: number;
    dueDate: string;
}) {
    return (
        <div className="flex items-center justify-between py-2 border-b last:border-0">
            <div>
                <p className="text-sm font-medium text-slate-900">{student}</p>
                <p className="text-xs text-slate-500">Due: {dueDate}</p>
            </div>
            <p className="text-sm font-semibold text-red-600">₹{(amount/1000).toFixed(1)}K</p>
        </div>
    );
}

function RiskItem({ student, attendance, lastContact }: {
    student: string;
    attendance: number;
    lastContact: string;
}) {
    return (
        <div className="flex items-center justify-between py-2 border-b last:border-0">
            <div>
                <p className="text-sm font-medium text-slate-900">{student}</p>
                <p className="text-xs text-slate-500">Last contact: {lastContact}</p>
            </div>
            <p className="text-sm font-semibold text-red-600">{attendance}%</p>
        </div>
    );
}

function CallItem({ student, reason, priority }: {
    student: string;
    reason: string;
    priority: 'high' | 'medium' | 'low';
}) {
    const colors = {
        high: 'bg-red-100 text-red-700',
        medium: 'bg-yellow-100 text-yellow-700',
        low: 'bg-blue-100 text-blue-700'
    };
    
    return (
        <div className="flex items-center justify-between py-2 border-b last:border-0">
            <div>
                <p className="text-sm font-medium text-slate-900">{student}</p>
                <p className="text-xs text-slate-500">{reason}</p>
            </div>
            <span className={`text-xs px-2 py-1 rounded-full ${colors[priority]}`}>
                {priority.charAt(0).toUpperCase() + priority.slice(1)}
            </span>
        </div>
    );
}
