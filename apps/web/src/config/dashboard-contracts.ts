/**
 * DASHBOARD CONTRACTS - IMMUTABLE
 * 
 * ⚠️ WARNING: These contracts are LOCKED.
 * Dashboards can change DATA, never PURPOSE.
 * 
 * DO NOT:
 * - Add CRUD operations to dashboards
 * - Add configuration to dashboards
 * - Mix role purposes
 * - Add "quick add" buttons
 * - Allow dashboards to grow horizontally
 * 
 * Last Updated: 2026-02-04
 * Next Review: 2027-02-04 (1 year)
 */

export const DASHBOARD_CONTRACTS = {
  PRINCIPAL: {
    purpose: 'Institutional health & risk (Executive)',
    audience: 'Principal / Management',
    timeHorizon: 'Month / Semester / Year',
    allowedWidgets: [
      'enrollment-trends',
      'attendance-compliance',
      'detention-risk',
      'fee-collection-summary',
      'hostel-pl',
      'high-risk-alerts',
      'pending-approvals',
      'department-performance'
    ],
    forbiddenWidgets: [
      'student-crud',
      'daily-operations',
      'staff-workflows',
      'individual-student-lists'
    ],
    mentalModel: 'Boardroom, not Admin Office'
  },
  
  PARENT: {
    purpose: 'Child monitoring & trust (Guardian)',
    audience: 'Parents',
    timeHorizon: 'Today / Semester',
    allowedWidgets: [
      'child-attendance',
      'fee-status',
      'exam-eligibility',
      'notices',
      'issues-raised',
      'gate-pass-activity',
      'grade-report',
      'attendance-calendar',
      'weekly-timetable'
    ],
    forbiddenWidgets: [
      'marks-editing',
      'staff-details',
      'discipline-internals',
      'comparative-analytics',
      'other-students-data'
    ],
    mentalModel: 'Parents should see, not interfere'
  },
  
  ENROLLED_STUDENT: {
    purpose: 'Academic self-management',
    audience: 'Confirmed students',
    timeHorizon: 'Today / Semester',
    allowedWidgets: [
      'todays-timetable',
      'attendance-percentage',
      'internal-marks',
      'assignment-status',
      'exam-eligibility',
      'fee-alerts',
      'notices',
      'library-books',
      'exam-schedule'
    ],
    forbiddenWidgets: [
      'application-steps',
      'admission-documents',
      'payment-gateway',
      'admin-workflows',
      'other-students-data'
    ],
    mentalModel: 'Academic self-service, not admission workflow',
    lifecycleRule: 'Completely separate from ApplicantDashboard'
  },
  
  APPLICANT: {
    purpose: 'Admission funnel conversion',
    audience: 'Prospects & applicants',
    timeHorizon: 'Application lifecycle',
    allowedWidgets: [
      'application-status',
      'payment-retry',
      'document-upload',
      'offer-letter',
      'next-steps',
      'application-timeline',
      'payment-status'
    ],
    forbiddenWidgets: [
      'academic-content',
      'enrolled-student-features',
      'attendance',
      'internal-marks',
      'timetable'
    ],
    mentalModel: 'Conversion funnel, not academic portal',
    lifecycleRule: 'Revoked upon enrollment confirmation'
  },
  
  FACULTY: {
    purpose: 'Teaching execution',
    audience: 'Faculty',
    timeHorizon: 'Today / This week',
    allowedWidgets: [
      'todays-classes',
      'attendance-pending',
      'lesson-plan-lag',
      'practical-evaluation',
      'student-shortage-alerts',
      'leave-substitution',
      'cr-dr-balance',
      'assignments-to-grade'
    ],
    forbiddenWidgets: [
      'admin-metrics',
      'finance-data',
      'settings',
      'institutional-metrics',
      'fee-collection'
    ],
    mentalModel: 'Teaching execution, not administration'
  },
  
  STAFF: {
    purpose: 'Operational responsibility (role-configured)',
    audience: 'Librarian, Warden, Accounts, SSE',
    timeHorizon: 'Today / This week',
    roleConfigs: {
      LIBRARIAN: {
        allowedWidgets: ['issues', 'returns', 'stock-alerts', 'overdue-books', 'new-arrivals'],
        mentalModel: 'Library operations only'
      },
      WARDEN: {
        allowedWidgets: ['occupancy', 'gate-passes', 'fines', 'complaints', 'mess-attendance'],
        mentalModel: 'Hostel operations only'
      },
      ACCOUNTS: {
        allowedWidgets: ['collections', 'dues', 'failures', 'concessions', 'payment-verification'],
        mentalModel: 'Finance operations only'
      },
      SSE: {
        allowedWidgets: ['attendance-risks', 'calls-pending', 'follow-ups', 'issues-raised'],
        mentalModel: 'Student support only'
      }
    },
    forbiddenWidgets: [
      'admin-dashboard-clone',
      'cross-role-data',
      'institutional-metrics'
    ],
    mentalModel: 'Role-specific operations, not generic admin'
  },
  
  SUPER_ADMIN: {
    purpose: 'System health monitoring',
    audience: 'ERP owners',
    timeHorizon: 'Real-time',
    allowedWidgets: [
      'system-errors',
      'job-failures',
      'config-completeness',
      'data-integrity-warnings',
      'api-health',
      'database-status'
    ],
    forbiddenWidgets: [
      'college-operations',
      'academic-data',
      'student-data'
    ],
    mentalModel: 'System health, not college operations'
  }
} as const;

/**
 * Dashboard Immutability Rules
 * These rules are enforced via code review and pre-commit hooks
 */
export const DASHBOARD_RULES = {
  1: 'Dashboards are role contracts - purpose NEVER changes',
  2: 'No CRUD on dashboards - read-only summaries only',
  3: 'No configuration on dashboards',
  4: 'No cross-role widgets',
  5: 'No "quick add" buttons',
  6: 'Dashboards cannot grow horizontally - new features go to modules'
} as const;

/**
 * Lifecycle Rule
 * Each lifecycle stage gets its own dashboard
 */
export const LIFECYCLE_RULE = {
  applicant: 'ApplicantDashboard',
  enrolled: 'EnrolledStudentDashboard',
  alumni: 'AlumniDashboard (future)'
} as const;

/**
 * Validate if a widget is allowed for a specific dashboard
 */
export function validateDashboardWidget(
  dashboard: keyof typeof DASHBOARD_CONTRACTS,
  widget: string
): { allowed: boolean; reason?: string } {
  const contract = DASHBOARD_CONTRACTS[dashboard];
  
  // Check forbidden widgets first
  if (contract.forbiddenWidgets.includes(widget)) {
    return {
      allowed: false,
      reason: `Widget "${widget}" violates ${dashboard} dashboard contract. This widget is explicitly forbidden.`
    };
  }
  
  // For staff dashboard, check role-specific configs
  if (dashboard === 'STAFF' && 'roleConfigs' in contract) {
    // Staff dashboard validation is role-specific
    return { allowed: true }; // Will be validated at runtime based on role
  }
  
  // Check if widget is in allowed list
  if ('allowedWidgets' in contract && !contract.allowedWidgets.includes(widget)) {
    return {
      allowed: false,
      reason: `Widget "${widget}" not in ${dashboard} allowed list. See dashboard-contracts.ts for allowed widgets.`
    };
  }
  
  return { allowed: true };
}

/**
 * Get dashboard contract for a specific role
 */
export function getDashboardContract(role: string): keyof typeof DASHBOARD_CONTRACTS | null {
  const roleMapping: Record<string, keyof typeof DASHBOARD_CONTRACTS> = {
    'PRINCIPAL': 'PRINCIPAL',
    'PARENT': 'PARENT',
    'STUDENT': 'ENROLLED_STUDENT', // Default to enrolled, check lifecycle at runtime
    'FACULTY': 'FACULTY',
    'LIBRARIAN': 'STAFF',
    'WARDEN': 'STAFF',
    'ACCOUNTS': 'STAFF',
    'SSE': 'STAFF',
    'SUPER_ADMIN': 'SUPER_ADMIN',
    'ADMIN': 'SUPER_ADMIN'
  };
  
  return roleMapping[role] || null;
}

/**
 * Check if a role should use staff dashboard
 */
export function isStaffRole(role: string): boolean {
  return ['LIBRARIAN', 'WARDEN', 'ACCOUNTS', 'SSE'].includes(role);
}

/**
 * Get staff role config
 */
export function getStaffRoleConfig(role: string) {
  const staffContract = DASHBOARD_CONTRACTS.STAFF;
  if ('roleConfigs' in staffContract) {
    return staffContract.roleConfigs[role as keyof typeof staffContract.roleConfigs];
  }
  return null;
}

/**
 * Validate dashboard change (for pre-commit hooks)
 */
export function validateDashboardChange(
  dashboard: keyof typeof DASHBOARD_CONTRACTS,
  changes: { addedWidgets?: string[]; removedWidgets?: string[]; modifiedPurpose?: boolean }
): { valid: boolean; errors: string[] } {
  const errors: string[] = [];
  
  // Rule 1: Purpose cannot change
  if (changes.modifiedPurpose) {
    errors.push(`VIOLATION: Dashboard purpose is immutable. Cannot change ${dashboard} purpose.`);
  }
  
  // Rule 2-6: Validate added widgets
  if (changes.addedWidgets) {
    for (const widget of changes.addedWidgets) {
      const validation = validateDashboardWidget(dashboard, widget);
      if (!validation.allowed) {
        errors.push(`VIOLATION: ${validation.reason}`);
      }
      
      // Check for CRUD operations
      if (widget.includes('create') || widget.includes('edit') || widget.includes('delete')) {
        errors.push(`VIOLATION: No CRUD operations on dashboards. Widget "${widget}" appears to be a CRUD operation.`);
      }
      
      // Check for configuration
      if (widget.includes('config') || widget.includes('settings')) {
        errors.push(`VIOLATION: No configuration on dashboards. Widget "${widget}" appears to be configuration.`);
      }
    }
  }
  
  return {
    valid: errors.length === 0,
    errors
  };
}
