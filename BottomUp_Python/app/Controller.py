from model.Connect import Connect


class Controller:
    def __init__(self):
        self.connect = Connect()

    def run(self):
        print(self.connect.get_data())


controller = Controller()
controller.run()
