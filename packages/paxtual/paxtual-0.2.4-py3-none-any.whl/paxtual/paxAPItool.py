import aiohttp
import time
import hashlib
import hmac
from urllib.parse import urlencode, urlunsplit
import os
from .pax_exceptions import InvalidOperationError, TerminalNotAvailableError, TerminalNotFoundError


class PaxApiTool():
    """
    Creates an aiohttp.ClientSession request object to interface with the public PaxStore API.

    Required parameters:
        apiKey (str): Your PaxStore API key.
        apiSecret (str): Your PaxStore API secret.
        session (aiohttp.ClientSession): An active aiohttp client session.
        operation (str): The API operation to perform.

    Possible operations:
        'createTerminal', 'findTerminal', 'activateTerminal', 'disableTerminal', 
        'moveTerminal', 'updateTerminal', 'deleteTerminal', 'terminalDetails', 
        'accessoryDetails', 'pushCommand', 'pushParamAPK', 'pushAPK', 'pushRKI', 
        'pushFirmware', 'terminalConfig', 'appPushHistory', 'pushStatus', 'uninstallApk'
    """

    def __init__(self, apiKey, apiSecret, session: aiohttp.ClientSession, operation: str, 
                 terminalId: str | None = None, serialNo=None, merchantName=None, 
                 modelName=None, name=None, resellerName=None, status=None, command=None, 
                 packageName=None, pushTemplateName=None, templateName=None, version=None, 
                 rkiKey=None, fmName=None, list=None) -> None:
        """
        Initializes a PaxApiTool object with the provided parameters.
        """

        self.apiKey = apiKey  # Store the API key
        self.apiSecret = apiSecret  # Store the API secret
        self.baseUrl = "https://api.paxstore.us"  # Base URL for the PaxStore API
        self.scheme = "https"  # URL scheme (https)
        self.netloc = "api.paxstore.us"  # Network location (domain) for the API
        self.session = session  # Store the aiohttp client session
        self.operation = operation  # Store the desired API operation

        # Terminal-related attributes
        self.terminalId = terminalId
        self.serialNo = serialNo
        self.merchantName = merchantName
        self.modelName = modelName
        self.name = name
        self.resellerName = resellerName
        self.status = status

        # Operation-specific attributes
        self.command = command
        self.packageName = packageName
        self.pushTemplateName = pushTemplateName
        self.templateName = templateName
        self.version = version
        self.rkiKey = rkiKey
        self.fmName = fmName
        self.list = list

        # Query parameters for the API request
        self.query = {
            "sysKey": self.apiKey,  # API key
            "timeStamp": round(time.time() * 1000)  # Current timestamp in milliseconds
        }

        # If a list is provided, join its elements into a comma-separated string
        if self.list:
            self.unpacked = str(f'{", ".join(self.list)}')
        else:
            self.unpacked = None

        # Dictionary mapping API operations to their corresponding request details
        self.operations_dict = {
            "createTerminal": {
                "path": "/p-market-api/v1/3rdsys/terminals",  # API endpoint path
                "method": self.session.post,  # HTTP method (POST)
                "str_method": "post",  # String representation of the HTTP method (used for requests.Session if not async)
                "addQuery": None,  # Additional query parameters (None for this operation)
                "body": {  # Request body
                    "merchantName": self.merchantName,
                    "modelName": self.modelName,
                    "name": self.name,
                    "resellerName": self.resellerName,
                    "serialNo": self.serialNo,
                    "status": self.status
                }
            },
            "findTerminal": {
                "path": "/p-market-api/v1/3rdsys/terminals",
                "method": self.session.get,
                "str_method": "get",
                "addQuery": {  # Additional query parameters
                    "snNameTID": self.serialNo
                },
                "body": None  # No request body for this operation
            },
            "activateTerminal": {
                "path": f"/p-market-api/v1/3rdsys/terminals/{self.terminalId}/active",
                "method": self.session.put,
                "str_method": "put",
                "addQuery": None,
                "body": None
            },
            "disableTerminal" : {
                "path": f"/p-market-api/v1/3rdsys/terminals/{self.terminalId}/disable",
                "method": self.session.put,
                "str_method": "put",
                "addQuery": None,
                "body": None
            },
            "moveTerminal" : {
                "path": f"/p-market-api/v1/3rdsys/terminals/{self.terminalId}/move",
                "method": self.session.put,
                "addQuery": None,
                "str_method": "put",
                "body": {
                    "merchantName": self.merchantName,
                    "resellerName": self.resellerName
                }
            },
            "updateTerminal" : {
                "path" : f"/p-market-api/v1/3rdsys/terminals/{self.terminalId}",
                "method" : self.session.put,
                "str_method": "put",
                "addQuery": None,
                "body": {
                    "merchantName":self.merchantName,
                    "modelName":self.modelName,
                    "name":self.name,
                    "resellerName":self.resellerName,
                    "serialNo":self.serialNo,
                    "status":self.status,
                }
            },
            "deleteTerminal" : {
                "path" : f"/p-market-api/v1/3rdsys/terminals/{self.terminalId}",
                "method": self.session.delete,
                "str_method": "delete",
                "addQuery": None,
                "body": None
            },
            "terminalDetails" : {
                "path" : f"/p-market-api/v1/3rdsys/terminals/{self.terminalId}",
                "method": self.session.get,
                "str_method": "get",
                "addQuery" : {
                    "includeDetailInfo" : "true",
                },
                "body": None
            },
            "accessoryDetails" : {
                "path" : f"/p-market-api/v1/3rdsys/terminals/{self.terminalId}",
                "method": self.session.get,
                "str_method": "get",
                "addQuery" : {
                    "includeDetailInfo": "true",
                    "includeDetailInfoList" : "true"
                },
                "body": None
            },
            "pushCommand": {
                "path": f"/p-market-api/v1/3rdsys/terminals/{self.terminalId}/operation",
                "method": self.session.post,
                "str_method": "post",
                "addQuery": {
                    "command": self.command
                },
                "body": None
            },
            "pushParamAPK": {
                "path": "/p-market-api/v1/3rdsys/terminalApks",
                "method": self.session.post,
                "str_method": "post",
                "addQuery": None,
                "body": {
                    "packageName": self.packageName,
                    "pushTemplateName": self.pushTemplateName,
                    "serialNo": self.serialNo,
                    "templateName": self.templateName,
                    "version": self.version
                }
            },
            "pushAPK": {
                "path": "/p-market-api/v1/3rdsys/terminalApks",
                "method": self.session.post,
                "str_method": "post",
                "addQuery": None,
                "body": {
                    "packageName": self.packageName,
                    "serialNo": self.serialNo
                }  
            },
            "pushRKI": {
                "path": "/p-market-api/v1/3rdsys/terminalRkis",
                "method": self.session.post,
                "str_method": "post",
                "addQuery": None,
                "body": {
                    "rkiKey": self.rkiKey,
                    "serialNo": self.serialNo
                }
            },
            "pushFirmware": {
                "path": "/p-market-api/v1/3rdsys/terminalFirmwares",
                "method": self.session.post,
                "str_method": "post",
                "addQuery": None,
                "body": {
                    
                    "fmName": self.fmName,
                    "serialNo": self.serialNo
                }
            },
            "terminalConfig":{
                "path":"/p-market-api/v1/3rdsys/terminals",
                "method":self.session.get,
                "str_method": "get",
                "addQuery": {
                    "includeInstalledApks":"true",
                    "includeInstalledFirmware": "true",
                    "pageNo":"",
                    "pageSize":"",
                    "snNameTID": self.serialNo,

                },
                "body": None
            },
            "appPushHistory": {
                "path": "/p-market-api/v1/3rdsys/parameter/push/history",
                "method":self.session.get,
                "str_method": "get",
                "addQuery": {
                    "onlyLastPushHistory": "false",
                    "packageName": self.packageName,
                    "pageNo": 1,
                    "pageSize": 20,
                    "pushStatus":2,
                    "serialNo": self.serialNo
                },
                "body": None
            },
            'pushStatus':{
                "path": "/p-market-api/v1/3rdsys/terminalApks",
                "method": self.session.get,
                "str_method": "get",
                "addQuery": {
                    "pageNo": 1,
                    "pageSize": 20,                
                    "terminalTid": self.terminalId,
                    },
                    "body": None
            },
            "uninstallApk":{
                "path": "/p-market-api/v1/3rdsys/terminalApks/uninstall",
                "method": self.session.post,
                "str_method": "post",
                "addQuery": None,
                "body": {
                    "packageName": self.packageName,
                    "serialNo": self.serialNo
                    },      
            }
        }
        # Determine the request details based on the provided operation
        v = self.operations_dict.get(self.operation)
        if v:
            self.path = v["path"]  # Get the API endpoint path
            if v["addQuery"]:
                self.query.update(v["addQuery"])  # Add any additional query parameters
            if v["body"]:
                self.body = v["body"]  # Get the request body
            else:
                self.body = None
            self.method = v["method"]  # Get the HTTP method
            self.str_method = v["str_method"]  # Get the string representation of the HTTP method
            # Construct the full URL
            self.encodedQuery = urlencode(self.query)  # URL-encode the query parameters
            self.fullurl = urlunsplit((self.scheme, self.netloc, self.path, self.encodedQuery, None))
            # Generate the signature for authentication
            self.signature = hmac.new(self.apiSecret, self.encodedQuery.encode('utf-8'), hashlib.md5).hexdigest().upper()
        else:
            raise InvalidOperationError 
        


async def buildRequest(session, operation: str, **kwargs):
    """
    Builds and sends an asynchronous request to the PAX API.

    This function handles constructing the API request, including authentication,
    sending the request, processing the response, and handling potential errors.

    Args:
        session: An HTTP session object for making API requests.
        operation: The API operation to perform (e.g., "findTerminal", "createTerminal").
        **kwargs: Keyword arguments containing additional data for the operation 
                  (e.g., serialNo).

    Returns:
        dict: The parsed JSON data from the API response.

    Raises:
        TerminalNotFoundError: If the "findTerminal" operation fails to find a terminal.
        TerminalNotAvailableError: If the "createTerminal" operation fails. 
    """

    apiKey = os.environ.get("APIKEY").encode('utf-8')
    apiSecret = os.environ.get("APISECRET").encode("utf-8")
    # Create a PaxApiTool instance to handle request construction and authentication
    term = PaxApiTool(apiKey, apiSecret, session, operation, **kwargs)  
    # Prepare request headers with content type and signature
    headers = {
        "Content-Type": "application/json; charset=UTF-8", 
        "signature": term.signature
    }  
    method = term.method  # Get the HTTP method (GET, POST, etc.)
    # Print request details for debugging (consider using a logging library instead)
    print(term.body)  
    print(term.fullurl)  
    # Send the asynchronous request using the appropriate HTTP method
    async with method(term.fullurl, json=term.body, headers=headers) as resp:  
        term_data = await resp.json(content_type=None)  # Parse the JSON response
        # Error handling for specific operations
        if operation == "findTerminal" and not term_data["dataset"]:  
            serial_no = kwargs.get("serialNo", None)  
            raise TerminalNotFoundError(serial_no)  # Raise error if terminal not found
        if operation == "createTerminal" and term_data['businessCode'] == 2332:  
            serial_no = kwargs.get("serialNo", None)  
            raise TerminalNotAvailableError(serial_no)  # Raise error if terminal creation fails
    return term_data  # Return the parsed JSON data