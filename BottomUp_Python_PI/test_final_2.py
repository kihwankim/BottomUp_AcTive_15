########## HOW TO USE ###########
# in terminal : python3 this-file.py target-ip target-port
#     example) python3 test_final_2.py 168.188.127.74 8000

import socket
import time
import sys
from threading import Thread
from queue import Queue

PI_NUM = 0
PI_NUM_BYTE = 0
emergency = False
queue = Queue()

def action_send(sock):
    global emergency   ##### send, receive에서 같이 사용. 크리티컬 섹션?

    # 초기 : 0.5초 주기로 재난상황 발생 체크
    while check_safe() and not emergency:
        time.sleep(0.5)

    sock.send(encode_message(255))
    
    queue.get() # 65번줄 코드를 기다림 (생산자-소비자)
    # 재난상황 발생 : 0.1초 주기로 서버에 안전상태 송신
    while emergency:
        sock.send(encode_message(check_safe()))
        time.sleep(0.1)

    # yield   # for next?

def action_receive(sock):
    global emergency

    data = sock.recv(10)
    received_pi_num, message = decode_data(data)
    print("수신", received_pi_num, message)
    if message != 255:
        print("첫 수신 메시지 에러")
        return

    emergency = True
    queue.put('change emrgency complete')

    while emergency:
        data = (sock.recv(10))
        received_pi_num, message = decode_data(data)
        print("수신", received_pi_num, message)

        # 수신 데이터 오류
        if received_pi_num != PI_NUM:
            print("오류 : %s의 데이터 수신. 이 파이의 번호는 %s" %(pi, PI_NUM))
        # 254는 상황 종료를 의미
        elif message == 254:
            emergency = False
            break
        else:
            ##### 방향 의미할  message 데이터 검사?
            show_direction(message)
    
    # yield    # for next?
        
def encode_message(message):
    byte_message = (message).to_bytes(1, byteorder='big')
    print("send this", PI_NUM_BYTE + byte_message)
    return PI_NUM_BYTE + byte_message

def decode_data(data):
    pi_num = data[0]
    message = data[1]
    return pi_num, message

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

if __name__ == '__main__':
    PI_NUM = int(input("input pi number : "))
    PI_NUM_BYTE = (PI_NUM).to_bytes(1, byteorder='big')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((sys.argv[1], int(sys.argv[2])))
        sock.send(PI_NUM_BYTE)

        ### TEST ###
        #t_test = Thread(target=test_change_safety_status)
        #t_test.start()
        ############

        # t_receive 스레드는 수신 담당
        t_receive = Thread(target=action_receive, args=(sock,))
        t_receive.start()

        # 메인 스레드는 송신 담당
        action_send(sock)

    finally:
        sock.close()
