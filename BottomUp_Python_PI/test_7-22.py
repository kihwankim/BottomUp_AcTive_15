import socket
import time
import sys
from threading import Thread
from queue import Queue

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

def action_check_send(sock):
    global emergency   ##### send, receive에서 같이 건드림. 크리티컬 섹션 유의

    # 초기 : 0.5초 주기로 재난상황 발생 체크
    while check_safe() and not emergency:
        time.sleep(0.5)

    # 상황 발생 송신
    sock.send(encode_message(255))
    
    queue.get() # 'change emergency complete' 기다림
    
    # 상황 발생 : 0.1초 주기로 서버에 안전상태 송신
    while emergency:
        sock.send(encode_message(check_safe()))
        time.sleep(1)
    
    # 상황 종료 송신
    sock.send(encode_message(254))

def interpret_message(message):
    if message == 253:
        return 'start checking'
    if message == 254:
        return 'stop checking'
    if message == 255:
        return 'emergency'
    return message

def wait_order(sock):
    while True:
        # 서버로부터 'start checking' 명령을 기다림 
        _, _, message = decode_data(sock.recv(10))
        print(message, interpret_message(message)) # for debug
        if interpret_message(message) != 'start checking':
            continue

        # 상황 점검 시작
        # 서버로부터 'stop checking' 메세지가 오면, send, recv 함수 둘 다 종료된다
        t_send = Thread(target=action_check_send, args=(sock,))
        t_send.start()
        action_check_recv(sock)

def action_check_recv(sock):
    global emergency

    while True:
        data = sock.recv(10)
        recv_pi_floor, recv_pi_num, message = decode_data(data)
        print("[DEBUG] %d층 %d번 수신 %s" %(recv_pi_floor, recv_pi_num, message))
        if message != 255:
            print("첫 수신 메시지 에러")
            return

        emergency = True
        queue.put('change emrgency complete')
        while emergency:
            data = sock.recv(10)
            recv_pi_floor, recv_pi_num, message = decode_data(data)
            print("[DEBUG] %d층 %d번 수신 %s" %(recv_pi_floor, recv_pi_num, message))
            
            if check_recv(recv_pi_floor, recv_pi_num):
                msg_interpreted = interpret_message(message)
                if type(msg_interpreted) is int:
                    show_direction(msg_interpreted)
                # 254는 상황 종료를 의미
                elif msg_interpreted == 'stop checking':
                    emergency = False
                    return
        
def encode_message(message):
    byte_message = (message).to_bytes(1, byteorder='big')
    print("[DEBUG] send this", PI_HEADER_BYTES + byte_message)
    return PI_HEADER_BYTES + byte_message

def decode_data(data):
    pi_floor = data[0]
    pi_num = data[1]
    message = data[2]
    return pi_floor, pi_num, message

# 데이터 배송지가 맞는지 확인
def check_recv(recv_pi_floor, recv_pi_num):
    if recv_pi_floor != PI_FLOOR or recv_pi_num != PI_NUM:
        print("[오류] : %s층 %s번 데이터 수신. 이 파이는 %s층 %s번" %(recv_pi_floor, recv_pi_num, PI_FLOOR, PI_NUM))
        return False
    return True

# 온도체크해서 안전하면 1, 위험하면 0 리턴
temp = 1
def check_safe():
    return temp

# 수신한 데이터로 방향 표시
def show_direction(direction):
    return 1

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
