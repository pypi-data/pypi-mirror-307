# sdk/trading_sdk/exceptions.py

class TradingClientException(Exception):
    """Base exception for TradingClient errors."""

class AuthenticationError(TradingClientException):
    """Raised when authentication fails."""

class ValidationError(TradingClientException):
    """Raised when input validation fails."""

class APIError(TradingClientException):
    """Raised when the API returns an error."""
