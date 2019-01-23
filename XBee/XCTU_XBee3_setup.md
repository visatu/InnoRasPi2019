# XBee3 setup in XCTU
Condensed version of [this](https://xbplib.readthedocs.io/en/latest/getting_started_with_xbee_python_library.html) guide

## Basic setup
The following should be done to each device. Saving the device profile will speed up the process if you have multiple devices.
1. [Default] - Load default firmware settings
2. Search for "AP" and set it to [1] (API mode without escapes)
3. "ID" to whatever ID you want to use
4. Scan channels "SC" to "FFF"
5. "CE" Device role: One of your devices should Form network, others should Join network.
6. Optionally, "NI" value will give your device a name.
7. Write settings to module (Write)
8. To test if the devices see each other, run "Discover radio nodes in same network" (middle button in a device's card under Radio Modules).

## Testing if the devices can send/receive messages:
1. Alt + C to switch to consoles working mode
2. Click "Open" to open a serial connection with receiving module.
3. In Python, give the following commands:
    ```python
    from digi.xbee.devices import XBeeDevice
    device = XBeeDevice("COM5", 9600) # COM port of the sending module
    device.open()
    device.send_data_broadcast("Hello World!")
    device.close()
    ```
4. In XCTU under the receiving device's Frame log, you should see a received frame as well as your chosen messsage in "Frame details"