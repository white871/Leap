import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)

hallpin = 12

gpio.setup(hallpin, gpio.IN)

while True:
    if (gpio.input(hallpin) == False):
        print("magnet detected")
    else:
        print("none")
    time.sleep(0.5)