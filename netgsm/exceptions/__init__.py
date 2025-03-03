"""
Netgsm exception classes package.
"""

from .api_exception import (
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

__all__ = [
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
