"""
Netgsm SMS cancellation example.
"""

from netgsm import Netgsm
from .utils import load_env_vars


def main():
    """
    Main function.
    """
    # Read values from .env file
    username, password, msgheader, appname = load_env_vars()

    # Initialize Netgsm client
    netgsm = Netgsm(username=username, password=password, appname=appname)

    # SMS job ID to be cancelled
    job_id = "12345678"  # Job ID of a previously sent SMS

    try:
        # Cancel SMS
        response = netgsm.sms.cancel(jobid=job_id)

        # Print response
        print("SMS cancelled:")
        print(f"Code: {response.get('code')}")
        print(f"Description: {response.get('description')}")
        print(f"Job ID: {response.get('jobid')}")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
