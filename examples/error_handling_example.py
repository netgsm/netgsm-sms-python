#!/usr/bin/env python
"""
Error handling example for Netgsm Python SDK.
"""

import os
from dotenv import load_dotenv
from netgsm import Netgsm
from netgsm.exceptions.api_exception import (
    ApiException,
    UnauthorizedException,
    NotFoundException,
    NotAcceptableException,
    ServerException,
)

# Load environment variables
load_dotenv()


def main():
    """Main function."""
    # Initialize Netgsm client
    client = Netgsm(
        username=os.getenv("NETGSM_USERNAME"),
        password=os.getenv("NETGSM_PASSWORD"),
    )

    # Example 1: Handle authentication error
    try:
        invalid_client = Netgsm(
            username="invalid_username",
            password="invalid_password",
        )
        invalid_client.sms.send(
            msgheader="INVALID",
            messages=[{"msg": "Test message", "no": "+905555555555"}],
        )
    except UnauthorizedException as e:
        print("Authentication error example:")
        print(f"Error code: {e.code}")
        print(f"Error message: {e.message}")
        print()

    # Example 2: Handle bad request error
    try:
        client.sms.send(
            msgheader="TEST",
            messages=[{"msg": "", "no": "+905555555555"}],  # Empty message
        )
    except ApiException as e:
        print("Bad request error example:")
        print(f"Error code: {e.code}")
        print(f"Error message: {e.message}")
        print()

    # Example 3: Handle not found error
    try:
        client.sms.get_report(
            startdate="01.01.2024 00:00:00",
            stopdate="01.01.2024 23:59:59",
            jobids=["invalid_id"],
        )
    except NotFoundException as e:
        print("Not found error example:")
        print(f"Error code: {e.code}")
        print(f"Error message: {e.message}")
        print()

    # Example 4: Handle rate limit error (simulated with NotAcceptableException)
    try:
        # Simulate rate limit error by raising NotAcceptableException
        raise NotAcceptableException(
            message="Rate limit exceeded",
            code="80",  # Using the "Sending limit exceeded" code
            http_status=406,
        )
    except NotAcceptableException as e:
        print("Rate limit error example:")
        print(f"Error code: {e.code}")
        print(f"Error message: {e.message}")
        print()

    # Example 5: Handle server error
    try:
        # Simulate server error
        raise ServerException(
            message="Internal server error",
            code="500",
        )
    except ServerException as e:
        print("Server error example:")
        print(f"Error code: {e.code}")
        print(f"Error message: {e.message}")
        print()

    # Example 6: Handle generic API error
    try:
        # Simulate generic API error
        raise ApiException(
            message="Unknown error",
            code="999",
        )
    except ApiException as e:
        print("Generic API error example:")
        print(f"Error code: {e.code}")
        print(f"Error message: {e.message}")
        print()


if __name__ == "__main__":
    main()
