from LCD_I2C.lcd_I2C import *
from LED.led_Driver import *

lcd_Display_Clear()

while True:
    lcd_Value = list(map(int, input("LCD 정보 입력: ").split(' ')))
    if lcd_Value[0] is -1:
        break
    if lcd_Value.__len__() is not 4:
        continue

    led_Value = list(map(int, input("LED 정보 입력: ").split(' ')))
    if led_Value.__len__() is not 4:
        continue

    lcd_Display_Write_Direction(lcd_Value)
    light_On_LED(led_Value)

lcd_Display_Clear()
light_Off()