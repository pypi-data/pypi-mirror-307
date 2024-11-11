
from textual.app import ComposeResult, App
from textual.widgets import Static, Button
from textual.screen import Screen
from textual.containers import Grid
from textual import on
from .scan_v2 import Scan_serials
from .scan_qr import Scan_qr


class Select_QR_or_Barcode(Screen[bool]):
    """
    A screen to allow the user to select between scanning a QR code or a barcode.
    """

    BINDINGS = [("escape", "app.pop_screen", "BACK")]
    CSS_PATH = "css_lib/confirm_screen.tcss"

    def compose(self) -> ComposeResult:
        """
        Composes the screen with buttons for selecting QR code or barcode scanning.
        """

        yield Grid(
            Static("Please select input method:", id="question"),
            Button("SCAN QR CODE", name="QR", id="qr"),
            Button("SCAN BARCODE", name='BC', id='BC'),
            id="confirmscreen"
        )

    @on(Button.Pressed, "#qr")
    def push_qr_screen(self) -> None:
        """
        Pushes the Scan_qr screen when the "SCAN QR CODE" button is pressed.
        """

        self.app.push_screen(Scan_qr())

    @on(Button.Pressed, "#BC")
    def push_bcScreen(self) -> None:
        """
        Pushes the Scan_serials screen when the "SCAN BARCODE" button is pressed.
        """

        self.app.push_screen(Scan_serials())


class PAX_TUI(App):
    """
    The main Textual application class for the Pax terminal tool.
    """

    def on_mount(self) -> None:
        """
        Called when the application is mounted. Pushes the Select_QR_or_Barcode screen.
        """

        self.push_screen(Select_QR_or_Barcode())
         

