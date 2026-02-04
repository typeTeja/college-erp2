/**
 * Dashboard Type Definitions
 * 
 * Defines TypeScript interfaces for all dashboard data structures.
 * These types ensure type safety across the dashboard API integration.
 */

// ============================================================================
// Common Types
// ============================================================================

export interface DashboardKPI {
  label: string;
  value: number | string;
  change?: number;
  trend?: 'up' | 'down' | 'stable';
}

// ============================================================================
// Principal Dashboard Types
// ============================================================================

export interface PrincipalDashboardData {
  kpis: {
    totalEnrollment: number;
    enrollmentChange: number; // percentage
    feeCollection: number;
    feeCollectionRate: number; // percentage
    attendanceRate: number;
    highRiskStudents: number;
  };
  enrollmentTrends: {
    month: string;
    count: number;
    department: string;
  }[];
  departmentPerformance: {
    department: string;
    students: number;
    attendance: number;
    avgGrade: number;
  }[];
  feeCollectionSummary: {
    category: string;
    collected: number;
    expected: number;
  }[];
  pendingApprovals: {
    type: string;
    count: number;
    urgent: number;
  }[];
  highRiskAlerts: {
    studentId: number;
    studentName: string;
    reason: string;
    severity: 'high' | 'medium' | 'low';
  }[];
}

// ============================================================================
// Parent Dashboard Types
// ============================================================================

export interface ParentDashboardData {
  student: {
    id: number;
    name: string;
    rollNo: string;
    program: string;
    semester: number;
    photo?: string;
  };
  kpis: {
    attendance: number; // percentage
    cgpa: number;
    feeStatus: 'paid' | 'pending' | 'overdue';
    alerts: number;
  };
  attendanceOverview: {
    date: string;
    status: 'present' | 'absent' | 'leave';
  }[];
  academicPerformance: {
    subject: string;
    marks: number;
    total: number;
    grade: string;
  }[];
  feePaymentStatus: {
    category: string;
    amount: number;
    paid: number;
    dueDate: string;
    status: 'paid' | 'pending' | 'overdue';
  }[];
  upcomingEvents: {
    title: string;
    date: string;
    type: 'exam' | 'meeting' | 'event';
  }[];
  teacherMessages: {
    from: string;
    message: string;
    date: string;
  }[];
}

// ============================================================================
// Student Dashboard Types
// ============================================================================

export interface StudentDashboardData {
  kpis: {
    attendance: number; // percentage
    cgpa: number;
    pendingAssignments: number;
    feeStatus: 'paid' | 'pending' | 'overdue';
  };
  todaysTimetable: {
    time: string;
    subject: string;
    faculty: string;
    room: string;
    type: 'lecture' | 'lab' | 'tutorial';
  }[];
  attendanceSummary: {
    subject: string;
    present: number;
    total: number;
    percentage: number;
  }[];
  internalMarks: {
    subject: string;
    test1: number;
    test2: number;
    assignment: number;
    total: number;
  }[];
  assignmentStatus: {
    title: string;
    subject: string;
    dueDate: string;
    status: 'pending' | 'submitted' | 'graded';
    marks?: number;
  }[];
  examSchedule: {
    subject: string;
    date: string;
    time: string;
    room: string;
  }[];
}

// ============================================================================
// Faculty Dashboard Types
// ============================================================================

export interface FacultyDashboardData {
  kpis: {
    classesToday: number;
    pendingAttendance: number;
    assignmentsToGrade: number;
    nextLecture: string;
    nextLectureDetail: string;
  };
  todaysClasses: {
    id: number;
    time: string;
    subject: string;
    room: string;
    batch: string;
    status: 'completed' | 'upcoming' | 'cancelled';
  }[];
  attendancePending: {
    id: number;
    date: string;
    subject: string;
    batch: string;
    period: number;
    status: 'pending';
  }[];
  assignmentsToGrade: {
    id: number;
    title: string;
    subject: string;
    submitted: number;
    total: number;
    dueDate: string;
  }[];
}

// ============================================================================
// Staff Dashboard Types
// ============================================================================

export type StaffRole = 'librarian' | 'warden' | 'accounts' | 'sse';

export interface StaffDashboardData {
  role: StaffRole;
  kpis: Record<string, number | string>;
  widgets: {
    [widgetName: string]: any[];
  };
}

export interface LibrarianDashboardData extends StaffDashboardData {
  role: 'librarian';
  kpis: {
    booksIssuedToday: number;
    overdueBooks: number;
    newArrivals: number;
    pendingReturns: number;
  };
  widgets: {
    overdueBooks: {
      student: string;
      book: string;
      daysOverdue: number;
    }[];
    stockAlerts: {
      book: string;
      current: number;
      minimum: number;
    }[];
  };
}

export interface WardenDashboardData extends StaffDashboardData {
  role: 'warden';
  kpis: {
    hostelOccupancy: string; // percentage as string (e.g., "92%")
    gatePassesToday: number;
    pendingFines: string; // amount as string (e.g., "₹12,500")
    openComplaints: number;
  };
  widgets: {
    occupancyChart: {
      block: string;
      occupied: number;
      total: number;
    }[];
    gatePassRequests: {
      student: string;
      time: string;
      reason: string;
      status: 'approved' | 'pending' | 'rejected';
    }[];
  };
}

export interface AccountsDashboardData extends StaffDashboardData {
  role: 'accounts';
  kpis: {
    collectionsToday: string; // amount as string (e.g., "₹2.5L")
    pendingDues: string; // amount as string (e.g., "₹8.2L")
    failedPayments: number;
    concessionRequests: number;
  };
  widgets: {
    collectionSummary: {
      category: string;
      amount: number;
      total: number;
    }[];
    pendingDues: {
      student: string;
      amount: number;
      dueDate: string;
    }[];
  };
}

export interface SSEDashboardData extends StaffDashboardData {
  role: 'sse';
  kpis: {
    attendanceRisks: number;
    callsPending: number;
    followupsDue: number;
    issuesRaised: number;
  };
  widgets: {
    attendanceRiskList: {
      student: string;
      attendance: number;
      lastContact: string;
    }[];
    callsPending: {
      student: string;
      reason: string;
      priority: 'high' | 'medium' | 'low';
    }[];
  };
}

// Union type for all staff dashboard data
export type AnyStaffDashboardData =
  | LibrarianDashboardData
  | WardenDashboardData
  | AccountsDashboardData
  | SSEDashboardData;
