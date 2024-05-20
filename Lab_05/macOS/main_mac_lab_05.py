import datetime
import warnings
from bleak import *

# Ignore the FutureWarning kind of warnings
warnings.filterwarnings("ignore", category=FutureWarning)

async def scan():
    """
    Scan for BLE devices and print the results to the console
    :return:
    """
    # Scan and save the list of devices
    devices = await BleakScanner.discover()

    # Get the current time
    scan_time = datetime.datetime.now()
    print(f"Scan: {scan_time}")

    # Print the list of devices found and some of their details
    for device in devices:
        # Comment this line if you want to see all the BLE devices around
        if device.name == 'Thingy':
            print(f"    Device {device.address} | RSSI={device.rssi} dB")


if __name__ == '__main__':
    # Run the scan function
    asyncio.run(scan())
