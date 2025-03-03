# Netgsm Python SDK

Official Python SDK for Netgsm SMS API. With this SDK, you can send SMS, cancel sent SMS, query reports, and more.

## Installation

```bash
pip install netgsm
```

## Usage

```python
from netgsm import Netgsm

# Initialize the SDK
netgsm = Netgsm(
    username="YOUR_USERNAME",   # Your Netgsm username
    password="YOUR_PASSWORD",   # Your Netgsm password
    appname="YOUR_APP_NAME"     # Optional, your application name 
)

# Send SMS
response = netgsm.sms.send(
    msgheader="HEADER",
    messages=[
        {
            "msg": "Hello, this is a test message.",
            "no": "5XXXXXXXXX"
        }
    ]
)

print(response)
```

## Features

- SMS sending and cancellation
- SMS report querying
- SMS header listing
- IYS filtering support
- Advanced error handling

## Documentation

For more detailed usage examples and complete API reference, see the [documentation](https://github.com/netgsm/netgsm-sms-python/tree/main/docs) directory.

## Examples

For more examples, see the [examples](https://github.com/netgsm/netgsm-sms-python/tree/main/examples) directory.

## Example Usage

```python
from netgsm import Netgsm

netgsm = Netgsm(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    appname="YOUR_APP_NAME"  # Optional
)

# Send SMS
response = netgsm.sms.send(
    msgheader="HEADER",
    messages=[
        {
            "msg": "Hello world!",
            "no": "5XXXXXXXXX"
        }
    ]
)

print(response)
```

### Using Environment Variables (.env)

In the examples that come with the SDK, user credentials are read from the `.env` file. To run the example applications, create a `.env` file in the project root directory and add the following information:

```
NETGSM_USERNAME=YOUR_USERNAME
NETGSM_PASSWORD=YOUR_PASSWORD
NETGSM_MSGHEADER=YOUR_SMS_HEADER
NETGSM_APPNAME=YOUR_APP_NAME
```

You can start by copying the `.env.example` file:

```bash
cp .env.example .env
```

Then update the `.env` file with your own information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Error Handling

The SDK provides an advanced error handling mechanism to manage various error conditions that the Netgsm API may return.

### Error Types

```python
from netgsm.exceptions.api_exception import (
    ApiException,           # Base API exception class
    HttpException,          # Base class for HTTP errors
    BadRequestException,    # HTTP 400 errors
    UnauthorizedException,  # HTTP 401 errors
    ForbiddenException,     # HTTP 403 errors
    NotFoundException,      # HTTP 404 errors
    NotAcceptableException, # HTTP 406 errors (Netgsm errors usually return this way)
    TimeoutException,       # Timeout errors
    ConnectionException,    # Connection errors
    ServerException         # HTTP 5XX server errors
)
```

### Example Usage

```python
from netgsm import Netgsm
from netgsm.exceptions.api_exception import ApiException, NotAcceptableException

# Initialize Netgsm client
netgsm = Netgsm(username="user", password="pass")

try:
    # Send SMS
    response = netgsm.sms.send(
        msgheader="HEADER",
        messages=[
            {
                "msg": "Test message",
                "no": "5XXXXXXXXX"
            }
        ]
    )
    print(f"SMS sent. JobID: {response.get('jobid')}")
except NotAcceptableException as e:
    # Error returned by Netgsm
    print(f"Netgsm error: {e.message}")
    print(f"HTTP status: {e.http_status}")
    print(f"Error code: {e.code}")
except ApiException as e:
    # General API error
    print(f"API error: {e.message}")
```

### HTTP Status Codes

- **HTTP 200 (OK)**: Operation successful
- **HTTP 406 (Not Acceptable)**: Netgsm API errors (e.g., invalid JobID, invalid header)

### Netgsm API Error Codes

The Netgsm API may return the following error codes with HTTP 406 status code:

| Code | Description |
|------|-------------|
| 20   | Could not be sent due to a problem in the message text or exceeded the standard maximum message character count |
| 30   | Invalid username, password or no API access permission. If IP restriction exists, request may have been made from an unauthorized IP |
| 40   | Message header (sender name) is not defined in the system |
| 50   | IYS controlled submissions cannot be made with your subscriber account |
| 51   | No IYS Brand information found for your subscription |
| 60   | Specified JobID not found |
| 70   | Invalid query. One of the parameters is incorrect or a required field is missing |
| 80   | Sending limit exceeded |
| 85   | Duplicate sending limit exceeded. Cannot create more than 20 tasks for the same number within 1 minute |

The SDK automatically recognizes these error codes and includes the relevant description in the `NotAcceptableException`. If the error code is not found in the table above, it is reported as "Undefined error code".

### Error Codes Example

For an example of how to catch and handle different error codes, see the [Error Codes Example](https://github.com/netgsm/netgsm-sms-python/blob/main/examples/error_codes_example.py).

```python
try:
    response = netgsm.sms.send(...)
except NotAcceptableException as e:
    if e.code == "40":
        print("Message header is not defined!")
    elif e.code == "30":
        print("Invalid credentials or no API access!")
    else:
        print(f"Netgsm error: {e.message}")
```

For more detailed information, see the [Error Handling Example](https://github.com/netgsm/netgsm-sms-python/blob/main/examples/error_handling_example.py). 