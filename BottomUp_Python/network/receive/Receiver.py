import time
class Receiver:
    def __init__(self, socket, floor, pi_num, status_safes, q_to_Main):
        self.socket = socket
        self.floor = floor
        self.pi_num = pi_num

        # 네트워크컨트롤러, 모든 Receiver가 공유
        self.status_safes = status_safes # 주소 복사
        self.q_to_Main = q_to_Main # 주소 복사

    def get_pi_info(self):
        return self.floor, self.pi_num
    
    def receive_data(self):
        data = self.socket.recv(10)
        if data == b'':
            raise ConnectionError
        received_floor = data[0]
        received_pi_num = data[1]
        message = data[2]
        print("received :", received_floor, received_pi_num, message)
        if received_floor != self.floor or received_pi_num != self.pi_num:
            return -1, -1, 'pi receive error'
        elif message < 254:
            return self.floor, self.pi_num, message
        elif message == 254:
            return self.floor, self.pi_num, 'stop checking'
        elif message == 255:
            return self.floor, self.pi_num, 'emergency'
        raise ConnectionError
    
    def close(self):
        self.socket.close()

    # 주기적으로 수신받아서 self.safes 업데이트 (파이 하나당 스레드 하나로 사용)
    def run(self):
        try:
            while True:
                # 첫 수신 처리
                pi_floor, pi_num, message = self.receive_data()
                print("첫 수신. %d층 %d번 : %s" %(pi_floor,pi_num,message)) # debug
                # 큐에 아이템을 넣어, 메인 컨트롤러에서 emergency 상황을 인지하도록 함
                if message =='emergency':
                    self.q_to_Main.put('emergency')
                # emergency 상황을 인지한 파이는, 서버에게 [파이번호, safe or unsafe] 데이터를 계속해서 송신
                elif message =='stop checking':
                    continue
                elif message =='pi receive error':
                    print("[수신 에러. PI floor 또는 num 오류]")
                else:
                    self.status_safes[pi_floor][pi_num] = message

                # 두 번째 수신부터 반복
                while True:
                    time.sleep(0.1)
                    pi_floor, pi_num, message = self.receive_data()
                    if message == 0:  # 부서지면 연결을 끊게한다
                        raise OSError
                    elif message == 'stop checking':
                        break
                    #print("수신",pi_num,message) # debug
                    self.status_safes[pi_floor][pi_num] = message
        except IndexError:
            pass
        except OSError:
            pass
        finally:
            self.q_to_Main.put('emergency')
            return 'delete this connection'

    ##### '' 맞는지 확인필요 #####
    # 연결이 끊겼는지 확인하는 함수
    # 연결이 끊키면 소켓으로 '' 데이터가 계속 들어온다.
    def check_disconnect(self, message):
        if message == '':
            raise OSError