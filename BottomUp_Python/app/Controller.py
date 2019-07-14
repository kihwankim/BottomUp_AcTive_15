#경로설정 에러시 추가
#import sys
#sys.path.append('D:\project\BottomUp_AcTive_15\BottomUp_Python')
from connectDB.Connect import Connect
from graph.Graph import Graph
from network.networkController import NetworkController

IP = '168.188.127.74'
PORT = 8000
class Controller(object):
    def __init__(self):
        self.connect = Connect()

    def run(self):
        tables = self.connect.get_data()
        print(tables)
        self.graph = Graph(tables)  # path 구하는 class 생성
        
        ### 통신 로직 ###
        self.NetworkController = NetworkController(tables, IP, PORT) # 통신을 담당할 class 생성
        self.NetworkController.run_server() # 스레드를 생성하며 통신 시작, 메인 스레드는 emergency 신호가 올때까지 여기서 멈춤

        #self.NetworkController.test_run_server()

        # safes는 각 파이별로 안전한지 나타낼 리스트.  [1]=1 : 1번 파이 safe,  [2]=0 : 2번 파이 unsafe...
        # 네트워크 객체 안의 safe를 주기적으로 업데이트 할테니, NetworkController.get_safes()로 계속 갖다써서 그래프에 이용하면 됨
        self.safes = self.NetworkController.get_safes()

controller = Controller()
controller.run()
print("print for debug")