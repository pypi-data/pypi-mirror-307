import aiohttp
import asyncio
import pandas as pd
import time
from .pax_exceptions import TerminalNotFoundError
from .paxterms import fill_device_details, PaxTerms
from .paxAPItool import buildRequest


async def findTerminal(serialNoList: list) -> list:
    """
    Locates PaxStore terminals based on their serial numbers.

    Parameters:
        serialNoList (list): A list of serial numbers to search for.

    Returns:
        list: A list of JSON responses, each containing information 
              about a found terminal. 
              If a terminal is not found, its corresponding response will be an empty list.
    """

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        tasks = []
        print(serialNoList)  # Print the list of serial numbers being processed
        for serialNo in serialNoList:
            # Create asynchronous tasks for each serial number to be searched
            tasks.append(asyncio.ensure_future(buildRequest(session, "findTerminal", serialNo=serialNo)))  
        responses = await asyncio.gather(*tasks)  # Execute all search tasks concurrently
    cleanResponses = []
    for resp in responses:
        cleanResponses.append(*resp['dataset'])  # Extract terminal data from responses
    return cleanResponses  # Return the list of terminal information


async def terminalDetails(idList: list, serialNoList=None, df=None) -> list:
    """
    Retrieves detailed information for a list of terminals.

    Args:
        idList (list): A list of terminal IDs.
        serialNoList (list, optional): A list of serial numbers (alternative to idList).
        df (pd.DataFrame, optional): A DataFrame containing terminal information.

    Returns:
        list: A list of JSON responses, each containing detailed information about a terminal.
    """

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        # Create asynchronous tasks to fetch details for each terminal ID
        tasks = [asyncio.create_task(buildRequest(session, "terminalDetails", terminalId=id)) for id in idList]  
        responses = await asyncio.gather(*tasks)  # Execute all detail retrieval tasks concurrently
    cleanResponses = []
    for resp in responses:
        cleanResponses.append(resp['data']['terminalDetail'])  # Extract detailed terminal information
    return cleanResponses  # Return the list of detailed terminal information


async def accessoryDetails(df: pd.DataFrame) -> pd.DataFrame:
    """
    Retrieves and processes accessory details for terminals in a DataFrame.

    Args:
        df (pd.DataFrame): A DataFrame containing terminal information, including 'id' column.

    Returns:
        pd.DataFrame: An updated DataFrame with added accessory information.
    """

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        # Create asynchronous tasks to fetch accessory details for each terminal ID in the DataFrame
        tasks = [asyncio.ensure_future(buildRequest(session, "accessoryDetails", terminalId=id)) for id in df["id"]]  
        responses = await asyncio.gather(*tasks)  # Execute all accessory detail tasks concurrently
        # Extract accessory serial number from responses, handling cases where no accessory is found
        accessoryList = [resp["data"]["terminalAccessory"]["basic"][0]["content"] if "terminalAccessory" in resp["data"] else None for resp in responses]  
        qf = pd.DataFrame({"accessory": accessoryList}, dtype=object)  # Create a DataFrame for accessory information
        ndf = pd.concat([df, qf], axis=1)  # Concatenate the original DataFrame with the accessory DataFrame
        print(ndf)  # Print the updated DataFrame with accessory information
        parent_serialNoList = ndf['serialNo']  # Extract the list of parent terminal serial numbers
        accessory_serialNoList = ndf['accessory'].dropna()  # Extract the list of accessory serial numbers (excluding missing values)
    try:
        # Attempt to find the accessories in PaxStore using their serial numbers
        accessoryid = await findTerminal(accessory_serialNoList)  
        mqf = pd.DataFrame(accessoryid, dtype=object)  # Create a DataFrame for found accessory information
        print(mqf)  # Print the DataFrame of found accessory information
    # Handle the case where an accessory is not found in PaxStore
    except TerminalNotFoundError:  
        na_accessory = []
        # Iterate through pairs of accessory and parent serial numbers
        for a_serialNo, p_serialNo in zip(accessory_serialNoList, parent_serialNoList):  
            accessories_properties = await fill_device_details(a_serialNo)  # Fetch detailed information for the accessory
            parent_properties = await fill_device_details(p_serialNo)  # Fetch detailed information for the parent terminal
            accessory_name = parent_properties['accessory'].get('name')  # Extract the accessory name from the parent's information
            # Update the accessory properties with name, status, and merchant information
            accessories_properties.update({'name': accessory_name, 'status': 'A', 'merchantName': 'North American Bancard'})  
            na_accessory.append(accessories_properties)  # Add the updated accessory information to the list
        mqf = pd.DataFrame(na_accessory)  # Create a DataFrame for the accessories not found in PaxStore
    bqf = pd.concat([ndf, mqf], ignore_index=True)  # Concatenate the DataFrames to include all accessory information
    return bqf  # Return the final DataFrame with complete accessory information

class apiPaxFunctions():
    """
    A class to manage Pax terminal operations through the Pax API.
    """

    def __init__(self) -> None:
        pass

    async def startPaxGroup(self, serialNoList, handleAccessory=True, idList=None, df=None) -> pd.DataFrame:
        """
        Initializes a group of Pax terminals by retrieving their details and optionally handling accessories.

        Args:
            serialNoList (list): A list of terminal serial numbers.
            handleAccessory (bool, optional): Whether to retrieve accessory details. Defaults to True.
            idList (list, optional): A list of terminal IDs (alternative to serialNoList). Defaults to None.
            df (pd.DataFrame, optional): A DataFrame containing terminal information. Defaults to None.

        Returns:
            pd.DataFrame: A DataFrame containing detailed information about the terminals, including accessory details if handleAccessory is True.
        """

        self.idList = []
        self.serialNoList = serialNoList
        findResp = await findTerminal(serialNoList)  # Find terminals based on serial numbers
        fullserial_List = []
        for resp in findResp:
            print("\n\n\nRESP:", resp)  # Print the response from findTerminal for each terminal
            self.idList.append(resp['id'])  # Collect the terminal IDs
        detailresp = await terminalDetails(self.idList)  # Retrieve detailed information for the terminals
        print("\n\n\nfindResp:", *findResp)  # Print the combined findTerminal responses
        self.groupList = []
        # Combine the basic and detailed information for each terminal
        for fresp, dresp in list(zip(findResp, detailresp)):  
            fresp.update(dresp)
            self.groupList.append(fresp)
            print(self.groupList)  # Print the combined information for each terminal
        if not handleAccessory:
            return pd.DataFrame(self.groupList)  # Return a DataFrame with basic and detailed information
        else:
            group_df = pd.DataFrame(self.groupList, dtype=object)  # Create a DataFrame for the terminals
            accessoryDetail = await accessoryDetails(group_df)  # Retrieve and process accessory details
            return accessoryDetail  # Return the DataFrame with accessory details included

    async def activateTerminals(self, idList, serialNoList=None, df=None):
        """
        Activates a list of Pax terminals.

        Args:
            idList (list): A list of terminal IDs.
            serialNoList (list, optional): A list of serial numbers (alternative to idList). Defaults to None.
            df (pd.DataFrame, optional): A DataFrame containing terminal information. Defaults to None.

        Returns:
            list: A list of responses indicating the activation status of each terminal.
        """

        tasks = []
        responses = []
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            for id in idList:
                # Create asynchronous tasks to activate each terminal
                tasks.append(asyncio.ensure_future(buildRequest(session, "activateTerminal", terminalId=id)))  
            result = await asyncio.gather(*tasks)  # Execute all activation tasks concurrently
        for res in result:
            if res is None:
                # If the response is None, the terminal was activated successfully
                responses.append({'businessCode': 0, 'message': 'The terminal has been activated'})  
            else:
                responses.append(res)  # Otherwise, append the actual response (likely an error)
        return responses  # Return the list of activation responses

    async def moveTerminals(self, idList, resellerName, merchantName, serialNoList=None, df=None):
        """
        Moves a list of Pax terminals to a different reseller and merchant.

        Args:
            idList (list): A list of terminal IDs.
            resellerName (str): The name of the new reseller.
            merchantName (str): The name of the new merchant.
            serialNoList (list, optional): A list of serial numbers (alternative to idList). Defaults to None.
            df (pd.DataFrame, optional): A DataFrame containing terminal information. Defaults to None.

        Returns:
            list: A list of responses indicating the status of each terminal move operation.
        """

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            # Create asynchronous tasks to move each terminal
            tasks = [asyncio.ensure_future(buildRequest(session, "moveTerminal", resellerName=resellerName, merchantName=merchantName, terminalId=id)) for id in idList]  
            results = await asyncio.gather(*tasks)  # Execute all move tasks concurrently
            # Generate responses based on the results (successful moves return None)
            responses = [f"Terminal Moved to {resellerName} successfully" for message in results if message is None]  
            return responses  # Return the list of move operation responses

    async def disableTerminals(self, idList: list, serialNoList=None, df=None):
        """
        Disables a list of Pax terminals.

        Args:
            idList (list): A list of terminal IDs.
            serialNoList (list, optional): A list of serial numbers (alternative to idList). Defaults to None.
            df (pd.DataFrame, optional): A DataFrame containing terminal information. Defaults to None.

        Returns:
            list: A list of responses indicating the disable status of each terminal.
        """

        tasks = []
        responses = []
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            for id in idList:
                # Create asynchronous tasks to disable each terminal
                tasks.append(asyncio.ensure_future(buildRequest(session, 'disableTerminal', terminalId=id)))  
            result = await asyncio.gather(*tasks)  # Execute all disable tasks concurrently
        for res in result:
            if res is None:
                # If the response is None, the terminal was disabled successfully
                responses.append({'businessCode': 0, 'message': 'The terminal has been disabled'})  
            else:
                responses.append(res)  # Otherwise, append the actual response (likely an error)
        return responses  # Return the list of disable responses

    async def createTerminals(self, serialNoList):
        """
        Creates new Pax terminals in PaxStore.

        Args:
            serialNoList (list): A list of terminal serial numbers.

        Returns:
            list: A list of responses indicating the creation status of each terminal.
        """

        tasks = []
        cleanResponses = []
        nameList = []
        self.exceptions = []
        for serialNo in serialNoList:
            terminal = PaxTerms(serialNo)  # Create a PaxTerms object to get terminal information
            nameList.append(terminal.name)  # Collect the terminal names
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            for serialNo, name in list(zip(serialNoList, nameList)):
                terminal = PaxTerms(serialNo)  # Create a PaxTerms object
                nameList.append(terminal.name)
                # Create asynchronous tasks to create each terminal with the retrieved information
                tasks.append(asyncio.ensure_future(buildRequest(serialNo=serialNo, session=session, operation="createTerminal", merchantName="North American Bancard", name=name, modelName=terminal.modelName, resellerName=terminal.resellerName, status="A")))  
            result = await asyncio.gather(*tasks)  # Execute all terminal creation tasks concurrently
            print(result)  # Print the raw result from the API calls
            for resp in result:
                cleanResponses.append(resp['data'])  # Extract the relevant data from the responses

            return cleanResponses  # Return the list of creation responses

    async def deleteTerminals(self, idList, df=None):
        """
        Deletes a list of Pax terminals from PaxStore.

        Args:
            idList (list): A list of terminal IDs.
            df (pd.DataFrame, optional): A DataFrame containing terminal information. Defaults to None.

        Returns:
            list: A list of responses indicating the deletion status of each terminal.
        """

        tasks = []
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            for id in idList:
                # Create asynchronous tasks to delete each terminal
                tasks.append(asyncio.ensure_future(buildRequest(session, "deleteTerminal", terminalId=id)))  
            result = await asyncio.gather(*tasks)  # Execute all deletion tasks concurrently

            return result  # Return the list of deletion responses

    async def pushTerminalAPK(self, serialNoList, paramApp: bool = None, packageName=None):
        """
        Pushes APK files to a list of Pax terminals.

        Args:
            serialNoList (list): A list of terminal serial numbers.
            paramApp (bool, optional): Whether to push a parameter app. Defaults to None.
            packageName (str, optional): The name of the APK package to push (if not a parameter app). Defaults to None.

        Returns:
            list: A list of responses indicating the status of each APK push operation.
        """

        tasks = []
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            for serialNo in serialNoList:
                if paramApp:
                    terminal = PaxTerms(serialNo)  # Create a PaxTerms object to get terminal information
                    # Create asynchronous tasks to push the parameter app with necessary information
                    tasks.append(asyncio.ensure_future(buildRequest(session, "pushParamAPK", serialNo=serialNo, packageName=terminal.bPosPackageName, templateName=terminal.bPosTemplateName, pushTemplateName=terminal.bPosPushTemplateName, version=terminal.bPosPackageVersion)))  
                else:
                    # Create asynchronous tasks to push the specified APK package
                    tasks.append(asyncio.ensure_future(buildRequest(session, "pushAPK", serialNo=serialNo, packageName=packageName)))  
            result = await asyncio.gather(*tasks)  # Execute all APK push tasks concurrently
            print(result)  # Print the raw result from the API calls
            return result  # Return the list of APK push responses

    async def pushThingy(self, terminalList, operation: str, **kwargs):
        """
        Pushes something (e.g., configuration, files) to a group of terminals.

        Args:
            terminalList (list): A list of terminal serial numbers.
            operation (str): The operation to perform (e.g., "pushConfig", "pushFile").
            **kwargs: Additional keyword arguments to pass to the buildRequest function.

        Returns:
            list: A list of responses indicating the status of each push operation.
        """

        tasks = []
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            for serialNo in terminalList:
                # Create asynchronous tasks to perform the specified operation on each terminal
                tasks.append(asyncio.ensure_future(buildRequest(session, operation, serialNo=serialNo, **kwargs)))  
            result = await asyncio.gather(*tasks)  # Execute all push tasks concurrently
            return result  # Return the list of push operation responses
        

class PushConfigs():
    """
    A class to manage pushing configurations and applications to Pax terminals.
    """

    def __init__(self):
        self.task = apiPaxFunctions()  # Create an instance of apiPaxFunctions to use its methods

    async def pushPAConfig(self, serialNoList, idList=None, df=None):
        """
        Pushes the current version of essential applications and configurations to Pax terminals for PA (Payment Application) setup.

        This method pushes the following:
            - BroadPosP2PE (PA Template)
            - CheckUp
            - PAInstaller
            - PayDroid Firmware
            - RKI

        Args:
            serialNoList (list): A list of terminal serial numbers.
            idList (list, optional): A list of terminal IDs (alternative to serialNoList). Defaults to None.
            df (pd.DataFrame, optional): A DataFrame containing terminal information. Defaults to None.
        """

        # Push BroadPosP2PE (parameter app)
        bpospush = await self.task.pushTerminalAPK(serialNoList, True)  
        print("BroadPosP2PEPush:", bpospush)
        # Push PAInstaller
        installerPush = await self.task.pushTerminalAPK(serialNoList, False, "com.nabancard.painstaller")  
        print("PAInstallerPush:", installerPush)
        # Push CheckUp
        checkupPush = await self.task.pushTerminalAPK(serialNoList, False, "com.pax.checkup")  
        print("CheckUpPush", checkupPush)
        # Push PayDroid Firmware (using the q10driver package name)
        paCFDpush = await self.task.pushTerminalAPK(serialNoList, False, "com.nabancard.q10driver")  
        print(paCFDpush)

    async def paPushByReseller(self, idList, **kwargs):
        """
        Performs a sequence of actions to update and configure Pax terminals for Payanywhere by moving to the configuration reseller.

        This method performs the following actions:
            - Deactivates the terminals.
            - Moves the terminals to the "A920 Config" reseller and "North American Bancard" merchant to for active PayAnwhere configuration pushes.
            - Activates the terminals.

        Args:
            idList (list): A list of terminal IDs.
            **kwargs: Additional keyword arguments (not used in the current implementation).

        Returns:
            list: A list of responses from the activateTerminals operation.
        """

        deactivate = await self.task.disableTerminals(idList)  # Deactivate terminals
        # Move terminals to the specified reseller and merchant
        move = await self.task.moveTerminals(idList=idList, resellerName="A920 Config", merchantName="North American Bancard")  
        activate = await self.task.activateTerminals(idList)  # Activate terminals
        return activate  # Return the activation responses

    async def pushBroadPosEPX(self, serialNoList, idList=None, df=None):
        """
        Pushes configurations and applications specifically for EPX devices (not using Payanywhere).

        This method pushes the following:
            - CheckUp
            - RKI (with the EPX_PIN_Slot1_Data_Slot3 key)

        Args:
            serialNoList (list): A list of terminal serial numbers.
            idList (list, optional): A list of terminal IDs (alternative to serialNoList). Defaults to None.
            df (pd.DataFrame, optional): A DataFrame containing terminal information. Defaults to None.
        """

        # Push CheckUp
        checkupPush = await self.task.pushTerminalAPK(serialNoList, False, "com.pax.checkup")  
        print("CheckUpPush", checkupPush)
        # Push RKI with the specific key for EPX devices
        rki = await self.task.pushThingy(serialNoList, "pushRKI", rkiKey="EPX_PIN_Slot1_Data_Slot3")  
        return rki

    async def pushBroadPos_nonEPX(self, serialNoList, idList=None, df=None):
        """
        Pushes configurations and applications for non-EPX devices.

        Currently, this method only pushes CheckUp.

        Args:
            serialNoList (list): A list of terminal serial numbers.
            idList (list, optional): A list of terminal IDs (alternative to serialNoList). Defaults to None.
            df (pd.DataFrame, optional): A DataFrame containing terminal information. Defaults to None.
        """

        # Push CheckUp
        checkupPush = await self.task.pushTerminalAPK(serialNoList, False, "com.pax.checkup")  
        return checkupPush        


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
    """
    Retrieves the installed configuration for a list of Pax terminals.

    Args:
        serialNoList (list): A list of terminal serial numbers.

    Returns:
        list: A list of dictionaries, where each dictionary represents the configuration of a terminal.
    """

    devices = []
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        # Create asynchronous tasks to fetch the configuration for each terminal
        tasks = [asyncio.ensure_future(buildRequest(session, "terminalConfig", serialNo=serialNo)) for serialNo in serialNoList]  
        responses = await asyncio.gather(*tasks)  # Execute all configuration retrieval tasks concurrently
        for response in responses:
            if response['businessCode'] == 0:  # Check if the API call was successful
                data = response['dataset']
                # Extend the devices list with the configuration data for each device
                devices.extend(device for device in data)  
    return devices  # Return the list of device configurations

async def resetTerminals(df: pd.DataFrame, idList=None, serialNoList=None):
    """
    Resets a group of Pax terminals by disabling, deleting, recreating, and restarting them.

    This function performs the following actions:
        1. Disables the terminals.
        2. Deletes the terminals from PaxStore.
        3. Creates new terminals in PaxStore with the same serial numbers.
        4. Filters out terminals with model names "Q20L" and "Q10A".
        5. Waits for 5 seconds to allow for processing.
        6. Locates the terminal details in the PaxStore.

    Args:
        df (pd.DataFrame): A DataFrame containing terminal information, including 'id' and 'serialNo' columns.
        idList (list, optional): A list of terminal IDs (alternative to df). Defaults to None.
        serialNoList (list, optional): A list of serial numbers (alternative to df). Defaults to None.

    Returns:
        pd.DataFrame: A DataFrame containing information about the restarted terminals (excluding Q20L and Q10A models).
    """

    func = apiPaxFunctions()  # Create an instance of apiPaxFunctions
    disable = await func.disableTerminals(df['id'])  # Disable the terminals
    delete = await func.deleteTerminals(df['id'])  # Delete the terminals
    create = await func.createTerminals(df['serialNo'])  # Recreate the terminals
    # Filter out terminals with model names "Q20L" and "Q10A" to avoid duplication in the DataFrame, The startPaxGrop() call will add them later.
    filteredDataFrame = df.drop(df[(df.modelName == "Q20L") | (df.modelName == "Q10A")].index)  
    time.sleep(5)  # Wait for 5 seconds  to allow for processing/propagation
    # Start the remaining terminals as a new group
    group = await func.startPaxGroup(filteredDataFrame['serialNo'])  
    return pd.DataFrame(group)  # Return a DataFrame with information about the restarted terminals
    

async def parseList(serialNoList)->dict:
    thing = apiPaxFunctions()
    termDetail = await thing.startPaxGroup(serialNoList, handleAccessory=False)
    config = await getInstalledConfig(serialNoList)
    for item in config:
        apklist = item['installedApks']
        df = pd.DataFrame(apklist)
    details = await terminalDetails(detail['id']for detail in config)
    termDetails_dict = termDetail.to_dict('records')

    return termDetails_dict, apklist

async def parseApk(serialNoList):
    config = await getInstalledConfig(serialNoList)
    for item in config:
        apklist = item['installedApks']
        df = pd.DataFrame(apklist)
    return df

async def main():
    start = apiPaxFunctions()
    
    serialNoList = ['2270005389','1851806588']
    
    responses = await start.startPaxGroup(serialNoList)

if __name__=='__main__':
    asyncio.run(main())
