from .notasync import findSingleTerminal, createSingleTerminal
from .tui_exceptions import TerminalNotFoundError, TerminalNotAvailableError


class PaxStoreChecker():
    """
    Checks the availability of Pax terminals in PaxStore.
    """

    def __init__(self, serialNoList) -> None:
        """
        Initializes the PaxStoreChecker with a list of serial numbers.

        Args:
            serialNoList (list): A list of serial numbers to check.
        """

        self.serialNoList = serialNoList
        self.terminal_data = []  # List to store data of terminals found in PaxStore
        self.not_in_paxStore = []  # List to store serial numbers not found in PaxStore
        for serialNo in self.serialNoList:
            try:
                response = findSingleTerminal(serialNo)  # Attempt to find the terminal in PaxStore
                self.terminal_data.append(response)  # Add the terminal data to the list if found
            except TerminalNotFoundError as not_found:
                self.not_in_paxStore.append(not_found.serial_no)  # Add the serial number to the not found list


class NA_Handler():
    """
    Handles the creation of Pax terminals in PaxStore.
    """

    def __init__(self, serialNoList) -> None:
        """
        Initializes the NA_Handler with a list of serial numbers.

        Args:
            serialNoList (list): A list of serial numbers to register in PaxStore.
        """

        self.serialNoList = serialNoList
        self.exceptions_list = []  # List to store serial numbers that could not be created
        self.terminal_data = []  # List to store data of successfully created terminals
        for serialNo in self.serialNoList:
            try:
                response = createSingleTerminal(serialNo)  # Attempt to create the terminal in PaxStore
                self.terminal_data.append(response)  # Add the terminal data to the list if created
            except TerminalNotAvailableError as n_a:
                self.exceptions_list.append(n_a.serial_no)  # Add the serial number to the exceptions list

    



        
        

    