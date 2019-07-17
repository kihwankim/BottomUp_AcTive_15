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
        doors = [[] for _ in range(len(result))]

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
                elif 'doors' in tableInfo.keys():
                    for door in tableInfo['doors']:
                        doors[insertIndex].append(Door(door))

        return tables

    @property
    def get_pi_tables(self):
        return self.__pi_tables

    @property
    def get_max_height(self):
        return self.max_height

    @get_max_height.setter
    def set_max_height(self, input_height):
        self.max_height = input_height
