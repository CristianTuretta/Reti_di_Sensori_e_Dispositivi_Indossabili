import struct

"""
https://nordicsemiconductor.github.io/Nordic-Thingy52-FW/documentation/firmware_architecture.html
"""

def raw_data_callback(sender, data):
    # Handle the incoming accelerometer data here

    # Accelerometer
    acc_x = (struct.unpack('h', data[0:2])[0] * 1.0) / 2 ** 10
    acc_y = (struct.unpack('h', data[2:4])[0] * 1.0) / 2 ** 10
    acc_z = (struct.unpack('h', data[4:6])[0] * 1.0) / 2 ** 10

    # Gyroscope
    gyro_x = (struct.unpack('h', data[6:8])[0] * 1.0) / 2 ** 5
    gyro_y = (struct.unpack('h', data[8:10])[0] * 1.0) / 2 ** 5
    gyro_z = (struct.unpack('h', data[10:12])[0] * 1.0) / 2 ** 5

    # Compass
    comp_x = (struct.unpack('h', data[12:14])[0] * 1.0) / 2 ** 4
    comp_y = (struct.unpack('h', data[14:16])[0] * 1.0) / 2 ** 4
    comp_z = (struct.unpack('h', data[16:18])[0] * 1.0) / 2 ** 4

    print(f"\rAccelerometer: X={acc_x: 2.3f}, Y={acc_y: 2.3f}, Z={acc_z: 2.3f}", end="", flush=True)