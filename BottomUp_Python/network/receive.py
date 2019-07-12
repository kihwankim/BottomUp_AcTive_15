class ReceiverSocket:
    def __init__(self, socket, addr):
        self.socket = socket
        self.addr = addr

    def receive_data(self):
        data = self.socket.recv()
        return data

