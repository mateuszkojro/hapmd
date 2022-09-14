from typing import Tuple, Union
import serial
import time


def send_and_await_resp(device: serial.Serial, message: str) -> str:
    if message[-1] != "\n":
        message += "\n"
    device.write(bytes(message, "utf-8"))
    resp = str(device.readline())
    return resp


class ArduinoConnector:
    device = None  # pyserial connector device
    angle: float

    def __init__(self, device) -> None:
        self.device = device
        self.angle = 0
        device_set_up_response = str(device.readline())
        assert (
            "ok" in device_set_up_response,
        )  # assert connection with arduino device is set correctly

    @staticmethod
    def connect_on_port(port: str, baudrate: int = 115200) -> "ArduinoConnector":
        return ArduinoConnector(serial.Serial(port=port, baudrate=baudrate, timeout=30))

    def move_to(self, new_angle: float) -> None:
        angle_diff = self.angle - new_angle
        self.move_by(angle_diff)

    def move_by(self, angle: float) -> None:
            
        resp = send_and_await_resp(
            device=self.device, message=str(angle)
        )
        self.angle = angle
        assert str(angle) in resp, resp

    def check_connection(self) -> Union[bool,Tuple[bool,str]]:
        resp = send_and_await_resp(device=self.device, message="test_connection\n")

        if "ok" in resp:
            return (True, None)
        return (False, resp)

    def get_anlge(self) -> float:
        return self.angle
