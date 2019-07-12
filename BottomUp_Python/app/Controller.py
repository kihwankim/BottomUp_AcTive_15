from connectDB.Connect import Connect
from graph.Graph import Graph


class Controller(object):
    def __init__(self):
        self.connect = Connect()

    def run(self):
        tables = self.connect.get_data()
        print(tables)
        self.graph = Graph(tables)  # path 구하는 cㅣass 생성

controller = Controller()
controller.run()
