"""
    entry point for application
"""

import sys
import datetime
from typing import Optional, Union
import pandas as pd

from hameg3010.device import Device
from hameg3010.device_mock import DeviceMock
from hameg_scripts import get_level

from rotor.arduino_connector import ArduinoConnector
from rotor.arduino_connector_mock import ArduinoConnectorMock

from assets.ci_colors import Colors

from rotor_ci import rotor_console_loop
from hameg_ci import hameg_console_loop

from hampd_config import HapmdConfig


def hapmd_console_loop(
    hapmd_config: HapmdConfig,
    hameg_handle: Union[Device, DeviceMock],
    rotor_handle: Union[ArduinoConnector, ArduinoConnectorMock],
):
    while True:
        command = input("hampd> ")
        command = command.casefold()
        command = command.replace(" ", "")
        if command == "start":
            return
        elif command == "hampd>":
            continue
        elif command == "rotor>":
            rotor_console_loop(rotor_handle)
        elif command == "hameg>":
            hameg_console_loop(hameg_handle)
        else:
            print(f"{Colors.FAIL}unknown command:{Colors.BOLD}'{command}'{Colors.ENDC}")


def measurement_loop(
    hapmd_config: HapmdConfig,
    hameg_handle: Union[Device, DeviceMock],
    rotor_handle: Union[ArduinoConnector, ArduinoConnectorMock],
) -> pd.DataFrame:
    print(
        f"Measurement no Angle states: {(hapmd_config.rotor_max_angle -hapmd_config.rotor_min_angle) // hapmd_config.rotor_angle_step} no Frequency states: {len(hapmd_config.hameg_frequencies)}"
    )

    measurement = []
    indexes = []
    angle = hapmd_config.rotor_min_angle

    while angle <= hapmd_config.rotor_max_angle:
        angle = angle + hapmd_config.rotor_angle_step
        rotor_handle.move_to(angle)
        angle = rotor_handle.angle
        sweep = []
        indexes.append(angle)
        print(f"current angle: {angle}")

        for frequency in hapmd_config.hameg_frequencies:
            sweep.append(get_level(hameg_handle, frequency))
        measurement.append(sweep)

    measurement_df = pd.DataFrame(
        measurement, columns=hapmd_config.hameg_frequencies, index=indexes
    )

    return measurement_df


def set_up_hameg_device(
    hapmd_config: HapmdConfig,
) -> Optional[Union[Device, DeviceMock]]:
    try:
        hameg_device = DeviceMock.connect_using_vid_pid(
            hapmd_config.hameg_vid, hapmd_config.hameg_pid
        )

        print("Hameg device set up: " + Colors.OKGREEN + "OK" + Colors.ENDC)
        print(
            f"""
IDN              : {Colors.BOLD}{hameg_device.send_await_resp("*IDN?")[1][2:-1]}{Colors.ENDC}
Software Version : {Colors.BOLD}{hameg_device.send_await_resp("SYSTem:SOFTware?")[1][2:-1]}{Colors.ENDC}
Hardware Version : {Colors.BOLD}{hameg_device.send_await_resp("SYSTem:HARDware?")[1][2:-1]}{Colors.ENDC}
            """
        )
        # clean errors
        hameg_device.send_await_resp("SYSTem:ERRor:ALL?")

    except Exception as ex:
        print("Hameg device set up: " + Colors.FAIL + "FAIL" + Colors.ENDC)
        print(str(ex))
        hameg_device = None

    return hameg_device


def set_up_rotor_device(
    hapmd_config: HapmdConfig,
) -> Optional[Union[ArduinoConnector, ArduinoConnectorMock]]:
    try:
        rotor_device = ArduinoConnectorMock.connect_on_port(hapmd_config.rotor_com_port)
        print("Arduino device set up: " + Colors.OKGREEN + "OK" + Colors.ENDC)
        print(f"Current angle: {Colors.BOLD}{rotor_device.get_angle()}{Colors.ENDC}")

    except Exception as ex:
        print("Arduino device set up: " + Colors.FAIL + "FAIL" + Colors.ENDC)
        print(str(ex))
        rotor_device = None

    return rotor_device


if __name__ == "__main__":

    hapmd_settings_file = None
    if len(sys.argv) == 2:
        hapmd_settings_file = str(sys.argv[1])

    print(
        """ 
 /$$   /$$  /$$$$$$  /$$$$$$$  /$$      /$$ /$$$$$$$         /$$$$$$  /$$$$$$
| $$  | $$ /$$__  $$| $$__  $$| $$$    /$$$| $$__  $$       /$$__  $$|_  $$_/
| $$  | $$| $$  \ $$| $$  \ $$| $$$$  /$$$$| $$  \ $$      | $$  \__/  | $$  
| $$$$$$$$| $$$$$$$$| $$$$$$$/| $$ $$/$$ $$| $$  | $$      | $$        | $$  
| $$__  $$| $$__  $$| $$____/ | $$  $$$| $$| $$  | $$      | $$        | $$  
| $$  | $$| $$  | $$| $$      | $$\  $ | $$| $$  | $$      | $$    $$  | $$  
| $$  | $$| $$  | $$| $$      | $$ \/  | $$| $$$$$$$/      |  $$$$$$/ /$$$$$$
|__/  |__/|__/  |__/|__/      |__/     |__/|_______/        \______/ |______/"""
    )
    print("Horizontal antenna pattern measurement device")

    if hapmd_settings_file:
        hapmd_config = HapmdConfig.from_json_config_file(hapmd_settings_file)
    else:
        hapmd_config = HapmdConfig()

    hapmd_config.print_config()
    hameg_device = set_up_hameg_device(hapmd_config)
    rotor_device = set_up_rotor_device(hapmd_config)

    if not (rotor_device and hameg_device):
        raise SystemExit

    hapmd_console_loop(hapmd_config, hameg_device, rotor_device)
    measurement = measurement_loop(hapmd_config, hameg_device, rotor_device).to_csv(
        datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + "_apm.csv", sep = '\t'
    )
