# 경로설정 에러시 추가
# import sys
# sys.path.append('D:\project\BottomUp_AcTive_15\BottomUp_Python')
from connectDB.Connect import Connect
from connectDB.Door import Door
from connectDB.Pi import Pi
from connectDB.Stair import Stair
from connectDB.Windows import Windows
from graph.Graph import Graph
from network.networkController import NetworkController
from interface.interface import *

from threading import Thread
from queue import Queue
import sys

IP = '192.168.0.27'
PORT = 8000


class Controller(object):
    change_row = (1, -1, 0, 0)
    change_col = (0, 0, 1, -1)

    def __init__(self):
        self.connect = None
        self.tables = None
        self.graph = None
        self.NetworkController = None
        self.emergency = False
        self.q_from_Network = Queue()
        self.max_row = 0
        self.max_col = 0
        self.max_height = 0

    def __get_way_from_index(self, index):
        if index == 0:
            return 'bottom'
        elif index == 1:
            return 'top'
        elif index == 2:
            return 'right'
        else:
            return 'left'

    def __check_index(self, row, col):
        if 0 <= row < self.max_row and 0 <= col < self.max_col:
            return True
        return False

    def __get_all_data_from_table(self):
        self.max_height = len(self.tables)
        for height in range(self.max_height):
            self.max_row = len(self.tables[height])
            for row in range(self.max_row):
                self.max_col = len(self.tables[height][row])
                for col in range(self.max_col):
                    self.__get_loop_data(height, row, col)

    def __get_loop_data(self, height, row, col):  # loop 문에 들어갈 내용들 작성
        inner_data = self.tables[height][row][col]
        if inner_data != '' and inner_data != "B":  # 공백이 아니면 S, W, Pi, Door 중 하나이다
            dict_of_way = dict()  # 정보를 담는 dict 형태
            for index_of_change in range(4):  # 4방향 check
                changed_row_data = row + self.change_row[index_of_change]
                changed_col_data = col + self.change_col[index_of_change]
                way_data = self.__get_way_from_index(index_of_change)  # 위치에 따른 key 값 가져와짐 bottom, top 과같은
                if self.__check_index(changed_row_data, changed_col_data):  # 유효성 check
                    changed_data = self.tables[height][changed_row_data][changed_col_data]
                    if changed_data == '':
                        dict_of_way[way_data] = 'N'
                    elif changed_data == 'S':
                        dict_of_way[way_data] = 'S, 1'
                    elif changed_data == 'W':
                        dict_of_way[way_data] = 'W, 1'
                    elif changed_data == 'B':
                        index_of_keep_going = 1
                        while True:
                            after_keep_going_row = row + self.change_row[
                                index_of_change] * index_of_keep_going
                            after_keep_going_col = col + self.change_col[
                                index_of_change] * index_of_keep_going
                            if self.__check_index(after_keep_going_row, after_keep_going_col):  # 다시 체크
                                changed_data_of_keep_going = self.tables[height][after_keep_going_row][
                                    after_keep_going_col]
                                if changed_data_of_keep_going == '':
                                    dict_of_way[way_data] = 'N'
                                    break
                                elif changed_data_of_keep_going == 'S':
                                    dict_of_way[way_data] = 'S, ' + str(index_of_keep_going)
                                    break
                                elif changed_data_of_keep_going == 'B':
                                    index_of_keep_going += 1
                                elif changed_data_of_keep_going == 'W':
                                    dict_of_way[way_data] = "W, " + str(index_of_keep_going)
                                else:
                                    dict_of_way[way_data] = changed_data_of_keep_going + ", " + str(
                                        index_of_keep_going)
                                    break
                            else:
                                dict_of_way[way_data] = 'N'
                                break
                    else:
                        dict_of_way[way_data] = changed_data + ', 1'
                else:
                    dict_of_way[way_data] = "N"
            if inner_data == 'W':
                self.connect.get_windows[height].append(Windows(dict_of_way, height))
            elif inner_data == 'S':
                new_stair_obj = Stair(dict_of_way, height, -(len(self.connect.get_stairs[height]) + 1),
                                      {'row': row, 'col': col, 'height': height})
                self.connect.get_stairs[height].append(new_stair_obj)
            else:
                pi_or_door_number = int(inner_data)
                if pi_or_door_number > 0:  # pi
                    self.connect.get_pis[height].append(Pi(dict_of_way, height, inner_data))
                else:  # door
                    self.connect.get_doors[height].append(Door(dict_of_way, height, str(pi_or_door_number)))
                    self.connect.is_door[height] = True

    def __excute_command(self, command):
        if command == 'exit':
            exit(0)
            sys.exit(0)
        if command == 'get DB':
            self.__excute_for_get_DB()  # 초기화 해주는 곳
            # 인자 다 넘길 필요있나? 주소 복사?
            if not self.NetworkController:
                self.NetworkController = NetworkController(self.connect.get_pis, self.connect.get_stairs, self.connect.get_max_height,
                                                           self.q_from_Network, IP, PORT, )  # 통신을 담당할 class 생성
                self.pi_status = self.NetworkController.get_safe_status()  # 주소복사?
            else:
                self.NetworkController.reset(self.connect.get_pis, self.connect.get_max_height)
        elif command == 'print status':
            if not self.tables:
                print("please setting first!!!")
                return False
            self.NetworkController.print_all_seat()
        elif command == 'start accept':
            if not self.tables:
                print("please setting first!!!")
                return False
            t_accept = Thread(target=self.NetworkController.start_accpet)
            t_accept.start()
        elif command == 'stop accept':
            self.NetworkController.stop_accept()
        elif command == 'start check':
            self.NetworkController.stop_accept()
            self.NetworkController.start_checking()
        elif command == 'stop check':
            self.NetworkController.stop_checking()
            self.emergency = False
        return True

    def __excute_for_get_DB(self):
        self.connect = Connect()
        self.tables = self.connect.get_data()

        self.__get_all_data_from_table()

        self.graph = Graph(self.connect, self.tables)  # path 구하는 class 생성
        path_data = self.graph.find_path()
        print(path_data)

        result_for_stairs = self.graph.find_stair_path(path_data)

        send_stair_data = self.__stair_path(result_for_stairs['stair_path'], result_for_stairs['top_floor_stair_path'])
        print(send_stair_data)

        send_data = self.__result_pi_direction(path_data, result_for_stairs['floor_path_for_stair'],
                                               result_for_stairs['top_floor_path'])
        print(send_data)  # send_data : 각각의 라즈베리파이에 대한 정보가 저장 되어있는것

    def __result_pi_direction(self, path_data, for_floor_path, for_top_path):
        send_data = self.__make_format(path_data, for_floor_path)
        send_data = self.__make_format_top_floor(send_data, for_top_path)

        return send_data

    def __stair_path(self, door_path, top_path):
        result_stair_path = []
        for index_of_floor in range(len(door_path)):
            each_floor = []
            for index_of_stair_pi in range(len(door_path[index_of_floor])):
                each_component = []
                for index_of_component in range(4):
                    door_data = door_path[index_of_floor][index_of_stair_pi][index_of_component]
                    top_data = top_path[index_of_floor][index_of_stair_pi][index_of_component]
                    if door_data > 0:
                        each_component.append(door_data)
                    elif top_data > 0:
                        each_component.append(top_data)
                    else:
                        each_component.append(0)
                each_floor.append(each_component)
            result_stair_path.append(each_floor)

        return result_stair_path

    def __action_send(self):
        # list_broken = []
        while True:
            # wait emergency
            if self.q_from_Network.get() != 'emergency':
                continue
            self.emergency = True
            self.NetworkController.start_emergency()

            while self.emergency:
                item = self.q_from_Network.get()
                if item == 'stop checking':
                    break
                if item == 'emergency':
                    continue
                try:
                    pi_floor = item[0]
                    pi_num = item[1]
                    self.pi_status[pi_floor][pi_num] = -1
                    if pi_num <= 200:
                        self.connect.get_pis[pi_floor - 1][pi_num - 1].broken = 0
                    else:
                        self.connect.get_stairs[pi_floor - 1][pi_num - 201].broken = 0

                    self.graph.pis = self.connect.get_pis
                    new_path_data = self.graph.find_path()
                    new_result_for_stairs = self.graph.find_stair_path(new_path_data)

                    # pi 에게 보낼 data
                    new_path_send_data = self.__result_pi_direction(new_path_data,
                                                                    new_result_for_stairs['floor_path_for_stair'],
                                                                    new_result_for_stairs['top_floor_path'])
                    # stair에게 보낼 data
                    send_stair_data = self.__stair_path(new_result_for_stairs['stair_path'],
                                                        new_result_for_stairs['top_floor_stair_path'])

                    self.NetworkController.send_path_non_stair(new_path_send_data)  # door 로 가는 경로
                    self.NetworkController.send_path_stair(send_stair_data)  # stair 로 가는 경로

                except Exception:
                    pass

    def __make_format(self, path_door_data, path_stair_data):
        result_path = []

        for index_of_height in range(self.max_height):
            row_array = []
            result_path.append(row_array)
            for index_of_row in range(len(path_door_data[index_of_height])):
                col_array = [0 for _ in range(8)]
                row_array.append(col_array)
                for index_of_col in range(len(path_door_data[index_of_height][index_of_row])):
                    door_inner_data = path_door_data[index_of_height][index_of_row][index_of_col]
                    stair_inner_data = path_stair_data[index_of_height][index_of_row][index_of_col]
                    if door_inner_data != -1:
                        result_path[index_of_height][index_of_row][index_of_col] = door_inner_data
                        result_path[index_of_height][index_of_row][index_of_col + 4] = 1
                    elif stair_inner_data != -1:
                        result_path[index_of_height][index_of_row][index_of_col] = stair_inner_data
                        result_path[index_of_height][index_of_row][index_of_col + 4] = 2
        return result_path

    def __make_format_top_floor(self, path_door_data, path_stair_data):
        result_path = []

        for index_of_height in range(self.max_height):
            row_array = []
            result_path.append(row_array)
            for index_of_row in range(len(path_stair_data[index_of_height])):
                col_array = [0 for _ in range(8)]
                row_array.append(col_array)
                for index_of_col in range(len(path_stair_data[index_of_height][index_of_row])):
                    door_inner_data = path_door_data[index_of_height][index_of_row][index_of_col]
                    stair_inner_data = path_stair_data[index_of_height][index_of_row][index_of_col]
                    if door_inner_data != 0:
                        result_path[index_of_height][index_of_row][index_of_col] = door_inner_data
                        result_path[index_of_height][index_of_row][index_of_col + 4] = 1
                    elif stair_inner_data != -1:
                        result_path[index_of_height][index_of_row][index_of_col] = stair_inner_data
                        result_path[index_of_height][index_of_row][index_of_col + 4] = 3
        return result_path

    def run(self):
        # self.NetworkController = NetworkController(self.connect.get_pis, self.connect.get_max_height,
        #                                            self.q_from_Network, IP, PORT, )  # 통신을 담당할 class 생성
        # self.pi_status = self.NetworkController.get_safe_status()  # 주소복사?

        t_send = Thread(target=self.__action_send)
        t_send.daemon = True
        t_send.start()

        num_menu = 1
        while True:

            new_num_menu, command = repeat_print(num_menu)
            if self.__excute_command(command):
                num_menu = new_num_menu


def main():
    controller = Controller()
    controller.run()
    print("print for debug")


if __name__ == "__main__":  # 메인문
    main()