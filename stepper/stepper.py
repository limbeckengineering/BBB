import Adafruit_BBIO.GPIO as GPIO
from BBstepper import Stepper
import config


stepper = Stepper()

stepper.init_pins(config.pins)	

stepper.spin_clockwise(config.pins, 3, 30)

stepper.cleanup(pins)
