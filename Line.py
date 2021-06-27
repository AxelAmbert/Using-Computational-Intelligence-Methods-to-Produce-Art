from Connection import Connection


class Line:

    x = 0

    def __init__(self, parent, positions, tag):
        Line.x = Line.x + 1
        self.id = Line.x
        self.parent = parent
        self.connections = []
        self.pos_x_start = positions[0]
        self.pos_x_end = positions[1]
        self.pos_y_start = positions[2]
        self.pos_y_end = positions[3]
        self.tag = tag
        self.joint_begin = -1
        self.joint_end = -1

    def add_a_link(self, line):
        self.connections.append(line)

    def get_start(self):
        return self.pos_x_start, self.pos_y_start

    def get_end(self):
        return self.pos_x_end, self.pos_y_end

    def set_join_values(self, begin, end):
        self.joint_begin = begin
        self.joint_end = end

    def get_joint_values(self):
        return self.joint_begin, self.joint_end

    def has_joint_ownership(self, joint_id):
        return joint_id == self.joint_begin or joint_id == self.joint_end

    def get_id(self):
        return self.id

    def __str__(self):
        string = 'Id :' + str(self.id) + ' | Connections: '
        for connection in self.connections:
            string += str(connection.get_id()) + ', '
        return string + '\n'
