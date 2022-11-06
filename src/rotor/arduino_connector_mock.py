from typing import Tuple, Union
from serial import Serial


def send_and_await_resp(device: Serial, message: str) -> Tuple[str, str]:
    return ("b'this is a mock\n'", b"this is a mock\n"[2:-3])


class ArduinoConnectorMock:
    _device: Serial = None  # pyserial connector device
    _angle: float

    def __init__(self, device) -> None:
        self._device = device
        self._angle = 0

    @staticmethod
    def connect_on_port(port: str, baudrate: int = 115200) -> "ArduinoConnectorMock":
        return ArduinoConnectorMock(device=None)

    def move_to(self, new_angle: float) -> float:
        self._angle = new_angle
        return new_angle

    def move_by(self, angle_step: float) -> float:
        return self.move_to(self._angle + angle_step)

    def override_angle(self, new_angle: float) -> float:
        self._angle = new_angle
        return self._angle

    def get_angle(self) -> float:
        return self._angle

    def check_connection(self) -> Union[bool, Tuple[bool, str]]:
        return (True, "b'this is a mock\n'")

    @property
    def angle(self) -> float:
        return self._angle
