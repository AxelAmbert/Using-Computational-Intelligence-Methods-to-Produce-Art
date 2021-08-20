from GeneticModifier import *
import Line
from Connection import *
import random
import LineCreationGM
from LineRemoveGM import *

"""
    This class override GeneticModifier
    It is a Genetic Modifier that split a line into two new lines
    After the process the base line is removed
"""


class LineSplitGM(GeneticModifier):

    def __init__(self, probability):
        self.line = None
        self.lines = None
        GeneticModifier.__init__(self, probability)

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

    def update_linked_connection(self, old_line, new_line, connected_line):
        for connection in connected_line.connections:
            if connection.child is not None and connection.child.id == old_line.id:
                connection.child = new_line
            if connection.root is not None and connection.root.id == old_line.id:
                connection.root = new_line

    def remove_old_connection_references(self, line1, line2):
        for connection in self.line.connections:
            new_connection = connection.copy()
            if connection.connection_parent == 'start':
                new_connection.parent = line1
                line1.add_connection(new_connection)
                self.update_linked_connection(self.line, line1, new_connection.child)
            elif connection.connection_parent == 'end':
                new_connection.parent = line2
                line2.add_connection(new_connection)
                self.update_linked_connection(self.line, line2, new_connection.child)

    def recreate_connections(self, line1, line2):
        new_connection = Connection().new(line1, line2, line1, 'end', 'start')

        line1.connections.append(new_connection)
        line2.connections.append(new_connection.reverse())
        self.remove_old_connection_references(line1, line2)

    def convert(self, pos):
        x_s, y_s, x_e, y_e = pos
        return x_s, x_e, y_s, y_e

    def get_two_uniques_ids(self):
        ids = []
        fail = False

        while len(ids) != 2:
            rdm = random.randint(0, 9223372036854775807)
            for line in self.lines:
                if line.id == rdm:
                    fail = True
                    break
            if fail is False and rdm not in ids:
                ids.append(rdm)
        return ids

    def create_two_new_lines(self):
        x_b, y_b, x_e, y_e = self.line.get_pos()
        split_xb = x_b + ((x_e - x_b) / 2)
        split_yb = y_b + ((y_e - y_b) / 2)
        ids = self.get_two_uniques_ids()

        line1 = Line.Line(ids[0], self.line.parent, [x_b, split_xb, y_b, split_yb], '')
        line2 = Line.Line(ids[1], line1, [split_xb, x_e, split_yb, y_e], '')
        self.recreate_connections(line1, line2)
        self.lines.append(line1)
        self.lines.append(line2)

    def evolve(self, line, lines):
        self.line = line
        self.lines = lines
        self.safe_remove(self.line, self.lines)
        self.create_two_new_lines()
        return True
