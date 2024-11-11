class PaxTerms():
    """
    This class stores and manages information about different PAX terminal models, 
    their accessories, and associated software packages.
    """
    def __init__(self, serialNo:str,**kwargs) -> None:
        """
        Initializes a PaxTerms object with the given serial number.

        Args:
            serialNo (str): The serial number of the PAX terminal.
            **kwargs: Optional keyword arguments (not used in the current implementation).
        """
        # Dictionary containing data for various terminal models
        self.termtool = {
            "119": {"modelName": "E600", "serial_range":"119", "name":"TR_E600", "type":"Ev1_Series", "terminal_no":"12", "resellerName": "Repair","fmName":"E600_PayDroid_7.1.1_Virgo_V04.1.18_20240124", "hasAccessory":True, "accessory":
            {"modelName":"Q20L", "serial_range": "114", "name": "TR_E600-Q20", "type":"Qv1_Series", "terminal_no":"124", "resellerName": "Repair", 'parent': 'E600'}},
            "134": {"modelName": "E700", "serial_range":"134", "name":"TR_E700", "type":"Ev1_Series", "resellerName": "Repair","fmName": "E700_PayDroid_7.1.2_Scorpio_V10.1.29_20240320", "hasAccessory":True, "accessory":
            {"modelName":"Q20L", "serial_range": "114", "name": "TR_E700-Q20", "type":"Qv1_Series", "terminal_no":"124", "resellerName": "Repair", 'parent': 'E700'}},
            "115": {"modelName": "E500", "serial_range":"115", "name":"TR_E500", "type":"Ev1_Series", "terminal_no":"2", "resellerName": "Repair","fmName": "E500_PayDroid_6.0.1_Taurus_V05.1.25_20230313","hasAccessory":True, "accessory":
            {"modelName":"Q20L", "serial_range": "114", "name": "TR_E500-Q20", "type":"Qv1_Series", "terminal_no":"124", "resellerName": "Repair", 'parent':'E500'}},
            "227": {"modelName": "E600M", "serial_range":"227", "name":"TR_E600M", "type":"Ev2_Series", "terminal_no":"415",  "resellerName": "Repair","fmName": "PayDroid_10.0.0_Acacia_V13.1.18_20240105","hasAccessory":True,"accessory":
            {"modelName":"Q10A", "serial_range": "240", "name": "TR_E600M-Q10", "type":"Qv2_Series", "terminal_no":"416", "resellerName": "Repair", 'parent': 'E600M'}},
            "082": {"modelName": "A920", "serial_range":"082", "name":"TR_A920", "type":"A_Series", "terminal_no":"1", "resellerName": "Repair","fmName": "PayDroid_5.1.1_Aquarius_V02.3.46_20240410","hasAccessory":False},
            "185": {"modelName": "A920Pro", "serial_range":"185", "name":"TR_A920Pro", "type":"A_Series", "terminal_no":"341", "resellerName": "Repair","fmName": "PayDroid_8.1.0_Sagittarius_V11.1.62_20240411","hasAccessory":False},
            "135": {"modelName": "A60", "serial_range":"135", "name":"TR_A60", "type":"A_Series", "terminal_no":"19",  "resellerName": "Repair","fmName": "A60_PayDroid_6.0_Leo_V07.1.17_20240415","hasAccessory":False},
            "124": {"modelName": "A80", "serial_range":"124", "name":"TR_A80", "type":"A_Series", "terminal_no":"26", "resellerName": "Repair","fmName": "PayDroid_10.0_Cedar_V17.2.19_20240313", "hasAccessory":False},
            "176": {"modelName": "A77", "serial_range":"176", "name":"TR_A77", "type":"A_Series", "terminal_no":"271", "resellerName": "Repair","fmName": "PayDroid_8.1.0_Sagittarius_V11.1.62_20240411","hasAccessory":False},
            "3A4": {"modelName": "SP30s", "serial_range":"3A4", "name":"TR_SP30", "type":"A_Series", "terminal_no":"180", "resellerName": "Repair","fmName":None, "hasAccessory":False},
            "3A6": {"modelName": "SP30s", "serial_range":"3A6", "name":"TR_SP30", "type":"A_Series", "terminal_no":"180", "resellerName": "Repair","fmName":None, "hasAccessory":False},
            "3A7": {"modelName": "SP30s", "serial_range":"3A7", "name":"TR_SP30", "type":"A_Series", "terminal_no":"180", "resellerName": "Repair","fmName":None, "hasAccessory":False},
            "3L0": {"modelName": "SP30s", "serial_range":"3L0", "name":"TR_SP30", "type":"A_Series", "terminal_no":"180", "resellerName": "Repair","fmName":None, "hasAccessory":False},
            "229": {"modelName": "A35", "serial_range":"229", "name":"RKI_A35", "type":"A_Series", "terminal_no":"362", "resellerName": "Repair","fmName": "PayDroid_10.0_Cedar_V17.2.19_20240313", "hasAccessory":False},
            "114": {"modelName": "Q20L", "serial_range":"114","name":'TR_E600-Q20', "type":"Qv1_Series", "hasAccessory":False, "resellerName":"Repair", "fmName":None},
            "240": {"modelName": "Q10A", "serial_range":"240","name":'TR_E600M-Q10', "type":"Qv2_Series","fmName": "Q10A_PayDroid_10_Cedar_V17.1.13_20240322","resellerName":"Repair", "hasAccessory":False},
            "189": {"modelName": "D135", "serial_range":"189", "name":"TR_D135", "type":"D-Series", "terminal_no":"421", "resellerName": "Repair", "fmName":None, "hasAccessory":False},
        }
        # Dictionary containing data for software packages to be pushed to the terminals NOT USED
        self.pushPATool = {
                "A_SeriespackageName": "com.pax.us.pay.std.broadpos.p2pe",
                "A_SeriespushTemplateName": "PA 6.9.1 E600M BroadPos P2PE V1.05.06",
                "A_SeriestemplateName":  "p2pe_20240325.zip",
                "A_Seriesversion": "V1.05.06_20240325",
                "Qv2_SeriespackageName": "com.pax.us.pay.std.broadpos.p2pe",
                "Qv2_SeriespushTemplateName": "PA 6.9.1 E600M BroadPos P2PE V1.05.06",
                "Qv2_SeriestemplateName": "p2pe_20240325.zip",
                "Qv2_Seriesversion": "V1.05.06_20240325",
                "Qv1_SeriespackageName":"BroadPOS-P2PE-Q20L",
                "Qv1_SeriespushTemplateName": "PA 6.8 Q20 BroadPOS P2PE Q20L V1.01.05_20230413",
                "Qv1_SeriestemplateName": "config.zip",
                "Qv1_Seriesversion": "V1.01.05_20230413",
                "Ev1_SeriespackageName": "com.pax.pdm",
                "Ev1_SeriestemplateName": "BasicSystem-Q20L_V1.00.07.zip",
                "Ev1_Seriesversion": None,
                "Ev1_SeriespushTemplateName": None,
                "Ev2_SeriespackageName": None,
                "Ev2_SeriestemplateName": None,
                "Ev2_Seriesversion": None,
                "Ev2_SeriespushTemplateName": None
        }

        self.serialNo = serialNo # Store the provided serial number
        serial_prefix = str(self.serialNo)[:3] # Extract the first 3 characters of the serial number

        # Access data from termtool based on serial number prefix
        if serial_prefix in self.termtool:
            term_data = self.termtool[serial_prefix]
            self.modelName = term_data.get("modelName")  # Get the model name
            self.name = term_data.get("name")  # Get the terminal name
            self.resellerName = term_data.get("resellerName")  # Get the reseller name
            self.type = term_data.get("type")  # Get the terminal type
            self.fmName = term_data.get("fmName")  # Get the firmware name
            self.hasAccessory = term_data.get("hasAccessory", False)  # Get whether the terminal has an accessory (default to False if not present)

            # If the terminal has an accessory, extract accessory details
            if self.hasAccessory:
                self.accessoryModelName = term_data["accessory"].get("modelName")
                self.accessoryName = term_data["accessory"].get("name")
                self.accessoryResellerName = term_data["accessory"].get("resellerName")
                self.accessoryType = term_data["accessory"].get("type")
            else:
                # If no accessory, set accessory attributes to None
                self.accessoryModelName = None
                self.accessoryName = None
                self.accessoryResellerName = None
                self.accessoryType = None

        # Access data from pushPATool based on terminal type NOT USED
        self.bPosPackageName = self.pushPATool[f"{self.type}packageName"]
        self.bPosPushTemplateName = self.pushPATool[f"{self.type}pushTemplateName"]
        self.bPosTemplateName = self.pushPATool[f"{self.type}templateName"]
        self.bPosPackageVersion = self.pushPATool[f"{self.type}version"]

async def fill_device_details(serial_number: str) -> dict:
    """
    Fills in device details in a dictionary using the PaxTerms class.

    Args:
        serial_number (str): The serial number of the device.

    Returns:
        dict: A dictionary with device details filled in.
    """

    device_details = {
        'id': None, 'name': None, 'tid': None, 'serialNo': None, 'status': None, 
        'merchantName': None, 'modelName': None, 'resellerName': None, 'createdDate': None, 
        'lastActiveTime': None, 'pn': None, 'osVersion': None, 'imei': None, 
        'screenResolution': None, 'language': None, 'ip': None, 'timeZone': None, 
        'macAddress': None, 'hasAccessory':None ,'accessory': None
    }
    pax_term = PaxTerms(serial_number)  # Create PaxTerms object
    # Update dictionary with matching attributes from PaxTerms object
    for key in device_details:
        if hasattr(pax_term, key):
            value = getattr(pax_term, key)
            if key == 'hasAccessory' and value is True:  # Check if hasAccessory is True
                device_details['accessory'] = pax_term.termtool[serial_number[:3]]['accessory'] 
            else:
                device_details[key] = value

    return device_details