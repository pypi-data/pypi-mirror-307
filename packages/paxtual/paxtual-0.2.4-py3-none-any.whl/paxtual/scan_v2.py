
from textual.app import App, ComposeResult
from textual.widgets import Static, Input, Header,Footer
from textual.screen import ModalScreen
from .confmscn import Confirm_Screen
from textual import on, work
import pandas as pd
from .operations import apiPaxFunctions
from .serialNoValidator import SerialNoValidator
from .paxStoreChecker import PaxStoreChecker, NA_Handler
from .functionsScreen import FunctionsScreen
from .replace_terminal_screen import ReplaceTerminal

class Scan_serials(ModalScreen):
    """
    This class represents a screen for scanning or typing serial numbers of payment terminals. 
    It handles user input, validates serial numbers, checks their existence in PaxStore, 
    and allows registration of new terminals.
    """

    BINDINGS = [
        ("escape", "app.pop_screen", "BACK"),  # Bind 'escape' key to go back to the previous screen
        ("0000", "", "SUBMIT"),  # Bind '0000' input to finish serial number entry
        ("BKSPC", "", "Delete Previous item")   # Bind 'BKSPC' input to delete the last entered serial number
    ]

    def __init__(self):
        """
        Initializes the Scan_serials screen.
        """
    def __init__(self):
        self.order_of_input = [] # list of all input in order of input
        self.serialValidator = SerialNoValidator()  # Create an instance of the validator
        self.exceptions = [] # list of all terminals not found in PaxStore
        self.ops = apiPaxFunctions() # Instance of apiPaxFunctions for PaxStore operations
        super().__init__()

    def compose(self) -> ComposeResult:
        """
        Composes the layout of the screen.
        """
        yield Header(name='PaxTools')  # Add a header with the title "PaxTools"
        yield Static("SCAN OR TYPE SERIAL NUMBER. Type 0000 to complete. Type BKSPC to delete previously scanned serial number:")  # Add a static label for instructions
        yield Input(placeholder="S/N", validators=[self.serialValidator])  # Add an input field for serial numbers with validation
        yield Footer()  # Add a footer to the screen

    @on(Input.Submitted)  # Decorator to trigger this function when Input is submitted
    @work  # Decorator to run this function as a background task
    async def update_serial_list(self):
        """
        Handles the submitted serial number input.
        """
        user_input = self.query_one(Input)  # Get the value from the Input field
        self.order_of_input.append(user_input.value)  # Add the input to the order_of_input list
        serialNo = user_input.value  # Assign the input value to serialNo
        self.mount(Static(str(user_input.value)))  # Display the entered serial number on the screen
        # Handle special inputs
        if user_input.value == "BKSPC":  # If input is "BKSPC", remove the last entry from order_of_input
            self.order_of_input.pop()
            self.order_of_input.pop() # list.pop is called twice due to idiosyncratic logic of the Textual Library. It needs to be there
        if ":" in user_input.value:  # If input contains ":", remove the  entry from order_of_input and produce a bell sound
            self.order_of_input.pop()
            self.app.bell()
        if user_input.value == "0000":  # If input is "0000", disable the input field, produce a bell sound, and proceed to check PaxStore
            self.disabled = True
            self.app.bell()
            self.order_of_input.pop()
            # Check if the entered serial numbers exist in PaxStore
            check = PaxStoreChecker(self.order_of_input)
            if check.not_in_paxStore:  # If some terminals are not found in PaxStore
                if await self.app.push_screen_wait(Confirm_Screen(f"These Terminals are not registered: {check.not_in_paxStore}\nDo you want to register now? ")):  # Ask the user if they want to register the missing terminals
                    adder = NA_Handler(check.not_in_paxStore)  # Handle the registration of new terminals
                    if adder.exceptions_list:  # If there are exceptions during registration
                        self.exceptions.extend(exception for exception in adder.exceptions_list)  # Add the exceptions to the exceptions list
                        if await self.app.push_screen_wait(Confirm_Screen(f"The following can not be added to the PaxStore\n{adder.exceptions_list}\n Please escalate to Eval 2. Please choose:", "Remove", "Replace")):  # Ask the user to either remove or replace the problematic terminals
                            for exception in self.exceptions:  # If the user chooses to replace the excepted terminal with different unit
                                replace = await self.app.push_screen_wait(ReplaceTerminal(exception))  # Get the replacement serial number from the user
                                index = self.order_of_input.index(exception)  # Find the index of the exception in the order_of_input list
                                self.order_of_input[index] = replace  # Replace the exception with the new serial number
                                self.app.notify(str(f'{exception} replaced with {replace}'))  # Notify the user about the replacement
                        else:  # If the user chooses to remove
                            self.app.push_screen(Confirm_Screen(f"Please remove these terminals before continuing \n{check.not_in_paxStore}"))  # Instruct the user to remove the problematic terminals
                    self.app.notify(str(adder.terminal_data))  # Notify the user about the added terminals
                else:  # If the user doesn't want to register the missing terminals
                    self.app.push_screen(Confirm_Screen(f"Please remove these terminals before continuing \n{check.not_in_paxStore}"))  # Instruct the user to remove the missing terminals
                    self.exceptions.extend(serial for serial in check.not_in_paxStore)  # Add the missing terminals to the exceptions list
            # Filter the order_of_input list to remove exceptions
            final_list = [serial for serial in self.order_of_input if serial not in self.exceptions]
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

        user_input.clear()  # Clear the input field

        
class scan_v2(App):

    def on_mount(self) -> None:
         self.push_screen(Scan_serials())
         

if __name__ == "__main__":
    app = scan_v2()
    app.run()

