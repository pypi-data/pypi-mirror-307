from textual.app import ComposeResult, App
from textual.widgets import Static, Input
from textual.screen import ModalScreen
from .confmscn import Confirm_Screen
from textual import on, work
from .serialNoValidator import SerialNoValidator
from .paxStoreChecker import PaxStoreChecker, NA_Handler


class ReplaceTerminal(ModalScreen):
    """
    A modal screen to handle replacing a terminal that can not be registered to the PaxStore with an alternate terminal.
    """

    def __init__(self, to_replace):
        """
        Initializes the ReplaceTerminal screen with the serial number of the terminal to be replaced.

        Args:
            to_replace (str): The serial number of the terminal to be replaced.
        """

        self.to_replace = to_replace
        self.serialValidator = SerialNoValidator()  # Create an instance of the serial number validator
        super().__init__()

    def compose(self) -> ComposeResult:
        """
        Composes the screen with widget to input the replacement terminal's serial number.
        """

        yield Static(f"SCAN OR TYPE SERIAL NUMBER TO REPLACE {self.to_replace}:")
        # Input widget with placeholder and serial number validator
        yield Input(placeholder="S/N", validators=[self.serialValidator])  

    @on(Input.Submitted)
    @work
    async def replace_terminal(self):
        """
        Handles the submission of the replacement terminal's serial number.

        Checks if the replacement terminal is in PaxStore and prompts for registration if not.
        Confirms the replacement and dismisses the screen with the replacement serial number.
        """

        user_input = self.query_one(Input)
        replacement = user_input.value  # Get the entered serial number as a string
        check = PaxStoreChecker([replacement])  # Check if the serial number is in PaxStore
        if check.not_in_paxStore:
            # If the terminal is not in PaxStore, ask if the user wants to register it
            if await self.app.push_screen_wait(Confirm_Screen(f"These Terminals are not registered: {check.not_in_paxStore}\nDo you want to register now? ")):  
                adder = NA_Handler(check.not_in_paxStore)  # Attempt to register the terminal
                if adder.exceptions_list:
                    # If there are exceptions during registration, display an error message
                    if await self.app.push_screen_wait(Confirm_Screen(f"The following can not be added to the PaxStore\n{adder.exceptions_list}\n Please escalate to Eval 2")):  
                        user_input.clear()  # Clear the input field
        else:
            # If the terminal is in PaxStore, confirm the replacement
            if await self.app.push_screen_wait(Confirm_Screen(f"Replace {self.to_replace} with {replacement}?")):  
                self.dismiss(replacement)  # Dismiss the screen and return the replacement serial number
            else:
                user_input.clear()  # Clear the input field
                
class replace(App):

    def on_mount(self) -> None:
        self.push_screen(ReplaceTerminal("test"))
         

if __name__ == "__main__":
    app = replace()
    app.run()
