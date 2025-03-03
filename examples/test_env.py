#!/usr/bin/env python
"""
.env file test example.

This example tests whether the .env file is being read correctly.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def main():
    """Main function."""
    # Print API information
    print("Netgsm API Information (from .env file):")
    print("=" * 50)

    # Get environment variables
    username = os.getenv("NETGSM_USERNAME")
    password = os.getenv("NETGSM_PASSWORD")
    msgheader = os.getenv("NETGSM_MSGHEADER")
    appname = os.getenv("NETGSM_APPNAME", "sdk-py")

    # Print values
    print(f"Username: {username}")
    print(f"Password: {'*' * len(password) if password else None}")
    print(f"Message Header: {msgheader}")
    print(f"App Name: {appname}")

    # Check for missing variables
    missing_vars = []

    if not username:
        missing_vars.append("NETGSM_USERNAME")
    if not password:
        missing_vars.append("NETGSM_PASSWORD")
    if not msgheader:
        missing_vars.append("NETGSM_MSGHEADER")

    # Print warning if any variables are missing
    if missing_vars:
        print("\nWARNING: The following variables are not defined in .env:")
        for var in missing_vars:
            print(f"  - {var}")


if __name__ == "__main__":
    main()
