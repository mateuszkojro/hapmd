
from arduino_connector import ArduinoConnector

if __name__ == "__main__":
    print("""
 /$$$$$$$              /$$                                /$$$$$$  /$$$$$$
| $$__  $$            | $$                               /$$__  $$|_  $$_/
| $$  \ $$  /$$$$$$  /$$$$$$    /$$$$$$   /$$$$$$       | $$  \__/  | $$  
| $$$$$$$/ /$$__  $$|_  $$_/   /$$__  $$ /$$__  $$      | $$        | $$  
| $$__  $$| $$  \ $$  | $$    | $$  \ $$| $$  \__/      | $$        | $$  
| $$  \ $$| $$  | $$  | $$ /$$| $$  | $$| $$            | $$    $$  | $$  
| $$  | $$|  $$$$$$/  |  $$$$/|  $$$$$$/| $$            |  $$$$$$/ /$$$$$$
|__/  |__/ \______/    \___/   \______/ |__/             \______/ |______/
          """)
    port:str = "COM3"
    device = ArduinoConnector.connect_on_port(port)
    print("Arduino device set up: OK")
    print(f"Connection Port: {port}")
    print(f"Current angle: {device.get_angle()}")
    
    while True:
        new_angle = input("command: ")
        if new_angle == "":
            print(device.check_connection())
        elif new_angle == " ":
            print(device.get_angle())
        else:
            device.move_to(float(new_angle))
