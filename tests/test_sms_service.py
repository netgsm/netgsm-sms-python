"""
SMS service test file.
"""

import unittest
from unittest import mock
import os
from dotenv import load_dotenv
from netgsm import Netgsm
from netgsm.exceptions import ApiException


class TestSmsService(unittest.TestCase):
    """
    Test class for SmsService class.
    """

    def setUp(self):
        """
        Setup to run before each test.
        """
        # Load .env file
        load_dotenv()

        # Get user credentials from environment variables or use default values
        username = os.getenv("NETGSM_USERNAME", "test_user")
        password = os.getenv("NETGSM_PASSWORD", "test_pass")
        self.msgheader = os.getenv("NETGSM_MSGHEADER", "TEST")

        # Initialize Netgsm client
        self.netgsm = Netgsm(username=username, password=password)

    @mock.patch("requests.post")
    def test_send_sms_success(self, mock_post):
        """
        Tests successful SMS sending.
        """
        # Set up mock response
        mock_response = mock.Mock()
        mock_response.json.return_value = {
            "code": "00",
            "description": "Operation successful",
            "jobid": "12345",
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        # Make SMS sending request
        response = self.netgsm.sms.send(
            msgheader=self.msgheader,
            messages=[{"msg": "Test message", "no": "5001112233"}],
        )

        # Check results
        self.assertEqual(response["code"], "00")
        self.assertEqual(response["jobid"], "12345")

        # Verify that the mock was called with correct parameters
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertIn("/sms/rest/v2/send", args[0])
        self.assertIn("msgheader", kwargs["json"])
        self.assertIn("messages", kwargs["json"])

    @mock.patch("requests.post")
    def test_send_sms_failure(self, mock_post):
        """
        Tests SMS sending failure case.
        """
        # Set up to throw an error
        mock_post.side_effect = Exception("API error")

        # Specify that we expect an error
        with self.assertRaises(ApiException):
            self.netgsm.sms.send(
                msgheader=self.msgheader,
                messages=[{"msg": "Test message", "no": "5001112233"}],
            )


if __name__ == "__main__":
    unittest.main()
