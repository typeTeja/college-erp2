from fastapi import APIRouter, Request, Depends, HTTPException, Form
from typing import Optional, Dict, Any
from app.services.easebuzz_service import easebuzz_service
from app.schemas.easebuzz import EasebuzzInitiateRequest, EasebuzzInitiateResponse, EasebuzzCallbackData
import uuid
import logging
import json

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/initiate", response_model=EasebuzzInitiateResponse)
async def initiate_payment(
    request: EasebuzzInitiateRequest
):
    """
    Initiate Easebuzz Payment
    Generates txnid, hash and calls Easebuzz API
    """
    try:
        # Generate unique transaction ID
        txnid = f"TXN-{uuid.uuid4().hex[:12].upper()}"
        
        # Prepare data for hash generation
        payment_data = request.model_dump()
        payment_data['txnid'] = txnid
        
        # Call service to initiate
        response = await easebuzz_service.initiate_payment(payment_data)
        
        if response.get("status") == 1:
            # Success
            return {
                "status": 1,
                "data": response.get("data"),
                "payment_url": response.get("data"), # Easebuzz returns access key as url or similar
                "txnid": txnid
            }
        else:
            # Failed
            return {
                "status": 0,
                "error": response.get("data", "Unknown error from Gateway"),
                "txnid": txnid
            }
            
    except Exception as e:
        logger.error(f"Payment initiation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/response")
async def handle_payment_response(request: Request):
    """
    Handle Redirect Response from Easebuzz (SURL/FURL)
    Receives Form Data
    """
    try:
        # Parse form data
        form_data = await request.form()
        data = dict(form_data)
        
        logger.info(f"Payment Response Received: {data}")
        
        # Verify Hash
        if not easebuzz_service.verify_response_hash(data):
            logger.error("Hash verification failed for payment response")
            return {"status": "failed", "message": "Hash verification failed"}
        
        status = data.get("status")
        txnid = data.get("txnid")
        amount = data.get("amount")
        
        if status == "success":
            logger.info(f"Payment Successful: {txnid} for amount {amount}")
            # TODO: Update database status here
            return {
                "status": "success", 
                "message": "Payment verified successfully",
                "txnid": txnid,
                "amount": amount
            }
        else:
            logger.warning(f"Payment Failed: {txnid} - {data.get('error_Message')}")
            return {
                "status": "failed", 
                "message": "Payment failed",
                "reason": data.get("error_Message")
            }

    except Exception as e:
        logger.error(f"Error handling payment response: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/webhook")
async def handle_webhook(request: Request):
    """
    Handle Webhook from Easebuzz
    """
    try:
        # Easebuzz sends form data for webhook too usually
        form_data = await request.form()
        data = dict(form_data)
        
        logger.info(f"Webhook Received: {data}")
        
        # Verify Hash
        if not easebuzz_service.verify_response_hash(data):
            logger.error("Hash verification failed for webhook")
            return {"status": "failure", "message": "Hash verification failed"}
            
        status = data.get("status")
        txnid = data.get("txnid")
        
        logger.info(f"Webhook Verified: Transaction {txnid} is {status}")
        
        # TODO: Update database independent of user redirect
        
        return {"status": "success", "message": "Webhook processed"}
        
    except Exception as e:
        logger.error(f"Webhook Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Webhook processing failed")
