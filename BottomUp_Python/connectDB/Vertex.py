class Vertex:
    def __init__(self, broken, direction_data):
        self.broken = broken
        self.cross_datas = []

        self.cross_datas.append(direction_data['top'].split(","))
        self.cross_datas.append(direction_data['right'].split(","))
        self.cross_datas.append(direction_data['bottom'].split(","))
        self.cross_datas.append(direction_data['left'].split(","))

        self.top = direction_data['top'].split(",")
        self.right = direction_data['right'].split(",")
        self.left = direction_data['left'].split(",")
        self.bottom = direction_data['bottom'].split(",")
        self.height = 0

