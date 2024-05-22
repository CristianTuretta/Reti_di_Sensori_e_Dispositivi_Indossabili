import datetime
from bluepy.btle import Scanner
from bluepy.thingy52 import Thingy52
from MotionDelegate import MotionDelegate


def scan(scan_duration=10.0):
    """
    Scan for BLE devices and print the results to the console
    :param scan_duration: The duration to scan for in seconds, default is 10 seconds
    :return: A list of Thingy devices found
    """
    # Create a scanner object to look for BLE devices
    scanner = Scanner()

    # Scan for 10 seconds and return a list of devices
    devices = scanner.scan(scan_duration, passive=True)

    # Get the current time
    scan_time = datetime.datetime.now()
    print(f"Scan: {scan_time}")

    # Print the list of devices found and some of their details
    thingy_devices = []
    for device in devices:
        # Comment this line if you want to see all the BLE devices around
        if 9 in device.scanData.keys() and device.scanData[9] == b'Thingy':
            print(f"    Device {device.addr} | RSSI={device.rssi} dB")
            thingy_devices.append(device)

    return thingy_devices

def connect_and_collect(device, sampling_frequency=60):
    """
    Connect to a BLE device and collect data from it
    :param device: The device to connect to
    :param sampling_frequency: The sampling frequency to set for the sensor, default is 60 Hz
    :return:
    """

    try:
        # Crete an object representing the Thingy 52 device
        thingy52 = Thingy52(device.addr)

        # Create a delegate to handle the motion data
        motion_delegate = MotionDelegate(device.addr)

        # Enable UI service, this allows us to control the LED color
        thingy52.ui.enable()

        # Enable the motion service and set the raw data notification
        thingy52.motion.enable()
        thingy52.motion.set_rawdata_notification(True)

        # Set the sampling frequency
        thingy52.motion.configure(motion_freq=sampling_frequency)

        # Set the delegate to the connected sensor
        thingy52.setDelegate(motion_delegate)
        print("Connected to Thingy52")
        print("Subscribed to accelerometer notifications.")

    except Exception as e:
        print(f"Failed initialization of Thingy52: {e}")
        return

    try:
        # Make the LED breathe during the recording
        thingy52.ui.set_led_mode_breathe(0x01, 50, 100)
        while True:
            thingy52.waitForNotifications(1.)

    except KeyboardInterrupt:
        print("Exiting...")

    except Exception as e:
        print(f"An error occurred: {e}")

    # Stop notifications before exiting
    thingy52.motion.set_rawdata_notification(False)


if __name__ == '__main__':
    # Run the scan function
    dev = scan()
    connect_and_collect(dev[0])
