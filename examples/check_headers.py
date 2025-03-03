"""
Netgsm SMS headers listing example.
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

    try:
        # Get SMS headers
        response = netgsm.sms.get_headers()

        # Print response
        print("SMS Headers:")
        print(f"Code: {response.get('code')}")
        print(f"Description: {response.get('description')}")

        # List headers
        headers = response.get("msgheaders", [])
        if headers:
            print(f"\nTotal {len(headers)} headers found:")
            for i, header in enumerate(headers, 1):
                print(f"{i}. {header}")
        else:
            print("\nNo headers found.")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
