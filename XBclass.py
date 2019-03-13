#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from digi.xbee.io import IOLine, IOMode, IOValue
from digi.xbee.devices import XBeeDevice
import digi.xbee.exception, serial.serialutil
import time,math
from threading import Thread,Semaphore
from XBDevices import deviceTypes

# threading for some functions (mainly for sensor polling)
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = Thread(name=fn.__name__,target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper


class masterXBee:
    '''
    Class for the local XBee device, containing all connected devices and their pins in a dictionary
    port = used COM/tty port
    baud = used baud rate
    callback_handler: function you want to handle callbacks!
        callback_handler should take two arguments:
        sensor(str) = name of sensor
        value(str) = value of sensor (HIGH or LOW)
    '''
    # functional devices dictionary
    devices = {}
    # sensor polling state
    polling = False
    # flask readable device data dictionary
    devicedata = {}
    # flask readable sensor data dictionary
    sensordata = {}

    
    

    def __init__(self, port, baud, callback_handler=None):
        #Semaphore for XBee action, limits acces to single user at a time
        self.sema = Semaphore()
        # instantiate local XBee device
        print("Opening local device", port, baud)
        self.localXB = XBeeDevice(port,baud)
        self.localXB.open()
        # find devices in network, store in dict
        devices = self.getNetworkDevices()
        # write flask readable device dict
        self.devicedata = self.get_device_data()
        # create sensor data dict
        self.sensordata = self.get_sensor_data()
        # set local device to receive IO callbacks
        self.localXB.set_dest_address(self.localXB.get_64bit_addr())
        self.localXB.add_io_sample_received_callback(self.io_sample_callback)
        self.callback_function = callback_handler
        #clear previous monitored IO lines:
        for dev in self.devices:
            self.devices[dev].xbee.set_dio_change_detection(None)

    def getNetworkDevices(self):
        """
        Returns devices in the network of given local xBee device, including the local device:
        devices = dict of all the devices in locals network and their sensors!
        devices : {
            "device ID" : <XBeeDev object>
                sensors = {
                    "NAME/TYPE"  : {
                        "line" : IOLine,
                        "mode" : IOMode,
                    }
                }
        }
        """
        print("Getting a list of network devices...")
        # Get devices in local xbee's network!
        self.localXB.send_data_broadcast("Getting a list of everyone :D")
        network = self.localXB.get_network()
        network.start_discovery_process()
        while network.is_discovery_running():
            time.sleep(.5)
        networkDevices = network.get_devices()
        networkDevices.insert(0, self.localXB)
        # loop through found network devices and create a XBeeDev object for each
        # containing device type and connected sensors
        print("Found devices and sensors:")
        for device in networkDevices:
            print(device)
            # new xbee device with its pins n stuff
            XBeeDevobj = XBeeDev(device)
            # add it to master class's device dict
            self.devices.update({XBeeDevobj.dvcID : XBeeDevobj})
        return networkDevices

    @threaded
    def polling_start(self, interval=1):
        "start updating all connected sensors with given interval"
        print("Starting sensor polling with interval %.3f seconds" %(interval))
        self.polling = True
        while self.polling == True:
            for dvc in self.devices:
                for sensor in self.devices[dvc].sensors:
                    self.sensor_update_value(self.devices[dvc].sensors[sensor])
            time.sleep(interval)

   
    def polling_stop(self):
        print("Stopped sensor polling!")
        "stop sensor value updating"
        self.polling = False

    def get_sensor_data(self):
        "returns sensor data dict to be written to by sensor value update function"
        sensordata = {}
        for dvc in self.devices:
            sensors = {}
            for sensor in self.devices[dvc].sensors:
                sensors.update({sensor : None})
            sensordata.update({dvc : sensors})
        return sensordata

    def get_device_data(self):
        "returns flask readable device data"
        devicedata = {}
        for device in self.devices:
            dvcID = self.devices[device].dvcID
            dvcType = self.devices[device].dvcType
            sensorlist = []
            for sensor in self.devices[device].sensors:
                    sensorlist.append(sensor)
            devicedata.update({dvcID : {
                    "type" : dvcType,
                    "sensors" : sensorlist,
                    }
            })
        return devicedata

    def register_callback(self, deviceID, sensorNames):
        """
        register a callback function for a value change in given XBeeSensor objects (DIGITAL I/O!)
        input is a list of sensor objects
        """
        lines =  []
        # get xbee device and sensor pin line from device library
        xbee = self.devices[deviceID].xbee
        xbee.set_dio_change_detection(None)
        for name in sensorNames:
            lines.append(self.devices[deviceID].sensors[name].pinLine)
        # xbee-python library function to register change detection sampling :D
        xbee.set_dio_change_detection(lines)

    @threaded
    def io_sample_callback(self, io_sample, remote_xbee, send_time):
        sender_id = str(remote_xbee).split()[0]
        for sensor in self.devices[sender_id].sensors:
            pinLine = self.devices[sender_id].sensors[sensor].pinLine
            if pinLine in io_sample.digital_values:
                value = str(io_sample.digital_values[pinLine]).strip("IOValue.")
                print("IO Sample callback:", sensor, value)
                self.sensordata[sender_id][sensor] = value
                self.callback_function(sensor, value)


    def general_io(self, sensor, value_in=None):
        """
        Function to read and write values from/to this sensor. Give value if you want to write, otherwise assumes you're reading stuff :D
        """
        self.sema.acquire()
        value_out=None
        for attempt in range(10):
            try:
                # PWM output
                if sensor.pinMode == IOMode.PWM:
                    if value_in:
                        if (0 < int(value_in) < 100):
                            sensor.xbee.set_pwm_duty_cycle(sensor.pinLine, value_in)
                            self.sensordata[sensor.dvcID][sensor.pinType] = value_in
                            value_out = value_in
                        break
                # ADC read
                if sensor.pinMode == IOMode.ADC:
                    value_out = sensor.xbee.get_adc_value(sensor.pinLine)
                    break
                # Digital INPUT
                elif sensor.pinMode == IOMode.DIGITAL_IN:
                    value_out = sensor.xbee.get_dio_value(sensor.pinLine)
                    break
                # Digital OUTPUT
                elif sensor.pinMode in [IOMode.DIGITAL_OUT_HIGH, IOMode.DIGITAL_OUT_LOW]:
                    if value_in == "HIGH":
                        sensor.xbee.set_dio_value(sensor.pinLine, IOValue.HIGH)
                        self.sensordata[sensor.dvcID][sensor.pinType] = value_in
                        value_out = value_in
                        break
                    elif value_in == "LOW":
                        sensor.xbee.set_dio_value(sensor.pinLine, IOValue.LOW)
                        self.sensordata[sensor.dvcID][sensor.pinType] = value_in
                        value_out = value_in
                        break
                    else:
                        value_out = value_in
                        break
            # errors that xbee gives when doing lots of stuff through serial.. . :D
            # might want to implement queue.
            # Added semaphores to compat this
            # except digi.xbee.exception.TimeoutException:
            #     pass
            # except ValueError:
            #     pass
            # or just skip everything. for now.
            except Exception as error:
                print("ERROR IN VALUE READ:", str(error))
                pass
        # if NTC, convert to celcius
        if "NTC" in str(sensor.pinType):
            if value_out:
                value_out = self.ntc_convert(value_out)
        self.sema.release()
        return value_out

    def ntc_convert(self, ADC_value):
        try:
            """ Returns NTC read temperature in Celsius"""
            R1 = 10000          # series resistor
            R0 = 10000          # NTC starting value
            T0 = 273 + 25       # Temp reference value in kelvins (273.15+25)
            Vs = 3.3            # supply voltage
            Vref = 3.3          # voltage reference
            Bval = 3450         # NTC B value
            # convert to analog voltage
            Vt = ADC_value/1023 * Vref
            # Vs---R1---(Sense)---tempR---GND
            tempR = Vt / (Vs-Vt) * R1
            # https://en.wikipedia.org/wiki/Thermistor#B_or_%CE%B2_parameter_equation
            tempK = Bval / math.log(tempR / (R0 * math.exp(-1 * Bval / T0)))
            # convert back to Celsius
            tempC = tempK - 273
            # print("NTC_convert\tADC: %04i\tR: %5.00f\tT: %.02f" %(ADC_value, tempR ,tempC))
            return "{:.1f}".format(tempC)
        except ZeroDivisionError:
            return(0)

    def sensor_update_value(self, sensor):
        "updtes the value of the sensor to sensordata dict"
        updated = self.general_io(sensor)
        if updated:
            value = str(updated).strip("IOValue.")
            self.check_trigger(sensor,value)

            self.sensordata[sensor.dvcID][sensor.pinType] = value
    
    def check_trigger(self, sensor, value):
        if not sensor.triggers:
            return
        if sensor.analogTrigger:
            if float(value) > sensor.limit:
                valueOut = "HIGH"
            else:
                valueOut = "LOW"
        else:
            if value == sensor.limit:
                valueOut = "HIGH"
            else:
                valueOut = "LOW"
            
        
        for dev in self.devices:
            devObj = self.devices[dev]
            for sens in devObj.sensors:
                if sens == sensor.target:
                    sensor = devObj.sensors[sens]
                    if self.sensordata[sensor.dvcID][sensor.pinType] != valueOut:
                        self.general_io(sensor,valueOut)


class XBeeDev:
    "Class for a single xbee device connected in network. contains info about sensors and stuff"
    def __init__(self,XBee):
        # get the type of the device (node id for now)
        self.dvcType = XBee.get_node_id()
        self.xbee = XBee
        # get unique identifier
        # binascii.hexlify(bytearray(array_alpha))
        self.dvcID = bytes(XBee.get_64bit_addr()).hex().upper()
        self.sensors = {}
        # loop through pins listed in deviceTypes dictionary, init pins on xbee accordinly
        for pinType in deviceTypes[self.dvcType]:
            sensor = XBeeSensor(pinType, XBee)
            self.sensors.update({pinType : sensor})


class XBeeSensor:
    "class for a single xbee pin/sensor. Has functions for reading and writing values!"
    def __init__(self, pinType, xbee):
        self.xbee = xbee
        self.dvcType = xbee.get_node_id()
        self.dvcID = bytes(xbee.get_64bit_addr()).hex().upper()
        self.pinType = pinType
        print("\t" + str(self.pinType) + " of " + self.dvcType, end="")
        self.pinLine = deviceTypes[self.dvcType][self.pinType]["line"]
        self.pinMode = deviceTypes[self.dvcType][self.pinType]["mode"]
        self.triggers = False
        self.analogTrigger = True
        self.target = ""
        self.limit = 0
        if "trigger" in deviceTypes[self.dvcType][self.pinType]:
            trig = deviceTypes[self.dvcType][self.pinType]["trigger"]
            self.triggers = True
            self.target = trig["target"]
            if trig["limit"] == "HIGH":
                self.analogTrigger = False
                self.limit = "HIGH"
            elif trig["limit"] == "LOW":
                self.analogTrigger = False
                self.limit = "LOW"
            else:
                self.limit = trig["limit"]
        self.xbee.set_io_configuration(self.pinLine,self.pinMode)
        print(" ...OK!")
