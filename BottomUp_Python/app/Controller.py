# 경로설정 에러시 추가
# import sys
# sys.path.append('D:\project\BottomUp_AcTive_15\BottomUp_Python')
from connectDB.Connect import Connect
from graph.Graph import Graph

# from network.networkController import NetworkController

IP = '168.188.127.74'
PORT = 8000


class Controller(object):
    def __init__(self):
        self.connect = Connect()

    def run(self):
        tables = self.connect.get_data()
        print(tables)
        # pi_datas = self.connect.get_pi_tables  # 통신해서 setting해야할 부분들
        # building_height = 2 # 건물 높이(총 층수). DB에서 가져와야함
        self.graph = Graph(tables, self.connect.get_pis, self.connect.get_doors)  # path 구하는 class 생성

        paths = self.graph.find_path()
        print(paths)
        ### 통신 로직 ###
        # self.NetworkController = NetworkController(pi_datas, building_height, IP, PORT)  # 통신을 담당할 class 생성
        # self.NetworkController.run_server()  # 스레드를 생성하며 통신 시작, 메인 스레드는 emergency 신호가 올때까지 여기서 멈춤

        # self.NetworkController.test_run_server()

        # 각 층별로, 파이가 안전한지 나타냄.
        # [0] = 사용 X
        # [1] = {1:1, 2:0, 7:0}    : 1층. 1번 안전, 2번 위험, 7번 위험 
        # [2] = {1:1, 4:0}         : 2층. 1번 안전, 4번 위험
        # 네트워크 객체의 safe_height가 실시간으로 업데이트 되니, 
        # .get_safes_hegiht()로 계속 갖다써서 그래프에 이용하면 됨
        # self.safes_height = self.NetworkController.get_safes_height()


def main():
    controller = Controller()
    controller.run()
    print("print for debug")


if __name__ == "__main__":  # 메인문
    main()
