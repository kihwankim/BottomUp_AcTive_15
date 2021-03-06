from connectDB.Vertex import Vertex


class Pi(Vertex):
    def __init__(self, direction_data, height, number):
        super().__init__(1, direction_data)
        self.piNumber = number
        self.height = height

    @property
    def get_height(self):
        return self.height
