# Classes for xbee / sensors?
- To initiate the local xbee device we need the COM port and baud rate.
- The local device can discover remote devices and get their names / functions.
- Using a list of devices and their names in the network, these can be given objects in our program?

- If we deside on set names for different sensors / configurations of XBee devices we can have a list of what pins with what modes they use:
    - Say we have an XBee named DOOR 01
    - DOOR type XBees always have only two pins in use:
      - DIO4 set as digital I/O pin connected to door opening sensor
      - AD3 set as Analog to Digital, connected to weight sensor under door
      - 