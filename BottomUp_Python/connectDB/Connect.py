from firebase import firebase
from connectDB.Pi import Pi


class Connect(object):
    def __init__(self):
        self.firebase = firebase.FirebaseApplication('https://bottomup-sync.firebaseio.com/', None)
        self.__pi_tables = []

    def get_data(self):
        result = self.firebase.get('/bottomup', None)
        print(result)
        tables = [[] for _ in range(len(result))]

        for key, value in result.items():
            for tableInfo in value:
                if 'height' in tableInfo.keys():
                    insertIndex = tableInfo['height'] - 1
                elif 'array' in tableInfo.keys():
                    tables[insertIndex].append(tableInfo['array'])
                else:
                    pi_data = Pi(tableInfo)
                    pi_data.set_height = insertIndex + 1
                    self.__pi_tables.append(pi_data)
        return tables

    @property
    def get_pi_tables(self):
        return self.__pi_tables
