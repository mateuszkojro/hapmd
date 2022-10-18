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
    rotor_state: ConnectionState,
    hameg_state: ConnectionState,
    current_rotor_angle: float,
):
    print(f"Rotor connection: {rotor_state}")
    print(f"Hameg3010 connection: {hameg_state}")

    pass


if __name__ == "__main__":
    print(
        """
        """
    )
    print("Horizontal antenna pattern measurement device")
    print("piotr223@github")
