import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
    try {
        const formData = await request.formData();
        const data = Object.fromEntries(formData.entries());
        console.log('Payment Failure Callback:', data);

        const txnid = data.txnid as string;
        const error_Message = data.error_Message as string || 'Payment Failed';

        // Redirect to the complete page
        const url = new URL('/apply/payment/complete', request.url);
        url.searchParams.set('status', 'failure');
        url.searchParams.set('txnid', txnid);
        url.searchParams.set('error', error_Message);
        
        return NextResponse.redirect(url, 303);
    } catch (error) {
        console.error('Error processing payment failure:', error);
        return NextResponse.redirect(new URL('/apply/payment/complete?status=error', request.url));
    }
}
