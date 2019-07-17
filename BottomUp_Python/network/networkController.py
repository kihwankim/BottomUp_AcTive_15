from threading import Thread
from queue import Queue
import socket
import time

from network.receive.Receiver import Receiver
from network.send.SendManager import SendManager
from network.send.Sender import Sender

class NetworkController:
    def __init__(self, pi_datas, building_height, ip, port):
        self.capacity = len(pi_datas) # 정점(파이) 수용량

        # 각 층별로, 파이가 안전한지 나타냄. 값의 의미는 (-1:미연결, 0:위험, 1:안전)
        # [0] = 사용 X
        # [1] = {1:1, 2:0, 3:-1, 7:0}    : 1층. 1번 안전, 2번 위험, 3번 미연결, 7번 위험 
        # [2] = {1:1, 4:0}         : 2층. 1번 안전, 4번 위험
        self.safes_height = [0]* (building_height+1)   # 각 파이별로 안전한지 나타냄.  [1]=1 : 1번 파이 safe,  [2]=0 : 2번 파이 unsafe

        # 송신을 담당할 객체 생성
        self.SendManager = SendManager(building_height)
        
        # 초기화
        for height in range(1, building_height+1):
            self.safes_height[height] = {int(x.piNumber):-1 for x in pi_datas if x.height==height}

        self.size_connection = 0
        
        # 서버 소켓 설정
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((ip, port))
        self.server_socket.listen(0)

         # 작업 Queue.
         # 큐에서 아이템을 꺼낼 때, 비어있으면 꺼낼때까지 그대로 멈춘다. 이 특성을 이용해 작업 순서 조율
        self.queue = Queue()

    def get_safes_height(self):
        return self.safes_height

    def get_queue_item(self):
        return self.queue.get()

    def put_queue(self, data):
        self.queue.put(data)

    # 서버의 통신 시작
    def run_server(self):
        # 접속요청 처리를 담당할 스레드
        self.t_server = Thread(target=self.accept_connect)
        self.t_server.daemon = True
        self.t_server.start()

        # 연결된 클라이언트들에게 송신을 담당할 스레드
        self.t_run_send = Thread(target=self.run_send_while_emergency)
        self.t_run_send.daemon = True
        self.t_run_send.start()
        
        #####
        self.t_server.join()

    def run_send_while_emergency(self):
        while True:
            # 재난상황 발생시 송신 시작
            if self.queue.get()==('emergency'):
                # 관리자에 의한 상황종료를 담당할 스레드
                t_stop = Thread(target=self.stop_emergency_by_admin)
                t_stop.start()
                self.action_send_emergency()
            else:
                print("run_send_while_emergency() else문")
    
    # 상황종료는 관리자가 판단
    def stop_emergency_by_admin(self):
        self.wait_YES_with_query("Stop Emergency?")

        # 송신스레드가 상황종료를 알아차리도록, 큐로 전달
        self.queue.put('stop emergency')

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
            self.size_connection += 1
            print(addr, "연결 시도")
            pi_floor, pi_num = self.judge_connect_piNum(client_socket)
            
            print("%s 접속, %d층 %d번 :" %(addr, pi_floor, pi_num))
            print("현재 접속 상태 \n"+self.string_extra_seat())
                    
            # 클라이언트에게서 수신할 객체, 클라이언트에게 송신할 객체 생성
            new_sender = Sender(client_socket, pi_floor, pi_num)
            new_receiver = Receiver(client_socket, pi_floor, pi_num, self.safes_height, self.queue)

            # 송신, 수신
            self.SendManager.add_sender(new_sender)
            message_return = new_receiver.action_receive()
            
            # 연결 끊킨 파이 제거
            if message_return == 'delete this connection':
                self.delete_disconnected_client(client_socket, pi_floor, pi_num)
                del new_sender
                del new_receiver
        except ConnectionError:
            client_socket.close()
            print(addr, "연결 종료. 소켓 close")
        else:
            print("%d층 %d번 파이 연결 끊킴. 파손 예상" %(pi_floor, pi_num))
        finally:
            self.size_connection -= 1

    def judge_connect_piNum(self, sock):
        while True:
            if self.capacity == self.size_connection:
                sock.send('[!!!] No extra seat'.encode())
                print("자리 부족. 접속 거부.")
                raise ConnectionError
            try:
                sock.send(self.string_extra_seat().encode())
                data_received = int.from_bytes(sock.recv(3), byteorder='big')
                pi_floor = data_received//256
                pi_num = data_received%256

                if self.safes_height[pi_floor][pi_num] !=-1:
                    raise IndexError
                
                self.safes_height[pi_floor][pi_num]=1
                sock.send(('connect accept').encode())
                return pi_floor, pi_num
            except TypeError:
                pass
            except IndexError:
                pass
            except KeyError:
                pass
            finally:
                print("%s의 번호 요청. %s층 %s번 할당 불가. 접속 거부" %(sock.getpeername(), pi_floor, pi_num))
    
    # 현재 빌딩의 남는 파이 자리를 문자열로 리턴
    def string_extra_seat(self):
        ret = str()
        for height, pi_dict in enumerate(self.safes_height):
            if height==0:
                continue
            height_remain_pi = [key for ix, key in enumerate(pi_dict) if pi_dict[key]==-1]
            ret += ("%s층 : %s\n" %(height, height_remain_pi))
        return ret     
    
    # 상황발생시, 파이에게 송신하는 함수. (스레드 하나가 사용) 
    def action_send_emergency(self):
        # 각각의 파이에게 255를 보내서 emergency 상황임을 알림
        self.SendManager.send_All_start_emergency()

        ### TEST ###
        #t = Thread(target=self.test_put_queue)
        #t.start()
        ############
        
        while True:
            try:
                list_path = self.queue.get()
                if list_path == 'emergency':
                    continue
                if list_path == 'stop emergency':
                    break
                for path in list_path:
                    # path[0]:층, path[0]:파이 번호, path[1]:가리킬 방향(숫자 0~100로 표시)
                    # 해당 번호의 파이에게 가리킬 방향을 송신
                    self.SendManager.send_message(path[0], path[1], path[2])
            except KeyError as e:
                print("[송신 에러] 존재하지 않는 파이(%s)에게 송신시도\n" %(str(e)))
            except OSError:
                print("[송신 예외처리][action_send] 닫힌 소켓에게 송신 시도")
            except OverflowError:
                print("[송신 예외처리] 1바이트(0~255) 범위 메세지만 송신 가능")

        # 모두에게 '상황종료' 송신
        self.SendManager.send_All_stop_checking()

        # 관리자 입력 대기
        self.wait_YES_with_query("상황체크 재시작?")

        # 모두에게 '상황체크 시작' 송신
        self.SendManager.send_All_start_checking()
    
    # query(질문)에 대한 관리자의 YES 입력 대기
    def wait_YES_with_query(self, query):
        while True:
            try:
                order = input(str(query)+"? (YES or NO) :")
                if order == 'YES':
                    return 'YES'
            except ValueError:
                print("[입력 에러]")
                pass
    
    # 실행도중 연결 끊킨 파이 처리
    def delete_disconnected_client(self, client_socket, floor, pi_num):
        try:
            # 소켓 close
            client_socket.close()
            # 미연결 상태로 변환
            self.safes_height[floor][pi_num] = -1
            # Sender 제거
            self.SendManager.delete_sender(floor, pi_num)
            # 소켓 제거
            del client_socket
        except NameError:
            #print("[delete_disconnected_socket] 이미 삭제된 객체")
            pass