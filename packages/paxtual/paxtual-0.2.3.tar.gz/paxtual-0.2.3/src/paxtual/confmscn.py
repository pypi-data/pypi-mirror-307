from textual.app import  ComposeResult
from textual.widgets import Static, Button
from textual.screen import  ModalScreen
from textual.containers import Grid



class Confirm_Screen(ModalScreen[bool]):
    """
    A modal screen to display a confirmation message with options.
    """

    CSS_PATH = "css_lib/confirm_screen.tcss"  # Specify the CSS file path for styling this screen

    def __init__(self, message: str, option1="Cancel", option2="OK"):
        """
        Initializes the Confirm_Screen with a message and button options.

        Args:
            message (str): The message to display.
            option1 (str, optional): The label for the first button. Defaults to "Cancel".
            option2 (str, optional): The label for the second button. Defaults to "OK".
        """

        self.message = message  # Store the message to display
        self.option1 = option1  # Store the label for the first button
        self.option2 = option2  # Store the label for the second button
        super().__init__()  # Call the superclass constructor

    def compose(self) -> ComposeResult:
        """
        Composes the screen with a message and buttons.
        """

        yield Grid(  # Create a Grid container to arrange the widgets
            Static(self.message, id="question"),  # Display the message as a Static widget
            Button(f"{self.option1}", id="cancel", variant="error"),  # Create the first button with the specified label and variant
            Button(f"{self.option2}", id="ok", variant="success"),  # Create the second button with the specified label and variant
            id="confirmscreen"  # Set an ID for the Grid container
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handles button presses to dismiss the screen with True or False.
        """

        if event.button.id == "ok":  # If the "OK" button is pressed
            self.dismiss(True)  # Dismiss the screen and return True
        else:  # If any other button (e.g., "Cancel") is pressed
            self.dismiss(False)  # Dismiss the screen and return False
            