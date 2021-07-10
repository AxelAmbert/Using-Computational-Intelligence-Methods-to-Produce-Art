from Connection import Connection


class Line:

    x = 0

    def __init__(self, parent, positions, tag):
        Line.x = Line.x + 1
        self.id = Line.x
        self.parent = parent
        self.begin_connections = []
        self.end_connections = []
        self.pos_x_start = positions[0]
        self.pos_x_end = positions[1]
        self.pos_y_start = positions[2]
        self.pos_y_end = positions[3]
        self.tag = tag
        self.joint_begin = None
        self.joint_end = None

    def add_a_link_begin(self, line):
        self.begin_connections.append(line)

    def add_a_link_end(self, line):
        self.end_connections.append(line)

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
        return joint_id == self.joint_begin.id or joint_id == self.joint_end.id

    def get_id(self):
        return self.id


    def set_id(self, newId):
        self.id = newId

    def get_pos(self):
        return self.pos_x_start, self.pos_y_start, self.pos_x_end, self.pos_y_end

    def set_pos(self, pos):
        self.pos_x_start = pos[0]
        self.pos_y_start = pos[1]
        self.pos_x_end = pos[2]
        self.pos_y_end = pos[3]

    def update_connections(self):
        for connection in self.begin_connections:
            connection.compute_parent_update()

    def compute_parent_update(self):
        self.pos_x_start = self.parent.pos_x_end
        self.pos_y_start = self.parent.pos_y_end

    def compute_child_update(self, child):
        self.pos_x_end = child.pos_x_start
        self.pos_y_end = child.pos_y_start
        self.update_connections()

    def move_pos(self, x, y):
        self.set_pos([self.pos_x_start + x, self.pos_y_start + y, self.pos_x_end + x, self.pos_y_end + y])
        if self.parent is not None:
            self.parent.compute_child_update(self)
        self.update_connections()


    def __str__(self):
        string = 'Id :' + str(self.id) + ' | Connections: '
        for connection in self.begin_connections:
            string += str(connection.get_id()) + ', '
        return string + '\n'
