class Pi(object):
    def __init__(self, pi):
        self.piNumber = pi['piNumber']
        self.top = pi['top']
        self.right = pi['right']
        self.left = pi['left']
        self.bottom = pi['bottom']
        self.height = 0

    @property
    def get_height(self):
        return self.height

    @get_height.setter
    def set_height(self, input_height):
        self.height = input_height

    def __str__(self):
        return "{ height : " + str(self.get_height) + ", piNumber : " + self.piNumber + ", top : " + self.top + ", right : " + self.right + ", left : " + self.left + ", bottom : " + self.bottom + " }"
