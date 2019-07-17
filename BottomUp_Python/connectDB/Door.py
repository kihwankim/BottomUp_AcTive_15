class Door(object):
    def __init__(self, pi):
        self.doorNumber = pi['doorNumber']
        self.top = pi['top'].split(",")
        self.right = pi['right'].split(",")
        self.left = pi['left'].split(",")
        self.bottom = pi['bottom'].split(",")
        self.height = 0

    @property
    def get_height(self):
        return self.height

    @get_height.setter
    def set_height(self, input_height):
        self.height = input_height

    def __str__(self):
        return "{ height : " + str(self.get_height) + ", piNumber : " + self.piNumber + ", top : " + self.top + ", right : " + self.right + ", left : " + self.left + ", bottom : " + self.bottom + " }"
