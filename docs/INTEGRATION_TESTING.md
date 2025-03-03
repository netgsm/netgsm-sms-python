# Netgsm Python SDK Integration Tests

This document describes the tests used to test the integration of the Netgsm Python SDK with the actual API.

## Requirements

- Valid credentials for Netgsm API access
- A valid phone number to which test SMS can be sent
- All required variables defined in the `.env` file

## Preparing the Tests

1. First, create the `.env` file:

```bash
cp .env.example .env
```

2. Edit the `.env` file to add your Netgsm credentials and test number:

```
NETGSM_USERNAME=YOUR_USERNAME
NETGSM_PASSWORD=YOUR_PASSWORD
NETGSM_MSGHEADER=YOUR_SMS_HEADER
NETGSM_APPNAME=YOUR_APP_NAME  # Optional
NETGSM_TEST_NUMBER=5XXXXXXXXX  # Valid phone number to send SMS to
```

> **Important:** You need to add a valid phone number for the `NETGSM_TEST_NUMBER` value. Test SMS messages will be sent to this number.

## Running the Tests

To run the tests:

```bash
python run_integration_tests.py
```

This command will run the integration tests and print the results to the console.

> **Note:** Integration tests make calls to the actual Netgsm API and may deduct credits from your Netgsm account. You will be asked for confirmation before the test starts.

## Test Scenarios

The integration test tests the following scenarios:

1. **Listing Headers**: Lists SMS headers and checks if the header specified in the `.env` file is in the list.

2. **Sending SMS**: Sends a test SMS to the number specified in the `.env` file.

3. **Sending Scheduled SMS**: Creates an SMS scheduled to be sent one day later.

4. **Cancelling Scheduled SMS**: Cancels the scheduled SMS created in step 3 and checks if an HTTP 200 OK response is received.

5. **Trying to Cancel a Sent SMS**: Tries to cancel the SMS sent in step 2. This operation should fail and return an HTTP 406 error response.

6. **Querying SMS Report**: Queries the report of the SMS sent in step 2.

7. **Querying Report with Invalid JobID**: Tries to query a report using a random JobID. This operation should fail and return an HTTP 406 code 60 error response.

8. **Querying Inbox**: Queries inbox messages for the last 7 days.

## HTTP Status Codes and Error Handling

The Netgsm API returns different HTTP status codes and custom error codes. The SDK interprets these codes as follows:

### HTTP Status Codes

- **HTTP 200 (OK)**: Operation successful.
- **HTTP 400 (Bad Request)**: Request format is incorrect.
- **HTTP 401 (Unauthorized)**: Authorization failed, credentials are incorrect.
- **HTTP 403 (Forbidden)**: You don't have permission for the operation.
- **HTTP 404 (Not Found)**: The requested resource was not found.
- **HTTP 406 (Not Acceptable)**: Operation not acceptable, Netgsm API returned an error related to the operation.
- **HTTP 408 (Request Timeout)**: Request timed out.
- **HTTP 5XX (Server Error)**: Server error occurred.

### Custom Exception Classes

The SDK uses a custom exception class for each HTTP status code:

- `ApiException`: Base API exception class.
- `HttpException`: Base class for HTTP errors.
- `BadRequestException`: For HTTP 400 errors.
- `UnauthorizedException`: For HTTP 401 errors.
- `ForbiddenException`: For HTTP 403 errors.
- `NotFoundException`: For HTTP 404 errors.
- `NotAcceptableException`: For HTTP 406 errors. Netgsm API usually returns errors related to operations with this code.
- `TimeoutException`: Represents request timeouts.
- `ConnectionException`: Represents connection errors.
- `ServerException`: Represents HTTP 5XX server errors.

Each exception contains the following information:

- `message`: Error message
- `code`: Netgsm API error code
- `http_status`: HTTP status code
- `response`: Original API response

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

The SDK automatically recognizes these error codes and provides more user-friendly error messages. If the error code is not in the above list, it is marked as "Undefined error code".

### Error Handling in Integration Tests

Integration tests use try-except blocks for each API call and catch the appropriate exception types. This allows us to handle different types of errors correctly and report test results in more detail.

As in tests 5 and 7, some tests deliberately create errors and expect to catch the expected exception type.

## Interpreting Test Results

The test output will show the result of each test. A "OK" mark will be shown for successful tests, and a "FAIL" mark for failed tests.

If all tests are successful, it can be understood that your Netgsm API integration is working correctly.

## Troubleshooting

If integration tests fail:

1. Make sure the credentials in the `.env` file are correct.
2. Check that your Netgsm account is active and has sufficient credit.
3. Check that the specified header is defined in your account.
4. Make sure the test number is valid and accessible.
5. Make sure there are no restrictions on your Netgsm API access.

### Common Error Codes

Common error codes returned by the Netgsm API:

- **30** - Invalid username, password, or API access is inactive
- **40** - Message header (originator) is not defined in the system
- **60** - Specified JobID not found
- **70** - Invalid query, missing or incorrect parameters
- **85** - Customer IP address restricted

For each of these error codes that return with HTTP 406 status code, a `NotAcceptableException` exception is thrown and the corresponding error code is in the `code` field.

If problems persist, try to identify the problem by examining the error messages. Contact the Netgsm support team if necessary. 