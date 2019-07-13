class SenderSocket:
    def __init__(self, socket, addr):
        self.socket = socket
        self.addr = addr

    def send_data(self, data):
        # 숫자하나를 chr로 인코딩해서 송신
        data = chr(data)
        #self.socket.send(bytes(data, encoding="utf-8"))
        self.socket.send(data)

    def get_addr(self):
        return self.addr