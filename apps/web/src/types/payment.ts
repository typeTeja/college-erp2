/**
 * Payment Gateway Types
 */

export interface PaymentGatewayConfig {
    id: number;
    gateway_name: 'razorpay' | 'easebuzz' | 'paytm';
    is_active: boolean;
    is_default: boolean;
    api_key: string;
    merchant_id?: string;
    webhook_secret?: string;
    config_data?: Record<string, any>;
    created_at: string;
    updated_at: string;
}

export interface OnlinePayment {
    id: number;
    student_id: number;
    gateway_config_id: number;
    payment_purpose: string;
    amount: number;
    currency: string;
    gateway_order_id: string;
    gateway_payment_id?: string;
    payment_status: 'pending' | 'success' | 'failed' | 'refunded';
    payment_method?: string;
    payment_date?: string;
    failure_reason?: string;
    gateway_response?: Record<string, any>;
    metadata?: Record<string, any>;
    created_at: string;
    updated_at: string;
}

export interface PaymentReceipt {
    id: number;
    payment_id: number;
    receipt_number: string;
    receipt_url?: string;
    generated_at: string;
    created_at: string;
}

// Request types
export interface PaymentInitiateRequest {
    student_id: number;
    amount: number;
    purpose: string;
    description?: string;
}

export interface PaymentVerifyRequest {
    payment_id: string;
    signature: string;
}

export interface PaymentHistoryFilters {
    status?: string;
    from_date?: string;
    to_date?: string;
}
