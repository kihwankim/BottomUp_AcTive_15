# 경로설정 에러시 추가
# import sys
# sys.path.append('D:\project\BottomUp_AcTive_15\BottomUp_Python')
from connectDB.Connect import Connect
from connectDB.Door import Door
from connectDB.Pi import Pi
from connectDB.Stair import Stair
from connectDB.Windows import Windows
from graph.Graph import Graph

from interface.interface import *

from threading import  Thread

IP = '192.168.0.30'
PORT = 8000

class Controller(object):
    change_row = (1, -1, 0, 0)
    change_col = (0, 0, 1, -1)

    def __init__(self):
        self.connect = Connect()
        self.tables = self.connect.get_data()
        self.graph = None
        self.emergency = False

    def __get_way_from_index(self, index):
        if index == 0:
            return 'bottom'
        elif index == 1:
            return 'top'
        elif index == 2:
            return 'right'
        else:
            return 'left'

    def __check_index(self, row, col, max_row, max_col):
        if 0 <= row and row < max_row and 0 <= col and col < max_col:
            return True
        return False

    def __get_all_data_from_table(self):
        for height in range(len(self.tables)):
            for row in range(len(self.tables[height])):
                for col in range(len(self.tables[height][row])):
                    self.__get_loop_data(height, row, col)

    def __get_loop_data(self, height, row, col):  # loop 문에 들어갈 내용들 작성
        inner_data = self.tables[height][row][col]
        if inner_data != '' and inner_data != "B":  # 공백이 아니면 S, W, Pi, Door 중 하나이다
            dict_of_way = dict()  # 정보를 담는 dict 형태
            for index_of_change in range(4):  # 4방향 check
                changed_row_data = row + self.change_row[index_of_change]
                changed_col_data = col + self.change_col[index_of_change]
                way_data = self.__get_way_from_index(index_of_change)  # 위치에 따른 key 값 가져와짐 bottom, top 과같은
                if self.__check_index(changed_row_data, changed_col_data,
                                      len(self.tables[height]), len(self.tables[height][row])):  # 유효성 check
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
                            if self.__check_index(after_keep_going_row, after_keep_going_col,
                                                  len(self.tables[height]), len(self.tables[height][row])):  # 다시 체크
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
                self.connect.get_stairs[height].append(Stair(dict_of_way, height))
            else:
                pi_or_door_number = int(inner_data)
                if pi_or_door_number > 0:  # pi
                    self.connect.get_pis[height].append(Pi(dict_of_way, height, inner_data))
                else:  # door
                    self.connect.get_doors[height].append(Door(dict_of_way, height, str(-pi_or_door_number)))

    def __excute_command(self, command):
        if command == 'exit':
            exit(0)
        if command == 'get DB':
            self.__get_all_data_from_table()
        elif command == 'print status':
            self.NetworkController.print_all_seat()
        elif command == 'start accept':
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

    def __action_send(self):
        #list_broken = []
        while True:
            self.NetworkController.wait_emergency()
            self.emergency = True

            while self.emergency:
                for height, pis in enumerate(self.NetworkController.get_safe_status()):
                    for pi_number in pis:
                        if pis[pi_number] == 0:
                            pis[pi_number]=-1
                            self.connect.get_pis[height-1][pi_number-1].broken = 0
                            self.graph.pis = self.connect.get_pis
                            self.NetworkController.send_All_path(self.graph.find_path())

    def run(self):
        self.__get_all_data_from_table()
        self.graph = Graph(self.connect.get_pis, self.connect.get_doors)  # path 구하는 class 생성
        self.NetworkController = NetworkController(self.connect.get_pis, self.connect.get_max_height, IP, PORT)  # 통신을 담당할 class 생성

        t_send = Thread(target=self.__action_send)
        t_send.start()

        num_menu = 1
        while True:
            num_menu, command = repeat_print(num_menu)
            self.__excute_command(command)

def main():
    controller = Controller()
    controller.run()
    print("print for debug")


if __name__ == "__main__":  # 메인문
    main()


"""
run에서 프린트문
print("window :", self.connect.get_windows)
        print("stair :", self.connect.get_stairs)
        print("doors :", self.connect.get_doors)
        print("pies :", self.connect.get_pis)

        print("pi : ")
        for height in range(len(self.connect.get_pis)):
            for number in range(len(self.connect.get_pis[height])):
                print(self.connect.get_pis[height][number], end=" ")
            print()

        print("windows : ")
        for height in range(len(self.connect.get_windows)):
            for number in range(len(self.connect.get_windows[height])):
                print(self.connect.get_windows[height][number], end=" ")
            print()

        print("stairs : ")
        for height in range(len(self.connect.get_stairs)):
            for number in range(len(self.connect.get_stairs[height])):
                print(self.connect.get_stairs[height][number], end=" ")
            print()

        print("doors : ")
        for height in range(len(self.connect.get_doors)):
            for number in range(len(self.connect.get_doors[height])):
                print(self.connect.get_doors[height][number], end=" ")
            print()
"""

''' 통신 로직
        # 각 층별로, 파이가 안전한지 나타냄.
        # [0] = 사용 X
        # [1] = {1:1, 2:0, 7:0}    : 1층. 1번 안전, 2번 위험, 7번 위험
        # [2] = {1:1, 4:0}         : 2층. 1번 안전, 4번 위험
        # 네트워크 객체의 safe_height가 실시간으로 업데이트 되니,
        # .get_safes_hegiht()로 계속 갖다써서 그래프에 이용하면 됨
        # self.safes_height = self.NetworkController.get_safes_height()

        # msg_from_admin = 'start checking'
        # if msg_from_admin == 'start checking':
        #     self.NetworkController.stop_accept()
        #     self.NetworkController.start_checking()

        #     if self.NetworkController.get_status() == 'emergency':
        #         self.NetworkController.start_emergency()
'''