from sqlite3 import connect
from device import Device


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

    hameg_device_handle = Device.connect_using_vid_pid(
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

    while True:
        x = input("\ncommand:  ")
        resp = hameg_device_handle.send_await_resp(x)
        print(f"response: {resp[1]}")
        # print(f"          {resp[1]}")
        print(
            f"errors:   {hameg_device_handle.send_await_resp('SYSTem:ERRor:ALL?')[1][2:-1]}"
        )
