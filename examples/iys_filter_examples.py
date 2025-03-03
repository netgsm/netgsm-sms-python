#!/usr/bin/env python
"""
IYS filter examples for Netgsm Python SDK.
"""

import os
from dotenv import load_dotenv

from netgsm import Netgsm
from netgsm.utils.enums import IysFilterType

# Load environment variables
load_dotenv()


def main():
    """Main function."""
    # Initialize Netgsm client
    client = Netgsm(
        username=os.getenv("NETGSM_USERNAME"),
        password=os.getenv("NETGSM_PASSWORD"),
        header=os.getenv("NETGSM_MSGHEADER"),
    )

    # Example 1: Send informational SMS (without IYS control)
    try:
        client.sms.send(
            message="This is an informational message",
            phones=["+905555555555"],
            iysfilter=IysFilterType.INFORMATIONAL,
        )
    except Exception as e:
        print("Error sending informational SMS:", e)

    # Example 2: Send commercial SMS to individuals (with IYS control)
    try:
        client.sms.send(
            message="This is a commercial message for individuals",
            phones=["+905555555555"],
            iysfilter=IysFilterType.INDIVIDUAL,
        )
    except Exception as e:
        print("Error sending commercial SMS to individuals:", e)

    # Example 3: Send commercial SMS to merchants (with IYS control)
    try:
        client.sms.send(
            message="This is a commercial message for merchants",
            phones=["+905555555555"],
            iysfilter=IysFilterType.MERCHANT,
        )
    except Exception as e:
        print("Error sending commercial SMS to merchants:", e)


if __name__ == "__main__":
    main()
