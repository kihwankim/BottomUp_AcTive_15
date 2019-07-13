class ReceiverSocket:
    def __init__(self, socket, addr):
        self.socket = socket
        self.addr = addr

    def receive_data(self):
        data = self.socket.recv(100)
        return str(data, encoding='utf-8')

    def get_addr(self):
        return self.addr

    def close(self):
        self.socket.close()

