from typing import Tuple, Union
from serial import Serial
import time


def send_and_await_resp(device: Serial, message: str) -> Tuple[str,str]:
    if message[-1] != "\n":
        message += "\n"
    device.write(bytes(message, "utf-8"))
    resp = str(device.readline())
    return (resp,resp[2:-3])


class ArduinoConnector:
    _device: Serial = None  # pyserial connector device
    _angle: float

    def __init__(self, device) -> None:
        self._device = device
        self._angle = 0
        assert "ok" in str(
            device.readline()
        )  # assert connection with arduino device is set correctly

    @staticmethod
    def connect_on_port(port: str, baudrate: int = 115200) -> "ArduinoConnector":
        return ArduinoConnector(device = Serial(port=port, baudrate=baudrate, timeout=30))

    def move_to(self, new_angle: float) -> None:
        send_and_await_resp(device=self._device, message='set' + str(new_angle))
        self._angle =  new_angle

    def move_by(self, angle_step: float) -> None:
        self.move_to(self._angle + angle_step)
        
    def get_angle(self)->float:
        _ , resp = send_and_await_resp(device=self._device, message="get")
        return resp
    
    def check_connection(self) -> Union[bool, Tuple[bool, str]]:
        raw_resp , resp = send_and_await_resp(device=self._device, message="con")
        if "ok" in resp:
            return (True, None)
        return (False, raw_resp)
    
    @property
    def angle(self) -> float:
        return self._angle
