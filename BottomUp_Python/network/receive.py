class ReceiverSocket:
    def __init__(self, socket, pi_num):
        self.socket = socket
        self.pi_num = pi_num
        #self.count_unsafe = 0      카운트가 10이 넘어가면 실제 unsafe로 간주?

    def get_pi_num(self):
        return self.pi_num
    
    def receive_data(self):
        data = self.socket.recv(10)
        if data == '':
            return self.pi_num, 'disconnected'
        received_pi_num = data[0]
        message = data[1]
        if message == 255:
            message = 'emergency'
        return received_pi_num, message
    def close(self):
        self.socket.close()