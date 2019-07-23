from connectDB.Vertex import Vertex


class Door(Vertex):
    def __init__(self, direction_data, height, number):
        super().__init__(1, direction_data)
        self.doorNumber = number
        self.height = height

    @property
    def get_height(self):
        return self.height

    def __str__(self):
        return str(self.broken) + str(self.cross_datas) + ", door : " + self.doorNumber