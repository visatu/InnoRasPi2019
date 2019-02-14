from XBclass import masterXBee
# conf
xbPort = "com6"
baud = 115200

# open local "master" xbee :D
master = masterXBee(xbPort, baud)
# list of connected devices
print(master.devices)
for dev in master.devices:
    for sensor in master.devices[dev].sensors:
        if sensor == "NTC":
            val = master.devices[dev].sensors[sensor].general_IO()
            print(str(val))