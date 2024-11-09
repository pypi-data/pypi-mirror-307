import json
import os
import requests
from .paxModule import PaxApiTool, PaxTerms
from .tui_exceptions import TerminalNotAvailableError, TerminalNotFoundError, IPnotWhitelisted


def buildSingleRequest(session:requests.Session,operation:str,**kwargs):
    apiKey = os.environ.get("APIKEY").encode('utf-8')
    apiSecret = os.environ.get("APISECRET").encode('utf-8')
    term = PaxApiTool(apiKey,apiSecret,session,operation, **kwargs)
    headers = {"Content-Type": "application/json; charset=UTF-8","signature":term.signature}
    method = term.str_method
    response = session.request(method,term.fullurl,json=term.body,headers=headers, verify=False)
    
    return response

def findSingleTerminal(serialNo:str):
    term = PaxTerms(serialNo)
    with requests.Session() as s:
        
        response = buildSingleRequest(s,operation="findTerminal",serialNo=serialNo)  
        data = json.loads(response.text)
        if not data['dataset']:
            raise TerminalNotFoundError(serialNo)
        return data['dataset'][0]
        
        


def createSingleTerminal(serialNo:str):
    term = PaxTerms(serialNo)
    with requests.Session() as s:
        response = buildSingleRequest(s,operation="createTerminal",serialNo=serialNo, merchantName="North American Bancard",name=term.name,modelName=term.modelName,resellerName=term.resellerName,status = "A")  
        data = json.loads(response.text)
        print(data)
        if data['businessCode']== 2332:
            raise TerminalNotAvailableError(serialNo)
        return data['data']
    
