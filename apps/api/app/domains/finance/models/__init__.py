"""
Finance Domain Models

Modular package for all finance-related database models.
"""

# Fee Configuration
from .fee_config import (
    FeeHead,
    InstallmentPlan,
    ScholarshipSlab
)

# Fee Management
from .fee_management import (
    FeeStructure,
    FeeComponent,
    FeeInstallment,
    StudentFee,
    FeePayment,
    FeeConcession,
    FeeFine,
    StudentFeeInstallment
)

# Payment Gateway
from .payment_gateway import (
    PaymentGatewayConfig,
    OnlinePayment,
    PaymentReceipt
)

# Enums (from shared)
from app.shared.enums import (
    FeeCategory,
    PaymentMode,
    PaymentStatus
)

__all__ = [
    # Fee Configuration
    "FeeHead",
    "InstallmentPlan",
    "ScholarshipSlab",
    
    # Fee Management
    "FeeStructure",
    "FeeComponent",
    "FeeInstallment",
    "StudentFee",
    "FeePayment",
    "FeeConcession",
    "FeeFine",
    "StudentFeeInstallment",
    
    # Payment Gateway
    "PaymentGatewayConfig",
    "OnlinePayment",
    "PaymentReceipt",
    
    # Enums
    "FeeCategory",
    "PaymentMode",
    "PaymentStatus",
]
