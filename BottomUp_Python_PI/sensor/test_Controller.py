from LCD_I2C.lcd_I2C import *
from LED.led_Driver import *

lcd_Display_Clear()
test_List = [1, 2, 4, 9]
lcd_Display_Write_Stair(test_List)

while True:
    lcd_Value = list(map(int, input("LCD 정보 입력: ").split(' ')))
    if lcd_Value[0] is -1:
        break
    if lcd_Value.__len__() is not 8:
        continue

    lcd_Display_Write_Direction(lcd_Value)
    
lcd_Display_Clear()
