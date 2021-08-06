from GeneticModifier import *
import Line
from Connection import *
import random
import LineCreationGM
from LineRemoveGM import *


def update_linked_connection(old_line, new_line, connected_line):
    for connection in connected_line.connections:
        if connection.child is not None and connection.child.id == old_line.id:
            connection.child = new_line
        elif connection.parent is not None and connection.parent.id == old_line.id:
            connection.parent = new_line


class LineSplitGM(GeneticModifier):

    def __init__(self, line, lines, probability):
        GeneticModifier.__init__(self, line, lines, probability)

    def sort_connections(self):
        start = []
        end = []

        for connection in self.lines.connections:
            if connection.connection_parent == 'start':
                start.append(connection)
            else:
                end.append(connection)
        return start, end

    def assign_relevant_connections(self, line1, line2):
        start, end = self.sort_connections()

        line1.connections.append(start)
        line2.connections.append(end)

    def remove_old_connection_references(self, line1, line2):
        for connection in self.line.connections:
            if connection.parent is not None and connection.parent.id == self.line.id:
                if connection.connection_parent == 'start':
                    connection.parent = line1
                    line1.add_connection(connection)
                    update_linked_connection(self.line, line1, connection.child)
                elif connection.connection_parent == 'end':
                    connection.parent = line2
                    line2.add_connection(connection)
                    update_linked_connection(self.line, line2, connection.child)
            elif connection.child is not None and connection.child.id == self.line.id:
                if connection.connection_child == 'start':
                    connection.child = line1
                    line1.add_connection(connection)
                    update_linked_connection(self.line, line1, connection.parent)
                elif connection.connection_child == 'end':
                    connection.child = line2
                    line2.add_connection(connection)
                    update_linked_connection(self.line, line2, connection.parent)

    def recreate_connections(self, line1, line2):
        new_connection = Connection().new(line1, line2, line1, 'end', 'start')

        line1.connections.append(new_connection)
        line2.connections.append(new_connection.reverse())
        self.remove_old_connection_references(line1, line2)

    def convert(self, pos):
        x_s, y_s, x_e, y_e = pos
        return x_s, x_e, y_s, y_e

    def create_two_new_lines(self):
        x_b, y_b, x_e, y_e = self.line.get_pos()
        split_xb = x_b + ((x_e - x_b) / 2)
        split_yb = y_b + ((y_e - y_b) / 2)

        line1 = Line.Line(-1, self.line.parent, [x_b, split_xb, y_b, split_yb], '')
        line2 =  Line.Line(-1, line1, [split_xb, x_e, split_yb, y_e], '')
        self.recreate_connections(line1, line2)
        self.lines.append(line1)
        self.lines.append(line2)

    def apply_evolution(self):
        if random.random() > self.probability:
            return
        try:
            self.lines.remove(self.line)
        except:
            pass
        self.create_two_new_lines()
