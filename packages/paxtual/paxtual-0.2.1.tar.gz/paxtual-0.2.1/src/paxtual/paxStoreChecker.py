from .paxModule import apiPaxFunctions
from.notasync import findSingleTerminal, createSingleTerminal
from .tui_exceptions import TerminalNotFoundError, TerminalNotAvailableError

class PaxStoreChecker():

    def __init__(self, serialNoList) -> None:
        
        self.serialNoList = serialNoList
        self.terminal_data = []
        self.not_in_paxStore = []
        self.ops = apiPaxFunctions()
        for serialNo in self.serialNoList:
            try:
                response =  findSingleTerminal(serialNo)
                self.terminal_data.append(response)
            except TerminalNotFoundError as not_found:
                self.not_in_paxStore.append(not_found.serial_no)

class NA_Handler():
        def __init__(self, serialNoList) -> None:
            
            self.serialNoList = serialNoList
            self.exceptions_list = []
            self.terminal_data = []
            for serialNo in self.serialNoList:
                try: 
                    response = createSingleTerminal(serialNo)
                    self.terminal_data.append(response)
                except TerminalNotAvailableError as n_a:
                    self.exceptions_list.append(n_a.serial_no)

    
        
        """print("These are in:"+str(self.terminal_data)+str(len(self.terminal_data)))
        print("Not found:",str(self.not_in_paxStore))"""


        """if self.not_in_paxStore:
            create = await self.ops.createTerminals(self.not_in_paxStore)"""


"""
serialNoList = [
    '0822639772',
    '0821674609',
    '1850116006',
    '1850282418',
    '0822777971'
    ]

test = PaxStoreChecker(serialNoList)
asyncio.run(test.check_for_terminal())
print(test.not_in_paxStore)
print(test.terminal_data)"""



        
        

    