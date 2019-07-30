from .lcd_Driver import lcd
from time import *

lcd = lcd()
lcd.lcd_clear()

def lcd_Display_Clear():
    lcd.lcd_clear()

def lcd_Display_Write_Direction(direction_Information):
    if direction_Information.__len__() is not 8:
        return

    up_Length = direction_Information[0]
    right_Length = direction_Information[1]
    down_Length = direction_Information[2]
    left_Length = direction_Information[3]
    up_Direction_Info = direction_Information[4]
    right_Direction_Info = direction_Information[5]
    down_Direction_Info = direction_Information[6]
    left_Direction_Info = direction_Information[7]

    first_Line_Message = ""
    second_Line_Message = ""

    '''
    Up, Down, Left, Right Length는 도면에서 PI별 상대 위치를 나타내는 것
    Direction(Up,Down,Left,Right)과 (X)가 표시 되는 경우에는 해당 방향으로 경로가 없는 경우
    (X)가 표시되지 않고, 해당 방향으로 탈출 시 Door(탈출구)까지의 총 거리를 표시한다.
    탈출 방향이 옥상으로 가는 방향이라면 (^) 를 거리 옆에 출력하도록 하였다.
    거리의 단위는 M(Meter)이며 1000M를 넘길 수도 있는 경우를 고려하여 3자리의 정수로된 M값을 표시한다.
    또한 아래의 코드는 출력값을 LCD에 보기좋게 출력하기 위해 줄맞춤을 하였다.
    '''
    if up_Length is 0:
        first_Line_Message = "U  (X)  "
    else:
        first_Line_Message = "U " + ("%03d"%up_Length)
        if up_Direction_Info == 3:
            first_Line_Message += "(^)"


    if down_Length is 0:
        first_Line_Message += "D  (X)"
    else:
        first_Line_Message += "D " + ("%03d"%down_Length)
        if down_Direction_Info == 3:
            first_Line_Message += "(^)"

    if left_Length is 0:
        second_Line_Message = "L  (X)  "
    else:
        second_Line_Message = "L " + ("%03d"%left_Length)
        if left_Direction_Info == 3:
            second_Line_Message += "(^)"

    if right_Length is 0:
        second_Line_Message += "R  (X)"
    else:
        second_Line_Message += "R " + ("%03d"%right_Length)
        if right_Direction_Info == 3:
            second_Line_Message += "(^)"

    lcd.lcd_display_string(first_Line_Message, 1)
    lcd.lcd_display_string(second_Line_Message, 2)

def lcd_Display_Write_String(string):
    str_Length = string.__len__()
    
    if str_Length < 17:
        lcd.lcd_display_string(string, 1)
    else:
        first_Line_Message = ""
        second_Line_Message = ""
        for index in range(16):
            first_Line_Message += string[index]
        for index in range(16, str_Length):
            second_Line_Message += string[index]

        lcd.lcd_display_string(first_Line_Message, 1)
        lcd.lcd_display_string(second_Line_Message, 2)

def lcd_Display_Write_Stair(stair_Information):
    if stair_Information.__len__() is not 4:
        return

    down = stair_Information[0]
    up = stair_Information[1]
    enter = stair_Information[2]
    # stair_Information[3] 은 무시한다.

    first_Line_Message = ""
    second_Line_Message = ""

    if enter is 1:
        first_Line_Message = "    Enter(O)    "
    else:
        first_Line_Message = "    Enter(X)    "

    if up is not 0:
        second_Line_Message = "U " + ("%03d"%up)
    else:
        second_Line_Message = "U  (X)  "

    if down is not 0:
        second_Line_Message += "D" + ("%03d"%down)
    else:
        second_Line_Message += "D  (X)  "

    lcd.lcd_display_string(first_Line_Message, 1)
    lcd.lcd_display_string(second_Line_Message, 2)