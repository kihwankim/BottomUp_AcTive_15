import socket
from time import *
import sys
from threading import Thread
from queue import Queue
from sensor.LCD_I2C.lcd_I2C import * # LCD
from sensor.Temperature_Check_DHT11.temp_Check import * # 온도

# how to use
# in terminal : python3 this-file.py target-ip target-port
#      example) python3 test_final_3_add_floor.py 168.188.127.74 8000

PI_FLOOR = 0
PI_FLOOR_BYTE = 0
PI_NUM = 0
PI_NUM_BYTE = 0

PI_HEADER_BYTES = 0

emergency = False
queue = Queue()

def encode_message(message):
    byte_message = (message).to_bytes(1, byteorder='big')
    print("[DEBUG] send this", PI_HEADER_BYTES + byte_message)
    return PI_HEADER_BYTES + byte_message

def decode_data(data):
    pi_floor = data[0]
    pi_num = data[1]
    if len(data)==3:
        message = data[2]
    else:
        message = [int.from_bytes(data[x:x+2], byteorder='big') for x in range(2, len(data), 2)]
    return pi_floor, pi_num, message

class sender(Thread):
    def __init__(self, sock):
        super(sender, self).__init__()
        self.sock = sock

    def run(self):
        global emergency  ##### send, receive에서 같이 건드림. 크리티컬 섹션 유의

        # 초기 : 0.5초 주기로 재난상황 발생 체크
        while check_safe() and not emergency:
            sleep(0.5)

        # 상황 발생 송신
        self.sock.send(encode_message(255))

        queue.get()  # 'change emergency complete' 기다림

        # 상황 발생 : 0.1초 주기로 서버에 안전상태 송신
        while emergency:
            self.sock.send(encode_message(check_safe()))
            sleep(1)

        # 상황 종료 송신
        self.sock.send(encode_message(254))

def start_check(sock):
    # 상황 점검 시작
    # 서버로부터 'stop checking' 메세지가 오면, send, recv 함수 둘 다 종료된다
    t_send = sender(sock)
    t_send.daemon = True
    t_send.start()
    start_recv(sock)


def interpret_message(message):
    if type(message) == list:
        if len(list)==4:
            return 'msg for stair'
        if len(list)==8:
            return 'msg for non-stair'
    if message == 253:
        return 'start checking'
    if message == 254:
        return 'stop checking'
    if message == 255:
        return 'emergency'
    return 'cant interpret'

def wait_order(sock):
    while True:
        # 서버로부터 'start checking' 명령을 기다림 
        _, _, message = decode_data(sock.recv(10))
        print(message, interpret_message(message)) # for debug
        if interpret_message(message) != 'start checking':
            continue

        # 상황 점검 시작
        # 서버로부터 'stop checking' 메세지가 오면, send, recv 함수 둘 다 종료된다
        start_check(sock)

def start_recv(sock):
    global emergency

    while True:
        data = sock.recv(10)
        recv_pi_floor, recv_pi_num, message = decode_data(data)
        print("[DEBUG] %d층 %d번 수신 %s" %(recv_pi_floor, recv_pi_num, message))
        msg_interpreted = interpret_message(message)
        if msg_interpreted == 'stop checking':
            return

        if msg_interpreted != 'emergency':
            print("첫 수신 메시지 에러")
            continue

        emergency = True
        queue.put('change emrgency complete')
        while emergency:
            data = sock.recv(10)
            recv_pi_floor, recv_pi_num, message = decode_data(data)
            print("[DEBUG] %d층 %d번 수신 %s" %(recv_pi_floor, recv_pi_num, message))
            print(message)
            if check_recv(recv_pi_floor, recv_pi_num):
                msg_interpreted = interpret_message(message)
                if msg_interpreted == 'msg for stair':
                    lcd_show_stair(message)
                elif msg_interpreted == 'msg for non-stair':
                    lcd_show_notstair(message)
                # 254는 상황 종료를 의미
                elif msg_interpreted == 'stop checking':
                    emergency = False
                    return

# 데이터 배송지가 맞는지 확인
def check_recv(recv_pi_floor, recv_pi_num):
    if recv_pi_floor != PI_FLOOR or recv_pi_num != PI_NUM:
        print("[오류] : %s층 %s번 데이터 수신. 이 파이는 %s층 %s번" %(recv_pi_floor, recv_pi_num, PI_FLOOR, PI_NUM))
        return False
    return True

# 온도체크해서 안전하면 1, 위험하면 0 리턴
temp = 1
def check_safe():
    print("check temperature")
    value = check_Temperature()
    print(value)
    return value

# 수신한 데이터(정수 4개를 가진 리스트)로 stair의 lcd 출력
def lcd_show_stair(message):
    lcd_Display_Write_Stair(message)

# 수신한 데이터(정수 8개를 가진 리스트) 로 non-stair의 lcd 출력
def lcd_show_notstair(message):
    lcd_Display_Write_Direction(message)

# 인자로 들어오는 문자열을 lcd에 출력
def show_message(message):
    lcd_Display_Write_String(message)

def test_change_safety_status():
    global temp
    while True:
        temp = int(input("입력. 1이면 안전, 0이면 미안전:"))

def try_connect(sock):
    pi_floor = 0
    pi_floor_byte = 0
    pi_num = 0
    pi_num_byte = 0
    
    count = 0
    while count<10 :
        count += 1 
        data_receive = sock.recv(1024).decode()
        
        if data_receive == 'connect accept':
            return pi_floor, pi_floor_byte, pi_num, pi_num_byte
        
        print("currently remaining pi \n"+data_receive)
        pi_floor = int(input("choose your pi floor :"))
        pi_num = int(input("choose your pi number :"))

        pi_floor_byte = (pi_floor).to_bytes(1, byteorder='big')
        pi_num_byte = (pi_num).to_bytes(1, byteorder='big')
        sock.send(pi_floor_byte+pi_num_byte)
        
    # 10번 실패시 종료
    sock.close()
    sys.exit(0)

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((sys.argv[1], int(sys.argv[2])))

        PI_FLOOR, PI_FLOOR_BYTE, PI_NUM, PI_NUM_BYTE = try_connect(sock)
        PI_HEADER_BYTES = PI_FLOOR_BYTE + PI_NUM_BYTE
        print("connect success, %d층 %d번." %(PI_FLOOR, PI_NUM))

        ### TEST ###
        t_test = Thread(target=test_change_safety_status)
        t_test.start()

        # 서버로부터 명령을 기다리고, 명령을 수행하는 함수
        wait_order(sock)

    finally:
        sock.close()
