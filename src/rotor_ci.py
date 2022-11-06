from typing import Union

from rotor.arduino_connector import ArduinoConnector
from rotor.arduino_connector_mock import ArduinoConnectorMock
from assets.ci_colors import Colors


# import os, sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def rotor_console_loop(rotor_handle: Union[ArduinoConnector, ArduinoConnectorMock]):
    while True:
        command = input("rotor> ")
        command = command.casefold()
        command = command.replace(" ", "")
        if command in ("quit", "q"):
            return

        elif command in ("connection?", "c?"):
            print(rotor_handle.check_connection())

        elif command in ("angle?", "a?"):
            print(rotor_handle.get_angle())

        else:
            try:
                print(rotor_handle.move_to(float(command)))
            except Exception as ex:
                print(
                    f"{Colors.FAIL}unknown command:{Colors.BOLD}'{command}'{Colors.ENDC}"
                )


if __name__ == "__main__":
    print(
        """
 /$$$$$$$              /$$                                /$$$$$$  /$$$$$$
| $$__  $$            | $$                               /$$__  $$|_  $$_/
| $$  \ $$  /$$$$$$  /$$$$$$    /$$$$$$   /$$$$$$       | $$  \__/  | $$  
| $$$$$$$/ /$$__  $$|_  $$_/   /$$__  $$ /$$__  $$      | $$        | $$  
| $$__  $$| $$  \ $$  | $$    | $$  \ $$| $$  \__/      | $$        | $$  
| $$  \ $$| $$  | $$  | $$ /$$| $$  | $$| $$            | $$    $$  | $$  
| $$  | $$|  $$$$$$/  |  $$$$/|  $$$$$$/| $$            |  $$$$$$/ /$$$$$$
|__/  |__/ \______/    \___/   \______/ |__/             \______/ |______/
          """
    )
    port: str = "COM3"
    device = ArduinoConnectorMock.connect_on_port(port)
    print("Arduino device set up: " + Colors.OKGREEN + Colors.BOLD + "OK" + Colors.ENDC)
    print(f"Connection Port: {Colors.BOLD}{port}{Colors.ENDC}")
    print(f"Current angle: {Colors.BOLD}{device.get_angle()}{Colors.ENDC}")

    rotor_console_loop(device)
