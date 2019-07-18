class ReceiverSocket:
    def __init__(self, socket, pi_num):
        self.socket = socket
        self.pi_num = pi_num
        #self.count_unsafe = 0      카운트가 10이 넘어가면 실제 unsafe로 간주?

    def get_pi_num(self):
        return self.pi_num
    
    def receive_data(self):
        data = self.socket.recv(10)
        received_pi_num = data[0]
        message = data[1]
        if received_pi_num != self.pi_num:
            return received_pi_num, 'pi num error'
        elif message < 254:
            return received_pi_num, message
        elif message == 254:
            return received_pi_num, 'stop emergency'
        elif message == 255:
            return received_pi_num, 'emergency'
        raise IndexError
    def close(self):
        self.socket.close()