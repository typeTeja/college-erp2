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
        
        # Create Payment Record in DB
        from app.models.admissions import ApplicationPayment, ApplicationPaymentStatus
        payment_record = ApplicationPayment(
            application_id=application.id,
            transaction_id=txnid,
            amount=request.amount,
            status=ApplicationPaymentStatus.PENDING,
            payment_method="EASEBUZZ"
        )
        session.add(payment_record)
        session.commit()
        
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
            payment_record.status = ApplicationPaymentStatus.FAILED
            session.add(payment_record)
            session.commit()
            
            raise HTTPException(status_code=500, detail=response.get("error", "Payment initiation failed"))
            
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()  # Print full stack trace to console
        logger.error(f"Payment initiation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/public/initiate/{application_number}")
async def initiate_payment_public(
    application_number: str,
    session: Session = Depends(get_session)
):
    """
    Public endpoint to initiate payment using application number (for email links)
    No authentication required - redirects directly to payment gateway
    """
    try:
        from app.models.admissions import Application
        from app.config.settings import settings
        from sqlmodel import select
        from fastapi.responses import RedirectResponse
        
        # Find application by number
        statement = select(Application).where(Application.application_number == application_number)
        application = session.exec(statement).first()
        
        if not application:
            raise HTTPException(status_code=404, detail="Application not found")
        
        # Check if already paid
        if application.payment_status == "PAID" or application.status == "PAID":
            # Redirect to success page or portal
            return RedirectResponse(url=f"{settings.PORTAL_BASE_URL}/apply/payment/complete?status=already_paid&application={application_number}")
        
        # Check if payment is required
        if not application.application_fee or application.application_fee <= 0:
            raise HTTPException(status_code=400, detail="No payment required for this application")

        # Generate unique transaction ID
        txnid = f"TXN-{uuid.uuid4().hex[:12].upper()}"
        
        # Prepare payment data
        payment_data = {
            "txnid": txnid,
            "amount": application.application_fee,
            "firstname": application.name,
            "email": application.email,
            "phone": application.phone,
            "productinfo": f"Application Fee for {application.application_number}",
            "udf1": str(application.id),
            "udf2": application.application_number,
            "surl": f"{settings.PORTAL_BASE_URL}/api/v1/payment/response",
            "furl": f"{settings.PORTAL_BASE_URL}/api/v1/payment/response"
        }
        
        # Create Payment Record
        from app.models.admissions import ApplicationPayment, ApplicationPaymentStatus
        payment_record = ApplicationPayment(
            application_id=application.id,
            transaction_id=txnid,
            amount=application.application_fee,
            status=ApplicationPaymentStatus.PENDING,
            payment_method="EASEBUZZ"
        )
        session.add(payment_record)
        session.commit()
        
        # Call service to initiate
        response = await easebuzz_service.initiate_payment(payment_data)
        
        if response.get("status") == 1:
            access_key = response.get("data")
            payment_url = f"{easebuzz_service.base_url}/pay/{access_key}"
            
            # Redirect directly to payment gateway
            return RedirectResponse(url=payment_url)
        else:
            # Failed
            payment_record.status = ApplicationPaymentStatus.FAILED
            session.add(payment_record)
            session.commit()
            raise HTTPException(status_code=500, detail=response.get("error", "Payment initiation failed"))
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Public payment initiation error: {str(e)}")
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
    from app.services.admission_service import AdmissionService

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
        application_id = int(data.get("udf1")) # We stored app ID in UDF1
        
        if status == "success":
            logger.info(f"Payment Successful: {txnid} for amount {amount}")
            
            # Process Payment
            AdmissionService.process_payment_completion(
                session=session,
                application_id=application_id,
                transaction_id=txnid,
                amount=amount,
                background_tasks=background_tasks
            )
            
            # Redirect to Success Page
            # Pass txnid and status to frontend to allow immediate feedback
            return RedirectResponse(
                url=f"{settings.PORTAL_BASE_URL}/apply/success?status=success&txnid={txnid}",
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
    from app.services.admission_service import AdmissionService

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
        application_id = int(data.get("udf1")) if data.get("udf1") else 0

        logger.info(f"Webhook Verified: Transaction {txnid} is {status}")
        
        if status == "success" and application_id:
             # Process Payment (Independent of user redirect)
            AdmissionService.process_payment_completion(
                session=session,
                application_id=application_id,
                transaction_id=txnid,
                amount=amount,
                background_tasks=background_tasks
            )
        
        return {"status": "success", "message": "Webhook processed"}
        
    except Exception as e:
        logger.error(f"Webhook Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Webhook processing failed")
