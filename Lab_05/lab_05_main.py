import datetime
from bluepy.btle import Scanner


def scan(scan_duration=10.0):
    """
    Scan for BLE devices and print the results to the console
    :param scan_duration: The duration to scan for in seconds, default is 10 seconds
    :return:
    """
    # Create a scanner object to look for BLE devices
    scanner = Scanner()

    # Scan for 10 seconds and return a list of devices
    devices = scanner.scan(scan_duration)

    # Get the current time
    scan_time = datetime.datetime.now()
    print(f"Scan: {scan_time}")

    # Print the list of devices found and some of their details
    for device in devices:
        # Comment this line if you want to see all the BLE devices around
        if 9 in device.scanData.keys() and device.scanData[9] == b'Thingy':
            print(f"    Device {device.addr} | RSSI={device.rssi} dB")


if __name__ == '__main__':
    # Run the scan function
    scan()
