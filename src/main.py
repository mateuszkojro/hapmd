"""
    entry point for application
"""
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

import json
from typing import Union

from hameg3010.device import Device
from rotor.arduino_connector import ArduinoConnector
from pydantic import BaseModel, StrictInt, StrictFloat, Field, StrictStr

Numeric = Union[StrictFloat,StrictInt]


class HapmdConfig(BaseModel):

    # hameg device must have specified sweep range
    hameg_vid : StrictInt = Field(default=0x0403)
    hameg_pid : StrictInt = Field(default=0xED72)
    hameg_sweep_time : Numeric = Field(default=0.2)
    hameg_sweep_min_frequency :Numeric = Field(default=1_000_000)
    hameg_sweep_max_frequency:Numeric= Field(default=8_000_000)
    hameg_frequency_step: Numeric = Field(default=1_000)

    rotor_com_port:StrictStr = Field(default="COM3")
    rotor_max_angle: Numeric = Field(default=90)
    rotor_min_angle: Numeric = Field(default=-90)
    rotor_angle_step: Numeric = Field(default=5)

    config_json_file_path: StrictStr = Field(default=None)
    
    @staticmethod
    def from_json_config_file(file_path : StrictStr)->"HapmdConfig":
        with open(file_path) as f:
            data = json.load(f) 
        config = HapmdConfig(**data)
        config.config_json_file_path = file_path
        return config

    def print_config(self:"HapmdConfig"):
        print(f"""
Connecting Hameg Device on VID: {Colors.BOLD}{hex(self.hameg_vid)}{Colors.ENDC} 
Connecting Hameg Device on PID: {Colors.BOLD}{hex(self.hameg_pid)}{Colors.ENDC}
Sweep Time: {Colors.BOLD}{self.hameg_sweep_time}{Colors.ENDC} s              
Frequency Step: {Colors.BOLD}{self.hameg_frequency_step}{Colors.ENDC} Hz
Sweep Start Frequency: {Colors.BOLD}{'{:.3e}'.format(self.hameg_sweep_min_frequency)}{Colors.ENDC} Hz 
Sweep Stop Frequency: {Colors.BOLD}{'{:.3e}'.format(self.hameg_sweep_max_frequency)}{Colors.ENDC} Hz

Connecting Rotor Device on Com port: {Colors.BOLD}{self.rotor_com_port}{Colors.ENDC}
Rotor Step Angle: {Colors.BOLD}{self.rotor_angle_step}{Colors.ENDC}
Rotor Start Angle: {Colors.BOLD}{self.rotor_min_angle}{Colors.ENDC}          
Stop Angle: {Colors.BOLD}{self.rotor_min_angle}{Colors.ENDC}
""")
    
 
if __name__ == "__main__":
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
    
    hapmd_config = HapmdConfig()
    hapmd_config.print_config()
    try:
        hameg_device = Device.connect_using_vid_pid(hapmd_config.hameg_vid,hapmd_config.hameg_pid)
        print("Hameg device set up: "+Colors.OKGREEN+"OK"+Colors.ENDC)
        print(
            f"""
    Connected to Hameg device
    IDN              : {Colors.BOLD}{hameg_device.send_await_resp("*IDN?")[1][2:-1]}{Colors.END}
    Software Version : {Colors.BOLD}{hameg_device.send_await_resp("SYSTem:SOFTware?")[1][2:-1]}{Colors.END}
    Hardware Version : {Colors.BOLD}{hameg_device.send_await_resp("SYSTem:HARDware?")[1][2:-1]}{Colors.END}
            """
        )
        # clean errors
        hameg_device.send_await_resp("SYSTem:ERRor:ALL?")
    except Exception as ex:
        print("Hameg device set up: "+Colors.FAIL+"FAIL"+Colors.ENDC)
        print(str(ex))
        hameg_device = None
        
    try:
        rotor_device = ArduinoConnector.connect_on_port(hapmd_config.rotor_com_port)
        print("Arduino device set up: "+Colors.OKGREEN+"OK"+Colors.ENDC)
        print(f"Current angle: {Colors.BOLD}{rotor_device.get_angle()}{Colors.ENDC}")
    except Exception as ex:
        print("Arduino device set up: "+Colors.FAIL+"FAIL"+Colors.ENDC)
        print(str(ex))
        rotor_device = None