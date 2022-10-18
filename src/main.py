"""
    entry point for application
"""
from dataclasses import Field, dataclass
from typing import Tuple

from hameg3010.device import Device
from rotor.arduino_connector import ArduinoConnector


@dataclass
class HampdConfig:

    hameg_device_handle: Device

    rotor_device_handle: ArduinoConnector

    # hameg device must have specified sweep range
    measured_frequency_range: Tuple[int, int]

    # sweep time, the longer the sweep time the bigger the precision
    sweep_time_milliseconds: int

    # the rotation span of transmitter
    angle_span: Tuple[int, int]

    # the change in Transmitter angle after each read
    step_angle: float


if __name__ == "__main__":
    hameg_device_handle = Device.connect_using_vid_pid(
        idVendor=0x0403, idProduct=0xED72
    )
    print(hameg_device_handle.send_await_resp())
