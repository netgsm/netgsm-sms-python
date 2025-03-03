"""
Netgsm SMS API service containing API methods.
"""

import requests
from netgsm.exceptions.api_exception import create_api_exception


class SmsService:
    """
    Service class for Netgsm SMS operations.

    This class performs operations such as sending SMS, cancellation,
    report querying, and listing headers.
    """

    def __init__(self, client):
        """
        Initializes the SMS service.

        Args:
            client (Netgsm): Netgsm API client
        """
        self.client = client

    def send(
        self,
        msgheader,
        messages,
        encoding=None,
        startdate=None,
        stopdate=None,
        iysfilter=None,
        partnercode=None,
    ):
        """
        Sends SMS.

        Args:
            msgheader (str): SMS header/sender ID
            messages (list): List of messages to send. Each message should
                           contain 'msg' and 'no' fields.
            encoding (str, optional): Message encoding. Only use 'tr' if your message
                                    contains Turkish characters. Otherwise, leave it empty.
            startdate (str, optional): Start date (in ddMMyyyyHHmm format). Example: "011220231430" for December 1, 2023 14:30.
            stopdate (str, optional): End date (in ddMMyyyyHHmm format). Example: "011220231430" for December 1, 2023 14:30.
            iysfilter (str, optional): IYS (Message Management System)
                                     filter type.
                                     "0": Informational content
                                     "11": Commercial content for individuals
                                     "12": Commercial content for merchants
            partnercode (str, optional): Partner code

        Returns:
            dict: API response

        Raises:
            ApiException: In case of API error
        """
        url = f"{self.client.api_url}/sms/rest/v2/send"

        # Prepare request data
        data = {"msgheader": msgheader, "messages": messages}

        # Add optional parameters
        if encoding:
            data["encoding"] = encoding
        if startdate:
            data["startdate"] = startdate
        if stopdate:
            data["stopdate"] = stopdate
        if iysfilter:
            data["iysfilter"] = iysfilter
        if partnercode:
            data["partnercode"] = partnercode
        if self.client.appname:
            data["appname"] = self.client.appname

        try:
            response = requests.post(url, headers=self.client.auth_header, json=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise create_api_exception(e)

    def cancel(self, jobid):
        """
        Cancels a scheduled SMS.

        Args:
            jobid (str): SMS job ID to cancel

        Returns:
            dict: API response

        Raises:
            ApiException: In case of API error
        """
        url = f"{self.client.api_url}/sms/rest/v2/cancel"

        # Prepare request data
        data = {"jobid": jobid}

        # Add optional parameters
        if self.client.appname:
            data["appname"] = self.client.appname

        try:
            response = requests.post(url, headers=self.client.auth_header, json=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise create_api_exception(e)

    def get_report(self, startdate, stopdate, jobids=None, pagesize=None, pagenumber=None):
        """
        Retrieves the report of sent SMS.

        Args:
            startdate (str): Start date (in dd.MM.yyyy HH:mm:ss format). Example: "01.12.2023 14:30:00" for December 1, 2023 14:30:00.
            stopdate (str): End date (in dd.MM.yyyy HH:mm:ss format). Example: "01.12.2023 14:30:00" for December 1, 2023 14:30:00.
            jobids (list, optional): List of message IDs to query
            pagesize (int, optional): Record count per page (1-100)
            pagenumber (int, optional): Page number (starts from 0)

        Returns:
            dict: API response

        Raises:
            ApiException: In case of API error
        """
        url = f"{self.client.api_url}/sms/rest/v2/report"

        # Prepare request data
        data = {"startdate": startdate, "stopdate": stopdate}

        # Add optional parameters
        if jobids:
            data["jobids"] = jobids
        if pagenumber is not None:
            data["pagenumber"] = pagenumber
        if pagesize:
            data["pagesize"] = pagesize
        if self.client.appname:
            data["appname"] = self.client.appname

        try:
            response = requests.post(url, headers=self.client.auth_header, json=data, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise create_api_exception(e)

    def get_headers(self):
        """
        Lists SMS headers for the user.

        Returns:
            dict: API response

        Raises:
            ApiException: In case of API error
        """
        url = f"{self.client.api_url}/sms/rest/v2/msgheader"

        params = {"appname": self.client.appname}

        try:
            response = requests.get(url, headers=self.client.auth_header, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise create_api_exception(e)

    def get_inbox(self, startdate, stopdate, pagesize=None, pageno=None):
        """
        Lists incoming SMS for a specific date range.

        Args:
            startdate (str): Start date (in ddMMyyyyHHmmss format). Example: "01122023143000" for December 1, 2023 14:30:00.
            stopdate (str): End date (in ddMMyyyyHHmmss format). Example: "01122023143000" for December 1, 2023 14:30:00.
            pagesize (int, optional): Page size
            pageno (int, optional): Page number

        Returns:
            dict: API response

        Raises:
            ApiException: In case of API error
        """
        url = f"{self.client.api_url}/sms/rest/v2/inbox"

        params = {
            "startdate": startdate,
            "stopdate": stopdate,
            "appname": self.client.appname,
        }

        try:
            response = requests.get(url, headers=self.client.auth_header, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise create_api_exception(e)
