from connectDB.Vertex import Vertex


class Stair(Vertex):
    def __init__(self, direction_data, height, stair_number, point):
        super().__init__(1, direction_data)
        self.height = height
        self.doorNumber = stair_number  # 코드 재사용 떄문에 doorNumber라고 함
        self.point = point

    @property
    def get_height(self):
        return self.height

    @property
    def get_stair_number(self):
        return self.doorNumber
