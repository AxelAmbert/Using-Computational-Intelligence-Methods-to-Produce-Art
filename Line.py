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
        self.joint_begin = None
        self.joint_end = None

    def add_connection(self, connection):
        self.connections.append(connection)

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
        if self.joint_begin is not None and self.joint_begin.id == joint_id:
            return True
        elif self.joint_end is not None and self.joint_end.id == joint_id:
            return True
        return False

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

    #
    # 1
    # 2
    # end
    # begin
    #
    def compute_connection_update(self, connection, deep):
        x = getattr(connection.parent, 'pos_x_' + connection.connection_parent)
        y = getattr(connection.parent, 'pos_y_' + connection.connection_parent)
        setattr(self, 'pos_x_' + connection.connection_child, x)
        setattr(self, 'pos_y_' + connection.connection_child, y)
        if deep is True:
            self.update_connections(deep=False)

    def update_connections(self, deep=True):
        for connection in self.connections:
            connection.child.compute_connection_update(connection, deep)


    def move_pos(self, xs, ys, xe, ye):
        self.set_pos([self.pos_x_start + xs, self.pos_y_start + ys, self.pos_x_end + xe, self.pos_y_end + ye])
        self.update_connections()

    def get_joint_pos(self, joint_id):
        if self.joint_begin.id == joint_id:
            return self.joint_begin.where
        elif self.joint_end.id == joint_id:
            return self.joint_end.where
        return 'unset'

    def __str__(self):
        string = 'Id :' + str(self.id) + ' | \nConnections: '
        for connection in self.connections:
            string += connection.__str__()
        return string + '\n'

