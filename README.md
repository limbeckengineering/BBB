BBB
===================================

This folder contains the files needed for the BeagleBone Black located on the float of our submersible. 

To install the necessary libraries run the _init.sh_ file. To initiate the Python code run the _setup.py_ file. 

The following code is only tested for Ubuntu Saucy (13.10) on the BeagleBone Black. It will work on most Ubuntu systems, although you needed an updated Bone kernel in order for the software to work. Check you bone kernel by using this comand: _uname -a_. Make sure it is Bone_28 or above. 


Dependencies
----------------------------------

The _init.sh_ file will install the following:
	
		•Python and Python GPIO dependencies
		•Adafruit_BBIO library files
		•Java 7 Runtime Environt
		•GPSd, GPSd-clients, and Python-GPS
		•Update and Upgrade of the operating system

To download everything run:

_sudo bash init.sh_



Stepper Library
-----------------------------------

Run this command to initate the stepper library:

_sudo python setup.py install_

The commands are as follows:
