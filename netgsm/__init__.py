"""
Netgsm Python SDK

This SDK provides access to Netgsm SMS API.
"""

from .netgsm import Netgsm
from .utils.enums import SmsStatus, Encoding, IysFilterType
from .exceptions.api_exception import (
    ApiException,
    HttpException,
    BadRequestException,
    UnauthorizedException,
    ForbiddenException,
    NotFoundException,
    NotAcceptableException,
    TimeoutException,
    ConnectionException,
    ServerException,
)

__version__ = "0.1.0"
__author__ = "Netgsm"
__license__ = "MIT"

# Public API
__all__ = [
    # Classes
    "Netgsm",
    # Enums
    "SmsStatus",
    "Encoding",
    "IysFilterType",
    "ApiException",
    "HttpException",
    "BadRequestException",
    "UnauthorizedException",
    "ForbiddenException",
    "NotFoundException",
    "NotAcceptableException",
    "TimeoutException",
    "ConnectionException",
    "ServerException",
]
