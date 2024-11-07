"""Library for control of an Omega PID Temperature Controller."""

from typing import Union

import minimalmodbus  # type: ignore


class Heater:
    """Create Heater object.

    This class provides methods for setting PID parameters, thermocouple types,
    operational modes, and more.

    Attributes:
        port (str): The serial port where the Heater is connected (default "").
        addr (Union[int, None]): The modbus address of the Heater (default None).
    """

    def __init__(self, port: str = "", addr: Union[int, None] = None) -> None:
        """Initialize the Heater class.

        Args:
            port (str): Define the serial port to connect the Heater to (default "").
            addr (Union[int, None]): modbus address of the Heater (default None).
        """
        self.port = port
        self.addr = addr
        self.ser = minimalmodbus.Instrument(port, addr, mode="rtu")

    def set_pid(
        self,
        max_rate: float,
        dev_gain: float,
        pro_gain: float,
        int_gain: float,
        pid_setpoint: float,
    ) -> None:
        """Set PID parameters for the Heater.

        Args:
            max_rate (float): The maximum rate of change for the process variable.
            dev_gain (float): The derivative gain of the PID controller.
            pro_gain (float): The proportional gain of the PID controller.
            int_gain (float): The integral gain of the PID controller.
            pid_setpoint (float): The setpoint for the PID controller.
        """
        self.ser.write_float(686, max_rate, 2)
        self.ser.write_float(676, pro_gain, 2)  # P gain
        self.ser.write_float(678, int_gain, 2)  # I gain
        self.ser.write_float(680, dev_gain, 2)  # D Gain
        self.ser.write_float(544, pid_setpoint, 2)  # Current Setpoint 1

    def set_thermocouple(self, couple_type: int = 1) -> None:
        """Set the type of thermocouple for the Heater.

        Args:
            couple_type (int): The type of thermocouple (default 1).
        """
        self.ser.write_register(643, couple_type, 0, 16, False)  # Thermocouple Type

    def get_temp(self) -> float:
        """Get the current temperature from the Heater.

        Returns:
            The current temperature from the Heater in degrees Celsius.
        """
        temperature = self.ser.read_float(528, 3, 2)  # Current Input Value
        temperature = "%.4f" % temperature
        temperature = f"{temperature:{6}.{6}}"
        return float(temperature)

    def run(self) -> None:
        """Start the Heater in run mode."""
        self.ser.write_register(576, 5, 0, 16, False)  # The running mode
        self.ser.write_register(576, 6, 0, 16, False)  # Run Mode

    def stop(self) -> None:
        """Stop the Heater."""
        self.ser.write_register(576, 8, 0, 16, False)  # The running mode

    def set_action(self, action_value: str) -> None:
        """Set the action (direct or reverse) for the PID controller.

        Args:
            action_value (str): The desired action value ("direct" or "reverse").
        """
        if action_value == "direct":
            self.ser.write_register(673, 1, 0, 16, False)  # PID Action
        elif action_value == "reverse":
            self.ser.write_register(673, 0, 0, 16, False)  # PID Action

    def action(self, output_value: str) -> None:
        """Set the action for the Heater output.

        Args:
            output_value (str): The desired output action ("off" or "pid").
        """
        if output_value == "off":
            self.ser.write_register(1025, 0, 0, 16, False)  # Output 1 Mode
        elif output_value == "pid":
            self.ser.write_register(1025, 1, 0, 16, False)  # Output 1 Mode

    def autotune_adaptive(self, enable: bool = False) -> None:
        """Enable or disable adaptive PID tuning.

        Args:
            enable (bool): Enable or disable adaptive tuning (default False).
        """
        if enable is True:
            self.ser.write_register(672, 1, 0, 16, False)  # PID Adaptive Control
        # self.ser.write_register(672, 0, 0, 16, False)  # PID Adaptive Control
        # return

    def set_pid_auto(
        self, max_rate: float, autotune_timeout: int, pid_setpoint: float
    ) -> None:
        """Set PID parameters for auto-tuning.

        Args:
            max_rate (float): The maximum rate of change for the process variable.
            autotune_timeout (int): The timeout for auto-tuning in milliseconds.
            pid_setpoint (float): The setpoint for the PID controller.
        """
        autotune_timeout = autotune_timeout * 1000
        self.ser.write_float(686, max_rate, 2)
        self.ser.write_float(544, pid_setpoint, 2)  # Current Setpoint 1
        self.ser.write_long(674, autotune_timeout, False)
        self.ser.write_register(579, 1, 0, 16, False)  # Autotune Start

    def filter_hold(self, filter_knob: int = 0) -> None:
        """Set the filter value for the Heater.

        Args:
            filter_knob (int): The filter knob value (default 0).
        """
        filter_knob = int(filter_knob)
        self.ser.write_register(655, filter_knob, 0, 16, False)  # Filter


# Example usage:
# c1 = Heater(port="/dev/ttyACM4", addr=1)
# c1.set_thermocouple()
# c1.set_action()
# c1.filter_hold()
# c1.set_pid(max_rate=1, dev_gain=1, pro_gain=8, int_gain=0, pid_setpoint=70)
# c1.run()
#
# c2 = Heater(port="/dev/ttyACM2", addr=2)
# c2.set_thermocouple()
# c2.set_action()
# c2.filter_hold()
# c2.set_pid(max_rate=1, dev_gain=1, pro_gain=8, int_gain=0, pid_setpoint=70)
# c2.run()
#
# while(1):
#     print("{},{}".format(c1.get_temp(), c2.get_temp()))
#     time.sleep(1)
