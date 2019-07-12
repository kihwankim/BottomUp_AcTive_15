from connectDB.Connect import Connect
from graph.Graph import Graph
from network.networkController import NetworkController


class Controller(object):
    def __init__(self):
        self.connect = Connect()

    def run(self):
        tables = self.connect.get_data()
        print(tables)
        self.graph = Graph(tables)  # path 구하는 cㅣass 생성
        self.NetworkController = NetworkController(tables) # 통신을 담당할 class 생성

controller = Controller()
controller.run()
