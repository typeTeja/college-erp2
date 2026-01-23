import { z } from 'zod';

/**
 * Environment Variable Validation
 * 
 * This module validates all environment variables at module load time.
 * Validation is lenient during builds to allow development builds.
 * Strict validation happens via validate-env.js script before production builds.
 */

// Define schema - all optional to allow development builds
const envSchema = z.object({
    NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
    NEXT_PUBLIC_API_URL_DEV: z.string().url().optional(),
    NEXT_PUBLIC_API_URL_PROD: z.string().url().optional(),
});

// Validate at module load time (fails fast on schema errors only)
const rawEnv = {
    NODE_ENV: process.env.NODE_ENV,
    NEXT_PUBLIC_API_URL_DEV: process.env.NEXT_PUBLIC_API_URL_DEV,
    NEXT_PUBLIC_API_URL_PROD: process.env.NEXT_PUBLIC_API_URL_PROD,
};

const parsed = envSchema.safeParse(rawEnv);

if (!parsed.success) {
    console.error('❌ Invalid environment variables:');
    console.error(JSON.stringify(parsed.error.format(), null, 2));
    throw new Error('Environment validation failed - check console for details');
}

export const env = parsed.data;

/**
 * Get the API base URL based on current environment
 * 
 * @returns API URL for the current environment
 */
export const getApiUrl = (): string => {
    const isProd = env.NODE_ENV === 'production';

    if (isProd) {
        // In production, use PROD URL if available, otherwise fall back to DEV
        // Actual validation happens in validate-env.js before deployment
        return env.NEXT_PUBLIC_API_URL_PROD || env.NEXT_PUBLIC_API_URL_DEV || 'http://localhost:8000';
    }

    // Development: use DEV URL or localhost
    return env.NEXT_PUBLIC_API_URL_DEV || 'http://localhost:8000';
};

// Log configuration in development (server-side only)
if (env.NODE_ENV === 'development' && typeof window === 'undefined') {
    console.log('🔧 Environment Configuration:');
    console.log(`   NODE_ENV: ${env.NODE_ENV}`);
    console.log(`   API URL: ${getApiUrl()}`);
}
