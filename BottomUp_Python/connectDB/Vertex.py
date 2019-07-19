class Vertex:
    def __init__(self, broken, direction_data):
        self.broken = broken
        self.cross_datas = []  # 떨어져있는 정도를 담는 곳

        self.cross_datas.append(self.__weight_to_int(direction_data['top'].split(",")))
        self.cross_datas.append(self.__weight_to_int(direction_data['right'].split(",")))
        self.cross_datas.append(self.__weight_to_int(direction_data['bottom'].split(",")))
        self.cross_datas.append(self.__weight_to_int(direction_data['left'].split(",")))

        self.top = direction_data['top'].split(",")
        self.right = direction_data['right'].split(",")
        self.left = direction_data['left'].split(",")
        self.bottom = direction_data['bottom'].split(",")
        self.height = 0
    def __weight_to_int(self, array):
        if len(array) < 2:
            return array
        else:
            array[1] = int(array[1]);
            return array
