from textual.app import ComposeResult, App
from textual.widgets import Static, Button, Input, Header, Footer
from textual.screen import Screen, ModalScreen
from textual.containers import Grid
from .confmscn import Confirm_Screen
from textual import  on, work
from .paxModule import *
from .serialNoValidator import SerialNoValidator
from .paxStoreChecker import PaxStoreChecker, NA_Handler




class ReplaceTerminal(ModalScreen):

    def __init__(self,to_replace):
        self.to_replace = to_replace
        self.serialValidator = SerialNoValidator()  # Create an instance of the validator
        super().__init__()


    def compose(self) -> ComposeResult:
        
        yield Static(f"SCAN OR TYPE SERIAL NUMBER TO REPLACE {self.to_replace}:")
        yield Input(placeholder="S/N",validators=[self.serialValidator])

    
    @on(Input.Submitted)
    @work

    async def replace_terminal(self):
        user_input = self.query_one(Input)
        replacement = user_input.value
        check = PaxStoreChecker([replacement])
        if check.not_in_paxStore:
            if await self.app.push_screen_wait(Confirm_Screen(f"These Terminals are not registered: {check.not_in_paxStore}\nDo you want to register now? ")):
                adder = NA_Handler(check.not_in_paxStore)
                if adder.exceptions_list:
                    if await self.app.push_screen_wait(Confirm_Screen(f"The following can not be added to the PaxStore\n{adder.exceptions_list}\n Please escalate to Eval 2")):
                        user_input.clear()
        else:
            if await self.app.push_screen_wait(Confirm_Screen(f"Replace {self.to_replace} with {replacement}?")):
                self.dismiss(replacement)
            else:
                user_input.clear()
                


class replace(App):

    def on_mount(self) -> None:
        self.push_screen(ReplaceTerminal("test"))
         

if __name__ == "__main__":
    app = replace()
    app.run()
