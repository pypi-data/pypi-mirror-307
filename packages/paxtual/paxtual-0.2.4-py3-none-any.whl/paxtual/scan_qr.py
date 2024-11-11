from textual.screen import Screen
from textual.widgets import Static, Input, Footer
from textual import on, work
from textual.app import ComposeResult
import pandas as pd
from .confmscn import Confirm_Screen
from .operations import apiPaxFunctions
from .functionsScreen import FunctionsScreen
from .paxStoreChecker import PaxStoreChecker, NA_Handler
from .replace_terminal_screen import ReplaceTerminal
 

class Scan_qr(Screen):
    """QR SCANNER"""
    BINDINGS = [("escape", "app.pop_screen", "BACK")]

    def __init__(self):
        self.serialNoList = []
        self.copySerialNoList = self.serialNoList
        self.exceptions = []
        self.ops = apiPaxFunctions()
        super().__init__()
    

    def compose(self) -> ComposeResult:
        yield Static("PlEASE SCAN QR CODE TO BEGIN", classes="question" )
        yield Input(placeholder=">>>>")
        yield Footer()
    @on(Input.Submitted)
    @work
    async def fix_qr(self) -> None:
        self.l = self.query_one(Input).value
        self.disabled = True
        self.serialNoList = eval(self.l)  # Assuming the QR code contains a list of serial numbers
        sndf = pd.DataFrame({"serialNo":self.serialNoList})
        if await self.app.push_screen_wait(Confirm_Screen(f"Are these terminals you wish to activate\n{self.serialNoList}?")):
            self.notify("SEARCHING>>>")
            check = PaxStoreChecker(self.serialNoList)
            if check.not_in_paxStore:  # If some terminals are not found in PaxStore
                if await self.app.push_screen_wait(Confirm_Screen(f"These Terminals are not registered: {check.not_in_paxStore}\nDo you want to register now? ")):  # Ask the user if they want to register the missing terminals
                    adder = NA_Handler(check.not_in_paxStore)  # Handle the registration of new terminals
                    if adder.exceptions_list:  # If there are exceptions during registration
                        self.exceptions.extend(exception for exception in adder.exceptions_list)  # Add the exceptions to the exceptions list
                        if await self.app.push_screen_wait(Confirm_Screen(f"The following can not be added to the PaxStore\n{adder.exceptions_list}\n Please escalate to Eval 2. Please choose:", "Remove", "Replace")):  # Ask the user to either remove or replace the problematic terminals
                            for exception in self.exceptions:  # If the user chooses to replace the excepted terminal with different unit
                                replace = await self.app.push_screen_wait(ReplaceTerminal(exception))  # Get the replacement serial number from the user
                                index = self.serialNoList.index(exception)  # Find the index of the exception in the order_of_input list
                                self.serialNoList[index] = replace  # Replace the exception with the new serial number
                                self.app.notify(str(f'{exception} replaced with {replace}'))  # Notify the user about the replacement
                        else:  # If the user chooses to remove
                            self.app.push_screen(Confirm_Screen(f"Please remove these terminals before continuing \n{check.not_in_paxStore}"))  # Instruct the user to remove the problematic terminals
                    self.app.notify(str(adder.terminal_data))  # Notify the user about the added terminals
                else:  # If the user doesn't want to register the missing terminals
                    self.app.push_screen(Confirm_Screen(f"Please remove these terminals before continuing \n{check.not_in_paxStore}"))  # Instruct the user to remove the missing terminals
                    self.exceptions.extend(serial for serial in check.not_in_paxStore)  # Add the missing terminals to the exceptions list
            # Filter the order_of_input list to remove exceptions
            final_list = [serial for serial in self.serialNoList if serial not in self.exceptions]
            self.exceptions.clear()  # Clear the exceptions list
            # Proceed with connecting to the network and opening PaxStore on the terminals
            if await self.app.push_screen_wait(Confirm_Screen("Please connect to network and open PaxStore on terminals")):
                self.group = await self.ops.startPaxGroup(final_list)  # Start a PaxGroup with the valid serial numbers
                # Check for accessories and their registration in PaxStore
                if self.group['accessory'].any():
                    check2 = PaxStoreChecker(self.group['accessory'].dropna())
                    if check2.not_in_paxStore:
                        if await self.app.push_screen_wait(Confirm_Screen(f"These Terminals are not registered: {check2.not_in_paxStore}\nDo you want to register now?")):
                            adder2 = NA_Handler(check2.not_in_paxStore)
                            if adder2.exceptions_list:
                                if await self.app.push_screen_wait(Confirm_Screen(f"The following can not be added to the PaxStore\n{adder2.exceptions_list}\n Please escalate to Eval 2.")):
                                    pass  # Handle exceptions for accessories (currently just passes)
                self.app.notify(str(self.group))  # Notify the user about the group details
                self.app.push_screen(FunctionsScreen(pd.DataFrame(self.group)))  # Push the FuctionsScreen with the group data

