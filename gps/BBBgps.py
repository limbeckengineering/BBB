#!/usr/bin/python

import gps

session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

while True:
	try:
		report = session.next()
		if report['class'] == 'TPV':
			if hasattr(report, 'lat' and 'lon'):
				latitude = report.lat
				longitude = report.lon
				lat = latitude
				lon = longitude
				latDeg = int(latitude)
				latMin = lat - latDeg
				lat = latMin*60
				if (lat < 0):
					lat = -lat
				latMin = int(lat)
				latSec = lat-latMin
				latSec = latSec*60
				lonDeg = int(longitude)
				lonMin = lon - lonDeg
				lon = lonMin*60
				if (lonDeg < 0):
					lon = -lon
				lonMin = int(lon)
				lonSec = lon-lonMin
				lonSec = lonSec*60
				print "Latitude:%s %s' %f''" %(int(latDeg), int(latMin), latSec)
				print "Longitude:%s %s' %f''" %(int(lonDeg), int(lonMin), lonSec)

	except KeyError:
		pass
	except KeyboardInterrupt:
		quit()
	except StopIteration:
		session = None
		print "GPSD has terminated"

