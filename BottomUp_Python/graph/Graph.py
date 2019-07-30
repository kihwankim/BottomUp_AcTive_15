import copy

from connectDB.Pi import Pi
from connectDB.Stair import Stair


class Graph(object):
    def __init__(self, connect, tables):
        self.vertices = []
        self.number_of_vertices = 0
        self.connect = connect
        self.pis = connect.get_pis
        self.doors = connect.get_doors
        self.max_height = len(self.doors)
        self.tables = tables
        self.is_not_door_floor_stairs = []

    def find_path(self):
        path = []
        for floor in range(self.max_height):
            path.append(self.__find_path_on_floor(self.doors[floor], self.pis[floor]))
        return path

    def __find_path_of_connected_stair(self, stair_array):
        path = []
        for floor in range(self.max_height):
            path.append(self.__find_path_on_floor(stair_array[floor], self.pis[floor]))
        return path

    def __find_path_on_floor(self, doors_on_floor, pis_on_floor):  # doors_on_floor에 해당 stair 객체 배열만 넣어주면 된다
        result_pi = [[-1 for _ in range(4)] for _ in range(len(pis_on_floor))]  # 4방향 배열 생성
        for door in doors_on_floor:  # 하나씩 가져와서 사용
            if door.broken == 0:
                continue
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

    def __get_is_door_floor_stairs(self):  # door가 존재 하는 stair들만 가져온다
        door_floor_stairs = []
        for floor in range(self.max_height):
            if self.connect.is_door[floor]:
                for stair in self.connect.get_stairs[floor]:
                    door_floor_stairs.append(stair)
        return door_floor_stairs

    def __check_near_pi_path(self, paths, stair):  # pi들의 paths에서 해당 위치에 존재 여부 판별
        for index in range(4):
            now_data = stair.cross_datas[index][0]
            if now_data != 'N' and now_data != 'W' and now_data != 'S' and int(now_data) > 0:
                pi_number = int(now_data)
                for weight_data in paths[stair.height][pi_number - 1]:
                    if weight_data > 0:
                        return True  # 방향 존재
        return False

    # stair의 [아래, 위, 현재, 의미없음]
    def __find_path_of_stairs(self, door_floor_stairs_with_way_pies):
        # 여기서 stair의 path를 찾아 줄 것이다
        path_of_stairs = []
        for index in range(self.max_height):
            path_of_stairs.append([[-1, -1, -1, -1]
                                   for _ in range(len(self.connect.get_stairs[index]))])
            # 모든 배열 형성 -> 접근은 stair 번호로 접근
        for stair_data in door_floor_stairs_with_way_pies:
            path_of_stairs[stair_data.get_height][-stair_data.get_stair_number - 1][2] = 1
            # 해당 stair가 존재하는 층은 door가 존재 한다고 것을 명시

        for stair in door_floor_stairs_with_way_pies:
            if stair.broken == 0:
                continue
            queue = list()
            visit = list()
            visit.append(str(stair.get_stair_number) + str(stair.get_height))
            if self.max_height > stair.height + 1 and self.tables[
                stair.height + 1][stair.point['row']][stair.point['col']] == 'S':
                stair_of_this = self.__find_stair(stair.point['row'], stair.point['col'],
                                                  self.connect.get_stairs[stair.height + 1])
                if isinstance(stair_of_this, Stair) and (str(stair_of_this.get_stair_number) + str(
                        stair_of_this.get_height)) not in visit and stair_of_this.broken == 1:
                    visit.append(str(stair_of_this.get_stair_number) + str(stair_of_this.get_height))
                    stair_number_of_this = -stair_of_this.doorNumber - 1
                    weight_of_now = path_of_stairs[stair_of_this.height][stair_number_of_this][0]
                    if weight_of_now < 0 or weight_of_now > 1:
                        path_of_stairs[stair_of_this.height][stair_number_of_this][0] = 1
                        queue.append([stair_of_this, 0])
                    # 새로운 stair, 전에 stair, 전 -> 현재 방향  0: 아래 1 : 위 2 : 현재

            if 0 <= stair.height - 1 and self.tables[
                stair.height - 1][stair.point['row']][stair.point['col']] == 'S':
                stair_of_this = self.__find_stair(stair.point['row'], stair.point['col'],
                                                  self.connect.get_stairs[stair.height - 1])
                if isinstance(stair_of_this, Stair) and (str(stair_of_this.get_stair_number) + str(
                        stair_of_this.get_height)) not in visit and stair_of_this.broken == 1:
                    visit.append(str(stair_of_this.get_stair_number) + str(stair_of_this.get_height))
                    stair_number_of_this = -stair_of_this.doorNumber - 1
                    weight_of_now = path_of_stairs[stair_of_this.height][stair_number_of_this][1]
                    if weight_of_now < 0 or weight_of_now > 1:
                        path_of_stairs[stair_of_this.height][stair_number_of_this][1] = 1
                        queue.append([stair_of_this, 1])

            while queue:
                node = queue.pop(0)
                now_stair = node[0]
                direction = node[1]
                # 2방향 체크
                if self.max_height > now_stair.height + 1 and self.tables[
                    now_stair.get_height + 1][now_stair.point['row']][now_stair.point['col']] == 'S':
                    stair_of_this = self.__find_stair(now_stair.point['row'], now_stair.point['col'],
                                                      self.connect.get_stairs[now_stair.height + 1])
                    stair_number_of_this = -stair_of_this.doorNumber - 1
                    if isinstance(stair_of_this, Stair) and (str(stair_of_this.get_stair_number) + str(
                            stair_of_this.get_height)) not in visit and stair_of_this.broken == 1:
                        visit.append(str(stair_of_this.get_stair_number) + str(stair_of_this.get_height))
                        weight_of_now = path_of_stairs[now_stair.height][-now_stair.doorNumber - 1][direction] + 1
                        weight_of_before = path_of_stairs[stair_of_this.height][stair_number_of_this][direction]
                        if weight_of_before < 0 or weight_of_now < weight_of_before:
                            path_of_stairs[stair_of_this.height][stair_number_of_this][direction] = weight_of_now
                            queue.append([stair_of_this, 0])
                            # 새로 초기화

                if 0 <= now_stair.height - 1 and self.tables[
                    now_stair.get_height - 1][now_stair.point['row']][now_stair.point['col']] == 'S':
                    stair_of_this = self.__find_stair(now_stair.point['row'], now_stair.point['col'],
                                                      self.connect.get_stairs[now_stair.height - 1])
                    stair_number_of_this = -stair_of_this.doorNumber - 1
                    if isinstance(stair_of_this, Stair) and (str(stair_of_this.get_stair_number) + str(
                            stair_of_this.get_height)) not in visit and stair_of_this.broken == 1:
                        visit.append(str(stair_of_this.get_stair_number) + str(stair_of_this.get_height))
                        weight_of_now = path_of_stairs[now_stair.height][-now_stair.doorNumber - 1][direction] + 1
                        weight_of_before = path_of_stairs[stair_of_this.height][stair_number_of_this][direction]
                        if weight_of_before < 0 or weight_of_now < weight_of_before:
                            path_of_stairs[stair_of_this.height][stair_number_of_this][direction] = weight_of_now
                            queue.append([stair_of_this, 1])
                        # 새로 초기화

        return path_of_stairs

    def __check_stairs_for_rooftop(self, path_data):
        for index in range(len(path_data) - 1, -1, -1):
            is_connect = False
            for stair_pi_ways in path_data[index]:
                for way_data in stair_pi_ways:
                    if way_data is not -1:
                        is_connect = True

            if is_connect:
                return index + 1
        return 0

    def __find_stair(self, row, col, deep_copy_stairs):
        for stair_vertex in deep_copy_stairs:
            if stair_vertex.point['row'] == row and stair_vertex.point['col'] == col:
                return stair_vertex
        return None

    def __delete_dont_use_data(self, path_data, dont_use_index):
        new_path_data = copy.deepcopy(path_data)
        for index_of_delete_floor in range(dont_use_index):
            for stair_way in new_path_data[index_of_delete_floor]:
                for index in range(3):
                    stair_way[index] = -1
        return new_path_data

    def __check_is_way_stair(self, path_of_door_stairs, stair):
        stair_number = -stair.get_stair_number - 1
        height = stair.get_height
        if path_of_door_stairs[height][stair_number][2] != 1:
            for index in range(2):
                if path_of_door_stairs[height][stair_number][index] != -1:
                    return True
        return False

    def __make_each_floor_path(self, path_of_door_stairs):
        stairs_in_each_height = [[] for _ in range(len(self.connect.get_stairs))]
        for index_of_height in range(len(self.connect.get_stairs)):
            for index_of_row in range(len(self.connect.get_stairs[index_of_height])):
                stair = self.connect.get_stairs[index_of_height][index_of_row]
                if self.__check_is_way_stair(path_of_door_stairs, stair):
                    stairs_in_each_height[index_of_height].append(stair)
        return stairs_in_each_height

    def find_stair_path(self, paths):
        """
            1. 층수별 door check한 것을 가져옴

            2.1 door 있으면 -> 해당층에 인접 pi가 방향 존재 여부 판별 -> 있으면 stair_bfs 배열에 추가
            2.2 없으면 해당 층 무시

            3.1 해당 stair에만 대한 bfs로 path 구하기
            3.2 옥상에 대한 stair연결 여부 판별 후 bfs로 path 구한다
            3.3 옥상 path에서 door로 연결 가능 한 path는 배제 한다

            4. path가 존재 하는 층에 bfs로 path 구하고 그 path를 리턴
        """
        door_floor_stairs = self.__get_is_door_floor_stairs()
        door_floor_stairs_with_way_pies = []
        for stair in door_floor_stairs:
            if self.__check_near_pi_path(paths, stair):
                door_floor_stairs_with_way_pies.append(stair)
            # 방향있는 pi를 인접한 stair만 넣음
        path_data_of_only_stairs = self.__find_path_of_stairs(door_floor_stairs_with_way_pies)  # stair들 끼리 bfs 한것
        print("stair에 대한 path data를 출력 :", path_data_of_only_stairs)

        floor_index_of_cant_move = self.__check_stairs_for_rooftop(path_data_of_only_stairs)
        # 옥상부터 연결 door가 있는 층까지 연결 되지 않는 곳을 찾아 주는 역할을 한다
        top_floor_stairs = []
        for stair_obj in self.connect.get_stairs[self.max_height - 1]:
            top_floor_stairs.append(stair_obj)
        path_data_to_top_floor = self.__find_path_of_stairs(top_floor_stairs)
        print("옥상과 연결된 모든 stair path를 추력 :", path_data_to_top_floor)

        path_data_to_top_floor = self.__delete_dont_use_data(path_data_to_top_floor, floor_index_of_cant_move)
        # 사용 하지 않을 path 데이터 제거

        print("옥상으로 가는 경로 최적화 시킨것 -> door있는 경로와 비교 한것 :", path_data_to_top_floor)

        stairs_to_find_path = self.__make_each_floor_path(path_data_of_only_stairs)  # 배열을 가져옴
        stairs_to_top_floor = self.__make_each_floor_path(path_data_to_top_floor)

        path_of_stair_to_pies = self.__find_path_of_connected_stair(stairs_to_find_path)
        path_of_stair_to_top_pies = self.__find_path_of_connected_stair(stairs_to_top_floor)
        print("해당 stair에 대해 내부 층의 path들 : ", path_of_stair_to_pies)

        return {'stair_path': path_data_of_only_stairs, 'top_floor_stair_path': path_data_to_top_floor,
                'floor_path_for_stair': path_of_stair_to_pies, 'top_floor_path': path_of_stair_to_top_pies}
