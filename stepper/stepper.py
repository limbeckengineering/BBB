import Adafruit_BBIO.GPIO as GPIO
from BBstepper import Stepper


pins = {"P8_13","P8_14","P8_15","P8_16"}

stepper = Stepper()

stepper.init_pins(pins)

stepper.spin_clockwise(pins, 3, 30)
