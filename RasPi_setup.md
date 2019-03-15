# Raspberry Pi setup for running python & communicating with XBees :D

## Raspbian install
1. Download system image [here](https://www.raspberrypi.org/downloads/raspbian/). Raspbian Lite should be enough since you will probably be using the command line interface anyway. A desktop environment can be installed later as well.
2. follow steps [here](https://www.raspberrypi.org/documentation/installation/installing-images/) to flash to SD card.

    TLDR:
    - Windows: Use [Etcher](https://www.balena.io/etcher/)
    - Linux: Check device name of the SD card with `lsblk`, unzip and write to sd card with 
        
        `unzip -p downloaded_raspbian.zip | sudo dd of=/dev/Your_SD_Card bs=4M status=progress conv=fsync`
3. Done'd!

We have a couple of options on how to connect to the RasPi to get a hold of its command line:
- Connect a display and a keyboard
- Connect to PC using ethernet cable between computers (This is probably the easiest way)
- Connect the device to a network and SSH in using PuTTY, for example. Look up the IP the device gets either from a connected display (IP shown during bootup) or from a router the RPi is connected to. The default port used for SSH is 22.

- Use the GPIO pins to use serial communication through USB, with PuTTY, for example.
  - Note: we tried this and couldn't get it to work. UART seems to be disabled by default on the RPi 3. After enabling this by adding `enable_uart=1` to /boot/config.txt on the Raspbian SD card, we still couldn't get a computer to recognise the serial connection.

Once you have your connection setup:

The default username is **pi** and the default password is **raspberry**. You probably want to change at least the password. This can be done with the command `passwd`.

Optionally you might want to update the system:
```
sudo apt update && sudo apt upgrade
```

.. and maybe restart the RPi after that : 
```
sudo shutdown -r now
```
Python 3 should be installed:
```
$ python3 --version
Python 3.5.3
```
Python package installer **pip** is probably not though:
```
sudo apt install python3-pip
```
For XBee devices we'll need the `digi-xbee` library:
```
python3 -m pip install digi-xbee
```
This should be all that is needed to start working with xbee devices on the Raspberry Pi

## Extra stuff
### git
You'll probably want to install git as well:
```
sudo apt install git
```
### finding master xbee in linux
Under linux you can find your connected XBee (and other USB) devices in `/dev`. This path can be given to the digi-xbee library insteand of a COM port:
```
$ ls /dev/ttyUSB*
/dev/ttyUSB0
```
and in python:
```python
port = "/dev/ttyUSB0"
baud = 921600
myLocalXBee = digi.xbee.devices.XBeeDevice(port,baud)
```