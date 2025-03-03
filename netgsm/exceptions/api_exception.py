"""
Netgsm API exception classes.
"""

import requests

# Netgsm API Common Error Codes (Used across multiple APIs)
NETGSM_COMMON_ERROR_CODES = {
    "00": "Operation successful",
    "30": (
        "Invalid username, password or no API access. "
        "If IP restriction exists, request may have been made from "
        "an unauthorized IP"
    ),
    "70": ("Invalid query. One of the parameters is incorrect or a " "required field is missing"),
}

# /sms/rest/v2/send API Error Codes
NETGSM_SEND_SMS_ERROR_CODES = {
    "20": (
        "Could not be sent due to a problem in the message text or "
        "exceeded the standard maximum message character count"
    ),
    "40": "Message header (sender name) is not defined in the system",
    "50": ("IYS controlled submissions cannot be made with your " "subscriber account"),
    "51": "No IYS Brand information found for your subscription",
    "80": "Sending limit exceeded",
    "85": (
        "Duplicate sending limit exceeded. Cannot create more than 20 "
        "tasks for the same number within 1 minute"
    ),
}

# /sms/rest/v2/inbox API Error Codes
NETGSM_INBOX_ERROR_CODES = {
    "40": (
        "Indicates that you have no messages to display. If you are not "
        "using the startdate and stopdate parameters, you can only list "
        "your messages once with the API. Listed messages will not "
        "appear in your other queries."
    )
}

# /sms/rest/v2/report API Error Codes
NETGSM_REPORT_ERROR_CODES = {
    "60": (
        "Indicates that there are no records to be listed according to " "your search criteria."
    ),
    "80": "Limit exceeded, can be queried 10 times per minute.",
    "100": "System error",
    "110": "System error",
}

# /sms/rest/v2/msgheader API Error Codes
NETGSM_MSGHEADER_ERROR_CODES = {"100": "System error", "101": "System error"}

# /sms/rest/v2/cancel API Error Codes
NETGSM_CANCEL_ERROR_CODES = {"60": "Specified JobID not found"}

# Other system errors (For all documented APIs)
NETGSM_SYSTEM_ERROR_CODES = {"100": "System error", "101": "System error"}

# All error codes combined
NETGSM_ALL_ERROR_CODES = {
    **NETGSM_COMMON_ERROR_CODES,
    **NETGSM_SEND_SMS_ERROR_CODES,
    **NETGSM_INBOX_ERROR_CODES,
    **NETGSM_REPORT_ERROR_CODES,
    **NETGSM_MSGHEADER_ERROR_CODES,
    **NETGSM_CANCEL_ERROR_CODES,
    **NETGSM_SYSTEM_ERROR_CODES,
}


def create_api_exception(e):
    """
    Create an appropriate API exception based on the error.

    Args:
        e (requests.exceptions.RequestException): Request exception

    Returns:
        ApiException: Appropriate API exception instance
    """
    if isinstance(e, requests.exceptions.Timeout):
        return TimeoutException()
    elif isinstance(e, requests.exceptions.ConnectionError):
        return ConnectionException()
    elif isinstance(e, requests.exceptions.HTTPError):
        status_code = e.response.status_code
        message = str(e)
        code = None

        # Try to get API error code from response
        try:
            response_json = e.response.json()
            code = response_json.get("code")
            if code:
                message = response_json.get("message", message)
        except (ValueError, AttributeError):
            pass

        # Create appropriate exception based on status code
        if status_code == 400:
            return BadRequestException(message, code)
        elif status_code == 401:
            return UnauthorizedException(message, code)
        elif status_code == 403:
            return ForbiddenException(message, code)
        elif status_code == 404:
            return NotFoundException(message, code)
        elif status_code == 406:
            return NotAcceptableException(message, code)
        elif status_code >= 500:
            return ServerException(message, code, status_code)
        else:
            return HttpException(message, code, status_code)
    else:
        return ApiException(str(e))


class ApiException(Exception):
    """
    Base exception class for all API errors.

    Attributes:
        message (str): Error message
        code (str): API error code
    """

    def __init__(self, message, code=None):
        """
        Initialize API exception.

        Args:
            message (str): Error message
            code (str, optional): API error code
        """
        self.message = message
        self.code = code

        # If code is "00", this is a success message
        if code == "00":
            self.message = NETGSM_ALL_ERROR_CODES.get(code, "Operation successful")
        # If we have a known error code, add its description to the message
        elif code in NETGSM_ALL_ERROR_CODES:
            self.message = f"{message}: {NETGSM_ALL_ERROR_CODES[code]}"

        super().__init__(self.message)


class HttpException(ApiException):
    """
    Exception for HTTP errors.

    Attributes:
        message (str): Error message
        code (str): API error code
        http_status (int): HTTP status code
    """

    def __init__(self, message, code=None, http_status=None):
        """
        Initialize HTTP exception.

        Args:
            message (str): Error message
            code (str, optional): API error code
            http_status (int, optional): HTTP status code
        """
        super().__init__(message, code)
        self.http_status = http_status


class BadRequestException(HttpException):
    """
    Exception for HTTP 400 Bad Request errors.
    """

    def __init__(self, message, code=None):
        """
        Initialize Bad Request exception.

        Args:
            message (str): Error message
            code (str, optional): API error code
        """
        super().__init__(message, code, 400)


class UnauthorizedException(HttpException):
    """
    Exception for HTTP 401 Unauthorized errors.
    """

    def __init__(self, message, code=None):
        """
        Initialize Unauthorized exception.

        Args:
            message (str): Error message
            code (str, optional): API error code
        """
        super().__init__(message, code, 401)


class ForbiddenException(HttpException):
    """
    Exception for HTTP 403 Forbidden errors.
    """

    def __init__(self, message, code=None):
        """
        Initialize Forbidden exception.

        Args:
            message (str): Error message
            code (str, optional): API error code
        """
        super().__init__(message, code, 403)


class NotFoundException(HttpException):
    """
    Exception for HTTP 404 Not Found errors.
    """

    def __init__(self, message, code=None):
        """
        Initialize Not Found exception.

        Args:
            message (str): Error message
            code (str, optional): API error code
        """
        super().__init__(message, code, 404)


class NotAcceptableException(HttpException):
    """
    Exception for HTTP 406 Not Acceptable errors.
    """

    def __init__(self, message, code=None):
        """
        Initialize Not Acceptable exception.

        Args:
            message (str): Error message
            code (str, optional): API error code
        """
        super().__init__(message, code, 406)


class TimeoutException(ApiException):
    """
    Exception for request timeout errors.
    """

    def __init__(self, message="Request timed out"):
        """
        Initialize Timeout exception.

        Args:
            message (str, optional): Error message
        """
        super().__init__(message)


class ConnectionException(ApiException):
    """
    Exception for connection errors.
    """

    def __init__(self, message="Connection error"):
        """
        Initialize Connection exception.

        Args:
            message (str, optional): Error message
        """
        super().__init__(message)


class ServerException(HttpException):
    """
    Exception for HTTP 5xx Server errors.
    """

    def __init__(self, message, code=None, http_status=500):
        """
        Initialize Server exception.

        Args:
            message (str): Error message
            code (str, optional): API error code
            http_status (int, optional): HTTP status code
        """
        super().__init__(message, code, http_status)
