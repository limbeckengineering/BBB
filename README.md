BBB
===================================

This folder contains the files needed for the BeagleBone Black located on the float of our submersible. 

To install the necessary libraries run the _init.sh_ file. To initiate the Python code run the _setup.py_ file. 

The following code is only tested for Ubuntu Saucy (13.10) on the BeagleBone Black. It will work on most Ubuntu systems, although you needed an updated Bone kernel in order for the software to work. Check you bone kernel by using this comand: _uname -a_. Make sure it is Bone_28 or above. 


Dependencies
----------------------------------

The _init.sh_ file will install the following:
	
-Python and Python GPIO dependencies
-Adafruit_BBIO library files
-Java 7 Runtime Environment
-GPSd, GPSd-clients, and Python-GPS
-Update and Upgrade of the operating system

To download everything run:

_sudo bash init.sh_



Stepper Library
-----------------------------------

Run this command to initate the stepper library:

_sudo python setup.py install_

This is a library made especally for the BeagleBone. It used the Adafruit_BBIO library to run a stepper motor using the TB6600 stepper motor driver. The BeagleBone Black pins 15 and 17 on header 8. 

-Pin 17 is the "Clk" signal
-Pin 15 is the "Dir" signal
	
Below is an example of how to use the stepper library (variables = rotations, rpm):


	stepper.init_pins(config.pins)
	stepper.spin_clockwise(config.pins, rotations, rpm)
	stepper.spin_counterclockwise(config.pins, rotations, rpm)
	stepper.cleanup(config.pins)


For more information open the stepper.py file. The pins used can be changed by accessing config.py. 
