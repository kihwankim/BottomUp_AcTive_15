from connectDB.Vertex import Vertex


class Pi(Vertex):
    def __init__(self, direction_data):
        super().__init__(1, direction_data)
        self.piNumber = direction_data['piNumber']

    @property
    def get_height(self):
        return self.height

    @get_height.setter
    def set_height(self, input_height):
        self.height = input_height

    def __str__(self):
        return "{ height : " + str(
            self.get_height) + ", piNumber : " + self.piNumber + ", top : " + self.top + ", right : " + self.right + ", left : " + self.left + ", bottom : " + self.bottom + " }"
