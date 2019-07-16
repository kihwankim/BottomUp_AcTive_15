class SenderSocket:
    def __init__(self, socket, pi_floor, pi_num):
        self.socket = socket
        self.pi_floor = pi_floor
        self.pi_num = pi_num
        self.pi_floor_byte = (self.pi_floor).to_bytes(1, byteorder='big')
        self.pi_num_byte = (self.pi_num).to_bytes(1, byteorder='big')
        self.pi_header = self.pi_floor_byte+self.pi_num_byte

    def get_pi_info(self):
        return self.pi_floor, self.pi_num
        
    # 전달할 message는 숫자 1바이트(0~255) 
    # 255는 emergency를 의미
    # 254는 stop emergency를 의미
    def send_data(self, message):
        byte_message = (message).to_bytes(1, byteorder='big')
        self.socket.send(self.pi_header + byte_message)
    def close(self):
        self.socket.close()