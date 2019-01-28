# XBee3 setup in XCTU
Condensed version of [this](https://xbplib.readthedocs.io/en/latest/getting_started_with_xbee_python_library.html) guide

## Basic setup
The following should be done to each device. Saving the device profile will speed up the process if you have multiple devices.
1. [Default] - Load default firmware settings
2. Search for "AP" and set it to [1] (API mode without escapes)
3. "ID" to whatever network ID you want to use
4. "CE" Device role: One of your devices should Form network, others should Join network.
5. "NI" value will give your device a name. It's  easier to remember than a long hex value
6. Write settings to module (Write)
7. To test if the devices see each other, run "Discover radio nodes in same network" (middle button in a device's card under Radio Modules).

## Testing if the devices can send/receive messages:
todo :D
asdf