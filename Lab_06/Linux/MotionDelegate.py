from utility.callbacks import *
from bluepy.btle import DefaultDelegate


class MotionDelegate(DefaultDelegate):

    def __init__(self, mac_adr: str):
        super().__init__()
        # Load configuration

        self.mac = mac_adr

        # Set handlers
        self.handlers = {
            65: raw_data_callback,
        }

    def handleNotification(self, handle_code, data):
        # Call the correct method to decode the received data
        self.handlers[handle_code](self, data)
