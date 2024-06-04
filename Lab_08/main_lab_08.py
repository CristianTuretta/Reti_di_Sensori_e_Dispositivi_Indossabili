from functools import partial
from bleak import *
from utility.UUIDS import *
from utility.callbacks import *
from utility.callbacks import raw_data_callback_with_info

async def scan():
    """
    Scan for BLE devices and print the results to the console
    :return: A list of Thingy devices found
    """
    # Scan and save the list of devices
    devices = await BleakScanner.discover(cb=dict(use_bdaddr=True))

    return devices

async def change_status(client, status: str):
    """
    Change the color of the LED on the Thingy52
    :param client: The client object
    :param status: The status to change to
    :return: None
    """
    payload = None

    if status == "connected":
        format_str = "<4B"
        constant_light = 1
        green = (0, 255, 0)
        payload = struct.pack(format_str, constant_light, *green)

    if status == "recording":
        format_str = "<4B"
        constant_light = 1
        red = (255, 0, 0)
        payload = struct.pack(format_str, constant_light, *red)

    if payload is not None:
        # Write the color data to the LED characteristic
        await client.write_gatt_char(UIS_LED_UUID, payload)

def get_uuid(device):
    return str(device.details[0].identifier).split(",")[1].split("= ")[1]

def find_my_devices(discovered_devices, addresses):
    my_devices = []
    for i in range(len(discovered_devices)):
        if discovered_devices[i].address in addresses:
            my_devices.append(discovered_devices[i])

    return my_devices

async def connection(devices):
    clients = await asyncio.gather(*[connect_to_device(device) for device in devices])

    return clients

async def connect_to_device(device):
    client = BleakClient(get_uuid(device))
    await client.connect()
    if client.is_connected:
        print(f"Connected to {device.address}")
        # Perform operations with the client here
        await change_status(client, "connected")
        return client, device.address
    else:
        print(f"Failed to connect to {device.address}")
        return None, None

async def record_from_client(client, device_address):
    await client.start_notify(TMS_RAW_DATA_UUID, partial(raw_data_callback_with_info, device_address))
    await change_status(client, "recording")

async def recording(clients):
    try:
        for client in clients:
            asyncio.ensure_future(record_from_client(*client))

        while True:
            await asyncio.sleep(1)

    except asyncio.exceptions.CancelledError or KeyboardInterrupt as _:
        print("Stopping...")
        for client, address in clients:
            print(f"Disconnecting from {address}...")
            await client.stop_notify(TMS_RAW_DATA_UUID)
            await client.disconnect()

async def main():
    my_thingy_addresses = ["EE:39:9A:D5:B5:D5", "E7:2F:13:17:C0:C4"]
    discovered_devices = await scan()

    my_devices = find_my_devices(discovered_devices, my_thingy_addresses)

    connected_thingy_devices = await connection(my_devices)

    input("Press enter to record data...")

    await recording(connected_thingy_devices)


if __name__ == '__main__':
    asyncio.run(main())
