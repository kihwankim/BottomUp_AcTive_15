class ReceiverSocket:
    def __init__(self, socket, pi_floor, pi_num):
        self.socket = socket
        self.pi_floor = pi_floor
        self.pi_num = pi_num
        #self.count_unsafe = 0      카운트가 10이 넘어가면 실제 unsafe로 간주?

    def get_pi_info(self):
        return self.pi_floor, self.pi_num
    
    def receive_data(self):
        data = self.socket.recv(10)
        received_pi_floor = data[0]
        received_pi_num = data[1]
        message = data[2]
        if received_pi_floor != self.pi_floor or received_pi_num != self.pi_num:
            return -1, -1, 'pi receive error'
        elif message < 254:
            return self.pi_floor, self.pi_num, message
        elif message == 254:
            return self.pi_floor, self.pi_num, 'stop emergency'
        elif message == 255:
            return self.pi_floor, self.pi_num, 'emergency'
        raise IndexError
    def close(self):
        self.socket.close()