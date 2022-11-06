from typing import Union
from device import Device
from device_mock import DeviceMock

def hameg_console_loop(hameg_handle:Union[Device,DeviceMock]):
    while True:
        command = input("hameg> ")
        command = command.casefold()
        command = command.replace(" ","")
        if command in ("quit", 'q'):
            return
        else:
            resp = hameg_handle.send_await_resp(command)
            print(f"response: {resp[1]}")
            print(
                f"errors:   {hameg_handle.send_await_resp('SYSTem:ERRor:ALL?')[1][2:-1]}"
            )
            
if __name__ == "__main__":
    print(
        """
        
 /$$   /$$                                                    /$$$$$$  /$$$$$$
| $$  | $$                                                   /$$__  $$|_  $$_/
| $$  | $$  /$$$$$$  /$$$$$$/$$$$   /$$$$$$   /$$$$$$       | $$  \__/  | $$  
| $$$$$$$$ |____  $$| $$_  $$_  $$ /$$__  $$ /$$__  $$      | $$        | $$  
| $$__  $$  /$$$$$$$| $$ \ $$ \ $$| $$$$$$$$| $$  \ $$      | $$        | $$  
| $$  | $$ /$$__  $$| $$ | $$ | $$| $$_____/| $$  | $$      | $$    $$  | $$  
| $$  | $$|  $$$$$$$| $$ | $$ | $$|  $$$$$$$|  $$$$$$$      |  $$$$$$/ /$$$$$$
|__/  |__/ \_______/|__/ |__/ |__/ \_______/ \____  $$       \______/ |______/
                                             /$$  \ $$                        
                                            |  $$$$$$/                        
                                             \______/                         """
    )

    hameg_device_handle = DeviceMock.connect_using_vid_pid(
        idVendor=0x0403, idProduct=0xED72
    )

    print(
        f"""
Connected to Hameg device
IDN              : {hameg_device_handle.send_await_resp("*IDN?")[1][2:-1]}
Software Version : {hameg_device_handle.send_await_resp("SYSTem:SOFTware?")[1][2:-1]}
Hardware Version : {hameg_device_handle.send_await_resp("SYSTem:HARDware?")[1][2:-1]}
          """
    )
    # clean errors
    hameg_device_handle.send_await_resp("SYSTem:ERRor:ALL?")
    
    hameg_console_loop(hameg_device_handle)