from firebase import firebase
from connectDB.Pi import Pi
from connectDB.Door import Door


class Connect(object):
    def __init__(self):
        self.firebase = firebase.FirebaseApplication('https://bottomup-sync.firebaseio.com/', None)
        self.__pi_tables = []

    def get_data(self):
        result = self.firebase.get('/bottomup', None)
        print(result)
        tables = [[] for _ in range(len(result))]
        self.__doors = [[] for _ in range(len(result))]
        self.__pis = [[] for _ in range(len(result))]

        self.set_max_height = len(result)

        for key, value in result.items():
            for tableInfo in value:
                if tableInfo is None:
                    continue
                elif 'height' in tableInfo.keys():
                    insertIndex = tableInfo['height'] - 1
                elif 'array' in tableInfo.keys():
                    tables[insertIndex].append(tableInfo['array'])
                elif 'piNumber' in tableInfo.keys():
                    pi_data = Pi(tableInfo)
                    pi_data.set_height = insertIndex + 1
                    self.__pi_tables.append(pi_data)
                    self.__pis[insertIndex].append(Pi(tableInfo))
                elif 'doors' in tableInfo.keys():
                    for door in tableInfo['doors']:
                        self.__doors[insertIndex].append(Door(door))
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
    def get_pi_tables(self):
        return self.__pi_tables

    @property
    def get_max_height(self):
        return self.__max_height

    @get_max_height.setter
    def set_max_height(self, input_height):
        self.__max_height = input_height
