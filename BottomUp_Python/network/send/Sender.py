
class Sender:
    def __init__(self, socket, floor, pi_num):
        self.socket = socket
        self.floor = floor
        self.pi_num = pi_num
        self.pi_header = (self.floor).to_bytes(1, byteorder='big') + (self.pi_num).to_bytes(1, byteorder='big')

    def get_pi_info(self):
        return self.floor, self.pi_num
        
    # 전달할 message는 숫자 1바이트(0~255) 
    # 255는 emergency를 의미
    # 254는 stop emergency를 의미
    def send(self, message):
        byte_message = (message).to_bytes(1, byteorder='big')
        self.socket.send(self.pi_header + byte_message)
    def close(self):
        self.socket.close()    