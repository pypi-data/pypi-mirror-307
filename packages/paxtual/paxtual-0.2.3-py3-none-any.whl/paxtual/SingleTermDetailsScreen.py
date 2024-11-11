from textual.widgets import MarkdownViewer, Button, Footer, Header, Static
from textual.app import  ComposeResult
from textual.screen import Screen
from textual.widgets import Footer
from textual.containers import Container, VerticalScroll
from textual import  on, work
import pandas as pd
from .ti_labels_iccid import create_pdf
from .confmscn import Confirm_Screen
from .commands import reboot
from .operations import apiPaxFunctions, getInstalledConfig, PushConfigs, resetTerminals



async def parseList(serialNoList) -> dict:
    """
    Parses a list of serial numbers to retrieve terminal details and installed configurations.

    Args:
        serialNoList (list): A list of terminal serial numbers.

    Returns:
        tuple: A tuple containing two elements:
            - termDetails_dict (dict): A dictionary of terminal details.
            - apklist (list): A list of installed APKs for the last terminal in the list.
    """

    thing = apiPaxFunctions()  # Create an instance of apiPaxFunctions
    # Get terminal details (excluding accessory information)
    termDetail = await thing.startPaxGroup(serialNoList, handleAccessory=False)  
    config = await getInstalledConfig(serialNoList)  # Get installed configuration for the terminals
    for item in config:  # Iterate through the configuration data for each terminal
        apklist = item['installedApks']  # Extract the list of installed APKs
    termDetails_dict = termDetail.to_dict('records')  # Convert the terminal details DataFrame to a dictionary
    return termDetails_dict, apklist  # Return the terminal details and the list of installed APKs


def update_table(appdata):
    """
    Formats application data into a markdown table.

    Args:
        appdata (list): A list of dictionaries, where each dictionary represents an installed application.

    Returns:
        str: A markdown formatted table of the application data.
    """

    headers = " | ".join(appdata[0].keys()) + " \n| --------------- | --------------- | --------------- | --------------- | --------------- |"
    rows = "\n|".join(["|".join(str(value) for value in item.values()) + "|" for item in appdata])
    content = f"## Installed Applications\n\n|{headers} \n|{rows}"
    return content


def format_terminal_details(termDetails: dict, appdata: list):
    """
    Formats terminal details and application data into a markdown string.

    Args:
        termDetails (dict): A dictionary of terminal details.
        appdata (list): A list of dictionaries, where each dictionary represents an installed application.

    Returns:
        str: A markdown formatted string of the terminal details and application data.
    """

    text = ""
    text += "## Basic Info\n\n"
    for key, value in termDetails.items():
        if key == "serialNo":
            text += f"**Serial No:** {value}\n"
    for key, value in termDetails.items():
        if key != "serialNo":
            text += f"* {key}: {value}\n"
    text += update_table(appdata)
    return text


class TerminalDetailsScreen(Screen):
    """
    A screen to display terminal details and perform actions on the terminal.
    """

    BINDINGS = [("escape", "app.pop_screen", "BACK")]
    CSS_PATH = "css_lib/singleTermDetails.tcss"

    def __init__(self, details: tuple):
        """
        Initializes the TerminalDetailsScreen with terminal details and application data.

        Args:
            details (tuple): A tuple containing two elements:
                - termdetails (dict): A dictionary of terminal details.
                - appdata (list): A list of dictionaries, where each dictionary represents an installed application.
        """

        self.termdetails = details[0]
        self.df = pd.DataFrame(details[0])
        self.appdata = details[1]
        self.markdown = format_terminal_details(*self.termdetails, self.appdata)
        #list to create operations buttons
        self.button_list = [
            {'name':'Reset Terminal', 'id': 'reset', 'classes':'gtask-buttons'},
            {'name':'Activate Terminal','id':'activate','classes':'gtask-buttons'},
            {'name':'Deactivate Terminal','id':'deactivate','classes':'gtask-buttons'},
            {'name':'Reboot Terminal', 'id':'reboot', 'classes':'gtask-buttons'},
            {'name':'Refresh Terminal Detials','id':'details','classes':'gtask-buttons'},
            {'name':'Create Label', 'id':'labels', 'classes':'gtask-buttons'}
        ]
        self.op = apiPaxFunctions()  # Create an instance of apiPaxFunctions
        self.configop = PushConfigs()  # Create an instance of PushConfigs
        # bind the button ids to PaxStoreApi operations
        self.operations = {
            "activate": self.op.activateTerminals,
            "details": self.op.startPaxGroup,
            "deactivate": self.op.disableTerminals, 
            "move": None,
            "reboot": reboot,
            "reset": resetTerminals,
            "labels": create_pdf,
            "payanywhere": self.configop.paPushByReseller,
            "broadpos":self.configop.pushBroadPosEPX,
            "other": self.configop.pushBroadPos_nonEPX
        }
        self.functionDict = {}
        super().__init__()

    def compose(self) -> ComposeResult:
        """
        Composes the screen with widgets to display terminal details and buttons for actions.
        """

        yield Header(name='PaxTools')
        with Container(id="app-grid"):
            with VerticalScroll(id="top-pane"):
                # Display terminal details and application data in a markdown viewer
                yield MarkdownViewer(markdown=self.markdown, show_table_of_contents=True, id="mkdn")  
            with VerticalScroll(id="bottom-left"):
                yield Static("Available Tasks", classes="titleheader")
                for button in self.button_list:
                    yield Button(button['name'], id=button['id'], classes=button['classes'])
            with VerticalScroll(id="bottom-right"):
                yield Static("Configuration Tasks", classes="titleheader")
                yield Button("Config for PayAnywhere", id="payanywhere", classes="buttons")
                yield Button("Config for BroadPOS - EPX", id="broadpos", classes="buttons")
                yield Button("Config for BroadPOS - Not EPX", id="other", classes="buttons")
        yield Footer()

    @on(Button.Pressed)
    @work
    async def do_stuff(self, event: Button.Pressed):
        """
        Handles button press events to perform actions on the terminal.
        """

        operation = self.operations.get(event.button.id)
        # Display a confirmation screen before proceeding with the operation
        if await self.app.push_screen_wait(Confirm_Screen("Please confirm terminal network connection and open PaxStore client on device.")):  
            try:
                result = await operation(idList = self.df['id'], serialNoList = self.df['serialNo'], df = self.df)  # type: ignore
                self.notify(str(result))
                if event.button.id == "details":
                    resp = await parseList(self.df['serialNo'])
                    updateTermDetails = resp[0]
                    updateAPKinfo = resp[1]
                    self.markdown=format_terminal_details(*updateTermDetails,updateAPKinfo)
            except Exception as e:
                    if await self.app.push_screen_wait(Confirm_Screen(f"Create Labels for Single Terminal Screen is temporarily not available for E-Series. Please create labels from the Group Functions Screen")):
                        pass