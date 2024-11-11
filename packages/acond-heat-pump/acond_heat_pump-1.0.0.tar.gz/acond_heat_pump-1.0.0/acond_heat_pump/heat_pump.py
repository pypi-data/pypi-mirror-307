from typing import Optional

from pymodbus.client.tcp import ModbusTcpClient
import logging

from acond_heat_pump.constants import RegulationMode, HeatPumpMode
from acond_heat_pump.heat_pump_data import HeatPumpStatus, HeatPumpResponse

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)


class AcondHeatPump:
    """
    A class to represent and interact with an Acond heat pump system.

    Usage:
        heat_pump = AcondHeatPump("192.168.1.16")
        heat_pump.connect()
        response = heat_pump.read_data()
        heat_pump.set_indoor_temperature(25.0, circuit=1)
        heat_pump.close()
    """

    def __init__(self, host: str, port: int = 502):
        """
        Initialize the heat pump object.
        :param host: IP or hostname of the heat pump.
        :param port: Port number of the Modbus TCP server. Default is 502.
        """
        self.client = ModbusTcpClient(host, port=port)

    def connect(self):
        """
        Connect to the heat pump.
        """
        self.client.connect()

    def close(self):
        """
        Close the connection to the heat pump.
        """
        self.client.close()

    def read_data(self) -> HeatPumpResponse:
        """
        Read all input registers and parse them into a HeatPumpResponse object.

        Returns:
            HeatPumpResponse: An object containing the parsed data from the heat pump.

        Raises:
            Exception: If there is an error reading the input registers.
        """

        # Reading 24 registers from 30001 to 30024
        result = self.client.read_input_registers(0, 24)
        if result.isError():
            log.error("Error reading input registers")
            raise Exception("Error reading input registers")

        return HeatPumpResponse(
            indoor1_temp_set=self._read_temp_register(
                result.registers[0], min=10.0, max=30.0
            ),
            indoor1_temp_actual=self._read_temp_register(
                result.registers[1], min=0.0, max=50.0
            ),
            indoor2_temp_set=self._read_temp_register(
                result.registers[2], min=10.0, max=30.0
            ),
            indoor2_temp_actual=self._read_temp_register(
                result.registers[3], min=0.0, max=50.0
            ),
            dhw_temp_set=self._read_temp_register(
                result.registers[4], min=10.0, max=50.0
            ),
            dhw_temp_actual=self._read_temp_register(
                result.registers[5], min=0.0, max=90.0
            ),
            status=self._parse_status_bits(result.registers[6]),
            water_back_temp_set=self._read_temp_register(
                result.registers[7], min=20.0, max=60.0
            ),
            water_back_temp_actual=self._read_temp_register(
                result.registers[8], min=-10.0, max=90.0
            ),
            outdoor_temp_actual=self._read_temp_register(
                result.registers[9], min=-50.0, max=50.0
            ),
            solar_temp_actual=self._read_temp_register(
                result.registers[10], min=-50.0, max=300.0
            ),
            pool_temp_actual=self._read_temp_register(
                result.registers[11], min=0.0, max=50.0
            ),
            pool_temp_set=self._read_temp_register(result.registers[12]),
            heat_pump_mode=HeatPumpMode(result.registers[13]),
            regulation_mode=RegulationMode(result.registers[14]),
            brine_temp=self._read_temp_register(
                result.registers[15], min=-30.0, max=50.0
            ),
            heart_beat=result.registers[16],
            water_outlet_temp_actual=self._read_temp_register(
                result.registers[17], min=-10.0, max=90.0
            ),
            water_outlet_temp_set=self._read_temp_register(
                result.registers[18], min=10.0, max=25.0
            ),
            compressor_capacity_max=result.registers[19],
            err_number=result.registers[20],
            err_number_SECMono=result.registers[21],
            err_number_driver=result.registers[22],
            compressor_capacity_actual=result.registers[23],
        )

    def set_indoor_temperature(self, temperature: float, circuit: int = 1) -> bool:
        """
        Set the desired indoor temperature for a given circuit (1 or 2).

        Parameters:
        - temperature (float): The temperature to set in °C. Must be between 10.0 and 30.0 °C.
        - circuit (int): The circuit number (1 or 2). Default is 1.

        Returns:
        - bool: True if the temperature was set successfully, False otherwise.
        """
        # Choose the appropriate register based on the circuit number
        if circuit == 1:
            register_address = 0  # 40001 offset
        elif circuit == 2:
            register_address = 2  # 40003 offset
        else:
            raise ValueError("Invalid circuit number. Use 1 or 2.")

        if not 10.0 <= temperature <= 30.0:
            raise ValueError("Temperature must be between 10.0 and 30.0 °C")

        # Scale the temperature by 10 for the Modbus register
        scaled_temperature = int(temperature * 10)

        # Write to the register
        result = self.client.write_register(
            register_address, scaled_temperature, slave=1
        )
        if not result.isError():
            log.info(f"Temperature for circuit {circuit} set to {temperature} °C")
            return True
        else:
            log.info(f"Failed to set temperature for circuit {circuit}")
            return False

    def set_dhw_temperature(self, temperature: float) -> bool:
        """
        Set the desired domestic hot water temperature.

        Parameters:
        - temperature (float): The temperature to set in °C. Must be between 10.0 and 50.0 °C.

        Returns:
        - bool: True if the temperature was set successfully, False otherwise.
        """
        if not 10.0 <= temperature <= 50.0:
            raise ValueError("Temperature must be between 10.0 and 50.0 °C")

        # Scale the temperature by 10 for the Modbus register
        scaled_temperature = int(temperature * 10)

        # Write to the register
        result = self.client.write_register(4, scaled_temperature, slave=1)
        if not result.isError():
            log.info(f"Domestic hot water temperature set to {temperature} °C")
            return True
        else:
            log.info("Failed to set domestic hot water temperature")

    def set_regulation_mode(self, mode: RegulationMode) -> bool:
        """
        Set the regulation mode.

        Parameters:
        - mode: The regulation mode to set.

        Returns:
        - bool: True if the mode was set successfully, False otherwise.
        """
        result = self.client.write_register(6, mode.value, slave=1)
        if not result.isError():
            log.info(f"Regulation mode set to {mode.name}")
            return True
        else:
            log.info("Failed to set regulation mode")
            return False

    def _update_bit(self, value: int, bit_position: int, set_bit: bool) -> int:
        """Set or clear a specific bit in an integer value."""
        return

    def change_setting(self, mode: Optional[HeatPumpMode] = None) -> bool:
        register_address = 5  # Modbus address for TC_set (40006)

        # Read the current value of TC_set register
        current_value = self.client.read_holding_registers(
            register_address, count=1, slave=1
        )
        if current_value is None:
            print("Error: Failed to read TC_set register.")
            return False
        current_value = current_value.registers[0]

        # Define bit positions for each flag
        flag_bits = [
            mode == HeatPumpMode.AUTOMATIC,
            mode == HeatPumpMode.HEAT_PUMP_ONLY,
            mode == HeatPumpMode.BIVALENT_ONLY,
            mode == HeatPumpMode.OFF,
            mode == HeatPumpMode.COOLING,
        ]

        # Update current_value based on flags that are not None
        bit_value = current_value
        for bit_position, flag in enumerate(flag_bits):
            if flag is not None:
                bit_value = (
                    bit_value | (1 << bit_position)
                    if flag
                    else bit_value & ~(1 << bit_position)
                )

        # Write the updated value to the TC_set register
        result = self.client.write_register(register_address, bit_value, slave=1)
        if result.isError():
            print("Error: Failed to update TC_set register.")
            return False

        print("Success: TC_set register flags updated.")
        return True

    def set_water_back_temperature(self, temperature: float) -> bool:
        """
        Set the desired return water temperature.

        Parameters:
        - temperature (float): The temperature to set in °C. Must be between 20.0 and 60.0 °C.

        Returns:
        - bool: True if the temperature was set successfully, False otherwise.
        """
        if not 20.0 <= temperature <= 60.0:
            raise ValueError("Temperature must be between 20.0 and 60.0 °C")

        # Scale the temperature by 10 for the Modbus register
        scaled_temperature = int(temperature * 10)

        # Write to the register
        result = self.client.write_register(7, scaled_temperature, slave=1)
        if not result.isError():
            log.info(f"Return water temperature set to {temperature} °C")
            return True
        else:
            log.info("Failed to set return water temperature")
            return False

    def set_pool_temperature(self, temperature: float) -> bool:
        """
        Set the desired pool water temperature.

        Parameters:
        - temperature (float): The temperature to set in °C. Must be between 0.0 and 50.0 °C.

        Returns:
        - bool: True if the temperature was set successfully, False otherwise.
        """
        if not 0.0 <= temperature <= 50.0:
            raise ValueError("Temperature must be between 0.0 and 50.0 °C")

        # Scale the temperature by 10 for the Modbus register
        scaled_temperature = int(temperature * 10)

        # Write to the register
        result = self.client.write_register(11, scaled_temperature, slave=1)
        if not result.isError():
            log.info(f"Pool water temperature set to {temperature} °C")
            return True
        else:
            log.info("Failed to set pool water temperature")
            return False

    def set_water_cool_temperature(self, temperature: float) -> bool:
        """
        Set the desired water outlet temperature in cooling mode.

        Parameters:
        - temperature (float): The temperature to set in °C. Must be between 15.0 and 30.0 °C.

        Returns:
        - bool: True if the temperature was set successfully, False otherwise.
        """
        if not 15.0 <= temperature <= 30.0:
            raise ValueError("Temperature must be between 15.0 and 30.0 °C")

        # Scale the temperature by 10 for the Modbus register
        scaled_temperature = int(temperature * 10)

        # Write to the register
        result = self.client.write_register(12, scaled_temperature, slave=1)
        if not result.isError():
            log.info(f"Water cool temperature set to {temperature} °C")
            return True
        else:
            log.info("Failed to set water cool temperature")
            return False

    @staticmethod
    def _read_temp_register(
        value: int, min: Optional[float] = None, max: Optional[float] = None
    ) -> Optional[float]:
        """
        Read temperature register and convert it to float.
        """
        signed = int.from_bytes(int(value).to_bytes(length=2), signed=True)
        temp = signed / 10.0
        if min is not None and temp < min:
            return 0
        if max is not None and temp > max:
            return 0
        return temp

    @staticmethod
    def _parse_status_bits(status: int) -> HeatPumpStatus:
        """
        Extract status bits from TC_status register.
        """

        status_bits = [bool(status & (1 << bit)) for bit in range(16)]
        return HeatPumpStatus(
            on=status_bits[0],
            running=status_bits[1],
            fault=status_bits[2],
            heating_dhw=status_bits[3],
            pump_circuit1=status_bits[4],
            pump_circuit2=status_bits[5],
            solar_pump=status_bits[6],
            pool_pump=status_bits[7],
            defrost=status_bits[8],
            bivalence_running=status_bits[9],
            summer_mode=status_bits[10],
            brine_pump=status_bits[11],
            cooling_running=status_bits[12],
        )
