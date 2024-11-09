
class ModbusException(Exception):
    """A custom exception for demonstration purposes."""

    def __init__(self, message, extra_info=None):
        super().__init__(message)
        self.extra_info = extra_info


class VictronException(Exception):
    """A custom exception for victron."""

    def __init__(self, message, extra_info=None):
        super().__init__(message)
        self.extra_info = extra_info