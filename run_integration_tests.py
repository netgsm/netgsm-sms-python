#!/usr/bin/env python
"""
Script to run Netgsm API integration tests.

This script runs integration tests to verify the Netgsm API works in a real environment.
"""

import os
import sys
import unittest
from dotenv import load_dotenv


def run_tests():
    """
    Run integration tests.
    
    Returns:
        bool: True if all tests pass, False otherwise
    """
    # Load .env file    
    load_dotenv()
    
    # Check required environment variables
    required_vars = ['NETGSM_USERNAME', 'NETGSM_PASSWORD', 'NETGSM_MSGHEADER', 'NETGSM_TEST_NUMBER']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"\nERROR: The following environment variables must be defined: {', '.join(missing_vars)}")
        print(f"Please check or create the '.env' file.\n")
        print(f"To create an example .env file:")
        print(f"cp .env.example .env\n")
        return False
    
    # Display Netgsm credentials
    print("\n------------------------------------------")
    print("Running Netgsm API Integration Test")
    print("------------------------------------------")
    print(f"User: {os.getenv('NETGSM_USERNAME')}")
    print(f"Header: {os.getenv('NETGSM_MSGHEADER')}")
    print(f"Test Number: {os.getenv('NETGSM_TEST_NUMBER')}")
    print("------------------------------------------\n")
    
    # Get user confirmation
    user_input = input("This test will send real SMS messages and use credits from your Netgsm account. Do you want to continue? (y/n): ")
    if user_input.lower() not in ['e', 'evet', 'y', 'yes']:
        print("Test cancelled.")
        return False
    
    # Discover and run tests
    loader = unittest.TestLoader()
    test_suite = loader.discover('tests', pattern='integration_test.py')
    
    # Run test results
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Show summary
    print("\n------------------------------------------")
    print("Test Results:")
    print("------------------------------------------")
    print(f"Ran: {result.testsRun}")
    print(f"Successful: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    # Return success state
    return len(result.failures) == 0 and len(result.errors) == 0


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1) 