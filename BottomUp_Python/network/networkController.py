from threading import Thread
from queue import Queue
import socket
import time

from network.receive import ReceiverSocket
from network.send import SenderSocket

class NetworkController:
    def __init__(self, tables, ip, port):
        self.capacity = len(tables) # 정점(파이) 수용량
        self.safes = [0]*(self.capacity+1)   # 각 파이별로 안전한지 나타냄.  [1]=1 : 1번 파이 safe,  [2]=0 : 2번 파이 unsafe
        self.safes[0] = -1 # [0]은 사용 X

        self.size_connection = 0
        
        # 서버 소켓 설정
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((ip, port))
        self.server_socket.listen(0)

        self.senders = dict() # 연결한 송신 소켓 리스트

         # 작업 Queue.
         # 큐에서 아이템을 꺼낼 때, 비어있으면 꺼낼때까지 그대로 멈춘다. 이 특성을 이용해 작업 순서 조율
        self.queue = Queue()

    def get_safes(self):
        return self.safes

    def get_queue_item(self):
        return self.queue.get()

    def put_queue(self, data):
        self.queue.put(data)

    # 서버의 통신 시작
    def run_server(self):
        # 클라이언트의 접속을 계속해서 처리할 스레드
        self.t_server = Thread(target=self.accept_connect)
        self.t_server.start()
        self.wait_status_emergency()

    # 클라이언트들에게 송신 시작
    def run_send(self):
        # 클라이언트들에게 송신을 담당할 스레드(오직 하나)
        self.t_action_send = Thread(target=self.action_send)
        self.t_action_send.start()

    # 재난상황 발생 대기 
    def wait_status_emergency(self):
        if self.queue.get()==('emergency'):
            self.run_send()
        else:
            print("wait_status_emergency() else문")

    # 재난상황 종료
    def stop_status_emergency(self):
        print('ww')
        self.wait_status_emergency()


    # 클라이언트의 접속을 무한히 처리. 클라이언트 연결시, 해당 클라이언트에게서 주기적으로 수신하는 스레드 생성
    def accept_connect(self):
        while True:
            # 새로운 클라이언트와 연결
            client_socket, addr = self.server_socket.accept()
            
            t_judge_accpet = Thread(target=self.judge_connect, args=(client_socket, addr))
            # 부모가 종료되면 데몬스레드도 모두 종료(self.t_server 스레드가 종료되면, 수신 스레드도 모두 종료)
            t_judge_accpet.daemon = True
            t_judge_accpet.start()

    def judge_connect(self, client_socket, addr):
        try:
            print(addr, "연결 시도")
            pi_num = self.match_piNum(client_socket)
            
            self.size_connection += 1

            print(addr, "접속, 파이번호 :",pi_num)
            print("현재 접속 상태 :", list(ix if status!=0 else 0 for ix, status in enumerate(self.safes)))
                    
            # 클라이언트에게서 수신할 객체, 클라이언트에게 송신할 객체 생성
            new_sender = SenderSocket(client_socket, pi_num)
            self.senders[pi_num] = new_sender

            # 주기적으로 수신 시작
            self.action_receive(ReceiverSocket(client_socket, pi_num))
        except ConnectionError:
            client_socket.close()
            print(addr, "연결 종료. 소켓 close")

    def match_piNum(self, sock):
        while True:
            if self.capacity == self.size_connection:
                sock.send('[!!!] No extra seat'.encode())
                print("자리 부족. 접속 거부.")
                raise ConnectionError

            status_connect = list(ix if status==0 else 0 for ix, status in enumerate(self.safes))
            try:
                sock.send(str(status_connect).encode())
                pi_num = int.from_bytes(sock.recv(1), byteorder='big')
                
                if self.safes[pi_num]!=0:
                    raise IndexError
                
                self.safes[pi_num]=1
                sock.send(('connect accept').encode())
                return pi_num
            except IndexError:
                print(str(sock.getpeername())+"의 번호 요청", pi_num, ": 할당 불가. 접속 거부")



    # 주기적으로 수신받아서 self.safes 업데이트 (파이 하나당 스레드 하나로 사용)
    def action_receive(self, ReceiverSock):
        try:
            while True:
                # 첫 수신 처리
                pi_num, message = ReceiverSock.receive_data()
                print("첫 수신",pi_num,message) # debug
                # 큐에 아이템을 넣어, 메인 컨트롤러에서 emergency 상황을 인지하도록 함
                if message=='emergency':
                    self.queue.put('emergency')
                # emergency 상황을 인지한 파이는, 서버에게 [파이번호, safe or unsafe] 데이터를 계속해서 송신
                elif message=='pi num error':
                    print("[수신 에러. PI NUM 오류] 소켓 PI번호:%d, 수신받은 PI번호:%d" %(pi_num, ReceiverSock.get_pi_num()))
                else:
                    self.safes[pi_num] = message

                # 두 번째 수신부터 반복
                while True:
                    time.sleep(0.1)
                    pi_num, message = ReceiverSock.receive_data()
                    
                    if message == 'stop emergency':
                        break
                    #print("수신",pi_num,message) # debug
                    self.safes[pi_num] = message
        except IndexError:
            #print("[수신 에러] Index Error")
            pass
        except OSError:
            pass
            #print("[수신 에러] OS Error")
        finally:
            # 실행도중 연결 끊킨 파이 처리
            #print("%d번 파이 수신 소켓 제거" %(pi_num))
            self.delete_disconnected_socket(ReceiverSock)
            return
            
    
    # 각각의 파이에게 송신을 반복. (스레드 하나가 사용) 
    def action_send(self):
        # 각각의 파이에게 255를 보내서 emergency 상황임을 알림
        while True:
            try:
                for SenderSock in self.senders.values():
                    SenderSock.send_data(255)
                break
            except OSError:
                    #print("%d번 파이 송신 소켓 제거" %(SenderSock.get_pi_num()))
                    self.delete_disconnected_socket(SenderSock)
        

        ### TEST ###
        t = Thread(target=self.test_put_queue)
        t.start()
        ############
        
        while True:
            try:
                list_path = self.queue.get()
                if list_path == 'emergency':
                    continue
                if list_path == 'stop emergency':
                    break
                for path in list_path:
                    # path[0] : 파이 번호, path[1] : 가리킬 방향(숫자 0~254로 표시)
                    # 해당 번호의 파이에게 가리킬 방향을 송신
                    self.senders[path[0]].send_data(path[1])
            except KeyError as e:
                print("[송신 에러] 존재하지 않는 파이(%s)에게 송신시도\n" %(str(e)))
            except OSError:
                print("[송신 예외처리][action_send] 닫힌 소켓에게 송신 시도")
            except OverflowError:
                print("[송신 예외처리] 1바이트(0~255) 범위 메세지만 송신 가능")
        
    # 실행도중 연결 끊킨 파이 처리
    def delete_disconnected_socket(self, Sock):
        try:
            pi_number = Sock.get_pi_num()
            print("%d번 파이 연결 끊킴. 파손 예상" %(pi_number))

            # 소켓 close : Receiver, Sender는 같은 소켓 사용하니 둘다 close됨
            Sock.close()
            # 객체 삭제
            del Sock
            
            # 딕셔너리에서 송신 키 삭제, 미연결로 바꿈
            del self.senders[pi_number]
            self.safes[pi_number] = 0
        except NameError:
            #print("[delete_disconnected_socket] 이미 삭제된 객체")
            pass
        except KeyError:
            #print("[delete_disconnected_socket] dictionary에서 이미 삭제")
            pass
        else:
            self.size_connection -= 1
            
        



    ### TEST ###
    def test_put_queue(self):
        while True:
            try:
                test_data_pi = int(input("송신 입력(파이 번호) : "))
                test_data_message = int(input("송신 입력(메세지) : "))
                self.queue.put([[test_data_pi, test_data_message]])
            except ValueError:
                print("[입력 오류][test_put_queue]")

    def test_run_server(self):
        self.t_server = Thread(target=self.test_accept_connect)
        self.t_server.start()
        self.test_action_send()

    def test_accept_connect(self):
        while True:
            # 새로운 클라이언트와 연결
            client_socket, addr = self.server_socket.accept()

            # 클라이언트에게서 수신할 객체, 클라이언트에게 송신할 객체 생성
            new_receiver = ReceiverSocket(client_socket, addr)
            new_sender = SenderSocket(client_socket, addr)


            # 주기적으로 수신 시작
            t_receive = Thread(target=self.test_action_receive, args=(new_receiver,))
            t_receive.daemon = True # 부모가 종료되면 데몬스레드도 모두 종료(self.t_server 스레드가 종료되면, 수신 스레드도 모두 종료)
            t_receive.start()

            #self.senders.append(new_sender)

    def test_action_receive(self, ReceiverSocket):
        # 수신할때마다 if문 체크를 피하기 위해서, while문을 두 개로 분리
        count = 0
        while True:
            data = ReceiverSocket.receive_data()
            if data == '':
                ReceiverSocket.close()
                break
            print(ReceiverSocket.get_addr(), data)
            
    def test_action_send(self):
        while True:
            text = input("입력 : ")
            for SenderSocket in self.senders:
                SenderSocket.send_data(text)
