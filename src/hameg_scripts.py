import time
from typing import Union
from hameg3010.device import Device
from hameg3010.device_mock import DeviceMock


def get_level(device: Union[Device, DeviceMock], frequency: int) -> float:

    device.send_await_resp(f"rmode:frequency {frequency}")
    time.sleep(2)
    value: float = 1
    counter: int = 0
    while value > 0 or value < -100:
        level_raw: str = device.send_await_resp("rmode:level?")[1][2:-1]
        try:
            level = level_raw[level_raw.find(",") + 1 :]
            value = float(level)

        except Exception as ex:
            print(f"Encountered Error: {str(ex)}, retrying readout")

        counter += 1
        if counter == 10:
            return None

    return value
