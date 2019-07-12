class NetworkController:
    def __init__(self, tables):
        self.safes = [1]*(len(tables[0])+1)   # 각 파이별로 안전한지 나타냄.  [1]=1 : 1번 파이 safe,  [2]=0 : 2번 파이 unsafe