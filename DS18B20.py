import time

w1 = "/sys/bus/w1/devices/28-00000494acf0/w1_slave"

while True:
	raw = open(w1, "r").read()
	print "Temp: "+str((float(raw.split("t=")[-1])/1000)*(9.0/5.0) + 32.0)+" F"
	time.sleep(1)

