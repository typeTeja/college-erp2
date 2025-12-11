import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
    const token = request.cookies.get('access_token')?.value;
    const { pathname } = request.nextUrl;

    // Define public routes (no authentication required)
    const isAuthPage = pathname.startsWith('/login') || pathname.startsWith('/register');

    // If user is NOT authenticated
    if (!token) {
        // Allow access to auth pages
        if (isAuthPage) {
            return NextResponse.next();
        }
        // Redirect all other pages to login
        return NextResponse.redirect(new URL('/login', request.url));
    }

    // If user IS authenticated
    // Redirect from auth pages to dashboard
    if (isAuthPage) {
        return NextResponse.redirect(new URL('/', request.url));
    }

    // Allow access to protected pages
    return NextResponse.next();
}

export const config = {
    matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
