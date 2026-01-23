import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
    try {
        const formData = await request.formData();
        const data = Object.fromEntries(formData.entries());
        console.log('Payment Success Callback:', data);

        const txnid = data.txnid as string;
        const amount = data.amount as string;
        const status = data.status as string;

        // Redirect to the complete page
        const url = new URL('/apply/payment/complete', request.url);
        url.searchParams.set('status', 'success');
        url.searchParams.set('txnid', txnid);
        url.searchParams.set('amount', amount);
        
        return NextResponse.redirect(url, 303); // 303 See Other is correct for POST -> GET redirect
    } catch (error) {
        console.error('Error processing payment success:', error);
        return NextResponse.redirect(new URL('/apply/payment/complete?status=error', request.url));
    }
}
