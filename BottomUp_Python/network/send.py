class SenderSocket:
    def __init__(self, socket, addr):
        self.socket = socket
        self.addr = addr

    def send_data(self, data):
        self.socket.send(bytes(data, encoding="utf-8"))