import json
import os
import requests
from .tui_exceptions import TerminalNotAvailableError, TerminalNotFoundError
from .paxAPItool import PaxApiTool
from .paxterms import PaxTerms

def buildSingleRequest(session: requests.Session, operation: str, **kwargs):
    """
    Builds and sends a single request to the Pax API.

    Args:
        session (requests.Session): A requests session object.
        operation (str): The API operation to perform.
        **kwargs: Keyword arguments containing the request parameters.

    Returns:
        requests.Response: The response object from the API request.
    """

    apiKey = os.environ.get("APIKEY").encode('utf-8')  # Retrieve API key from environment variable
    apiSecret = os.environ.get("APISECRET").encode('utf-8')  # Retrieve API secret from environment variable
    term = PaxApiTool(apiKey, apiSecret, session, operation, **kwargs)  # Create a PaxApiTool instance
    headers = {"Content-Type": "application/json; charset=UTF-8", "signature": term.signature}  # Construct headers
    method = term.str_method  # Get the HTTP method
    # Send the API request
    response = session.request(method, term.fullurl, json=term.body, headers=headers, verify=False)  
    return response  # Return the response object


def findSingleTerminal(serialNo: str):
    """
    Finds a single terminal in PaxStore by its serial number.

    Args:
        serialNo (str): The serial number of the terminal.

    Returns:
        dict: The terminal information if found.

    Raises:
        TerminalNotFoundError: If the terminal is not found in PaxStore.
    """

    term = PaxTerms(serialNo)  # Create a PaxTerms instance
    with requests.Session() as s:
        response = buildSingleRequest(s, operation="findTerminal", serialNo=serialNo)  # Send the API request
        data = json.loads(response.text)  # Parse the JSON response
        if not data['dataset']:  # Check if the terminal was found
            raise TerminalNotFoundError(serialNo)  # Raise an exception if not found
        return data['dataset'][0]  # Return the terminal information


def createSingleTerminal(serialNo: str):
    """
    Creates a single terminal in PaxStore.

    Args:
        serialNo (str): The serial number of the terminal.

    Returns:
        dict: The data from the API response if the terminal was created successfully.

    Raises:
        TerminalNotAvailableError: If the terminal cannot be created (e.g., already exists).
    """

    term = PaxTerms(serialNo)  # Create a PaxTerms instance
    with requests.Session() as s:
        # Send the API request to create the terminal
        response = buildSingleRequest(s, operation="createTerminal", serialNo=serialNo, merchantName="North American Bancard", name=term.name, modelName=term.modelName, resellerName=term.resellerName, status="A")  
        data = json.loads(response.text)  # Parse the JSON response
        print(data)  # Print the response data
        if data['businessCode'] == 2332:  # Check for a specific error code
            raise TerminalNotAvailableError(serialNo)  # Raise an exception if the terminal cannot be created
        return data['data']  # Return the data from the response
    
