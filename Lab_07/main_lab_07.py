import warnings
from bleak import *
from utility.UUIDS import *
from utility.callbacks import *

# Ignore the FutureWarning kind of warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def get_uuid(device):
    return str(device.details[0].identifier).split(",")[1].split("= ")[1]

def motion_characteristics(
        step_counter_interval=100,
        temperature_comp_interval=100,
        magnetometer_comp_interval=100,
        motion_processing_unit_freq=60,
        wake_on_motion=1
):
    """

    :param step_counter_interval:
    :param temperature_comp_interval:
    :param magnetometer_comp_interval:
    :param motion_processing_unit_freq:
    :param wake_on_motion:
    :return:
    """

    """
    The format string '<4H B' specifies the following:
        <  : Little-endian byte order.
        4H : Four 16-bit unsigned integers.
        B  : One 8-bit unsigned integer.
    """
    format_str = "<4H B"

    return struct.pack(format_str,
                       step_counter_interval,
                       temperature_comp_interval,
                       magnetometer_comp_interval,
                       motion_processing_unit_freq,
                       wake_on_motion)

async def scan():
    """
    Scan for BLE devices and print the results to the console
    :return: A list of Thingy devices found
    """
    # Scan and save the list of devices
    devices = await BleakScanner.discover(cb=dict(use_bdaddr=True))

    # Get the current time
    scan_time = datetime.now()
    print(f"Scan: {scan_time}")

    # Print the list of devices found and some of their details
    for device in devices:
        print(f"    Device {device.address} | RSSI={device.rssi} dB")

    return devices


async def connect_and_collect(device, sampling_frequency=60):
    """
    Connect to a BLE device and collect data from it
    :param device: The device to connect to
    :param sampling_frequency: The sampling frequency to set for the sensor, default is 60 Hz
    :return:
    """
    async with BleakClient(get_uuid(device)) as client:
        # Ensure the client is connected
        if not await client.is_connected():
            print("Failed to connect to Thingy52")
            return

        print("Connected to Thingy52")

        # Set the sampling frequency
        payload = motion_characteristics(motion_processing_unit_freq=sampling_frequency)
        await client.write_gatt_char(TMS_CONF_UUID, payload)
        # Subscribe to accelerometer notifications
        await client.start_notify(TMS_RAW_DATA_UUID, raw_data_callback)

        print("Subscribed to accelerometer notifications.")

        try:
            while True:
                await asyncio.sleep(1)
        except Exception:
            print("Exiting...")

        # Stop notifications before exiting
        await client.stop_notify(TMS_RAW_DATA_UUID)

if __name__ == '__main__':
    # MAC address of my Nordic Thingy52
    my_thingy_mac_address = "EE:39:9A:D5:B5:D5"

    # Run the scan function
    discovered_thingy = asyncio.run(scan())

    # Retain only my device, None if my device has not being discovered
    my_thingy_device = next((t for t in discovered_thingy if t.address.lower() == my_thingy_mac_address.lower()), None)

    # Connect and gather the data
    if my_thingy_device:
        asyncio.run(connect_and_collect(my_thingy_device))
    else:
        print("Device not detected")
