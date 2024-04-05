import RPi.GPIO as GPIO
import time
import math

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

pin_A = 31
pin_B = 29

Encoder_Count = 0

GPIO.setup(pin_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def do_Encoder(channel):
    global Encoder_Count
    if GPIO.input(pin_B) == 1:
        Encoder_Count += 1
    else:
        Encoder_Count -= 1
GPIO.add_event_detect (pin_A, GPIO.FALLING, callback=do_Encoder)

while True:
    print(Encoder_Count)