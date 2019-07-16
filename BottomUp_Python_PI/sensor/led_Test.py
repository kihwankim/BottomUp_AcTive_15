import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

while True:
    value = int(input())
    GPIO.output(23, False)
    GPIO.output(24, False)
    GPIO.output(25, False)

    if value == 1: # Turn on green LED
        GPIO.output(23, True)
    elif value == 2:
        GPIO.output(24, True)
    elif value == 3:
        GPIO.output(25, True)

GPIO.output(23, False)
GPIO.output(24, False)
GPIO.output(25, False)
