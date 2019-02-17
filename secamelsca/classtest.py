from XBee.XBclass import masterXBee
import time
from threading import Thread


# open local "master" xbee :D
master = masterXBee(port="com6", baud="921600")
# start polling sensors in a new thread
xbeethread = Thread(target=master.polling_start, args=(0.01,))
xbeethread.start()
time.sleep(1)

print(master.get_device_data())
print(master.get_sensor_data())
