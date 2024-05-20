from utility.UUIDS import *
from bleak import *


async def scan():
    devices = await BleakScanner.discover()
    for device in devices:
        if device.name == 'Thingy':
            print(device.address)


if __name__ == '__main__':
    asyncio.run(scan())
