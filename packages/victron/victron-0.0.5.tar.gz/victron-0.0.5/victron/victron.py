from pyModbusTCP.client import ModbusClient
from loguru import logger as log

from . import constants as c
from . import exceptions as vException
from .exceptions import VictronException

class Victron():
    def __init__(self, host:str, port:int=502, unit_id:int=100, config:dict={}, timeout:int=10) -> None:
        self.host = host
        self.port = port
        self.unit_id = unit_id
        self.timeout = timeout
        self.client = None

        self.gridLimit = config.get(c.CFG_GRID_LIMIT, 2000)
        self.essFeedLimit = config.get(c.CFG_ESS_FEED_LIMIT, 2000)
        self.essChargeLimit = config.get(c.CFG_ESS_CHARGE_LIMIT, 2000)
        self.socDischargeLimit = config.get(c.CFG_SOC_DISCHARGE_LIMIT, 0)
        self.socChargeLimit = config.get(c.CFG_SOC_CHARGE_LIMIT, 100)
        self.batteryCapacity = config.get(c.CFG_BATTERY_CAPACITY, 0)

        self.connect()

    def connect(self, unit_id:int|None=None):
        """
        Connect to the Modbus TCP server.
        """
        self.client = ModbusClient(
            host=self.host,
            port=self.port,
            auto_open=True,
            auto_close=True,
            unit_id=self.unit_id if unit_id is None else unit_id,
            timeout=self.timeout
        )

    def parseValue(self, value:int) -> int:
        """
        Parse the value to a signed integer.
        """
        if value is not None:
            if value >= 32768:
                value = value - 65536
            return value

    def parseSetPoint(self, value:float) -> int:
        """
        Parse the Set Point value to an unsigned integer.
        """
        if value is not None:
            if value < 0:
                value = 65536 + value
            return int(value)

    def readSingleHoldingRegisters(self, address:int, parse:bool=True, unit_id:int|None=None) -> int:
        """
        Read a single holding register.
        When it fails, it will return None.
        """
        try:
            if self.client is None or unit_id is not None:
                log.error("Client not connected.")
                self.connect(unit_id=unit_id)
            value = self.client.read_holding_registers(address, 1)
            if value is None:
                raise vException.ModbusException(f"Failed to read register at address {address}.")
            value = value[0]
            if parse:
                return self.parseValue(value)
            return value
        except Exception as generalEx:
            raise VictronException(f"Failed to read register at address {address}. {generalEx}") from generalEx

    def writeSingleHoldingRegisters(self, address:int, value:float):
        """
        Write a single holding register.
        """
        try:
            if self.client is None:
                log.error("Client not connected.")
                self.connect()
            result = self.client.write_single_register(address, int(value))
            return result
        except Exception as generalEx:
            raise VictronException(f"Failed to write register at address {address}. {generalEx}") from generalEx

    def getSoc(self, address:int=843) -> float|None:
        """
        Get the State of Charge (SOC) from the the supplied address.
        """
        return self.readSingleHoldingRegisters(address)
    
    def isSocDischargeLimitReached(self, soc:float|None=None, socDischargeLimit:float|None=None) -> bool:
        """
        Check if the SOC limit is reached.
        """
        if soc is None:
            soc = self.getSoc()
            if soc is None:
                raise VictronException("Failed to get SOC.")
        if socDischargeLimit is None:
            if self.socDischargeLimit is None:
                raise VictronException("Failed to get SOC Limit.")
            socDischargeLimit = self.socDischargeLimit
        return soc <= socDischargeLimit

    def isSocChargeLimitReached(self, soc:float|None=None, socChargeLimit:float|None=None) -> bool:
        """
        Check if the SOC limit is reached.
        """
        if soc is None:
            soc = self.getSoc()
            if soc is None:
                raise VictronException("Failed to get SOC.")
        if socChargeLimit is None:
            if self.socChargeLimit is None:
                raise VictronException("Failed to get SOC Limit.")
            socChargeLimit = self.socChargeLimit
        return soc >= socChargeLimit

    def getPower(self, address:int=820):
        """
        Get the AC Power from the the supplied address.
        """
        return self.readSingleHoldingRegisters(address)

    def getEssSetPoint(self, address:int=2700):
        """
        Get the ESS Set Point from the the supplied address.
        """
        return self.readSingleHoldingRegisters(address)

    def applyLimit(self, value:int, limit:int) -> int:
        """
        Apply a limit to the value.
        """
        if value < 0:
            if value < (limit * -1):
                log.debug(f"Limit reached: {value} of {limit * -1}.")
                value = limit * -1
        else:
            if value > limit:
                log.debug(f"Limit reached: {value} of {limit}.")
                value = limit
        return value

    def applyGridLimit(self, value:int, girdLimit:int|None=None) -> int:
        """
        Apply the grid limit to the value.
        """
        if girdLimit is None:
            if self.gridLimit is None:
                raise VictronException("Failed to apply grid limit.")
            gridLimit = self.gridLimit
        return self.applyLimit(value, gridLimit)

    def applyFeedLimit(self, value:int, essFeedLimit:int|None=None) -> int:
        """
        Apply the feed limit to the value.
        """
        if essFeedLimit is None:
            if self.essFeedLimit is None:
                raise VictronException("Failed to apply feed limit.")
            essFeedLimit = self.essFeedLimit
        return self.applyLimit(value, essFeedLimit)

    def applyChargeLimit(self, value:int, essChargeLimit:int|None=None) -> int:
        """
        Apply the charge limit to the value.
        """
        if essChargeLimit is None:
            if self.essChargeLimit is None:
                raise VictronException("Failed to apply charge limit.")
            essChargeLimit = self.essChargeLimit
        return self.applyLimit(value, essChargeLimit)

    def setEssSetPoint(
            self,
            value:int,
            address:int=2700,
            soc:float|None=None,
            socDischargeLimit:float|None=None,
            socChargeLimit:float|None=None
    ) -> int:
        """
        Set the ESS Set Point.
        Applys the limit provided or by the configuration.

        Automatically sets the ESS Set Point to 0 if the SOC discharge or charge limit is reached.
        """
        if soc is None:
            soc = self.getSoc()
            if soc is None:
                raise VictronException("Failed to get SOC.")

        if socChargeLimit is None:
            if self.socDischargeLimit is None:
                raise VictronException("Failed to get SOC Discharge Limit.")
            socChargeLimit = self.socDischargeLimit # FIXME: should be socDischargeLimit

        if socDischargeLimit is None:
            if self.socDischargeLimit is None:
                raise VictronException("Failed to get SOC Charge Limit.")
            socDischargeLimit = self.socChargeLimit

        value = self.applyGridLimit(value) # apply grid limit for feed & charge
        if value < 0: # only apply feed limit if value is negative
            if self.isSocDischargeLimitReached(soc=soc, socDischargeLimit=socDischargeLimit):
                log.debug(f"SOC limit reached. Setting ESS feed limit to 0.")
                value = 0
            else:
                value = self.applyFeedLimit(value)
        else: # would charge
            if self.isSocChargeLimitReached(soc=soc, socChargeLimit=socChargeLimit):
                log.debug(f"SOC limit reached. Setting ESS charge limit to 0.")
                value = 0
            else:
                value = self.applyChargeLimit(value)
        value = self.parseSetPoint(value)
        self.writeSingleHoldingRegisters(address, value)
        return self.parseValue(value)

    def get_energy_consumed(self, address:int=77):
        """
        Get the energy from grid to inverter in Wh
        """
        return self.readSingleHoldingRegisters(address, False, 228) * 10
    
    def get_energy_returned(self, address:int=87):
        """
        Get the energy from inverter to grid in Wh
        """
        return self.readSingleHoldingRegisters(address, False, 228) * 10