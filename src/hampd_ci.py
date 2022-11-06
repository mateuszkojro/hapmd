# Console Interface
# hampd control panel

from colorama import Style, Fore
from enum import Enum


class ConnectionState(Enum):
    OK = ((Fore.GREEN, "Ok"),)
    NOT_CONNECTED = (Fore.YELLOW, "Not connected")
    UNABLE_TO_CONNECT = (Fore.RED, "Unable to connect")
    NONE = (Fore.WHITE, "Unknown")


def format_stats(
    rotor_state: str,
    hameg_state: str,
    current_rotor_angle: float,
    sweep_min_frequency: float,
    sweep_max_frequency: float,
    sweep_step: float,
    measurement_time: float,
):
    print(f"Rotor connection: {rotor_state}")
    print(f"Hameg3010 connection: {hameg_state}")

    pass


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
