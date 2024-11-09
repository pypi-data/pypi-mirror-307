__all__ = ["Pulsar"]

import hid
from .definitions import *
from .system_message import *

# VID and PID constants definition.
NXP_VID     = 0x1FC9
LPC5516_PID = 0x82FD

def getConnectedPulsarDevicesList() -> list:
    '''
    This function can be used to scan all the Pulsar devices connected
    to the host computer.

    Arguments
    ---------
    None

    Returns
    -------
    devices: list
        Python list that holds devices dictionary.
    '''

    # Get a list of dictionaries of devices info.
    devices = hid.enumerate(NXP_VID, LPC5516_PID)

    # For each device, print de VID and PID in hex, and convert the path
    # from bytes to String
    for device in devices:
        device['path'] = device['path'].decode(encoding='utf-8')
        device['vendor_id'] = hex(device['vendor_id'])
        device['product_id'] = hex(device['product_id'])

    # Return list of devices.
    return devices
