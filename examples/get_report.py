"""
Netgsm SMS report retrieval example.
"""

from netgsm import Netgsm
from datetime import datetime, timedelta
from .utils import load_env_vars


def main():
    """
    Main function.
    """
    # Read values from .env file
    username, password, msgheader, appname = load_env_vars()

    # Initialize Netgsm client
    netgsm = Netgsm(username=username, password=password, appname=appname)

    # Set date range (last 7 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)

    # Date formats (dd.MM.yyyy HH:mm:ss)
    start_date_str = start_date.strftime("%d.%m.%Y %H:%M:%S")
    end_date_str = end_date.strftime("%d.%m.%Y %H:%M:%S")

    # Optional parameters
    job_ids = ["12345678"]  # Query specific job IDs (optional)
    page_number = 0  # First page
    page_size = 20  # Results per page

    try:
        # Get SMS report
        response = netgsm.sms.get_report(
            startdate=start_date_str,
            stopdate=end_date_str,
            jobids=job_ids,
            pagenumber=page_number,
            pagesize=page_size,
        )

        # Print response
        print("SMS Report:")
        print(f"Code: {response.get('code')}")
        print(f"Description: {response.get('description')}")

        # Print SMS messages
        jobs = response.get("jobs", [])
        if jobs:
            print(f"\nTotal {len(jobs)} messages found:")
            for i, job in enumerate(jobs, 1):
                print(f"\nMessage {i}:")
                print(f"  Job ID: {job.get('jobid')}")
                print(f"  Status: {job.get('status')}")
                print(f"  Phone: {job.get('phone')}")
                print(f"  Message: {job.get('message')}")
                print(f"  Sent Date: {job.get('sentdate')}")
        else:
            print("\nNo messages found in the specified date range.")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
