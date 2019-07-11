from firebase import firebase


class Pi:
    def __init__(self, pi):
        self.piNumber = pi['piNumber']
        self.top = pi['top']
        self.right = pi['right']
        self.left = pi['left']
        self.bottom = pi['bottom']


class Connect:
    def __init__(self):
        self.firebase = firebase.FirebaseApplication('https://bottomup-sync.firebaseio.com/', None)

    def get_data(self):

        result = self.firebase.get('/bottomup', None)

        tables = [[] for _ in range(len(result))]

        insertIndex = 0

        for key, value in result.items():
            for tableInfo in value:
                if ('height' in tableInfo.keys()):
                    insetIndex = tableInfo['height'] - 1
                else:
                    tables[insetIndex].append(Pi(tableInfo))
        return tables
