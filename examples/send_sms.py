#!/usr/bin/env python

"""
Example for sending SMS via Netgsm.
"""

import os
from dotenv import load_dotenv
from netgsm import Netgsm
from netgsm.utils.enums import Encoding
from netgsm.exceptions.api_exception import ApiException


def main():
    """Main function."""
    # Load environment variables
    load_dotenv()

    # Initialize Netgsm client
    client = Netgsm(
        username=os.getenv("NETGSM_USERNAME"),
        password=os.getenv("NETGSM_PASSWORD"),
    )

    try:
        # Define message to send
        message = {
            "msg": "Hello, this is a test message without Turkish characters.",
            "no": os.getenv("NETGSM_TEST_NUMBER"),
        }

        # Send SMS without encoding (for messages without Turkish characters)
        response = client.sms.send(msgheader=os.getenv("NETGSM_MSGHEADER"), messages=[message])

        print("SMS sent successfully without encoding!")
        print(f"JobID: {response.get('jobid')}")
        print("Response:", response)
        print()

        # Define a message with Turkish characters
        message_with_turkish = {
            "msg": "Merhaba, bu Türkçe karakterler içeren bir test mesajıdır: ğüşıöç",
            "no": os.getenv("NETGSM_TEST_NUMBER"),
        }

        # Send SMS with Turkish encoding (for messages with Turkish characters)
        response_turkish = client.sms.send(
            msgheader=os.getenv("NETGSM_MSGHEADER"),
            messages=[message_with_turkish],
            encoding=Encoding.TR,  # Specify encoding for Turkish characters
        )

        print("SMS with Turkish characters sent successfully!")
        print(f"JobID: {response_turkish.get('jobid')}")
        print("Response:", response_turkish)

    except ApiException as e:
        print(f"Error: {e.message}")
        if hasattr(e, "code") and e.code:
            print(f"Error code: {e.code}")


if __name__ == "__main__":
    main()
