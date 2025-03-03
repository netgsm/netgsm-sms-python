#!/usr/bin/env python
"""
Error codes example for Netgsm Python SDK.
"""

import os
from netgsm import Netgsm
from netgsm.exceptions.api_exception import ApiException
from dotenv import load_dotenv

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

    # Example error codes and their meanings
    error_codes = {
        "20": "The posted XML is missing or incorrect.",
        "30": "Invalid username, password or API access is not active.",
        "40": "Sender name (msgheader) is not defined in the system.",
        "50": "The sent header (msgheader) is incorrect.",
        "51": "The sent header (msgheader) is not defined in the system.",
        "60": "The specified JobID was not found.",
        "70": "Incorrect query, missing or incorrect parameter.",
        "80": "No message to send.",
        "85": "Customer IP address is restricted.",
    }

    # Print error codes and their meanings
    print("\nNetgsm API Error Codes:")
    print("=" * 50)
    for code, meaning in error_codes.items():
        print(f"Code {code}: {meaning}")

    # Example: Handle error code 30 (Invalid credentials)
    try:
        invalid_client = Netgsm(
            username="invalid_username",
            password="invalid_password",
            header="INVALID",
        )
        invalid_client.sms.send(
            msgheader="INVALID",
            messages=[{"msg": "Test message", "no": "+905555555555"}],
        )
    except ApiException as e:
        print("\nExample - Error code 30:")
        print(f"Error code: {e.code}")
        print(f"Error message: {e.message}")

    # Example: Handle error code 40 (Invalid header)
    try:
        client.sms.send(
            msgheader="INVALID_HEADER",
            messages=[{"msg": "Test message", "no": "+905555555555"}],
        )
    except ApiException as e:
        print("\nExample - Error code 40:")
        print(f"Error code: {e.code}")
        print(f"Error message: {e.message}")

    # Example: Handle error code 70 (Invalid parameters)
    try:
        client.sms.send(
            msgheader=os.getenv("NETGSM_MSGHEADER"),
            messages=[{"msg": "", "no": "+905555555555"}],  # Empty message
        )
    except ApiException as e:
        print("\nExample - Error code 70:")
        print(f"Error code: {e.code}")
        print(f"Error message: {e.message}")


if __name__ == "__main__":
    main()
