# PulsarSDK: Python SDK for Binho Pulsar USB Host Adapter

PulsarSDK is a Python package for interacting with the Binho Pulsar USB host adapter. The Pulsar adapter provides simplified control of embedded systems, supporting I2C, SPI, UART, and GPIO communication protocols.

## Prerequisites

Ensure your system meets the following requirements before installing the PulsarSDK:

- Python 3.8 or higher
- Windows, macOS, or Linux
- Binho Pulsar USB host adapter with up-to-date firmware

## Installation

Install the latest version of the PulsarSDK from PyPi using pip:

```sh
pip install BinhoPulsar
```

After installation, the SDK is ready for use in your Python projects.

## API Overview

The Pulsar host adapter shares its API with the Binho Supernova adapter. If you're familiar with the SupernovaSDK, transitioning to the PulsarSDK will be straightforward, as the same commands and interfaces are used for the supported protocols.

## Basic Usage Example

This example demonstrates how to use the Pulsar SDK with a Pulsar device. The Pulsar operates asynchronously; commands are sent to the host adapter, and responses are handled via a callback function.

```python
from BinhoPulsar import getConnectedPulsarDevicesList
from BinhoPulsar.Pulsar import Pulsar
from BinhoPulsar.definitions import *

# Get connected Pulsar devices
devices = getConnectedPulsarDevicesList()
print(devices)

# Open a connection to the first Pulsar device
pulsar = Pulsar()
print(pulsar.open(path=devices[0]["path"]))

# Define a callback function to handle responses from the device
def callback(pulsar_message: dict, system_message: dict):
    print(f"Transaction ID: {pulsar_message['id']}")
    print(f"Command Code: {pulsar_message['command']}")
    print(f"Command Name: {pulsar_message['name']}")
    print(f"Message Length: {pulsar_message['length']}")
    print(f"Message Content: {pulsar_message['message']}")

# Register the callback function
print(pulsar.onEvent(callback))

# Define a transaction ID for tracking requests
transaction_id = 0

# Send a request to retrieve the manufacturer string from a connected USB device
request_result = pulsar.getUsbString(transaction_id, GetUsbStringSubCommand.MANUFACTURER)
# Example result: {'type': 'request_validation_result', 'id': 0, 'command': 96, 'code value': 0, 'code name': 'SUCCESS', 'message': 'GET USB STRING request successful'}
```