from connectDB.Vertex import Vertex


class Windows(Vertex):
    def __init__(self, direction_data, height):
        super().__init__(1, direction_data)
        self.height = height

    @property
    def get_height(self):
        return self.height
