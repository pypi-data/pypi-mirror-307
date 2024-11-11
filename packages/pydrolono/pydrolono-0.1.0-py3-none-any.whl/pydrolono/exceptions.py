"""Custom exceptions for the pydrolono package."""

class PydrolonoError(Exception):
    """Base exception for all pydrolono errors."""
    pass

class APIError(PydrolonoError):
    """Raised when the API returns an error."""
    pass

class ValidationError(PydrolonoError):
    """Raised when input validation fails."""
    pass

class AuthenticationError(PydrolonoError):
    """Raised when authentication fails."""
    pass
