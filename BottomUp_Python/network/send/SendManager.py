class SendManager:
    def __init__(self, building_height):
        self.building_height = building_height
        self.senders = [0]* (building_height+1)
        
        # 초기화
        for floor in range(1, building_height+1):
            self.senders[floor] = {}

    def add_sender(self, Sender):
        self.senders[Sender.floor][Sender.pi_num] = Sender

    def delete_sender(self, floor, pi_num):
        try:
            self.senders[floor][pi_num].close()
            del self.senders[floor][pi_num]
        except NameError:
            pass
        except KeyError:
            pass

    # 층, 번호로 메세지 송신
    def send_message(self, floor, pi_num, message):
        self.senders[floor][pi_num].send(message)

    # 연결된 모든 파이에게 메세지 송신
    def send_All(self, message):
        list_disconnected = []
        for floor, floor_senders in enumerate(self.senders, 0):
            if floor == 0:
                continue
            for Sender in floor_senders.values():
                try:
                    Sender.send(message)
                except OSError:
                    list_disconnected.append(Sender)

        # 끊킨 파이는 삭제
        for Sender in list_disconnected:
            self.delete_sender(Sender.floor, Sender.pi_num)

    # 연결된 모든 파이에게 '상황체크 시작' 송신
    def send_All_start_checking(self):
        self.send_All(253)
    
    # 연결된 모든 파이에게 '상황체크 종료' 송신
    def send_All_stop_checking(self):
        self.send_All(254)

    # 연결된 모든 파이에게 '상황시작' 송신
    def send_All_start_emergency(self):
        self.send_All(255) 

    def send_All_path(self, list_path):
        for floor in list_path:
            for pi in floor:
                self.send_message(pi.floor, pi.num, pi.message)