# Netgsm Python SDK Documentation

This document is a comprehensive resource for the Netgsm Python SDK. It contains detailed information about the installation, configuration, and usage of the SDK.

## Contents

- [Installation](#installation)
- [Authentication](#authentication)
- [SMS Service](#sms-service)
- [Error Handling](#error-handling)
- [Examples](#examples)

## Installation

```bash
pip install netgsm
```

## Authentication

To start using the SDK, you need to create a client using your Netgsm account credentials.

```python
from netgsm import Netgsm

netgsm = Netgsm(
    username="YOUR_USERNAME",
    password="YOUR_PASSWORD",
    appname="YOUR_APP_NAME"  # Optional
)
```

- `username`: Your Netgsm username
- `password`: Your Netgsm password
- `appname`: Your application name (optional, default value is used if not specified)

## SMS Service

Using the SMS service, you can send single or bulk SMS, cancel scheduled SMS, get reports of sent SMS, and list your SMS headers.

### Sending SMS

```python
response = netgsm.sms.send(
    msgheader="HEADER",
    messages=[
        {
            "msg": "Hello world!",
            "no": "5XXXXXXXXX"
        }
    ]
)
```

### Sending Bulk SMS

```python
response = netgsm.sms.send(
    msgheader="HEADER",
    messages=[
        {
            "msg": "Hello world!",
            "no": "5XXXXXXXXX"
        },
        {
            "msg": "Hello Türkiye!",
            "no": "5XXXXXXXXX"
        }
    ]
)
```

### Sending Scheduled SMS

```python
response = netgsm.sms.send(
    msgheader="HEADER",
    messages=[
        {
            "msg": "Hello world!",
            "no": "5XXXXXXXXX"
        }
    ],
    startdate="ddMMyyyyHHmm"  # Example: 010120231200 (January 1, 2023, 12:00)
)
```

### Cancelling SMS

```python
response = netgsm.sms.cancel(
    jobid="12345678"
)
```

### Getting SMS Report

```python
response = netgsm.sms.get_report(
    jobids=["12345678"]  
    # Or
    startdate="01.01.2023 00:00:00",
    stopdate="31.01.2023 23:59:59",    
)
```

### Listing SMS Headers

```python
response = netgsm.sms.get_headers()
```

## Error Handling

The SDK provides an advanced error handling mechanism to manage various error conditions that the Netgsm API may return.

### Error Types

```python
from netgsm.exceptions import (
    ApiException,           # Base API exception class
    HttpException,          # Base class for HTTP errors
    BadRequestException,    # HTTP 400
    UnauthorizedException,  # HTTP 401
    ForbiddenException,     # HTTP 403
    NotFoundException,      # HTTP 404
    NotAcceptableException, # HTTP 406
    ServerException,        # HTTP 5xx
    TimeoutException,       # Request timeout
    ConnectionException     # Connection error
)
```

### HTTP 406 Error Codes

Netgsm API may return the following error codes with HTTP 406 (Not Acceptable) status code:

| Code | Description |
|------|-------------|
| 20   | Message text may not be sent due to problem and/or exceeds standard maximum message character limit |
| 30   | Invalid username, password, or API access permission. If IP restriction is enabled, request may be made from IP outside allowed IP |
| 40   | Message header (sender name) not defined in system |
| 50   | Sending of IYS controlled messages to your account is not possible |
| 51   | No IYS Brand information defined for your subscription |
| 60   | Specified JobID not found |
| 70   | Invalid query. One or more parameters are invalid or missing |
| 80   | Sending limit exceeded |
| 85   | Repeated Sending limit exceeded. Cannot create more than 20 tasks in 1 minute for the same number |

The SDK automatically recognizes these error codes and includes the relevant description in the `NotAcceptableException`. If a code is not listed in the table, it is reported as "Undefined error code".

### Example Error Handling

```python
try:
    response = netgsm.sms.send(
        msgheader="BASLIK",
        messages=[
            {
                "msg": "Test message",
                "no": "5XXXXXXXXX"
            }
        ]
    )
    print(f"SMS sent. JobID: {response.get('jobid')}")
except NotAcceptableException as e:
    print(f"Netgsm error: {e.message}")
    print(f"HTTP status: {e.http_status}")
    print(f"Error code: {e.code}")
    
    # Perform action based on error code
    if e.code == "40":
        print("Message header not defined!")
    elif e.code == "30":
        print("Invalid or missing credentials or API access!")
    elif e.code == "20":
        print("Message text too long or invalid!")
except TimeoutException as e:
    print(f"Timeout error: {e.message}")
except ConnectionException as e:
    print(f"Connection error: {e.message}")
except ApiException as e:
    print(f"General API error: {e.message}")
```

## Examples

For more examples, see the [examples](https://github.com/netgsm/netgsm-sms-python/tree/main/examples) directory. 