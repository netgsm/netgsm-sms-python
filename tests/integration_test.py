"""
Netgsm API Integration Test.

This test file tests the Netgsm API in a real environment.
To run it, you need to create an .env file with your valid Netgsm credentials.
"""

import unittest
import os
import uuid
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from netgsm import Netgsm
from netgsm.exceptions.api_exception import (
    ApiException,
    NotAcceptableException,
    TimeoutException,
    ConnectionException,
    ServerException,
)


class NetgsmIntegrationTest(unittest.TestCase):
    """
    Integration test class for Netgsm API.

    This class tests whether the Netgsm API works in a real environment.
    """

    @classmethod
    def setUpClass(cls):
        """
        Setup to run once before all tests.
        """
        # Load .env file
        load_dotenv()

        # Check required environment variables
        required_vars = [
            "NETGSM_USERNAME",
            "NETGSM_PASSWORD",
            "NETGSM_MSGHEADER",
            "NETGSM_TEST_NUMBER",
        ]
        missing_vars = [var for var in required_vars if not os.getenv(var)]

        if missing_vars:
            raise EnvironmentError(
                f"The following environment variables must be defined: {', '.join(missing_vars)}"
            )

        # Get user credentials from environment variables
        cls.username = os.getenv("NETGSM_USERNAME")
        cls.password = os.getenv("NETGSM_PASSWORD")
        cls.msgheader = os.getenv("NETGSM_MSGHEADER")
        cls.test_number = os.getenv("NETGSM_TEST_NUMBER")

        # Initialize Netgsm client
        cls.netgsm = Netgsm(username=cls.username, password=cls.password)

        # Define variables needed for testing
        cls.sent_jobid = None  # jobid value for normally sent SMS
        cls.scheduled_jobid = None  # jobid value for scheduled SMS

        print("\n--------------------------------")
        print("Netgsm API Integration Test")
        print("--------------------------------")

    def test_01_list_headers(self):
        """
        Test 1: List SMS headers and check if the header in the .env file is in the list.
        """
        print("\n1. Testing SMS headers listing...")

        try:
            # Get SMS headers
            response = self.netgsm.sms.get_headers()

            # Check response
            self.assertEqual(response.get("code"), "00", "Could not get header list")

            # Get the list of headers
            headers = response.get("msgheaders", [])

            # Check if the header in .env is in the list
            self.assertIn(
                self.msgheader,
                headers,
                f"Header {self.msgheader} not found in the list",
            )

            print(f"✓ Header list retrieved. Total {len(headers)} headers found.")
            print(f"✓ '{self.msgheader}' header verified.")
        except ServerException as e:
            print(f"✗ Server error: [{e.http_status}] {e.message}")
            if e.code:
                print(f"✗ API code: {e.code}")
            raise
        except ConnectionException as e:
            print(f"✗ Connection error: {e.message}")
            raise
        except TimeoutException as e:
            print(f"✗ Timeout error: {e.message}")
            raise
        except ApiException as e:
            print(f"✗ API error: {e.message}")
            if hasattr(e, "http_status") and e.http_status:
                print(f"✗ HTTP Status: {e.http_status}")
            if e.code:
                print(f"✗ API code: {e.code}")
            raise

    def test_02_send_sms(self):
        """
        Test 2: Send SMS to a single number.
        """
        print("\n2. Testing SMS sending to a single number...")

        try:
            # Create test message
            test_message = (
                "This is an API integration test message. "
                f"Date: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
            )

            # Send SMS
            response = self.netgsm.sms.send(
                msgheader=self.msgheader,
                messages=[{"msg": test_message, "no": self.test_number}],
            )

            # Check response
            self.assertEqual(response.get("code"), "00", "SMS could not be sent")
            self.assertIsNotNone(response.get("jobid"), "JobID could not be obtained")

            # Save the JobID (to be used in other tests)
            self.__class__.sent_jobid = response.get("jobid")

            print(f"✓ SMS successfully sent. Job ID: {self.__class__.sent_jobid}")

            # After sending SMS, wait a bit for the report to be generated
            print("   Waiting 10 seconds for the report to be generated...")
            time.sleep(10)
        except ServerException as e:
            print(f"✗ Server error: [{e.http_status}] {e.message}")
            if e.code:
                print(f"✗ API code: {e.code}")
            raise
        except ConnectionException as e:
            print(f"✗ Connection error: {e.message}")
            raise
        except TimeoutException as e:
            print(f"✗ Timeout error: {e.message}")
            raise
        except ApiException as e:
            print(f"✗ API error: {e.message}")
            if hasattr(e, "http_status") and e.http_status:
                print(f"✗ HTTP Status: {e.http_status}")
            if e.code:
                print(f"✗ API code: {e.code}")
            raise

    def test_03_send_scheduled_sms(self):
        """
        Test 3: Send scheduled SMS test.
        """
        print("\n3. Testing scheduled SMS sending...")

        try:
            # Create date for tomorrow
            tomorrow = datetime.now() + timedelta(days=1)
            tomorrow = tomorrow.replace(second=0, microsecond=0)

            # Create test message
            test_message = (
                "This is a scheduled API integration test message. "
                f"Planned delivery: {tomorrow.strftime('%d.%m.%Y %H:%M')}"
            )

            # Send scheduled SMS - Using the correct format (ddMMyyyyHHmm)
            response = self.netgsm.sms.send(
                msgheader=self.msgheader,
                messages=[{"msg": test_message, "no": self.test_number}],
                startdate=tomorrow.strftime("%d%m%Y%H%M"),
            )

            # Check response
            self.assertEqual(response.get("code"), "00", "Scheduled SMS could not be sent")
            self.assertIsNotNone(response.get("jobid"), "JobID could not be obtained")

            # Save the JobID (to be used in other tests)
            self.__class__.scheduled_jobid = response.get("jobid")

            print(
                "✓ Scheduled SMS successfully planned. " f"Job ID: {self.__class__.scheduled_jobid}"
            )
            print("✓ Planned delivery time: " f"{tomorrow.strftime('%d.%m.%Y %H:%M')}")
        except ServerException as e:
            print(f"✗ Server error: [{e.http_status}] {e.message}")
            if e.code:
                print(f"✗ API code: {e.code}")
            raise
        except ConnectionException as e:
            print(f"✗ Connection error: {e.message}")
            raise
        except TimeoutException as e:
            print(f"✗ Timeout error: {e.message}")
            raise
        except ApiException as e:
            print(f"✗ API error: {e.message}")
            if hasattr(e, "http_status") and e.http_status:
                print(f"✗ HTTP Status: {e.http_status}")
            if e.code:
                print(f"✗ API code: {e.code}")
            raise

    def test_04_cancel_scheduled_sms(self):
        """
        Test 4: Cancel scheduled SMS.
        """
        print("\n4. Testing scheduled SMS cancellation...")

        try:
            # Check if we have the scheduled SMS jobid
            self.assertIsNotNone(
                self.__class__.scheduled_jobid, "Scheduled SMS jobid value not found"
            )

            # Cancel the scheduled SMS
            response = self.netgsm.sms.cancel(jobid=self.__class__.scheduled_jobid)

            # Check response
            self.assertEqual(response.get("code"), "00", "Scheduled SMS cancelled")

            print(
                f"✓ Scheduled SMS successfully cancelled. Job ID: {self.__class__.scheduled_jobid}"
            )
        except ServerException as e:
            print(f"✗ Server error: [{e.http_status}] {e.message}")
            if e.code:
                print(f"✗ API code: {e.code}")
            raise
        except ConnectionException as e:
            print(f"✗ Connection error: {e.message}")
            raise
        except TimeoutException as e:
            print(f"✗ Timeout error: {e.message}")
            raise
        except ApiException as e:
            print(f"✗ API error: {e.message}")
            if hasattr(e, "http_status") and e.http_status:
                print(f"✗ HTTP Status: {e.http_status}")
            if e.code:
                print(f"✗ API code: {e.code}")
            raise

    def test_05_cancel_sent_sms(self):
        """
        Test 5: Try to cancel an already sent SMS (error expected).
        """
        print("\n5. Trying to cancel an already sent SMS (error expected)...")

        # Check if we have the sent SMS jobid
        self.assertIsNotNone(self.__class__.sent_jobid, "Sent SMS jobid value not found")

        try:
            # Cancel the sent SMS (this operation should fail)
            response = self.netgsm.sms.cancel(jobid=self.__class__.sent_jobid)

            # If cancellation is successful, fail the test
            if response.get("code") == "00":
                self.fail("Sent SMS cancelled, but error was expected")
            else:
                # Check error code
                print(f"✓ Expected error code: {response.get('code')}")
        except NotAcceptableException as e:
            # If HTTP 406 error is received, test is successful
            print(f"✓ Expected NotAcceptableException error: HTTP {e.http_status}")
            if e.code:
                print(f"✓ API code: {e.code}")
        except ApiException as e:
            print(f"✓ Expected API error: {e.message}")
            if hasattr(e, "http_status") and e.http_status:
                print(f"✓ HTTP Status: {e.http_status}")
            if e.code:
                print(f"✓ API code: {e.code}")

    def test_06_get_report_for_sent_sms(self):
        """
        Test 6: Get report for sent SMS.
        """
        print("\n6. Getting report for sent SMS...")

        # Check if we have the sent SMS jobid
        self.assertIsNotNone(self.__class__.sent_jobid, "Sent SMS jobid value not found")

        # Set date range (last 1 day)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1)

        # Date formats
        start_date_str = start_date.strftime("%d.%m.%Y %H:%M:%S")
        end_date_str = end_date.strftime("%d.%m.%Y %H:%M:%S")

        try:
            # Get report
            response = self.netgsm.sms.get_report(
                startdate=start_date_str, stopdate=end_date_str, jobids=[self.__class__.sent_jobid]
            )

            # Check response
            self.assertEqual(response.get("code"), "00", "SMS report could not be obtained")

            # Check jobs list
            jobs = response.get("jobs", [])
            self.assertTrue(len(jobs) > 0, "SMS report is empty")

            # Check first job's jobid
            first_job = jobs[0]
            self.assertEqual(first_job.get("jobid"), self.__class__.sent_jobid, "JobID mismatch")

            print(f"✓ SMS report successfully obtained. Job ID: {self.__class__.sent_jobid}")
            print(f"✓ Message status: {first_job.get('status')}")
        except ServerException as e:
            print(f"✗ Server error: [{e.http_status}] {e.message}")
            if e.code:
                print(f"✗ API code: {e.code}")
            raise
        except ConnectionException as e:
            print(f"✗ Connection error: {e.message}")
            raise
        except TimeoutException as e:
            print(f"✗ Timeout error: {e.message}")
            raise
        except ApiException as e:
            print(f"✗ API error: {e.message}")
            if hasattr(e, "http_status") and e.http_status:
                print(f"✗ HTTP Status: {e.http_status}")
            if e.code:
                print(f"✗ API code: {e.code}")
            raise

    def test_07_get_report_for_invalid_jobid(self):
        """
        Test 7: Get report for invalid jobid (error expected).
        """
        print("\n7. Getting report for invalid jobid...")

        # Generate random jobid
        random_jobid = str(uuid.uuid4().int)[:10]

        # Set date range (last 1 day)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1)

        # Date formats
        start_date_str = start_date.strftime("%d.%m.%Y %H:%M:%S")
        end_date_str = end_date.strftime("%d.%m.%Y %H:%M:%S")

        try:
            # Get report (this operation should fail)
            response = self.netgsm.sms.get_report(
                startdate=start_date_str, stopdate=end_date_str, jobids=[random_jobid]
            )

            # Check response (expected error code 60)
            self.assertNotEqual(response.get("code"), "00", "Unexpected success for invalid jobid")
            print(f"✓ Expected error code: {response.get('code')}")
        except NotAcceptableException as e:
            # If HTTP 406 error is received, test is successful
            print(f"✓ Expected NotAcceptableException error: HTTP {e.http_status}")
            if e.code:
                print(f"✓ API code: {e.code}")
        except ApiException as e:
            print(f"✓ Expected API error: {e.message}")
            if hasattr(e, "http_status") and e.http_status:
                print(f"✓ HTTP Status: {e.http_status}")
            if e.code:
                print(f"✓ API code: {e.code}")

    def test_08_get_inbox_messages(self):
        """
        Test 8: Get inbox messages for the last 7 days.
        """
        print("\n8. Getting inbox messages for the last 7 days...")

        # Set date range (last 7 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        # Date formats (ddMMyyyyHHmmss)
        start_date_str = start_date.strftime("%d%m%Y%H%M%S")
        end_date_str = end_date.strftime("%d%m%Y%H%M%S")

        try:
            # Get inbox messages
            response = self.netgsm.sms.get_inbox(startdate=start_date_str, stopdate=end_date_str)

            # Check response
            self.assertIn("code", response, "Inbox retrieval failed")

            # Display messages
            if response.get("code") == "00":
                messages = response.get("messages", [])
                print(f"✓ Inbox successfully retrieved. {len(messages)} messages found.")
            else:
                print(
                    f"✓ Inbox retrieved, but no messages found or other status: {response.get('code')}"
                )
        except ServerException as e:
            print(f"✗ Server error: [{e.http_status}] {e.message}")
            if e.code:
                print(f"✗ API code: {e.code}")
            raise
        except ConnectionException as e:
            print(f"✗ Connection error: {e.message}")
            raise
        except TimeoutException as e:
            print(f"✗ Timeout error: {e.message}")
            raise
        except ApiException as e:
            print(f"✗ API error: {e.message}")
            if hasattr(e, "http_status") and e.http_status:
                print(f"✗ HTTP Status: {e.http_status}")
            if e.code:
                print(f"✗ API code: {e.code}")
            raise


if __name__ == "__main__":
    unittest.main()
