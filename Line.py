import LineSplitGM
from LineCreationGM import *
import LineRemoveGM


def random_color():
    t = '#'

    for i in range(0, 6):
        t += str(random.randint(0, 9))
    return t

"""
    This class represents a line and every useful information about a specific line
"""

class Line:

    def __init__(self, line_id, parent, positions, tag):
        self.id = line_id
        self.parent = parent
        self.connections = []
        self.pos_x_start = positions[0]
        self.pos_x_end = positions[1]
        self.pos_y_start = positions[2]
        self.pos_y_end = positions[3]
        self.tag = tag
        self.joint_begin = None
        self.joint_end = None
        self.redraw = True
        self.color = random_color()


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
        if self.pos_x_start != pos[0] or self.pos_y_start != pos[1] or \
                self.pos_x_end != pos[2] or self.pos_y_end != pos[3]:
            self.redraw = True

        self.pos_x_start = pos[0]
        self.pos_y_start = pos[1]
        self.pos_x_end = pos[2]
        self.pos_y_end = pos[3]

    def compute_connection_update(self, connection):
        impact = []

        x = getattr(connection.parent, 'pos_x_' + connection.connection_parent)
        y = getattr(connection.parent, 'pos_y_' + connection.connection_parent)
        x_child = getattr(self, 'pos_x_' + connection.connection_child)
        y_child = getattr(self, 'pos_y_' + connection.connection_child)

        if x != x_child or y != y_child:
            setattr(self, 'pos_x_' + connection.connection_child, x)
            setattr(self, 'pos_y_' + connection.connection_child, y)
            impact.append(connection.connection_child)
        self.redraw = True

        self.update_connections(impact)

    """
        This function is called when the line moves
        It then go recursively through every other connections to move them accordingly
    """
    def update_connections(self, impact):
        for connection in self.connections:
            if connection.connection_parent in impact:
                connection.child.compute_connection_update(connection)

    def move_pos(self, xs, ys, xe, ye):
        impact = []

        if xs != 0 or ys != 0:
            impact.append('start')
        if xe != 0 or ye != 0:
            impact.append('end')

        self.set_pos([self.pos_x_start + xs, self.pos_y_start + ys, self.pos_x_end + xe, self.pos_y_end + ye])
        self.update_connections(impact)

    def get_joint_pos(self, joint_id):
        if self.joint_begin.id == joint_id:
            return self.joint_begin.where
        elif self.joint_end.id == joint_id:
            return self.joint_end.where
        return 'unset'

    """
        Scale the line size and pos to a new ratio
    """
    def scale(self, old_size, new_size):
        old_size_x, old_size_y = old_size
        new_size_x, new_size_y = new_size
        ratio_x = old_size_x / new_size_x
        ratio_y = old_size_y / new_size_y

        self.pos_x_start /= ratio_x
        self.pos_x_end /= ratio_x
        self.pos_y_start /= ratio_y
        self.pos_y_end /= ratio_y

    def copy(self):
        lin = Line(self.id, self.parent, [self.pos_x_start, self.pos_x_end, self.pos_y_start, self.pos_y_end], self.tag)

        for connection in self.connections:
            lin.connections.append(connection.copy())
        return lin

    def __str__(self):
        string = 'Id :' + str(self.id) + ' Color ' + str(self.color) + '| \nConnections: \n'
        for connection in self.connections:
            string += connection.__str__()
        return string + '\n'
