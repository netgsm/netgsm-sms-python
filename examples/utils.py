#!/usr/bin/env python
"""
Utility functions for examples.
"""

import os
from dotenv import load_dotenv


def load_env_vars():
    """
    Load environment variables from .env file.

    Returns:
        tuple: (username, password, msgheader, appname)
    """
    # Load environment variables from .env file
    load_dotenv()

    # Get environment variables
    username = os.getenv("NETGSM_USERNAME")
    password = os.getenv("NETGSM_PASSWORD")
    msgheader = os.getenv("NETGSM_MSGHEADER")
    appname = os.getenv("NETGSM_APPNAME", "sdk-py")

    return username, password, msgheader, appname
