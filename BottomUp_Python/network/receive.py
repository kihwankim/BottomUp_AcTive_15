class ReceiverSocket:
    def __init__(self, socket, addr):
        self.socket = socket
        self.addr = addr
        #self.count_unsafe = 0      카운트가 10이 넘어가면 실제 unsafe로 간주?

    def receive_data(self):
        data = self.socket.recv(5)
        return str(data, encoding='utf-8')

    def receive_and_check_safe(self):
        data = self.receive_data()
        if data == '':
            self.close()
            return False
        
    def get_addr(self):
        return self.addr

    def close(self):
        self.socket.close()