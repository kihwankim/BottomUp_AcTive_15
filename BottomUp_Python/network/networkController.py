from threading import Thread
from queue import Queue
import socket
import time

from network.receive.Receiver import Receiver
from network.send.SendManager import SendManager
from network.send.Sender import Sender

class NetworkController:
    def __init__(self, pi_datas, max_height, ip, port):
        self.ip = ip
        self.port = port
        self.capacity = 0 # 정점(파이) 수용량
        for floor in pi_datas:
            self.capacity += len(floor)

        # 각 층별로, 파이가 안전한지 나타냄. 값의 의미는 (-1:미연결, 0:위험, 1:안전)
        # [0] = 사용 X
        # [1] = {1:1, 2:0, 3:-1, 7:0}    : 1층. 1번 안전, 2번 위험, 3번 미연결, 7번 위험 
        # [2] = {1:1, 4:0}         : 2층. 1번 안전, 4번 위험
        self.safe_status = [0]*(max_height+1)   # 각 파이별로 안전한지 나타냄.  [1]=1 : 1번 파이 safe,  [2]=0 : 2번 파이 unsafe

        # 송신을 담당할 객체 생성
        self.SendManager = SendManager(max_height)
        
        # 초기화
        for height in range(1, max_height+1):
            self.safe_status[height] = {int(pi.piNumber):-1 for pi in pi_datas[height-1]}

        self.size_connection = 0

         # 작업 Queue.
         # 큐에서 아이템을 꺼낼 때, 비어있으면 꺼낼때까지 그대로 멈춘다. 이 특성을 이용해 작업 순서 조율
        self.q_from_Receiver = Queue()

    def get_safe_status(self):
        return self.safe_status

    # 객체 정보 리셋
    def reset(self, pi_datas, max_height):
        del self.safe_status

        self.capacity = 0 # 정점(파이) 수용량
        for floor in pi_datas:
            self.capacity += len(floor)

        self.safe_status = [0]*(max_height+1)
        for height in range(1, max_height+1):
            self.safe_status[height] = {int(pi.piNumber):-1 for pi in pi_datas[height-1]}

        self.size_connection = 0
        self.q_from_Receiver.queue.clear()
        self.SendManager.reset_senders_list(max_height)


    def wait_emergency(self):
        while True:
            if self.q_from_Receiver.get() == 'emergency':
                break

#-----------------------------------#
    def start_accpet(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(0)

        try:
            while True:
                # 새로운 클라이언트와 연결
                client_socket, addr = self.server_socket.accept()
                
                t_judge_accpet = Thread(target=self.__judge_connect, args=(client_socket, addr))
                # 데몬 True : 부모 스레드가 종료되면 자신도 종료
                t_judge_accpet.daemon = True
                t_judge_accpet.start()
        except OSError:
            print("server stopped")



    def stop_accept(self):
        self.server_socket.close()
        del self.server_socket

    def start_checking(self):
        self.SendManager.send_All_start_checking()

    def stop_checking(self):
        self.SendManager.send_All_stop_checking()
        self.q_from_Receiver.queue.clear()

    def start_emergency(self):
        self.SendManager.send_All_start_emergency()

    def __judge_connect(self, client_socket, addr):
        try:
            self.size_connection += 1
            print(addr, "연결 시도")
            pi_floor, pi_num = self.__judge_connect_piNum(client_socket)
            
            print("%s 접속 허가, %d층 %d번" %(addr, pi_floor, pi_num))
            self.print_all_seat()
                    
            # 클라이언트에게서 수신할 객체, 클라이언트에게 송신할 객체 생성
            new_sender = Sender(client_socket, pi_floor, pi_num)
            new_receiver = Receiver(client_socket, pi_floor, pi_num, self.safe_status, self.q_from_Receiver)

            # 송신, 수신
            self.SendManager.add_sender(new_sender)
            message_return = new_receiver.run()
            
            # 연결 끊킨 파이 제거
            if message_return == 'delete this connection':
                self.__delete_disconnected_client(client_socket, pi_floor, pi_num)
                del new_sender
                del new_receiver
        except ConnectionError:
            client_socket.close()
            print(addr, "연결 종료. 소켓 close")
        else:
            print("%d층 %d번 파이 연결 끊킴. 파손 예상" %(pi_floor, pi_num))
        finally:
            self.size_connection -= 1

    def __judge_connect_piNum(self, sock):
        while True:
            if self.capacity == self.size_connection:
                sock.send('[!!!] No extra seat'.encode())
                print("자리 부족. 접속 거부.")
                raise ConnectionError
            try:
                sock.send(self.__string_extra_seat().encode())
                data_received = int.from_bytes(sock.recv(3), byteorder='big')
                if data_received==0:
                    raise ConnectionError
                pi_floor = data_received//256
                pi_num = data_received%256

                if self.safe_status[pi_floor][pi_num] !=-1:
                    raise IndexError
                
                self.safe_status[pi_floor][pi_num]=1
                sock.send(('connect accept').encode())
                return pi_floor, pi_num
            except TypeError:
                pass
            except IndexError:
                pass
            except KeyError:
                pass
            print("%s의 번호 요청 (%s층 %s번) 할당 불가. 접속 거부" %(sock.getpeername(), pi_floor, pi_num))
  
    def send_All_path(self, list_path):
        self.SendManager.send_All_path(list_path)

    # 건물의 모든 파이 자리. 접속 가능여부 출력
    def print_all_seat(self):
        ret = str()
        for height, pi_dict in enumerate(self.safe_status):
            if height==0:
                continue
            pi_seat_OX = dict()
            for pi in pi_dict:
                if pi_dict[pi] == -1:
                    pi_seat_OX[pi] = 'O'
                else:
                    pi_seat_OX[pi] = 'X'
            ret += ("%s층 : %s\n" %(height, pi_seat_OX))
        print("현재 파이 접속 가능 여부('O':접속가능, 'X':접속불가)")
        print(ret)

    # 현재 건물의 남는 파이 자리를 문자열로 리턴
    def __string_extra_seat(self):
        ret = str()
        for height, pi_dict in enumerate(self.safe_status):
            if height==0:
                continue
            height_remain_pi = [key for ix, key in enumerate(pi_dict) if pi_dict[key]==-1]
            ret += ("%s층 : %s\n" %(height, height_remain_pi))
        return ret     

    # 연결 끊킨 파이 처리
    def __delete_disconnected_client(self, client_socket, floor, pi_num):
        try:
            # 소켓 close
            client_socket.close()
            # 미연결 상태로 변환
            self.safe_status[floor][pi_num] = -1
            # Sender 제거
            self.SendManager.delete_sender(floor, pi_num)
            # 소켓 제거
            del client_socket
        except NameError:
            #print("[delete_disconnected_socket] 이미 삭제된 객체")
            pass

    # query(질문)에 대한 관리자의 YES 입력 대기
    def __wait_YES_with_query(self, query):
        while True:
            try:
                order = input(str(query)+"? (YES or NO) :")
                if order == 'YES':
                    return 'YES'
            except ValueError:
                print("[입력 에러]")
                pass