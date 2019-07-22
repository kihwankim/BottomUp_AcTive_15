import copy

from connectDB.Pi import Pi


class Graph(object):
    def __init__(self, connect, tables):
        self.vertices = []
        self.number_of_vertices = 0
        self.connect = connect
        self.pis = connect.get_pis
        self.doors = connect.get_doors
        self.max_height = len(self.doors)
        self.tables = tables

    def find_path(self):
        path = []
        for floor in range(self.max_height):
            path.append(self.__find_path_on_floor(self.doors[floor], self.pis[floor]))
        return path

    def __find_path_on_floor(self, doors_on_floor, pis_on_floor):  # doors_on_floor에 해당 stair 객체 배열만 넣어주면 된다
        result_pi = [[-1 for _ in range(4)] for _ in range(len(pis_on_floor))]  # 4방향 배열 생성
        for door in doors_on_floor:  # 하나씩 가져와서 사용
            pis_for_bfs = copy.deepcopy(pis_on_floor)  # pi 객체 깊은 복사
            visit = list()  # 공백의 list 생성
            queue = list()
            if door.broken == 0:
                continue
            for direction in range(4):
                get_door_cross_data_of_direction = door.cross_datas[direction][0]
                if get_door_cross_data_of_direction != 'N' and get_door_cross_data_of_direction != 'S' and get_door_cross_data_of_direction != 'W':
                    pi_number = int(door.cross_datas[direction][0])
                    weight = door.cross_datas[direction][1]
                    result_pi[pi_number - 1][(direction + 2) % 4] = 1
                    queue.append([pis_for_bfs[pi_number - 1], weight, door.doorNumber])
                    # pis_for_bfs : 파이 객체 배열, weight : 가중치, doorNumber : 해당 위치에 접근 가능한 door

            while queue:
                node = queue.pop(0)
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
                            elif pi.cross_datas[direction][0] == node[2] and int(node[2]) > 0:  # door번호랑
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

    # def make_stair_path(self, empty_stair):
    #     path = []
    #     path_of_stair = []
    #     for floor in range(self.max_height):
    #         path.append(self.__find_path_on_floor(empty_stair[floor], self.pis[floor]))
    #         path_of_stair.append(self.__find_path_stair(empty_stair))
    #     return {'floor_path': path, 'stair_path': path_of_stair}
    #
    # def __find_path_stair(self, empty_stair):
    #     now_height_stair_way = []
    #     for floor_of_empty_stair in empty_stair:
    #         for stair_vertex in floor_of_empty_stair:  # stair 하나씩 가져온다
    #             can_upper = 0
    #             can_under = 0
    #             if stair_vertex.broken == 1:
    #                 now_row = stair_vertex.point['row']
    #                 now_col = stair_vertex.point['col']
    #                 now_height = stair_vertex.point['height']
    #                 if 0 <= now_height + 1 < self.max_height and self.tables[now_height + 1][now_row][now_col] == 'S':
    #                     upper_stair = self.__find_stair(now_row, now_col, now_height + 1)
    #                     if upper_stair and upper_stair.broken == 1:
    #                         can_upper = 1
    #                 elif 0 <= now_height - 1 < self.max_height:
    #                     under_stair = self.__find_stair(now_row, now_col, now_height - 1)
    #                     if under_stair and under_stair.broken == 1:
    #                         can_under = 1
    #             now_stair_way = [can_under, can_upper, -1, -1]
    #             now_height_stair_way.append(now_stair_way)
    #     return now_height_stair_way
    #
    # def __find_stair(self, row, col, height):
    #     for stair_vertex in self.connect.get_stairs[height]:
    #         if stair_vertex.point['row'] == row and stair_vertex.point['col'] == col:
    #             return stair_vertex
    #     return None
