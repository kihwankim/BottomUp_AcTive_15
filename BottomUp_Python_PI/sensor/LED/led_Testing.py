from led_Driver import *

while True:
    input_Info = list(map(int, input().split(' ')))
    if input_Info.__len__() is 4:
        light_On_LED(input_Info)

light_Off()