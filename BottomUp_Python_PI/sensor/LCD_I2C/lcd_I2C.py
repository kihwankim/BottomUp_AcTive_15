import lcd_Driver
from time import *

lcd = lcd_Driver.lcd()
lcd.lcd_clear()

def lcd_Control():
    while True:
        message_Value = list(map(int, input().split(' ')))
        lcd.lcd_clear()
        lcd_Display(message_Value)

def lcd_Display(message_Value):
    up = message_Value[0]
    right = message_Value[1]
    down = message_Value[2]
    left = message_Value[3]

    first_Line_Message = ""
    second_Line_Message = ""

    if up is 0:
        first_Line_Message = "U  (X)  "
    else:
        first_Line_Message = "U " + ("%04d"%up) + "  "

    if down is 0:
        first_Line_Message += "D  (X)"
    else:
        first_Line_Message += "D " + ("%04d"%down)

    if left is 0:
        second_Line_Message = "L  (X)  "
    else:
        second_Line_Message = "L " + ("%04d"%left) + "  "

    if right is 0:
        second_Line_Message += "R  (X)"
    else:
        second_Line_Message += "R " + ("%04d"%right)

    lcd.lcd_display_string(first_Line_Message, 1)
    lcd.lcd_display_string(second_Line_Message, 2)

lcd_Control()