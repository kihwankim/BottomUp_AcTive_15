import lcd_Driver
from time import *

lcd = lcd_Driver.lcd()
lcd.lcd_clear()

def lcd_Display_Clear():
    lcd.lcd_clear()

def lcd_Display_Write(message_Value):
    up = message_Value[0]
    right = message_Value[1]
    down = message_Value[2]
    left = message_Value[3]

    first_Line_Message = ""
    second_Line_Message = ""

    '''
    Up, Down, Left, Right는 도면에서 PI별 상대 위치를 나타내는 것
    Direction(Up,Down,Left,Right)과 (X)가 표시 되는 경우에는 해당 방향으로 경로가 없는 경우
    (X)가 표시되지 않고 해당 방향으로 탈출 시 Door(탈출구)까지의 총 거리를 표시한다.
    거리의 단위는 M(Meter)이며 1000M를 넘길 수도 있는 경우를 고려하여 4자리의 정수로된 M값을 표시한다.
    또한 아래의 코드는 출력값을 LCD에 보기좋게 출력하기 위해 줄맞춤을 하였다.
    '''
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
