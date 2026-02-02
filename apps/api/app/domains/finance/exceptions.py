"""
Finance Domain Exceptions

Custom exceptions for the finance domain.
"""


class FinanceDomainError(Exception):
    """Base exception for finance domain"""
    pass


class FeeNotFoundError(FinanceDomainError):
    """Raised when a fee record is not found"""
    pass


class PaymentNotFoundError(FinanceDomainError):
    """Raised when a payment is not found"""
    pass


class InvalidPaymentStatusError(FinanceDomainError):
    """Raised when payment status is invalid"""
    pass


class PaymentGatewayError(FinanceDomainError):
    """Raised when payment gateway operation fails"""
    pass


class InsufficientPaymentError(FinanceDomainError):
    """Raised when payment amount is insufficient"""
    pass


class DuplicatePaymentError(FinanceDomainError):
    """Raised when trying to create a duplicate payment"""
    pass
