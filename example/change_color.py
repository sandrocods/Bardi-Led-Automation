import time

from src.BardiHelper import BardiConnector

# Use wifi connection
# 1. Connect usb cable to your phone
# 2. Open cmd
# 3. Type: adb tcpip 5555
# 4. Get your phone ip address

connector_bardi = BardiConnector(
    timeout=10.0, # timeout for waiting element
    connection_type="wifi", # connection type, can be "wifi" or "usb"
    address="192.168.0.161:5555" # address for wifi connection
)

# Get device name
get_device_bardi = connector_bardi.get_bardi_device()
if get_device_bardi["status"]:
    print(
        get_device_bardi["data_device"]
    )

    # Connect to device
    connect_device_bardi = connector_bardi.connect_bardi_device(get_device_bardi["data_device"][0])
    if connect_device_bardi["status"]:
        print("Device connected")

        # change power device to on
        print("Changing power to on")
        connector_bardi.change_state("on")

        # change color to red
        print("Changing color to pink")
        connector_bardi.change_color(
            color="pink"
        )

        # change color to white
        print("Changing color to white")
        connector_bardi.change_color(
            color="white"
        )

        time.sleep(2)

        # change color to half white
        print("Changing color to half white")
        connector_bardi.change_color(
            color="half white"
        )

        time.sleep(2)

        # change color to sepia
        print("Changing color to sepia")
        connector_bardi.change_color(
            color="sepia"
        )






    else:
        print("Device not connected")

else:
    print("Device not found")