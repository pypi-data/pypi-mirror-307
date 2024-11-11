import pandas as pd
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button, Header, Footer
from textual import on, work
from textual.containers import Container, VerticalScroll
from .DFTable import DataFrameTable
from .ti_labels_iccid import create_pdf
from .confmscn import Confirm_Screen
from .SingleTermDetailsScreen import parseList
from .SingleTermDetailsScreen import TerminalDetailsScreen
from .commands import reboot
from .operations import apiPaxFunctions, PushConfigs, resetTerminals


class FunctionsScreen(Screen):
    """
    A screen to display and perform functions on a group of Pax terminals.
    """

    BINDINGS = [("escape", "app.pop_screen", "BACK")]
    CSS_PATH = "css_lib/group_gunctions.tcss"

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Initializes the FunctionsScreen with a DataFrame of terminal information.

        Args:
            df (pd.DataFrame): A DataFrame containing terminal details.
        """

        self.df = df
        self.button_list = [
            {'name': 'Reset Group', 'id': 'reset', 'classes': 'gtask-buttons'},
            {'name': 'Activate Group', 'id': 'activate', 'classes': 'gtask-buttons'},
            {'name': 'Deactivate', 'id': 'deactivate', 'classes': 'gtask-buttons'},
            {'name': 'Reboot Group', 'id': 'reboot', 'classes': 'gtask-buttons'},
            {'name': 'Refresh Terminal Detials', 'id': 'details', 'classes': 'gtask-buttons'},
            {'name': 'Create Ticket Labels', 'id': 'labels', 'classes': 'gtask-buttons'}
        ]
        self.op = apiPaxFunctions()  # Create an instance of apiPaxFunctions
        self.configop = PushConfigs()  # Create an instance of PushConfigs
        self.operations = {
            "activate": self.op.activateTerminals,
            "details": self.op.startPaxGroup,
            "deactivate": self.op.disableTerminals,
            "reboot": reboot,  # Assuming reboot is defined elsewhere
            "reset": resetTerminals,
            "labels": create_pdf,
            "payanywhere": self.configop.paPushByReseller,
            "broadpos": self.configop.pushBroadPosEPX,
            "other": self.configop.pushBroadPos_nonEPX
        }
        self.functionDict = {}
        super().__init__()

    def compose(self) -> ComposeResult:
        """
        Composes the screen with widgets to display the terminal data and buttons for actions.
        """

        yield Header(name='PaxTools')
        with Container(id="app-grid"):
            with VerticalScroll(id="top-pane"):
                yield DataFrameTable()  # Display the terminal data in a table
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

    async def on_mount(self):
        """
        Called when the screen is mounted. Adds the DataFrame to the table and reorders columns.
        """

        self.table = self.query_one(DataFrameTable)
        # Define the desired column order
        self.new_order = ['serialNo', 'status', 'modelName', 'pn', 'resellerName', 'iccid', 'accessory', 'osVersion']
        # Reorder columns based on the new order, keeping only those present in the new order list
        self.reordered_columns = [col for col in self.new_order if col in self.df.columns]  
        self.ordered_df = self.df[self.reordered_columns]
        self.table.add_df(self.ordered_df)  # Add the DataFrame to the table

    @on(Button.Pressed)
    @work
    async def do_stuff(self, event: Button.Pressed):
        """
        Handles button press events to perform actions on the group of terminals.
        """

        operation = self.operations.get(event.button.id)
        # Display a confirmation screen before proceeding with the operation
        if await self.app.push_screen_wait(Confirm_Screen("Please confirm terminal network connection and open PaxStore client on device.")):  
            try:
                # Perform the selected operation on the terminals
                result = await operation(idList=self.df['id'], serialNoList=self.df['serialNo'], df=self.df)  
                self.notify(str(result))  # Display a notification with the result
                refresh = await self.op.startPaxGroup(self.df['serialNo'])  # Refresh terminal details
                self.ndf = pd.DataFrame(refresh).drop_duplicates(subset=["serialNo"])
                # Reorder columns in the refreshed DataFrame
                refresh_reordered_columns = [col for col in self.new_order if col in self.ndf.columns]  
                self.reorg = self.ndf[refresh_reordered_columns]
                self.table.update_df(self.reorg)  # Update the table with the refreshed data
                self.df = self.ndf  # Update the DataFrame
            except Exception as e:
                # If an error occurs, display an error message
                if await self.app.push_screen_wait(Confirm_Screen(f"Encountered Error. Stop messing up")):  
                    pass

    @work
    @on(DataFrameTable.CellSelected)
    async def note_cell(self, event: DataFrameTable.CellSelected):
        """
        Handles cell selection events in the DataFrameTable.

        If a serial number is selected, displays a confirmation screen to view the terminal details.
        """

        if event.value in self.df['serialNo'].values: #if the clicked cell's value matches an item in the list of serial numbers
            # Display a confirmation screen before navigating to the terminal details screen
            if await self.app.push_screen_wait(Confirm_Screen(message=f"View {event.value} Terminal Page?")):  
                try:
                    dList = [event.value] #clicked terminal serial number in a list
                    termDetails = await parseList(dList)  # Get terminal details and application data
                    self.app.notify(str(termDetails))
                    # Navigate to the TerminalDetailsScreen to display the information
                    self.app.push_screen(TerminalDetailsScreen(termDetails))  
                except Exception as e:
                    # If an error occurs, display an error message with instructions
                    if await self.app.push_screen_wait(Confirm_Screen(f"An error occured! Make sure the terminal is connected to a network and the PaxStore client is open on the Device!")):  
                        pass    
