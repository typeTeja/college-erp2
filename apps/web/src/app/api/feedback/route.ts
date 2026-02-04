import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth';
import { authOptions } from '@/lib/auth';

/**
 * Feedback API Endpoint
 * 
 * POST /api/feedback
 * 
 * Accepts user feedback submissions and stores them in the database.
 * Sends email notifications to support team.
 */

interface FeedbackSubmission {
  rating: 'happy' | 'neutral' | 'sad' | null;
  category: 'bug' | 'feature' | 'general';
  message: string;
  url: string;
  timestamp: string;
}

export async function POST(request: NextRequest) {
  try {
    // Get user session
    const session = await getServerSession(authOptions);
    
    if (!session?.user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    // Parse request body
    const body: FeedbackSubmission = await request.json();

    // Validate required fields
    if (!body.message || !body.category) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      );
    }

    // TODO: Store feedback in database
    // Example:
    // await prisma.feedback.create({
    //   data: {
    //     userId: session.user.id,
    //     rating: body.rating,
    //     category: body.category,
    //     message: body.message,
    //     url: body.url,
    //     timestamp: new Date(body.timestamp),
    //   },
    // });

    // TODO: Send email notification to support team
    // Example:
    // await sendEmail({
    //   to: 'support@college-erp.com',
    //   subject: `New Feedback: ${body.category}`,
    //   body: `
    //     User: ${session.user.email}
    //     Rating: ${body.rating || 'N/A'}
    //     Category: ${body.category}
    //     Message: ${body.message}
    //     URL: ${body.url}
    //   `,
    // });

    // Log feedback for development
    console.log('[Feedback]', {
      user: session.user.email,
      rating: body.rating,
      category: body.category,
      message: body.message,
      url: body.url,
    });

    return NextResponse.json(
      { success: true, message: 'Feedback submitted successfully' },
      { status: 200 }
    );
  } catch (error) {
    console.error('[Feedback API] Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

// GET endpoint to retrieve feedback (admin only)
export async function GET(request: NextRequest) {
  try {
    // Get user session
    const session = await getServerSession(authOptions);
    
    if (!session?.user) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    // Check if user is admin
    const isAdmin = session.user.roles?.some((role: string) => 
      ['ADMIN', 'SUPER_ADMIN'].includes(role)
    );

    if (!isAdmin) {
      return NextResponse.json(
        { error: 'Forbidden' },
        { status: 403 }
      );
    }

    // TODO: Fetch feedback from database
    // Example:
    // const feedback = await prisma.feedback.findMany({
    //   orderBy: { timestamp: 'desc' },
    //   take: 100,
    //   include: {
    //     user: {
    //       select: {
    //         email: true,
    //         name: true,
    //       },
    //     },
    //   },
    // });

    // Return mock data for now
    return NextResponse.json(
      { feedback: [] },
      { status: 200 }
    );
  } catch (error) {
    console.error('[Feedback API] Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
