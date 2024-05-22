import asyncio
import struct
import datetime
import warnings
from bleak import *
from utility.UUIDS import *
from utility.callbacks import *

# Ignore the FutureWarning kind of warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def motion_characteristics(
        step_counter_interval=100,
        temperature_comp_interval=100,
        magnetometer_comp_interval=100,
        motion_processing_unit_freq=60,
        wake_on_motion=1
):

    return struct.pack("<4H B",
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
    devices = await BleakScanner.discover()

    # Get the current time
    scan_time = datetime.datetime.now()
    print(f"Scan: {scan_time}")

    # Print the list of devices found and some of their details
    thingy_devices = []
    for device in devices:
        # Comment this line if you want to see all the BLE devices around
        if device.name == 'Thingy':
            print(f"    Device {device.address} | RSSI={device.rssi} dB")
            thingy_devices.append(device)

    return thingy_devices


async def connect_and_collect(device, sampling_frequency=60):
    """
    Connect to a BLE device and collect data from it
    :param device: The device to connect to
    :param sampling_frequency: The sampling frequency to set for the sensor, default is 60 Hz
    :return:
    """
    async with BleakClient(device.address) as client:
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
    # Run the scan function
    dev = asyncio.run(scan())
    asyncio.run(connect_and_collect(dev[0]))
