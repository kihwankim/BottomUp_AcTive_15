import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
# Up
GPIO.setup(27, GPIO.OUT) # Yellow
GPIO.setup(22, GPIO.OUT) # Green
# Right
GPIO.setup(23, GPIO.OUT) # Yellow
GPIO.setup(24, GPIO.OUT) # Green
# Down
GPIO.setup(20, GPIO.OUT) # Yellow
GPIO.setup(21, GPIO.OUT) # Green
# Left
GPIO.setup(5, GPIO.OUT) # Yellow
GPIO.setup(6, GPIO.OUT) # Green

def light_On_LED(information_Of_Lighting):
    light_Of_Up = information_Of_Lighting[0]
    light_Of_Right = information_Of_Lighting[1]
    light_Of_Down = information_Of_Lighting[2]
    light_Of_Left = information_Of_Lighting[3]

    # light information is 0 -> Nothing, 1 -> Door, 2 -> Stair
    light_On_Up(light_Of_Up)
    light_On_Right(light_Of_Right)
    light_On_Down(light_Of_Down)
    light_On_Left(light_Of_Left)

def light_On_Up(light):
    GPIO.output(27, False)
    GPIO.output(22, False)

    if light is 1:
        GPIO.output(22, True)
    elif light is 2:
        GPIO.output(27, True)

def light_On_Right(light):
    GPIO.output(23, False)
    GPIO.output(24, False)

    if light is 1:
        GPIO.output(24, True)
    elif light is 2:
        GPIO.output(23, True)

def light_On_Down(light):
    GPIO.output(20, False)
    GPIO.output(21, False)

    if light is 1:
        GPIO.output(21, True)
    elif light is 2:
        GPIO.output(20, True)

def light_On_Left(light):
    GPIO.output(5, False)
    GPIO.output(6, False)

    if light is 1:
        GPIO.output(6, True)
    elif light is 2:
        GPIO.output(5, True)

def light_Off():
    GPIO.output(27, False)
    GPIO.output(22, False)
    GPIO.output(23, False)
    GPIO.output(24, False)
    GPIO.output(20, False)
    GPIO.output(21, False)
    GPIO.output(5, False)
    GPIO.output(6, False)