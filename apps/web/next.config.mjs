import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/** @type {import('next').NextConfig} */
const nextConfig = {
    // Enable React strict mode for better error detection
    reactStrictMode: true,

    // Turbopack configuration (Next.js 16+)
    turbopack: {},

    // Security headers
    async headers() {
        // CSP Configuration
        const csp = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-eval' 'unsafe-inline'",
            "style-src 'self' 'unsafe-inline'",
            "img-src 'self' data: https:",
            "font-src 'self' data:",
            `connect-src 'self' https://api.rchmct.org https://minio.rchmct.org ${process.env.NODE_ENV !== 'production' ? 'http://localhost:8000' : ''}`,
            "frame-ancestors 'none'",
            "base-uri 'self'",
            "form-action 'self'",
            ...(process.env.NODE_ENV === 'production' ? [
                "upgrade-insecure-requests",
                "block-all-mixed-content"
            ] : [])
        ].join('; ');

        return [
            {
                source: '/:path*',
                headers: [
                    {
                        key: 'Content-Security-Policy',
                        value: csp
                    },
                    ...(process.env.NODE_ENV === 'production' ? [{
                        key: 'Strict-Transport-Security',
                        value: 'max-age=31536000; includeSubDomains; preload'
                    }] : []),
                    {
                        key: 'X-DNS-Prefetch-Control',
                        value: 'on'
                    },
                    {
                        key: 'X-Frame-Options',
                        value: 'DENY'
                    },
                    {
                        key: 'X-Content-Type-Options',
                        value: 'nosniff'
                    },
                    {
                        key: 'Referrer-Policy',
                        value: 'strict-origin-when-cross-origin'
                    },
                    {
                        key: 'Permissions-Policy',
                        value: 'camera=(), microphone=(), geolocation=()'
                    },
                    {
                        key: 'X-XSS-Protection',
                        value: '1; mode=block'
                    }
                ],
            },
        ];
    },

    // Disable x-powered-by header
    poweredByHeader: false,

    // Enable compression
    compress: true,

    // Image optimization - use remotePatterns instead of deprecated domains
    images: {
        remotePatterns: [
            {
                protocol: 'https',
                hostname: 'minio.rchmct.org',
                pathname: '/**',
            },
        ],
        formats: ['image/avif', 'image/webp'],
    },
};

// Build-time validation (Layer 6)
// Only validate HTTPS when NEXT_PUBLIC_API_URL_PROD is actually set
if (process.env.NEXT_PUBLIC_API_URL_PROD) {
    if (!process.env.NEXT_PUBLIC_API_URL_PROD.startsWith('https://')) {
        throw new Error(
            `🚨 BUILD FAILED: NEXT_PUBLIC_API_URL_PROD must use HTTPS in production.\n` +
            `   Got: ${process.env.NEXT_PUBLIC_API_URL_PROD}\n` +
            `   Expected: https://api.rchmct.org`
        );
    }
    console.log('✅ Production API URL validated:', process.env.NEXT_PUBLIC_API_URL_PROD);
}

export default nextConfig;
