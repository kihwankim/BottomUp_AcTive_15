from connectDB.Pi import Pi
from graph.Vertex import Vertex


class Graph(object):
    def __init__(self, tables):
        self.vertices = []
        self.number_of_vertices = 0
        for table in tables:
            for vertex in table:
                if type(vertex) is Pi:
                    new_vertex = Vertex(self.number_of_vertices, vertex)
                    self.vertices.append(new_vertex)
                    self.number_of_vertices += 1
