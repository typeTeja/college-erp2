"""Status transition validation for applications"""
from typing import Dict, List
from app.shared.enums import ApplicationStatus


# Define allowed status transitions
ALLOWED_TRANSITIONS: Dict[ApplicationStatus, List[ApplicationStatus]] = {
    ApplicationStatus.PENDING_PAYMENT: [
        ApplicationStatus.PAID,
        ApplicationStatus.PAYMENT_FAILED,
        ApplicationStatus.WITHDRAWN
    ],
    ApplicationStatus.PAYMENT_FAILED: [
        ApplicationStatus.PAID,
        ApplicationStatus.WITHDRAWN
    ],
    ApplicationStatus.PAID: [
        ApplicationStatus.FORM_COMPLETED,
        ApplicationStatus.WITHDRAWN
    ],
    ApplicationStatus.FORM_COMPLETED: [
        ApplicationStatus.UNDER_REVIEW,
        ApplicationStatus.WITHDRAWN
    ],
    ApplicationStatus.UNDER_REVIEW: [
        ApplicationStatus.APPROVED,
        ApplicationStatus.REJECTED
    ],
    ApplicationStatus.APPROVED: [
        ApplicationStatus.ADMITTED,
        ApplicationStatus.REJECTED
    ],
    ApplicationStatus.ADMITTED: [],  # Final state
    ApplicationStatus.REJECTED: [],  # Final state
    ApplicationStatus.WITHDRAWN: []  # Final state
}

def can_transition(current_status: ApplicationStatus, new_status: ApplicationStatus) -> bool:
    """
    Check if a status transition is allowed
    
    Args:
        current_status: Current application status
        new_status: Desired new status
    
    Returns:
        True if transition is allowed, False otherwise
    """
    if current_status == new_status:
        return True  # Same status is always allowed
    
    allowed = ALLOWED_TRANSITIONS.get(current_status, [])
    return new_status in allowed

def get_allowed_transitions(current_status: ApplicationStatus) -> List[ApplicationStatus]:
    """
    Get list of allowed transitions from current status
    
    Args:
        current_status: Current application status
    
    Returns:
        List of allowed next statuses
    """
    return ALLOWED_TRANSITIONS.get(current_status, [])
