# XBee3 setup in XCTU
Condensed version of [this](https://xbplib.readthedocs.io/en/latest/getting_started_with_xbee_python_library.html) guide

## Basic setup
The following should be done to each device. Saving the device profile will speed up the process if you have multiple devices.

[Default] - Load default firmware settings. Using the search function you might want to adjust the following settings:
- "**CE**" Device role: Your local "master" device should **Form** the network, others should **Join** the network.
- "**ID**" to whatever network ID you want to use. This is the network your devices will join / search
- "**AP**" to [1] (API mode without escapes) for the device to work with digi-xbee python library
- "**NI**" value will give your device a name. It's  easier to remember than a long hex value
- "**BD**" adjusting baud rate might make reading and writing to device a little bit snappier!
- "**EE, EO**" you might want to encrypt wireless comms between devices 

For digi-xbee library use you only need to make sure all your devices have the same **ID** set. Other settings can be mostly adjusted wirelessly in your program if needed.

Write settings to module (Write)

To test if the devices see each other, run "Discover radio nodes in same network" (middle button in a device's card under Radio Modules).

