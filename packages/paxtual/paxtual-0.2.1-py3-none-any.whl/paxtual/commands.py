from .paxModule import buildRequest, apiPaxFunctions
import asyncio
import aiohttp

async def push_command(idList:list, command:str, **kwargs):
    
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        reslist = []
        tasks = [asyncio.create_task(buildRequest(session, "pushCommand", command=command , terminalId = id)) for id in idList]
        request = await asyncio.gather(*tasks)
        responses = [f"Success" for message in request if message == None]
        for message in request: 
            if message == None: 
                reslist.append({'businessCode':0, 'message':'The terminal has been rebooted'})
            else: reslist.append(message)
        return reslist

async def reboot(idList:list, **kwargs):
    command = await push_command(idList=idList,command='Restart')
    #return ['success' for response in command if response is None]
    return command

"""if __name__ == '__main__':
    asyncio.run(reboot(['0821609592','1851726394']))"""

    
