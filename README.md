BBB
===================================

This folder contains the files needed for the BeagleBone Black located on the float of our submersible. 

To install the necessary libraries run the _init.sh_ file. To initiate the Python code run the _setup.py_ file. 

The following code is only tested for Ubuntu Saucy (13.10) on the BeagleBone Black. It will work on most Ubuntu systems, although you needed an updated Bone kernel in order for the software to work. Check you bone kernel by using this comand: _uname -a_. Make sure it is Bone_28 or above. 

If you would like a more detalied explanation on the RoboGoby folder and what it contains please refer to out other repositoy name robogoby. Thanks.


Dependencies
----------------------------------

The _init.sh_ file will install the following:
	
•Python and Python GPIO dependencies

•Adafruit_BBIO library files

•Java 7 Runtime Environment

•GPSd, GPSd-clients, and Python-GPS

•Update and Upgrade of the operating system

To download everything run:

_sudo bash init.sh_



Stepper Library
-----------------------------------

Run this command to initate the stepper library:

_sudo python setup.py install_

This is a library made especally for the BeagleBone. It used the Adafruit_BBIO library to run a stepper motor using the TB6600 stepper motor driver. The BeagleBone Black pins 15 and 17 on header 8. 

•Pin 17 is the "Clk" signal

•Pin 15 is the "Dir" signal
	
Below is an example of how to use the stepper library (variables = rotations, rpm):


	stepper.init_pins(config.pins)
	stepper.spin_clockwise(config.pins, rotations, rpm)
	stepper.spin_counterclockwise(config.pins, rotations, rpm)
	stepper.cleanup(config.pins)


For more information open the stepper.py file. The pins used can be changed by accessing config.py. 


GPSd through UART
--------------------------------------

The GPSd instillation will have been completed after the init.sh file was run.


The BBBgps.py file will read GPS data coming from UART4 on the BeagleBone, parse the data, and then send it in DD/MM/SS.SSL format back to the user. Enabling UART on the BeagleBone uses device tree overlays. If you already have the correct files in /lib/firmware then enabling UART is easy (bone_capemgr.# depends on the Bone kernel you have installed):
 
           sudo su
           echo BB-UART4 > /sys/devices/bone_capemgr.9/slots

And then lock the UART port with gpsd-clients (which was installed in during _init.sh_)

           gpsd /dev/ttyO4 -F /var/run/gpsd.sock

Now the BBBgps.py file can be run using Python:

          sudo python BBBgps.py
          


Reading Battery Life
------------------------------------------

The Battery.py file is used to read incoming voltages and relate that to % of battery. The hardware consists of a simple voltage step-down attached to the BeaglBone's ADC pins. The file was converted into a "RoboGobySensors.py" module for Project RoboGoby. For more information on how to use this code please read out blogpost found here:
	
	http://robogoby.blogspot.com/2014/05/measuring-battery-life-beaglebone-black.html


Depth Sensor
----------------------------------------

The depth.py file is a module created to measure psi and then conovert it to distance below sea level. This specific setup uses the BeagleBone Black's ADC pins and an SC150 pressure sensors. For more information on the sensors please read this blog post:

	http://robogoby.blogspot.com/2014/02/waterproofing-tru-stability-pressure.html


Temp with DS18B20
----------------------------------------

This repository also contains the file used to read a DS118B20 temperature sensor through the BeagleBone Black. This sensor is a one-wire sensors and has been extremely useful for things other than Project RoboGoby. If you would like to know more about this sensor please read out blogpost:

	http://robogoby.blogspot.com/2014/05/beaglebone-and-ds18b20-temp-sensor.html
	

