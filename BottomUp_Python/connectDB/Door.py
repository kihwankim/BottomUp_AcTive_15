from connectDB.Vertex import Vertex


class Door(Vertex):
    def __init__(self, direction_data):
        super().__init__(0, direction_data)
        self.doorNumber = direction_data['doorNumber']
        self.height = 0

    @property
    def get_height(self):
        return self.height

    @get_height.setter
    def set_height(self, input_height):
        self.height = input_height

    def __str__(self):
        return "{ height : " + str(
            self.get_height) + ", piNumber : " + self.piNumber + ", top : " + self.top + ", right : " + self.right + ", left : " + self.left + ", bottom : " + self.bottom + " }"
