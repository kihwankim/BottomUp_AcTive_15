import socket
from time import *
import sys
from threading import Thread
from queue import Queue
from sensor.LCD_I2C.lcd_I2C import * # LCD
from sensor.Temperature_Check_DHT11.temp_Check import *
import signal

# how to use
# in terminal : python3 this-file.py target-ip target-port
#      example) python3 test_final_3_add_floor.py 168.188.127.74 8000

PI_FLOOR = 0
PI_FLOOR_BYTE = 0
PI_NUM = 0
PI_NUM_BYTE = 0

PI_HEADER_BYTES = 0

RECV_SIZE = 20

emergency = False
queue = Queue()

def check_safe():
    value = check_Temperature()
    print("check temperature", value)
    return value

def show_message(message):
    lcd_Display_Write_String(message)

def lcd_show_stair(message):
    print("[DEBUG] lcd show stair", message)
    lcd_Display_Write_Stair(message)

def lcd_show_notstair(message):
    print("[DEBUG] lcd show not stair", message)
    lcd_Display_Write_Direction(message)

def lcd_show_pi_num():
    showing_message = "Floor  : " + ("%03d"%PI_FLOOR) + "    "
    showing_message += "Number : " + ("%03d"%PI_NUM) + "    "
    show_message(showing_message) 

def lcd_show_monitoring():
    show_message("   monitoring      danger...")

def sigint_handler(signal, frame):
    show_message("    WARNING!     GO OTHER WAY!!")
    sys.exit(0)

def check_recv(recv_pi_floor, recv_pi_num):
    if recv_pi_floor != PI_FLOOR or recv_pi_num != PI_NUM:
        return False
    return True
    
def encode_message(message):
    byte_message = (message).to_bytes(1, byteorder='big')
    print("[DEBUG] send this", PI_HEADER_BYTES + byte_message)
    return PI_HEADER_BYTES + byte_message

def decode_data(data):
    print("lets decode", data)
    if data == b'':
        return 0, 0, 1
    pi_floor = data[0]
    pi_num = data[1]
    if len(data)==3:
        message = data[2]
    else:
        message = [int.from_bytes(data[x:x+2], byteorder='big') for x in range(2, len(data), 2)]

    print("[DEBUG] decoded message is", type(message), message)
    return pi_floor, pi_num, message

def interpret_message(message):
    if type(message) == list:
        if len(message)==4:
            return 'msg for stair'
        if len(message)==8:
            return 'msg for non-stair'
    if message == 253:
        return 'start checking'
    if message == 254:
        return 'stop checking'
    if message == 255:
        return 'emergency'
    print("[DEBUG] can't interpret message", type(message), message)
    return 'cant interpret'

def start_recv(sock):
    global emergency

    while True:
        data = sock.recv(RECV_SIZE)
        recv_pi_floor, recv_pi_num, message = decode_data(data)
        print("[DEBUG] %d floor, %d number pi recv %s" %(recv_pi_floor, recv_pi_num, message))
        msg_interpreted = interpret_message(message)
        if msg_interpreted == 'stop checking':
            queue.put('stop checking')
            return

        if msg_interpreted != 'emergency':
            print("first recv message error")
            continue

        emergency = True
        queue.put('change emrgency complete')
        while emergency:
            data = sock.recv(RECV_SIZE)
            recv_pi_floor, recv_pi_num, message = decode_data(data)
            print("[DEBUG] %d floor, %d number pi recv %s" % (recv_pi_floor, recv_pi_num, message))
            print(message)
            if check_recv(recv_pi_floor, recv_pi_num):
                msg_interpreted = interpret_message(message)
                if msg_interpreted == 'msg for stair':
                    lcd_show_stair(message)
                elif msg_interpreted == 'msg for non-stair':
                    lcd_show_notstair(message)
                elif msg_interpreted == 'stop checking':
                    emergency = False
                    return

def start_send(sock):
    global emergency

    try:
        while check_safe() and not emergency:
            try:
                current_status = queue.get_nowait()
                print('send get from queue :', current_status) 
                if current_status == 'stop checking':
                    return
                elif current_status == 'change emrgency complete':
                    queue.put('change emrgency complete')
            except Exception:
                pass
            finally:
                sleep(0.5)

        sock.send(encode_message(255))

        queue.get()  # 'change emergency complete'

        while emergency:
            if not check_safe():
                sock.send(encode_message(False))
            sleep(1)
    except Exception:
        pass
    finally:
        sock.send(encode_message((254)))

def start_check(sock):
    t_send = Thread(target=start_send, args=(sock,))
    t_send.daemon = True
    t_send.start()
    start_recv(sock)

def wait_order(sock):
    while True:
        lcd_show_pi_num()
        _, _, message = decode_data(sock.recv(RECV_SIZE))
        print(sock.gettimeout())
        if message == 1:
            continue
        print(message, interpret_message(message)) # for debug
        if interpret_message(message) != 'start checking':
            continue

        lcd_show_monitoring()
        start_check(sock)

def response_IamAlive(server_ip):
    response_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    response_sock.bind(('', 10001))

    _, server_addr = response_sock.recvfrom(5)

    while True:
        response_sock.sendto(' '.encode(), server_addr)
        response_sock.recv(5)
    

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
        try:
            pi_floor = int(input("choose your pi floor :"))
            pi_num = int(input("choose your pi number :"))

            pi_floor_byte = (pi_floor).to_bytes(1, byteorder='big')
            pi_num_byte = (pi_num).to_bytes(1, byteorder='big')
        except Exception:
            sock.send((1).to_bytes(1, byteorder='big')+(255).to_bytes(1, byteorder='big'))
        else:
            sock.send(pi_floor_byte+pi_num_byte)

    sock.close()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_ip = sys.argv[1]
        server_port = int(sys.argv[2])
        sock.connect((server_ip, server_port))
        
        t_response = Thread(target=response_IamAlive, args=(server_ip,))
        t_response.daemon = True
        t_response.start()

        PI_FLOOR, PI_FLOOR_BYTE, PI_NUM, PI_NUM_BYTE = try_connect(sock)
        PI_HEADER_BYTES = PI_FLOOR_BYTE + PI_NUM_BYTE

        print("connect success, %d층 %d번." %(PI_FLOOR, PI_NUM))

        wait_order(sock)

    finally:
        sock.close()
