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
import pandas as pd
from hameg3010.device import Device
from hameg3010.hameg_mock import DeviceMock
from rotor.arduino_connector_mock import ArduinoConnectorMock
from rotor.arduino_connector import ArduinoConnector
from pydantic import BaseModel, StrictInt, StrictFloat, Field, StrictStr
import numpy as np
import matplotlib.pyplot as plt

Numeric = Union[StrictFloat,StrictInt]

class HapmdConfig(BaseModel):

    # hameg device must have specified sweep range
    hameg_vid : StrictInt = Field(default=0x0403)
    hameg_pid : StrictInt = Field(default=0xED72)
    hameg_sweep_time : Numeric = Field(default=0.001)
    hameg_sweep_min_frequency :Numeric = Field(default=1_000_000)
    hameg_sweep_max_frequency:Numeric= Field(default=2_000_000)
    hameg_frequency_step: Numeric = Field(default=10_000)
    rotor_com_port:StrictStr = Field(default="COM3")
    rotor_min_angle: Numeric = Field(default=-90)
    rotor_max_angle: Numeric = Field(default=90)
    rotor_angle_step: Numeric = Field(default=15)

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
    
def hapmd_console_loop(hapmd_config:HapmdConfig, hameg_handle:Union[Device,DeviceMock], rotor_handle:Union[ArduinoConnector,ArduinoConnectorMock]):
    while True:
        command = input("hampd> ")
        command = command.casefold()
        command = command.replace(" ","")
        if command == "start":
            return
        elif command == "hampd>":
            continue
        elif command == "rotor>":
            rotor_console_loop(rotor_handle)    
        elif command == "hameg>":
            hameg_console_loop(hameg_handle)
        elif command == "show":
            hapmd_config.print_config()
        elif "hameg_vid" in command:
            hapmd_config.hameg_vid = int(command[len("hameg_vid"):])
        elif "hameg_pid" in command:
            hapmd_config.hameg_pid= int(command[len("hameg_pid"):])
        elif "hameg_sweep_time" in command:
            hapmd_config.hameg_sweep_time= float(command[len("hameg_sweep_time"):])
        elif "hameg_sweep_min_frequency" in command:
            hapmd_config.hameg_sweep_min_frequency= float(command[len("hameg_sweep_min_frequency"):])
        elif "hameg_sweep_max_frequency" in command:
            hapmd_config.hameg_sweep_max_frequency= float(command[len("hameg_sweep_max_frequency"):])
        elif "hameg_frequency_step" in command:
            hapmd_config.hameg_frequency_step = float(command[len("hameg_frequency_step"):])
        elif "rotor_com_port" in command:
            hapmd_config.rotor_com_port= float(command[len("rotor_com_port"):])
        elif "rotor_max_angle" in command:
            hapmd_config.rotor_max_angle= float(command[len("rotor_max_angle"):])
        elif "rotor_min_angle" in command:
            hapmd_config.rotor_min_angle= float(command[len("rotor_min_angle"):])
        elif "rotor_angle_step" in command:
            hapmd_config.rotor_angle_step= float(command[len("rotor_angle_step"):])
        else:
            print(f"{Colors.FAIL}unknown command:{Colors.BOLD}'{command}'{Colors.ENDC}")
def rotor_console_loop(rotor_handle:Union[ArduinoConnector,ArduinoConnectorMock]):
    while True:
        command = input("rotor> ")
        command = command.casefold()
        command = command.replace(" ","")
        if command == "quit":
            return
        elif command == "":
            print(rotor_handle.check_connection())
            
        elif command == "angle?":
            print(rotor_handle.get_angle())
        
        else:
            try:
                print(rotor_handle.move_to(float(command)))
            except Exception as ex:
                print(f"{Colors.FAIL}unknown command:{Colors.BOLD}'{command}'{Colors.ENDC}")
        
def hameg_console_loop(hameg_handle:Union[Device,DeviceMock]):
    while True:
        command = input("hameg> ")
        command = command.casefold()
        command = command.replace(" ","")
        if command == "quit":
            return
        else:
            resp = hameg_handle.send_await_resp(command)
            print(f"response: {resp[1]}")
            print(
                f"errors:   {hameg_handle.send_await_resp('SYSTem:ERRor:ALL?')[1][2:-1]}"
            )
            
def measurement_loop(hapmd_config:HapmdConfig, hameg_handle:Union[Device,DeviceMock], rotor_handle:Union[ArduinoConnector,ArduinoConnectorMock])->pd.DataFrame:
    measurement = []
    angles = [angle for angle in range(hapmd_config.rotor_min_angle,hapmd_config.rotor_max_angle,hapmd_config.rotor_angle_step)]
    frequencies = [frequency for frequency in range(hapmd_config.hameg_sweep_min_frequency,hapmd_config.hameg_sweep_max_frequency, hapmd_config.hameg_frequency_step)] 
    print(f"Measurement start no Angle states: {len(angles)} no Frequency states: {len(frequencies)}")
    for angle in angles:
        rotor_handle.move_to(angle)
        angle = rotor_handle.angle
        sweep = []
        print(f"current angle: {angle}")
        for frequency in frequencies:
            hameg_handle.send_await_resp(f"rmode:frequency {frequency}")
            level = hameg_handle.send_await_resp("rmode:level?")[1][2:-1]            
            sweep.append(float(level))
        measurement.append(sweep)
    measurement_df = pd.DataFrame(measurement,columns=frequencies,index=angles) 
    return measurement_df

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
        hameg_device = DeviceMock.connect_using_vid_pid(hapmd_config.hameg_vid,hapmd_config.hameg_pid)
        print("Hameg device set up: "+Colors.OKGREEN+"OK"+Colors.ENDC)
        print(f"""
IDN              : {Colors.BOLD}{hameg_device.send_await_resp("*IDN?")[1][2:-1]}{Colors.ENDC}
Software Version : {Colors.BOLD}{hameg_device.send_await_resp("SYSTem:SOFTware?")[1][2:-1]}{Colors.ENDC}
Hardware Version : {Colors.BOLD}{hameg_device.send_await_resp("SYSTem:HARDware?")[1][2:-1]}{Colors.ENDC}
            """
        )
        # clean errors
        hameg_device.send_await_resp("SYSTem:ERRor:ALL?")
    except Exception as ex:
        print("Hameg device set up: "+Colors.FAIL+"FAIL"+Colors.ENDC)
        print(str(ex))
        hameg_device = None
        
    try:
        rotor_device = ArduinoConnectorMock.connect_on_port(hapmd_config.rotor_com_port)
        print("Arduino device set up: "+Colors.OKGREEN+"OK"+Colors.ENDC)
        print(f"Current angle: {Colors.BOLD}{rotor_device.get_angle()}{Colors.ENDC}")
    except Exception as ex:
        print("Arduino device set up: "+Colors.FAIL+"FAIL"+Colors.ENDC)
        print(str(ex))
        rotor_device = None
        
    if not (rotor_device and hameg_device):
        raise SystemExit
    
    hapmd_console_loop(hapmd_config,hameg_device,rotor_device)
    measurement = measurement_loop(hapmd_config,hameg_device,rotor_device).to_csv("output.csv")

