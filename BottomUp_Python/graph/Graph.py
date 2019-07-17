from connectDB.Pi import Pi
import copy
from connectDB.Vertex import Vertex


class Graph(object):
    def __init__(self, tables, pi_table, door_table):
        self.vertices = []
        self.number_of_vertices = 0
        self.pis = pi_table
        self.doors = door_table
        self.max_height = len(self.doors)
        # for table in tables:
        #     for vertex in table:
        #         if type(vertex) is Pi:
        #             new_vertex = Vertex(self.number_of_vertices, vertex)
        #             self.vertices.append(new_vertex)
        #             self.number_of_vertices += 1

        self.find_path()

    def find_path(self):
        path = [[] for _ in range(self.max_height)]
        for floor in range(self.max_height):
            path = self.find_path_on_floor(floor)

    def find_path_on_floor(self, height):
        doors_on_floor = self.doors[height]
        pis_on_floor = self.pis[height]
        result_pi = [[-1 for _ in range(4)] for _ in range(len(pis_on_floor))]

        for door in doors_on_floor:
            visit = list()
            queue = list()
            pis_for_bfs = copy.deepcopy(pis_on_floor)
            for direction in range(4):
                if(door.cross_datas[direction][0] != 'N'):
                    pi_number = int(door.cross_datas[direction][0])
                    weight = door.cross_datas[direction][1]
                    queue.append([pis_for_bfs[pi_number -1], weight, door.doorNumber])

            while queue:
                node = queue.pop(0)
                if isinstance(node[0], Pi) and node[0].piNumber not in visit:
                    pi = node[0]
                    pi_number = int(pi.piNumber);
                    visit.append(pi.piNumber)
                    for direction in range(4):
                        if pi.cross_datas[direction][0] != 'N':
                            target_pi_number = int(pi.cross_datas[direction][0])
                            if target_pi_number < 0:
                                continue
                            if pi.cross_datas[direction][0] == node[2] and int(node[2]) > 0:
                                a = int(node[2]) - 1
                                b = (direction + 2)%4
                                pi.cross_datas[direction][1] = pis_for_bfs[int(node[2]) - 1].cross_datas[(direction + 2)%4][1]
                                if(result_pi[pi_number-1][direction] == -1 or result_pi[pi_number-1][direction] > pi.cross_datas[direction][1]):
                                    result_pi[pi_number - 1][direction] = pi.cross_datas[direction][1]
                                continue

                            pi.cross_datas[direction][1] = pi.cross_datas[direction][1] + node[1]
                            target_pi = pis_for_bfs[target_pi_number - 1]
                            if target_pi.piNumber in visit and pi.cross_datas[direction][1] > target_pi.cross_datas[(direction + 2)%4][1]:
                                pi.cross_datas[direction][1] = target_pi.cross_datas[(direction + 2)%4][1]
                            else:
                                queue.append([target_pi, pi.cross_datas[direction][1], pi.piNumber])

        print(pis_for_bfs)

