class TerminalNotFoundError(Exception):
    """Exception raised when a terminal is not found in PaxStore."""
    def __init__(self, serial_no):
        super().__init__(f"Terminal SN {serial_no} not found in PaxStore.")
        self.serial_no = serial_no

class TerminalNotAvailableError(Exception):
    """Exception raised when a terminal is registered to another PaxStore."""
    def __init__(self, serial_no):
        super().__init__(f"Terminal SN {serial_no} can not be registered. Please remove terminal and Escalate to Eval 2")
        self.serial_no = serial_no

class InvalidOperationError(Exception):
    """Exception raised when an unsupported operation is called"""
    def __init__(self, operation):
        super().__init__(f"Specified {operation} does not exist. Please verify operation type") 
        self.operation = operation
