from firebase import firebase


class Connect(object):
    def __init__(self):
        self.firebase = firebase.FirebaseApplication('https://bottomup-sync.firebaseio.com/', None)
        

    def get_data(self):
        result = self.firebase.get('/bottomup', None)
        if not result:
            return None

        tables = []
        self.__doors = [[] for _ in range(len(result))]
        self.__pis = [[] for _ in range(len(result))]
        self.__windows = [[] for _ in range(len(result))]
        self.__stairs = [[] for _ in range(len(result))]
        self.set_max_height = len(result)
        self.is_door = [False for _ in range(len(result))]

        for table in result.values():
            for tableInfo in table:  # table : 각 층
                if tableInfo is None:  # tableInfo : 각 각 의 컴포넌트
                    continue
                elif 'array' in tableInfo.keys():
                    tables.append(tableInfo['array'])
        return tables


    @property
    def get_doors(self):
        return self.__doors

    @get_doors.setter
    def set_doors(self, input_doors):
        self.__doors = input_doors


    @property
    def get_pis(self):
        return self.__pis

    @get_pis.setter
    def set_max_height(self, input_pis):
        self.__pis = input_pis

    @property
    def get_doors(self):
        return self.__doors

    @property
    def get_pis(self):
        return self.__pis

    @property
    def get_stairs(self):
        return self.__stairs

    @property
    def get_windows(self):
        return self.__windows

    @property
    def get_max_height(self):
        return self.__max_height

    @get_max_height.setter
    def set_max_height(self, input_height):
        self.__max_height = input_height
