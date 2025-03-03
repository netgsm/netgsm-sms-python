"""
Netgsm API enums.
"""

from enum import Enum, IntEnum


class IysFilterType(str, Enum):
    """
    IYS (Message Management System) filter type.

    Values:
        INFORMATIONAL: Informational content (without IYS control)
        INDIVIDUAL: Commercial content to be sent to individuals
        MERCHANT: IYS controlled for merchants
    """

    INFORMATIONAL = "0"  # Informational content (without IYS control)
    INDIVIDUAL = "11"  # Commercial content to be sent to individuals
    MERCHANT = "12"  # IYS controlled for merchants


class Encoding(str, Enum):
    """
    Message encoding type.

    Note: Only use encoding when your message contains Turkish characters.
    For messages without special characters, do not set the encoding parameter.

    Values:
        TR: Turkish - Use this for messages with Turkish characters
    """

    TR = "tr"  # Turkish


class SmsStatus(IntEnum):
    """
    SMS status codes.
    """

    NOT_DELIVERED = 0
    DELIVERED = 1
    PENDING = 2
    TIMEOUT = 3
    ERROR = 4
    CURRENTLY_UNREACHABLE = 11
    ORIGINAL_NETGSM = 12
    NETGSM_ERROR = 13
    NETGSM_ERROR_2 = 100
    NETGSM_ERROR_3 = 101
    NETGSM_ERROR_4 = 102
    NETGSM_ERROR_5 = 103
