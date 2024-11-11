from .paxAPItool import buildRequest
import asyncio
import aiohttp

    
async def push_command(idList: list, command: str, **kwargs):
    """
    Pushes a command to a list of Pax terminals.

    Args:
        idList (list): A list of terminal IDs.
        command (str): The command to push (e.g., 'Restart', 'Reboot').
        **kwargs: Additional keyword arguments (not used in the current implementation).

    Returns:
        list: A list of responses indicating the status of the command push for each terminal.
    """

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        reslist = []
        # Create asynchronous tasks to push the command to each terminal
        tasks = [asyncio.create_task(buildRequest(session, "pushCommand", command=command, terminalId=id)) for id in idList]  
        request = await asyncio.gather(*tasks)  # Execute all command push tasks concurrently
        # Generate a list of "Success" messages for successful pushes (where the response is None)
        responses = [f"Success" for message in request if message is None]  
        for message in request:
            if message is None:
                # If the response is None, the command was pushed successfully
                reslist.append({'businessCode': 0, 'message': 'The terminal has been rebooted'})  
            else:
                reslist.append(message)  # Otherwise, append the actual response (likely an error)
        return reslist  # Return the list of responses


async def reboot(idList: list, **kwargs):
    """
    Reboots a list of Pax terminals.

    Args:
        idList (list): A list of terminal IDs.
        **kwargs: Additional keyword arguments (not used in the current implementation).

    Returns:
        list: A list of responses indicating the reboot status of each terminal.
    """

    command = await push_command(idList=idList, command='Restart')  # Push the 'Restart' command
    return command  # Return the list of responses from push_command


    
