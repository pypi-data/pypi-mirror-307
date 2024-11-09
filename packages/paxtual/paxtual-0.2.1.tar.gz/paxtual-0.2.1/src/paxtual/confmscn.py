from textual.app import  ComposeResult
from textual.widgets import Static, Button
from textual.screen import  ModalScreen
from textual.containers import Grid



class Confirm_Screen(ModalScreen[bool]):
    CSS_PATH = "css_lib/cofirm_screen.tcss"

    def __init__(self, message:str, option1 = "Cancel", option2 = "OK"):
        self.message = message
        self.option1 = option1
        self.option2 = option2
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Grid(
            Static(self.message, id="question"),
            Button(f"{self.option1}", id="cancel", variant="error"),
            Button(f"{self.option2}", id="ok", variant="success")
            ,id="confirmscreen"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "ok":
            self.dismiss(True)
        else:
            self.dismiss(False)