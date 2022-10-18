from time import sleep
import serial

from arduino_connector import ArduinoConnector


def send_and_await_resp(device: serial.Serial, message: str) -> str:
    if message[-1] != "\n":
        message += "\n"
    device.write(bytes(message, "utf-8"))
    resp = str(device.readline())
    return resp


if __name__ == "__main__":

    device = ArduinoConnector.connect_on_port("COM3")

    while True:
        print("move to 45")
        device.move_by(90)
        sleep(3)
        print("move to -180")
        device.move_by(-180)
