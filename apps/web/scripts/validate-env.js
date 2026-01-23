#!/usr/bin/env node

/**
 * Environment Variable Validation Script
 * 
 * Validates required environment variables before build/start
 * Ensures production builds have HTTPS API URLs configured
 */

const requiredEnvVars = {
    production: [
        'NEXT_PUBLIC_API_URL_PROD',
    ],
    development: [
        // DEV URL is optional - it's in .env file and loaded by Next.js
    ],
};

const env = process.env.NODE_ENV || 'development';
const required = requiredEnvVars[env] || [];

console.log(`🔍 Validating environment variables for: ${env}`);
console.log('');

let hasErrors = false;

required.forEach((varName) => {
    const value = process.env[varName];

    if (!value) {
        console.error(`❌ Missing required env var: ${varName}`);
        hasErrors = true;
        return;
    }

    // Validate HTTPS in production
    if (env === 'production' && varName.includes('API_URL')) {
        if (!value.startsWith('https://')) {
            console.error(`❌ ${varName} must use HTTPS in production. Got: ${value}`);
            hasErrors = true;
        } else {
            console.log(`✅ ${varName}: ${value}`);
        }
    } else {
        console.log(`✅ ${varName}: ${value}`);
    }
});

if (hasErrors) {
    console.error('');
    console.error('❌ Environment validation failed');
    console.error('');
    console.error('💡 Tip: Set NEXT_PUBLIC_API_URL_PROD in your deployment platform');
    console.error('   Example: NEXT_PUBLIC_API_URL_PROD=https://api.rchmct.org');
    process.exit(1);
}

console.log('');
console.log('✅ All environment variables validated');
