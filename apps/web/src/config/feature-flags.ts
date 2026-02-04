/**
 * Feature Flags Configuration
 * 
 * Controls gradual rollout of frontend architecture changes
 * 
 * Usage:
 * - Set environment variables to enable/disable features
 * - Use ROLLOUT_PERCENTAGE for gradual deployment (0-100)
 * 
 * Example .env.local:
 * NEXT_PUBLIC_NEW_NAV=true
 * NEXT_PUBLIC_PRINCIPAL_DASH=true
 * NEXT_PUBLIC_ROLLOUT_PERCENT=10
 */

export const FEATURE_FLAGS = {
  // Navigation restructure
  NEW_NAVIGATION: process.env.NEXT_PUBLIC_NEW_NAV === 'true',
  NEW_SETTINGS_STRUCTURE: process.env.NEXT_PUBLIC_NEW_SETTINGS === 'true',
  
  // Dashboard rollout (individual toggles for testing)
  PRINCIPAL_DASHBOARD: process.env.NEXT_PUBLIC_PRINCIPAL_DASH === 'true',
  PARENT_DASHBOARD: process.env.NEXT_PUBLIC_PARENT_DASH === 'true',
  ENROLLED_STUDENT_DASHBOARD: process.env.NEXT_PUBLIC_ENROLLED_DASH === 'true',
  STAFF_DASHBOARD: process.env.NEXT_PUBLIC_STAFF_DASH === 'true',
  FACULTY_DASHBOARD_V2: process.env.NEXT_PUBLIC_FACULTY_V2 === 'true',
  
  // Gradual rollout percentage (0-100)
  ROLLOUT_PERCENTAGE: parseInt(process.env.NEXT_PUBLIC_ROLLOUT_PERCENT || '0', 10)
} as const;

/**
 * Check if user is in rollout group
 * Uses simple hash of user ID to determine inclusion
 */
export function isUserInRollout(userId: number, percentage: number): boolean {
  if (percentage === 0) return false;
  if (percentage === 100) return true;
  
  // Simple hash: user ID modulo 100
  const hash = userId % 100;
  return hash < percentage;
}

/**
 * Check if a specific feature is enabled for a user
 */
export function isFeatureEnabled(
  feature: keyof typeof FEATURE_FLAGS,
  userId?: number
): boolean {
  // If feature is explicitly disabled, return false
  if (feature === 'ROLLOUT_PERCENTAGE') {
    return false; // This is not a feature, it's a config value
  }
  
  const flagValue = FEATURE_FLAGS[feature];
  
  // If flag is boolean, return it directly
  if (typeof flagValue === 'boolean') {
    // If enabled and we have rollout percentage, check user inclusion
    if (flagValue && userId && FEATURE_FLAGS.ROLLOUT_PERCENTAGE > 0) {
      return isUserInRollout(userId, FEATURE_FLAGS.ROLLOUT_PERCENTAGE);
    }
    return flagValue;
  }
  
  return false;
}

/**
 * Get rollout status for monitoring
 */
export function getRolloutStatus() {
  return {
    navigation: {
      enabled: FEATURE_FLAGS.NEW_NAVIGATION,
      settingsStructure: FEATURE_FLAGS.NEW_SETTINGS_STRUCTURE
    },
    dashboards: {
      principal: FEATURE_FLAGS.PRINCIPAL_DASHBOARD,
      parent: FEATURE_FLAGS.PARENT_DASHBOARD,
      enrolledStudent: FEATURE_FLAGS.ENROLLED_STUDENT_DASHBOARD,
      staff: FEATURE_FLAGS.STAFF_DASHBOARD,
      facultyV2: FEATURE_FLAGS.FACULTY_DASHBOARD_V2
    },
    rollout: {
      percentage: FEATURE_FLAGS.ROLLOUT_PERCENTAGE,
      stage: 
        FEATURE_FLAGS.ROLLOUT_PERCENTAGE === 0 ? 'disabled' :
        FEATURE_FLAGS.ROLLOUT_PERCENTAGE <= 10 ? 'pilot' :
        FEATURE_FLAGS.ROLLOUT_PERCENTAGE <= 50 ? 'beta' :
        FEATURE_FLAGS.ROLLOUT_PERCENTAGE < 100 ? 'staged' :
        'full'
    }
  };
}
