import copy

from connectDB.Pi import Pi


class Graph(object):
    def __init__(self, pi_table, door_table):
        self.vertices = []
        self.number_of_vertices = 0
        self.pis = pi_table
        self.doors = door_table
        self.max_height = len(self.doors)

    def find_path(self):
        path = []
        for floor in range(self.max_height):
            path.append(self.__find_path_on_floor(floor))

        return path

    def __find_path_on_floor(self, height):
        doors_on_floor = self.doors[height]  # 해당 층에 door의 객체 리턴
        pis_on_floor = self.pis[height]  # 해당 층에 pi의 객체 리턴
        result_pi = [[-1 for _ in range(4)] for _ in range(len(pis_on_floor))]  # 4방향 배열 생성

        for door in doors_on_floor:  # 하나씩 가져와서 사용
            visit = list()  # 공백의 list 생성
            queue = list()
            pis_for_bfs = copy.deepcopy(pis_on_floor)  # pi 객체 깊은 복사
            for direction in range(4):
                get_door_cross_data_of_direction = door.cross_datas[direction][0]
                if get_door_cross_data_of_direction != 'N' and get_door_cross_data_of_direction != 'S' and get_door_cross_data_of_direction != 'W':
                    pi_number = int(door.cross_datas[direction][0])
                    weight = door.cross_datas[direction][1]
                    result_pi[pi_number - 1][(direction + 2) % 4] = 1
                    queue.append([pis_for_bfs[pi_number - 1], weight, door.doorNumber])

            while queue:
                node = queue.pop()
                if isinstance(node[0], Pi) and node[0].piNumber not in visit and node[0].broken == 1:
                    pi = node[0]
                    pi_number = int(pi.piNumber)
                    visit.append(pi.piNumber)
                    for direction in range(4):
                        get_pi_cross_data = pi.cross_datas[direction][0]
                        if get_pi_cross_data != 'N' and get_pi_cross_data != 'S' and get_pi_cross_data != 'W':
                            target_pi_number = int(pi.cross_datas[direction][0])
                            if target_pi_number < 0:
                                continue
                            elif pi.cross_datas[direction][0] == node[2] and int(node[2]) > 0:
                                pi.cross_datas[direction][1] = \
                                    pis_for_bfs[int(node[2]) - 1].cross_datas[(direction + 2) % 4][1]
                                if result_pi[pi_number - 1][direction] == -1 or result_pi[pi_number - 1][direction] > \
                                        pi.cross_datas[direction][1]:
                                    result_pi[pi_number - 1][direction] = pi.cross_datas[direction][1]
                                continue

                            pi.cross_datas[direction][1] = pi.cross_datas[direction][1] + node[1]
                            target_pi = pis_for_bfs[target_pi_number - 1]
                            queue.append([target_pi, pi.cross_datas[direction][1], pi.piNumber])
            print(pis_for_bfs)

        return result_pi
