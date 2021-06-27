from Connection import Connection


class Line:

    def __init__(self):
        self.connections = []
        self.pos_x_start = 0
        self.pos_x_end = 0
        self.pos_y_start = 0
        self.pos_y_end = 0

    def add_a_link(self, line):
        self.connections.append(Connection(self, line))