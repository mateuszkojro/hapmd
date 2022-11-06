
from device import Device
def level(device : Device,frequency:int)->float:
    
    device.send_await_resp(f"rmode:frequency {frequency}")
    level_raw: str = device.send_await_resp("rmode:level?")[1][2:-1]
    value:float = 0.0
    try: 
        level = level_raw[level_raw.find(",") + 1 :]
        value = float(level)
    
    except Exception as ex:
        print(f"Encountered Error: {str(ex)}")
        print(level_raw)
        value = None
    return value