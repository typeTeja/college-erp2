from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any

class EasebuzzInitiateRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Payment amount")
    firstname: str = Field(..., min_length=1, description="Payer name")
    email: EmailStr = Field(..., description="Payer email")
    phone: str = Field(..., min_length=10, max_length=15, description="Payer phone")
    productinfo: str = Field(..., description="Description of product")
    udf1: Optional[str] = ""
    udf2: Optional[str] = ""
    surl: Optional[str] = None # Success URL
    furl: Optional[str] = None # Failure URL

class PaymentInitiateRequest(BaseModel):
    application_id: int
    amount: float
    surl: Optional[str] = None
    furl: Optional[str] = None

class EasebuzzInitiateResponse(BaseModel):
    status: int
    data: Optional[str] = None # Payment URL (access key usually)
    payment_url: Optional[str] = None
    txnid: Optional[str] = None
    error: Optional[str] = None

class EasebuzzCallbackData(BaseModel):
    txnid: str
    firstname: str
    email: str
    phone: str
    key: str
    mode: Optional[str] = None
    status: str
    unmappedstatus: Optional[str] = None
    cardCategory: Optional[str] = None
    addedon: Optional[str] = None
    payment_source: Optional[str] = None
    PG_TYPE: Optional[str] = None
    bank_ref_num: Optional[str] = None
    bankcode: Optional[str] = None
    error: Optional[str] = None
    error_Message: Optional[str] = None
    amount: str
    net_amount_debit: Optional[str] = None
    cash_back_percentage: Optional[str] = None
    deduction_percentage: Optional[str] = None
    productinfo: str
    udf1: Optional[str] = None
    udf2: Optional[str] = None
    udf3: Optional[str] = None
    udf4: Optional[str] = None
    udf5: Optional[str] = None
    udf6: Optional[str] = None
    udf7: Optional[str] = None
    udf8: Optional[str] = None
    udf9: Optional[str] = None
    udf10: Optional[str] = None
    hash: str
    
    class Config:
        extra = "allow" # Allow extra fields from gateway
