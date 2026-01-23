from fastapi import APIRouter, Request, Depends, HTTPException, Form, BackgroundTasks
from typing import Optional, Dict, Any
from app.services.easebuzz_service import easebuzz_service
from app.services.email_service import email_service
from app.schemas.easebuzz import EasebuzzInitiateRequest, EasebuzzInitiateResponse, EasebuzzCallbackData, PaymentInitiateRequest
from app.db.session import get_session
from sqlmodel import Session
import uuid
import logging
import json
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

router = APIRouter()

async def complete_payment_process(
    session: Session,
    txnid: str,
    amount: float,
    application_id: str,
    email: str,
    background_tasks: BackgroundTasks
):
    """
    Helper to complete payment process:
    1. Update Application Status
    2. Create Portal Account
    3. Send Emails
    """
    try:
        from app.models.admissions import Application
        from app.services.admission_service import AdmissionService
        
        # Get Application
        app_id = int(application_id)
        application = session.get(Application, app_id)
        
        if not application:
            logger.error(f"Application {app_id} not found for payment {txnid}")
            return False
            
        # Check if already paid to avoid double processing
        if application.status == 'PAYMENT_COMPLETED' or application.payment_status == 'PAID':
            logger.info(f"Application {app_id} already marked as paid")
            return True

        # Update Payment Status
        application.status = 'PAYMENT_COMPLETED'
        application.payment_status = 'PAID'
        application.payment_id = txnid
        application.payment_date = datetime.now()
        session.add(application)
        session.commit()
        session.refresh(application)
        
        # Create Portal Account
        portal_username, portal_password = AdmissionService.create_portal_account_after_payment(
            session=session,
            application=application
        )
        
        # Send Payment Success Email
        background_tasks.add_task(
            email_service.send_payment_success,
            to_email=email,
            name=application.name,
            application_number=application.application_number,
            amount=amount,
            transaction_id=txnid
        )
        
        # Send Credentials Email
        if portal_username and portal_password:
             background_tasks.add_task(
                email_service.send_portal_credentials,
                to_email=email,
                name=application.name,
                application_number=application.application_number,
                username=portal_username,
                password=portal_password
            )
            
        return True
    except Exception as e:
        logger.error(f"Error completing payment process: {str(e)}")
        return False

@router.post("/initiate", response_model=EasebuzzInitiateResponse)
async def initiate_payment(
    request: PaymentInitiateRequest,
    session: Session = Depends(get_session)
):
    """
    Initiate Easebuzz Payment
    Generates txnid, hash and calls Easebuzz API
    Now populates details from Application ID
    """
    try:
        # Fetch Application
        from app.models.admissions import Application
        application = session.get(Application, request.application_id)
        if not application:
            raise HTTPException(status_code=404, detail="Application not found")

        # Generate unique transaction ID
        txnid = f"TXN-{uuid.uuid4().hex[:12].upper()}"
        
        # Prepare data for hash generation
        # We construct the strict schema data internally
        payment_data = {
            "txnid": txnid,
            "amount": request.amount,
            "firstname": application.name,
            "email": application.email,
            "phone": application.phone,
            "productinfo": f"Application Fee for {application.application_number}",
            "udf1": str(application.id), # Store App ID in UDF1
            "udf2": application.application_number, # Store App Number in UDF2
            "surl": request.surl,
            "furl": request.furl
        }
        
        # Call service to initiate
        response = await easebuzz_service.initiate_payment(payment_data)
        
        if response.get("status") == 1:
            # Success
            access_key = response.get("data")
            payment_url = f"{easebuzz_service.base_url}/pay/{access_key}"
            
            return {
                "status": 1,
                "data": access_key,
                "payment_url": payment_url, 
                "txnid": txnid
            }
        else:
            # Failed
            return {
                "status": 0,
                "error": response.get("data", "Unknown error from Gateway"),
                "txnid": txnid
            }
            
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()  # Print full stack trace to console
        logger.error(f"Payment initiation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/response")
async def handle_payment_response(
    request: Request,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)
):
    """
    Handle Redirect Response from Easebuzz (SURL/FURL)
    Receives Form Data
    """
    from fastapi.responses import RedirectResponse
    from app.config.settings import settings

    try:
        # Parse form data
        form_data = await request.form()
        data = dict(form_data)
        
        logger.info(f"Payment Response Received: {data}")
        
        # Verify Hash
        if not easebuzz_service.verify_response_hash(data):
            logger.error("Hash verification failed for payment response")
            return RedirectResponse(
                url=f"{settings.PORTAL_BASE_URL}/apply/payment/failure?reason=hash_verification_failed",
                status_code=303
            )
        
        status = data.get("status")
        txnid = data.get("txnid")
        amount = float(data.get("amount", 0))
        email = data.get("email")
        application_id = data.get("udf1") # We stored app ID in UDF1
        
        if status == "success":
            logger.info(f"Payment Successful: {txnid} for amount {amount}")
            
            # Process Payment
            await complete_payment_process(
                session=session,
                txnid=txnid,
                amount=amount,
                application_id=application_id,
                email=email,
                background_tasks=background_tasks
            )
            
            # Redirect to Success Page
            return RedirectResponse(
                url=f"{settings.PORTAL_BASE_URL}/apply/payment/success",
                status_code=303
            )
        else:
            reason = data.get("error_Message", "Payment Failed")
            logger.warning(f"Payment Failed: {txnid} - {reason}")
            
            # Redirect to Failure Page
            return RedirectResponse(
                url=f"{settings.PORTAL_BASE_URL}/apply/payment/failure?reason={reason}",
                status_code=303
            )

    except Exception as e:
        logger.error(f"Error handling payment response: {str(e)}")
        # Fallback redirect
        return RedirectResponse(
            url=f"{settings.PORTAL_BASE_URL}/apply/payment/failure?reason=internal_error",
            status_code=303
        )

@router.post("/webhook")
async def handle_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session)
):
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
        amount = float(data.get("amount", 0))
        email = data.get("email")
        application_id = data.get("udf1") # We stored app ID in UDF1

        logger.info(f"Webhook Verified: Transaction {txnid} is {status}")
        
        if status == "success":
             # Process Payment (Independent of user redirect)
            await complete_payment_process(
                session=session,
                txnid=txnid,
                amount=amount,
                application_id=application_id,
                email=email,
                background_tasks=background_tasks
            )
        
        return {"status": "success", "message": "Webhook processed"}
        
    except Exception as e:
        logger.error(f"Webhook Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Webhook processing failed")
