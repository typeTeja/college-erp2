import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

/**
 * Security Headers Proxy
 * 
 * Adds comprehensive security headers to all responses:
 * - Content Security Policy (CSP) with mixed-content blocking
 * - HTTP Strict Transport Security (HSTS)
 * - Clickjacking protection
 * - MIME sniffing prevention
 * - And more...
 */

// Export as 'proxy' (Next.js 16 requirement)
export function proxy(request: NextRequest) {
    const response = NextResponse.next();

    // Content Security Policy - Block mixed content and XSS
    const csp = [
        "default-src 'self'",
        "script-src 'self' 'unsafe-eval' 'unsafe-inline'", // Next.js requires these
        "style-src 'self' 'unsafe-inline'", // Tailwind requires unsafe-inline
        "img-src 'self' data: https:",
        "font-src 'self' data:",
        "connect-src 'self' https://api.rchmct.org https://minio.rchmct.org",
        "frame-ancestors 'none'",
        "base-uri 'self'",
        "form-action 'self'",
        "upgrade-insecure-requests", // Auto-upgrade HTTP to HTTPS
        "block-all-mixed-content",   // Block HTTP requests (Layer 4)
    ].join('; ');

    response.headers.set('Content-Security-Policy', csp);

    // HSTS - Force HTTPS for 1 year (Layer 5)
    response.headers.set(
        'Strict-Transport-Security',
        'max-age=31536000; includeSubDomains; preload'
    );

    // Prevent clickjacking
    response.headers.set('X-Frame-Options', 'DENY');

    // Prevent MIME sniffing
    response.headers.set('X-Content-Type-Options', 'nosniff');

    // Referrer policy
    response.headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');

    // Permissions policy - disable unnecessary features
    response.headers.set(
        'Permissions-Policy',
        'camera=(), microphone=(), geolocation=()'
    );

    // XSS Protection (legacy but still useful)
    response.headers.set('X-XSS-Protection', '1; mode=block');

    return response;
}

// Apply proxy to all routes except static files
export const config = {
    matcher: [
        /*
         * Match all request paths except:
         * - _next/static (static files)
         * - _next/image (image optimization)
         * - favicon.ico, favicon.png (favicons)
         * - public files (images, etc)
         */
        '/((?!_next/static|_next/image|favicon.ico|favicon.png|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
    ],
};
