from threading import Thread
from queue import Queue
import socket
import time

from network.receive import ReceiverSocket
from network.send import SenderSocket

class NetworkController:
    def __init__(self, pi_datas, building_height, ip, port):
        self.capacity = len(pi_datas) # 정점(파이) 수용량

        # 각 층별로, 파이가 안전한지 나타냄.
        # [0] = 사용 X
        # [1] = {1:1, 2:0, 7:0}    : 1층. 1번 안전, 2번 위험, 7번 위험 
        # [2] = {1:1, 4:0}         : 2층. 1번 안전, 4번 위험
        self.safes_height = [0]* (building_height+1)   # 각 파이별로 안전한지 나타냄.  [1]=1 : 1번 파이 safe,  [2]=0 : 2번 파이 unsafe
        
        # 층별 연결한 송신 소켓 리스트
        self.senders_height = [0]* (building_height+1)
        
        # 초기화
        for height in range(1, building_height+1):
            self.safes_height[height] = {int(x.piNumber):0 for x in pi_datas if x.height==height}
            self.senders_height[height] = {}

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
        #self.t_server.join()

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
            print(addr, "연결 시도")
            pi_floor, pi_num = self.judge_connect_piNum(client_socket)
            
            self.size_connection += 1
            print("%s 접속, %d층 %d번 :" %(addr, pi_floor, pi_num))
            print("현재 접속 상태 \n"+self.string_status_building())
                    
            # 클라이언트에게서 수신할 객체, 클라이언트에게 송신할 객체 생성
            new_sender = SenderSocket(client_socket, pi_floor, pi_num)
            self.senders_height[pi_floor][pi_num] = new_sender

            # 주기적으로 수신 시작
            self.action_receive(ReceiverSocket(client_socket, pi_floor, pi_num))
        except ConnectionError:
            client_socket.close()
            print(addr, "연결 종료. 소켓 close")

    def judge_connect_piNum(self, sock):
        while True:
            if self.capacity == self.size_connection:
                sock.send('[!!!] No extra seat'.encode())
                print("자리 부족. 접속 거부.")
                raise ConnectionError

            try:
                sock.send(self.string_status_building().encode())
                data_received = int.from_bytes(sock.recv(3), byteorder='big')
                pi_floor = data_received//256
                pi_num = data_received%256

                if self.safes_height[pi_floor][pi_num] !=0:
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
    
    # 현재 빌딩의 파이 상태를 문자열로 리턴
    def string_status_building(self):
        ret = str()
        for height, pi_dict in enumerate(self.safes_height):
            if height==0:
                continue
            height_remain_pi = [key for ix, key in enumerate(pi_dict) if pi_dict[key]==0]
            ret += ("%s층 : %s\n" %(height, height_remain_pi))
        return ret

    # 주기적으로 수신받아서 self.safes 업데이트 (파이 하나당 스레드 하나로 사용)
    def action_receive(self, ReceiverSock):
        try:
            while True:
                # 첫 수신 처리
                pi_floor, pi_num, message = ReceiverSock.receive_data()
                print("첫 수신. %d층 %d번 : %s" %(pi_floor,pi_num,message)) # debug
                # 큐에 아이템을 넣어, 메인 컨트롤러에서 emergency 상황을 인지하도록 함
                if message=='emergency':
                    self.queue.put('emergency')
                # emergency 상황을 인지한 파이는, 서버에게 [파이번호, safe or unsafe] 데이터를 계속해서 송신
                elif message=='pi receive error':
                    print("[수신 에러. PI floor 또는 num 오류]")
                else:
                    self.safes_height[pi_floor][pi_num] = message

                # 두 번째 수신부터 반복
                while True:
                    time.sleep(0.1)
                    pi_floor, pi_num, message = ReceiverSock.receive_data()
                    if message == 'stop emergency':
                        break
                    #print("수신",pi_num,message) # debug
                    self.safes_height[pi_floor][pi_num] = message
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
            
    
    # 상황발생시, 파이에게 송신하는 함수. (스레드 하나가 사용) 
    def action_send_emergency(self):
        # 각각의 파이에게 255를 보내서 emergency 상황임을 알림
        self.send_All_start_emergency()

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
                    self.send_message(path[0], path[1], path[2])
            except KeyError as e:
                print("[송신 에러] 존재하지 않는 파이(%s)에게 송신시도\n" %(str(e)))
            except OSError:
                print("[송신 예외처리][action_send] 닫힌 소켓에게 송신 시도")
            except OverflowError:
                print("[송신 예외처리] 1바이트(0~255) 범위 메세지만 송신 가능")

        # 모두에게 '상황종료' 송신
        self.send_All_stop_checking()

        # 관리자 입력 대기
        self.wait_YES_with_query("상황체크 재시작?")

        # 모두에게 '상황체크 시작' 송신
        self.send_All_start_checking()
    
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

    # 한 파이에게 메세지 송신
    def send_message(self, floor, number, message):
        self.senders_height[floor][number].send_data(message)

    # 연결된 모든 파이에게 메세지 송신
    def send_All(self, message):
        disconnected_list = []
        for floor, dict_senders in enumerate(self.senders_height, 0):
            if floor == 0:
                continue
            for SenderSock in dict_senders.values():
                try:
                    SenderSock.send_data(message)
                except OSError:
                    disconnected_list.append(SenderSock)

        # 끊킨 파이는 삭제
        for SenderSock in disconnected_list:
            self.delete_disconnected_socket(SenderSock)

    # 연결된 모든 파이에게 '상황체크 시작' 송신
    def send_All_start_checking(self):
        self.send_All(253)
    
    # 연결된 모든 파이에게 '상황체크 종료' 송신
    def send_All_stop_checking(self):
        self.send_All(254)

    # 연결된 모든 파이에게 '상황시작' 송신
    def send_All_start_emergency(self):
        self.send_All(255) 
        
    # 실행도중 연결 끊킨 파이 처리
    def delete_disconnected_socket(self, Sock):
        try:
            pi_floor, pi_number = Sock.get_pi_info()
            print("%d층 %d번 파이 연결 끊킴. 파손 예상" %(pi_floor, pi_number))

            # 소켓 close : Receiver, Sender는 같은 소켓 사용하니 둘다 close됨
            Sock.close()
            # 객체 삭제
            del Sock
            
            # 딕셔너리에서 송신 키 삭제, 미연결로 바꿈
            del self.senders_height[pi_floor][pi_number]
            self.safes_height[pi_floor][pi_number] = 0
        except NameError:
            #print("[delete_disconnected_socket] 이미 삭제된 객체")
            pass
        except KeyError:
            #print("[delete_disconnected_socket] dictionary에서 이미 삭제")
            pass
        else:
            self.size_connection -= 1