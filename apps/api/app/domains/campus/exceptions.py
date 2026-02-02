"""
Campus Domain Exceptions

Custom exceptions for the campus domain and all subdomains.
"""


class CampusDomainError(Exception):
    """Base exception for campus domain"""
    pass


# Hostel Exceptions
class HostelNotFoundError(CampusDomainError):
    """Raised when a hostel is not found"""
    pass


class RoomNotAvailableError(CampusDomainError):
    """Raised when a room is not available"""
    pass


class AllocationNotFoundError(CampusDomainError):
    """Raised when an allocation is not found"""
    pass


# Library Exceptions
class BookNotFoundError(CampusDomainError):
    """Raised when a book is not found"""
    pass


class BookNotAvailableError(CampusDomainError):
    """Raised when a book is not available for issue"""
    pass


class IssueNotFoundError(CampusDomainError):
    """Raised when an issue record is not found"""
    pass


class OverdueBookError(CampusDomainError):
    """Raised when a book is overdue"""
    pass


# Transport Exceptions
class RouteNotFoundError(CampusDomainError):
    """Raised when a route is not found"""
    pass


class VehicleNotFoundError(CampusDomainError):
    """Raised when a vehicle is not found"""
    pass


class TransportAllocationError(CampusDomainError):
    """Raised when transport allocation fails"""
    pass


# Inventory Exceptions
class AssetNotFoundError(CampusDomainError):
    """Raised when an asset is not found"""
    pass


class AssetNotAvailableError(CampusDomainError):
    """Raised when an asset is not available"""
    pass


# Infrastructure Exceptions
class FacilityNotFoundError(CampusDomainError):
    """Raised when a facility is not found"""
    pass


class MaintenanceRequestError(CampusDomainError):
    """Raised when maintenance request fails"""
    pass
