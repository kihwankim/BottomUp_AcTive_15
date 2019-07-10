from firebase import firebase

class Pi:
    def __init__(self, pi):
        self.piNumber = pi['piNumber']
        self.top = pi['top']
        self.right = pi['right']
        self.left = pi['left']
        self.bottom = pi['bottom']


firebase = firebase.FirebaseApplication('https://bottomup-sync.firebaseio.com/', None)
result = firebase.get('/bottomup', None)
tables = [[] for i in range(len(result))]
insetIndex = 0
print(tables)
for key, value in result.items():
    table = []
    for tableInfo in value:
        # height가 밑에서부터 자동으로 생성되기 때문에
        if('height' in tableInfo.keys()):
            insetIndex = tableInfo['height'] - 1
        else:
            tables[insetIndex].append(Pi(tableInfo))

print(tables)



