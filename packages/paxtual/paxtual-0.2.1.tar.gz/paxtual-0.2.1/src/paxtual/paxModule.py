import asyncio
import aiohttp
import hmac
import time
import hashlib
from urllib.parse import urlencode, urlunsplit
import pandas as pd
import os
from .tui_exceptions import TerminalNotFoundError, InvalidOperationError


class PaxTerms():
    """
    This class stores and manages information about different PAX terminal models, 
    their accessories, and associated software packages.
    """
    def __init__(self, serialNo:str,**kwargs) -> None:
        """
        Initializes a PaxTerms object with the given serial number.

        Args:
            serialNo (str): The serial number of the PAX terminal.
            **kwargs: Optional keyword arguments (not used in the current implementation).
        """
        # Dictionary containing data for various terminal models
        self.termtool = {
            "119": {"modelName": "E600", "serial_range":"119", "name":"TR_E600", "type":"Ev1_Series", "terminal_no":"12", "resellerName": "Repair","fmName":"E600_PayDroid_7.1.1_Virgo_V04.1.18_20240124", "hasAccessory":True, "accessory":
            {"modelName":"Q20L", "serial_range": "114", "name": "TR_E600-Q20", "type":"Qv1_Series", "terminal_no":"124", "resellerName": "Repair", 'parent': 'E600'}},
            "134": {"modelName": "E700", "serial_range":"134", "name":"TR_E700", "type":"Ev1_Series", "resellerName": "Repair","fmName": "E700_PayDroid_7.1.2_Scorpio_V10.1.29_20240320", "hasAccessory":True, "accessory":
            {"modelName":"Q20L", "serial_range": "114", "name": "TR_E700-Q20", "type":"Qv1_Series", "terminal_no":"124", "resellerName": "Repair", 'parent': 'E700'}},
            "115": {"modelName": "E500", "serial_range":"115", "name":"TR_E500", "type":"Ev1_Series", "terminal_no":"2", "resellerName": "Repair","fmName": "E500_PayDroid_6.0.1_Taurus_V05.1.25_20230313","hasAccessory":True, "accessory":
            {"modelName":"Q20L", "serial_range": "114", "name": "TR_E500-Q20", "type":"Qv1_Series", "terminal_no":"124", "resellerName": "Repair", 'parent':'E500'}},
            "227": {"modelName": "E600M", "serial_range":"227", "name":"TR_E600M", "type":"Ev2_Series", "terminal_no":"415",  "resellerName": "Repair","fmName": "PayDroid_10.0.0_Acacia_V13.1.18_20240105","hasAccessory":True,"accessory":
            {"modelName":"Q10A", "serial_range": "240", "name": "TR_E600M-Q10", "type":"Qv2_Series", "terminal_no":"416", "resellerName": "Repair", 'parent': 'E600M'}},
            "082": {"modelName": "A920", "serial_range":"082", "name":"TR_A920", "type":"A_Series", "terminal_no":"1", "resellerName": "Repair","fmName": "PayDroid_5.1.1_Aquarius_V02.3.46_20240410","hasAccessory":False},
            "185": {"modelName": "A920Pro", "serial_range":"185", "name":"TR_A920Pro", "type":"A_Series", "terminal_no":"341", "resellerName": "Repair","fmName": "PayDroid_8.1.0_Sagittarius_V11.1.62_20240411","hasAccessory":False},
            "135": {"modelName": "A60", "serial_range":"135", "name":"TR_A60", "type":"A_Series", "terminal_no":"19",  "resellerName": "Repair","fmName": "A60_PayDroid_6.0_Leo_V07.1.17_20240415","hasAccessory":False},
            "124": {"modelName": "A80", "serial_range":"124", "name":"TR_A80", "type":"A_Series", "terminal_no":"26", "resellerName": "Repair","fmName": "PayDroid_10.0_Cedar_V17.2.19_20240313", "hasAccessory":False},
            "176": {"modelName": "A77", "serial_range":"176", "name":"TR_A77", "type":"A_Series", "terminal_no":"271", "resellerName": "Repair","fmName": "PayDroid_8.1.0_Sagittarius_V11.1.62_20240411","hasAccessory":False},
            "3A4": {"modelName": "SP30s", "serial_range":"3A4", "name":"TR_SP30", "type":"A_Series", "terminal_no":"180", "resellerName": "Repair","fmName":None, "hasAccessory":False},
            "3A6": {"modelName": "SP30s", "serial_range":"3A6", "name":"TR_SP30", "type":"A_Series", "terminal_no":"180", "resellerName": "Repair","fmName":None, "hasAccessory":False},
            "3A7": {"modelName": "SP30s", "serial_range":"3A7", "name":"TR_SP30", "type":"A_Series", "terminal_no":"180", "resellerName": "Repair","fmName":None, "hasAccessory":False},
            "3L0": {"modelName": "SP30s", "serial_range":"3L0", "name":"TR_SP30", "type":"A_Series", "terminal_no":"180", "resellerName": "Repair","fmName":None, "hasAccessory":False},
            "229": {"modelName": "A35", "serial_range":"229", "name":"RKI_A35", "type":"A_Series", "terminal_no":"362", "resellerName": "Repair","fmName": "PayDroid_10.0_Cedar_V17.2.19_20240313", "hasAccessory":False},
            "114": {"modelName": "Q20L", "serial_range":"114","name":'TR_E600-Q20', "type":"Qv1_Series", "hasAccessory":False, "resellerName":"Repair", "fmName":None},
            "240": {"modelName": "Q10A", "serial_range":"240","name":'TR_E600M-Q10', "type":"Qv2_Series","fmName": "Q10A_PayDroid_10_Cedar_V17.1.13_20240322","resellerName":"Repair", "hasAccessory":False},
            "189": {"modelName": "D135", "serial_range":"189", "name":"TR_D135", "type":"D-Series", "terminal_no":"421", "resellerName": "Repair", "fmName":None, "hasAccessory":False},
        }
        # Dictionary containing data for software packages to be pushed to the terminals NOT USED
        self.pushPATool = {
                "A_SeriespackageName": "com.pax.us.pay.std.broadpos.p2pe",
                "A_SeriespushTemplateName": "PA 6.9.1 E600M BroadPos P2PE V1.05.06",
                "A_SeriestemplateName":  "p2pe_20240325.zip",
                "A_Seriesversion": "V1.05.06_20240325",
                "Qv2_SeriespackageName": "com.pax.us.pay.std.broadpos.p2pe",
                "Qv2_SeriespushTemplateName": "PA 6.9.1 E600M BroadPos P2PE V1.05.06",
                "Qv2_SeriestemplateName": "p2pe_20240325.zip",
                "Qv2_Seriesversion": "V1.05.06_20240325",
                "Qv1_SeriespackageName":"BroadPOS-P2PE-Q20L",
                "Qv1_SeriespushTemplateName": "PA 6.8 Q20 BroadPOS P2PE Q20L V1.01.05_20230413",
                "Qv1_SeriestemplateName": "config.zip",
                "Qv1_Seriesversion": "V1.01.05_20230413",
                "Ev1_SeriespackageName": "com.pax.pdm",
                "Ev1_SeriestemplateName": "BasicSystem-Q20L_V1.00.07.zip",
                "Ev1_Seriesversion": None,
                "Ev1_SeriespushTemplateName": None,
                "Ev2_SeriespackageName": None,
                "Ev2_SeriestemplateName": None,
                "Ev2_Seriesversion": None,
                "Ev2_SeriespushTemplateName": None
        }

        self.serialNo = serialNo # Store the provided serial number
        serial_prefix = str(self.serialNo)[:3] # Extract the first 3 characters of the serial number

        # Access data from termtool based on serial number prefix
        if serial_prefix in self.termtool:
            term_data = self.termtool[serial_prefix]
            self.modelName = term_data.get("modelName")  # Get the model name
            self.name = term_data.get("name")  # Get the terminal name
            self.resellerName = term_data.get("resellerName")  # Get the reseller name
            self.type = term_data.get("type")  # Get the terminal type
            self.fmName = term_data.get("fmName")  # Get the firmware name
            self.hasAccessory = term_data.get("hasAccessory", False)  # Get whether the terminal has an accessory (default to False if not present)

            # If the terminal has an accessory, extract accessory details
            if self.hasAccessory:
                self.accessoryModelName = term_data["accessory"].get("modelName")
                self.accessoryName = term_data["accessory"].get("name")
                self.accessoryResellerName = term_data["accessory"].get("resellerName")
                self.accessoryType = term_data["accessory"].get("type")
            else:
                # If no accessory, set accessory attributes to None
                self.accessoryModelName = None
                self.accessoryName = None
                self.accessoryResellerName = None
                self.accessoryType = None

        # Access data from pushPATool based on terminal type NOT USED
        self.bPosPackageName = self.pushPATool[f"{self.type}packageName"]
        self.bPosPushTemplateName = self.pushPATool[f"{self.type}pushTemplateName"]
        self.bPosTemplateName = self.pushPATool[f"{self.type}templateName"]
        self.bPosPackageVersion = self.pushPATool[f"{self.type}version"]

async def fill_device_details(serial_number: str) -> dict:
    """
    Fills in device details in a dictionary using the PaxTerms class.

    Args:
        serial_number (str): The serial number of the device.

    Returns:
        dict: A dictionary with device details filled in.
    """

    device_details = {
        'id': None, 'name': None, 'tid': None, 'serialNo': None, 'status': None, 
        'merchantName': None, 'modelName': None, 'resellerName': None, 'createdDate': None, 
        'lastActiveTime': None, 'pn': None, 'osVersion': None, 'imei': None, 
        'screenResolution': None, 'language': None, 'ip': None, 'timeZone': None, 
        'macAddress': None, 'hasAccessory':None ,'accessory': None
    }
    pax_term = PaxTerms(serial_number)  # Create PaxTerms object
    # Update dictionary with matching attributes from PaxTerms object
    for key in device_details:
        if hasattr(pax_term, key):
            value = getattr(pax_term, key)
            if key == 'hasAccessory' and value is True:  # Check if hasAccessory is True
                device_details['accessory'] = pax_term.termtool[serial_number[:3]]['accessory'] 
            else:
                device_details[key] = value

    return device_details
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
    return term_data  # Return the parsed JSON data


async def findTerminal(serialNoList: list) -> list:
    """
    Purpose:
    Locates a PaxStore terminal based on its serial number.
    
    Parameters: serialNoList (list): A list of serial numbers to search for.

    Returns: list: A list of JSON responses, each containing information about a found terminal. If a terminal is not found, its corresponding response will be an empty list."""
        
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        tasks = []
        print(serialNoList)
        for serialNo in serialNoList:
            tasks.append(asyncio.ensure_future(buildRequest(session, "findTerminal", serialNo = serialNo)))
        responses = await asyncio.gather(*tasks)
        cleanResponses = []
        for resp in responses:  
            cleanResponses.append(*resp['dataset'])
        return cleanResponses

async def terminalDetails(idList: list, serialNoList=None, df=None) -> list:
    """
    Retrieves detailed information for a list of terminals.

    Args:
        id_list (list): A list of terminal IDs.
        serial_no_list (list, optional): A list of serial numbers (alternative to id_list).
        df (pd.DataFrame, optional): A DataFrame containing terminal information.

    Returns:
        list: A list of JSON responses, each containing detailed information about a terminal.
    """
    
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        tasks = [asyncio.create_task(buildRequest(session, "terminalDetails", terminalId=id)) for id in idList]
        responses = await asyncio.gather(*tasks)
        cleanResponses = []
        for resp in responses:
            cleanResponses.append(resp['data']['terminalDetail'])
        return cleanResponses

async def accessoryDetails(df:pd.DataFrame, handleaccessory=True)->pd.DataFrame:
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        tasks = [asyncio.ensure_future(buildRequest(session, "accessoryDetails", terminalId=id)) for id in df["id"]]
        responses = await asyncio.gather(*tasks)
        accessoryList = [resp["data"]["terminalAccessory"]["basic"][0]["content"] if "terminalAccessory" in resp["data"] else None for resp in responses]
        qf = pd.DataFrame({"accessory":accessoryList}, dtype=object)
        ndf = pd.concat([df,qf],axis=1)
        print(ndf)
        parent_serialNoList = ndf['serialNo']
        accessory_serialNoList = ndf['accessory'].dropna()
    try:
        accessoryid = await findTerminal(accessory_serialNoList)
        mqf = pd.DataFrame(accessoryid,dtype=object)
        print(mqf)
    # Create a "placeholder" accessory to be added to the PaxStore later
    except TerminalNotFoundError: 
        na_accessory = []
        for a_serialNo, p_serialNo in zip(accessory_serialNoList,parent_serialNoList):
            accessories_properties = await fill_device_details(a_serialNo)
            parent_properties = await fill_device_details(p_serialNo)
            accessory_name = parent_properties['accessory'].get('name')
            accessories_properties.update({'name':accessory_name, 'status':'A', 'merchantName': 'North American Bancard'})
            na_accessory.append(accessories_properties)
        mqf = pd.DataFrame(na_accessory)
    bqf = pd.concat([ndf,mqf], ignore_index=True)
    print(bqf.to_dict('records'))
    if handleaccessory == False:
        return ndf
    else:
        return bqf

async def findGroup(serialNoList:list)->pd.DataFrame:
    func = apiPaxFunctions()
    group = await func.startPaxGroup(serialNoList=serialNoList)
    return group

async def updateTerminals(idList,serialNoList, df=None):
    tasks = []
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:

        for serialNo,id in list(zip(serialNoList,idList)): 
            terminal = PaxTerms(serialNo)
            #nameList.append(terminal.name)
            tasks.append(asyncio.ensure_future(buildRequest(serialNo=serialNo,terminalId=id,session=session, operation="updateTerminal",merchantName="North American Bancard",name=terminal.name,modelName=terminal.modelName,resellerName=terminal.resellerName,status = "A")))
        responses = await asyncio.gather(*tasks)
        print(responses)


class apiPaxFunctions(): 

    def __init__(self) -> None:
        pass

    async def startPaxGroup(self, serialNoList, handleAccessory = True, idList = None, df = None) -> pd.DataFrame:
        self.idList = []
        self.serialNoList = serialNoList
        findResp = await findTerminal(serialNoList)
        fullserial_List = []
        for resp in findResp:   
            print("\n\n\nRESP:",resp)
            self.idList.append(resp['id'])
        detailresp = await terminalDetails(self.idList)
        print("\n\n\nfindResp:",*findResp)
        self.groupList = []
        for fresp,dresp in list(zip(findResp,detailresp)):
            fresp.update(dresp)
            self.groupList.append(fresp)
        if not handleAccessory:
            return pd.DataFrame(self.groupList)
        else:
            group_df = pd.DataFrame(self.groupList, dtype=object)
            accessoryDetail = await accessoryDetails(group_df)
            return accessoryDetail
    
    async def activateTerminals(self, idList, serialNoList=None, df=None):
        
        tasks = []
        responses = []
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            for id in idList:
                tasks.append(asyncio.ensure_future(buildRequest(session,"activateTerminal",terminalId = id)))
            result = await asyncio.gather(*tasks)
            for res in result:
                if res == None:
                    responses.append({'businessCode':0, 'message':'The terminal has been activated'})
                else: responses.append(res)   
            return responses

    async def moveTerminals(self, idList, resllerName, merchantName,serialNoList=None, df=None):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            tasks = [asyncio.ensure_future(buildRequest(session,"moveTerminal",resellerName = resllerName, merchantName = merchantName,terminalId = id)) for id in idList]
            results = await asyncio.gather(*tasks)
            responses = [f"Terminal Moved to {resllerName} successfully" for message in results if message == None]
            return responses
    
    async def disableTerminals(self, idList:list, serialNoList=None, df=None):

        tasks = []
        responses = []
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            for id in idList: 
                tasks.append(asyncio.ensure_future(buildRequest(session,'disableTerminal', terminalId = id)))
            result = await asyncio.gather(*tasks)
            for res in result:
                if res == None:
                    responses.append({'businessCode':0, 'message':'The terminal has been disabled'})
                else: responses.append(res)   
            return responses
    
    async def createTerminals(self,serialNoList):

        tasks = []
        cleanResponses = []
        nameList = []
        for serialNo in serialNoList:
            terminal = PaxTerms(serialNo)
            nameList.append(terminal.name)
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            for serialNo, name in list(zip(serialNoList, nameList)): 
                terminal = PaxTerms(serialNo)
                nameList.append(terminal.name)
                tasks.append(asyncio.ensure_future(buildRequest(serialNo=serialNo,session=session, operation="createTerminal",merchantName="North American Bancard",name=name,modelName=terminal.modelName,resellerName=terminal.resellerName,status = "A")))
            result = await asyncio.gather(*tasks) 
            for resp in result:
                cleanResponses.append(resp['data'])
            #cleanResponses.append(*[resp['data'] for resp in result])
            return cleanResponses

    async def deleteTerminals(self, idList, df=None):
        responses=[]
        tasks = []
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            for id in idList:
                tasks.append(asyncio.ensure_future(buildRequest(session, "deleteTerminal", terminalId = id )))
            result = await asyncio.gather(*tasks)
            for res in result:
                if res == None:
                    responses.append({'businessCode':0, 'message':'The terminal has been deleted'})
                else: responses.append(res)   
            return responses
        
        

        
    
    async def pushTerminalAPK(self, serialNoList, paramApp:bool=None, packageName=None):
        tasks = []
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            for serialNo in serialNoList: 
                if paramApp:
                    terminal = PaxTerms(serialNo)
                    tasks.append(asyncio.ensure_future(buildRequest(session, "pushParamAPK",serialNo=serialNo, packageName=terminal.bPosPackageName,templateName=terminal.bPosTemplateName, pushTemplateName=terminal.bPosPushTemplateName, version=terminal.bPosPackageVersion)))
                else:
                    tasks.append(asyncio.ensure_future(buildRequest(session, "pushAPK",serialNo=serialNo, packageName=packageName)))
            result = await asyncio.gather(*tasks)
            print(result)
            return result

    async def pushThingy(self, terminalList ,operation:str, **kwargs):
        """Pushes thing to group of terminals. """
        tasks = []
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            for serialNo in terminalList:
                tasks.append(asyncio.ensure_future(buildRequest(session,operation, serialNo=serialNo, **kwargs)))
            result = await asyncio.gather(*tasks)
            return result

class PushConfigs():
    
    def __init__(self) :
        pass

        self.task = apiPaxFunctions()

    async def pushPAConfig(self, serialNoList, idList = None, df = None):
        """Pushes current version of:\n BroadPosP2PE (PA Template),\n CheckUp,\n PAInstaller, \n PayDroid Firmware, \n RKI"""
       
        bpospush = await self.task.pushTerminalAPK(serialNoList,True)
        print("BroadPosP2PEPush:",bpospush)
        installerPush = await self.task.pushTerminalAPK(serialNoList,False, "com.nabancard.painstaller")
        print("PAInstallerPush:", installerPush)
        checkupPush = await self.task.pushTerminalAPK(serialNoList,False,"com.pax.checkup")
        print("CheckUpPush",checkupPush)
        paCFDpush = await self.task.pushTerminalAPK(serialNoList,False, "com.nabancard.q10driver")
        print(paCFDpush)
        
    async def paPushByReseller(self, idList, **kwargs):
        deactivate = await self.task.disableTerminals(idList)
        move = await self.task.moveTerminals(idList=idList,resllerName="A920 Config",merchantName="North American Bancard")
        activate = await self.task.activateTerminals(idList)
        return activate
 
        

    async def pushBroadPosEPX(self, serialNoList,idList = None, df = None):
        
        
        task = apiPaxFunctions()
        checkupPush = await task.pushTerminalAPK( serialNoList,False,"com.pax.checkup")
        print("CheckUpPush",checkupPush)
        rki = await task.pushThingy(serialNoList,"pushRKI",rkiKey="EPX_PIN_Slot1_Data_Slot3")
        print(rki)


    async def pushBroadPos_nonEPX(self, serialNoList,idList = None, df = None):
        
        task = apiPaxFunctions()
        checkupPush = await task.pushTerminalAPK(serialNoList,False,"com.pax.checkup")
        print("CheckUpPush",checkupPush)

async def findGroup(serialNoList:list)->pd.DataFrame:
    func = apiPaxFunctions()
    group = await func.startPaxGroup(serialNoList=serialNoList)
    return group

def parse_responses(responses):
    results = []
    for response in responses:
        if response.get('businessCode') == 0:
            data = response['dataset']
            for device in data:
                firmware_name = device['installedFirmware'].get('firmwareName')
                installed_apks = [
                    {
                        "serialNo": device.get("serialNo"),
                        "firmwareName": firmware_name,
                        "appName": apk.get("appName"),
                        "packageName": apk.get("packageName"),
                        "versionName": apk.get("versionName"),
                        # ... (add other relevant APK details as needed)
                    }
                    for apk in device['installedApks']
                ]
                results.extend(installed_apks)
    return results

def checker(installedVersion:tuple, targetVersion:dict) ->bool:
    
    #check if APK is a config APK
    if installedVersion[0] not in targetVersion.keys():
        pass
    elif installedVersion[0] in targetVersion.keys():
        #check if installed version of config is target version
        if installedVersion[1] == targetVersion.get(installedVersion[0]):
            isTarget = True
        else: isTarget = False
    return isTarget

        

async def getInstalledConfig(serialNoList):
    devices = []
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        tasks = [asyncio.ensure_future(buildRequest(session, "terminalConfig", serialNo=serialNo))for serialNo in serialNoList]
        responses = await asyncio.gather(*tasks)
        for response in responses:
            if response['businessCode'] == 0: 
                data = response['dataset']
                devices.extend(device for device in data)
                #installedFirmaware.extend(device['installedFirmware']['firmwareName'] for device in data)
                #installedApps.extend(device['installedApks'] for device in data)
    return devices
    
async def resetTerminals(df:pd.DataFrame, idList=None,serialNoList=None):
    func = apiPaxFunctions()
    disable = await func.disableTerminals(df['id'])
    delete = await func.deleteTerminals(df['id'])
    create = await func.createTerminals(df['serialNo'])
    return create

async def pushStatus(serialNoList):

    termData = await findTerminal(serialNoList)
    print(termData)
    idList = [term['tid'] for term in termData]
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        tasks = [asyncio.ensure_future(buildRequest(session, "pushStatus",packageName='com.pax.checkup', terminalId=id)) for id in idList]
        responses = await asyncio.gather(*tasks)
        print(responses)
        if responses['businessCode'] == 0:
            pass


    
   

    






