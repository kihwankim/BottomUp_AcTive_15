class SenderSocket:
    def __init__(self, socket, pi_num):
        self.socket = socket
        self.pi_num = pi_num
        self.pi_num_byte = (self.pi_num).to_bytes(1, byteorder='big')

    def get_pi_num(self):
        return self.pi_num
        
    # 전달할 message는 숫자 1바이트(0~255) 
    # 255는 emergency를 의미
    def send_data(self, message):
        byte_message = (message).to_bytes(1, byteorder='big')
        self.socket.send(self.pi_num_byte + byte_message)