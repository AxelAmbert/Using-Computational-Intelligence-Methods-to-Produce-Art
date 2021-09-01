from GeneticModifier import *
from Line import *
from Connection import *
import random

"""
    This class override GeneticModifier
    It is a Genetic Modifier that removes a line
"""


class LineRemoveGM(GeneticModifier):

    def __init__(self, probability):
        self.visited_lines = []
        self.found = False
        self.line = None
        self.lines = None
        self.lines_to_remove = []
        self.visited_connections = []
        GeneticModifier.__init__(self, probability)

    def line_has_not_been_visited(self, line_to_test):
        for line in self.visited_lines:
            if line.id == line_to_test.id:
                return False
        return True

    def old_look_for_line_looping(self, line):
        for connection in list(filter(lambda c: c.connection_parent == 'end', line.connections)):
            if self.found == True or (connection.child is not None and connection.child.id == self.line.id):
                self.found = True
                return
            elif line.id != self.line.id:
                self.visited_lines.append(line)
            if self.line_has_not_been_visited(connection.child) is True:
                self.look_for_line_looping(connection.child)

    def is_a_non_root_connection(self, line):
        for connection in self.line.connections:
            if connection.root.id == self.line.id:
                continue
            return True
        return False

    # test each line to know if it can find every other lines
    def look_for_line_looping(self, line):
        if line.id != self.line.id:
            self.visited_lines.append(line)
        for connection in line.connections:
            if self.found is True or self.is_a_non_root_connection(self.line):
                self.found = True
                return
            if connection.child not in self.visited_lines:
                self.look_for_line_looping(connection.child)

    def can_find_every_other_lines(self, line):
        for connection in line.connections:
            if connection.child.id != self.line.id and connection.child not in self.visited_lines:
                self.visited_lines.append(connection.child)
                self.can_find_every_other_lines(connection.child)

    def not_a_connection(self, line_to_test):
        indirectly_linked = []
        good_connections = list(filter(lambda c: True if c.child.id != c.root.id else False, self.line.connections))

        self.get_indirectly_linked(indirectly_linked, good_connections)

        for line in indirectly_linked:
            for connection in line.connections:
                if line_to_test.id == connection.child.id:
                    return False
        return True

    def has_found_every_line(self):
        line_buff = list(filter(self.not_a_connection, self.lines))
        is_found = False
        self.visited_lines.append(self.line)

        for line_to_find in line_buff:
            for visited_line in self.visited_lines:
                if line_to_find.id == visited_line.id:
                    is_found = True
                    break
            if is_found is False:
                return False
            is_found = False
        return True

    def is_deleted(self, connection, lines_to_remove):
        for line in lines_to_remove:
            if line.id == connection.child.id:
                return False
        return True

    # This function determines if it worth or not to delete the line
    # It consider the number of lines deleted compared to the number of total line
    # It then applies a random number to see if the delete operation will happen
    def worth_removing(self, lines_to_remove):
        rdm = random.random()
        percent = len(self.lines) / len(lines_to_remove)

        return rdm > percent

    def remove_lines(self, lines_to_remove):
        if self.worth_removing(lines_to_remove) is False:
            return
        for line in self.lines:
            line.connections = list(filter(lambda c: self.is_deleted(c, lines_to_remove), line.connections))

        for line in lines_to_remove:
            if len(self.lines) == 1:
                break
            self.safe_remove(line, self.lines)

    def get_every_line_to_remove(self, line):
        for connection in line.connections:
            if connection.child not in self.visited_connections:
                self.visited_connections.append(connection.child)
                self.visited_lines = []
                self.can_find_every_other_lines(connection.child)
                if self.has_found_every_line() is False:
                    self.lines_to_remove.append(connection.child)
                self.get_every_line_to_remove(connection.child)

    def get_indirectly_linked(self, arr, connections):
        for connection in connections:
            if connection.child.id != connection.root.id and connection.child not in arr:
                arr.append(connection.child)
                self.get_indirectly_linked(arr, connection.child.connections)

    def apply_remove(self):
        self.lines_to_remove = [self.line]
        self.visited_connections = [self.line]
        self.get_every_line_to_remove(self.line)
        self.remove_lines(self.lines_to_remove)

    def old_test(self):
        lines_to_remove = [self.line]

        for connection in self.line.connections:
            self.visited_lines = []
            self.can_find_every_other_lines(connection.child)
            if self.has_found_every_line() is False:
                lines_to_remove.append(connection.child)

        self.remove_lines(lines_to_remove)

    def get_a_random_line(self):
        connection = random.choice(list(filter(lambda c: c.connection_parent == 'end', self.line.connections)))
        return connection.child

    def is_not_the_owner_line(self, connection):
        for line in self.deleted_line:
            if connection.child is not None and connection.child.id == line.id:
                return False
            elif connection.parent is not None and connection.parent.id == line.id:
                return False
        return True

    def remove_every_lost_connection(self):
        for line in self.lines:
            line.connections = list(filter(self.is_not_the_owner_line, line.connections))

    def replace_connection(self, connection, new_base):
        if connection.child is not None and connection.child.id == self.line.id:
            connection.child = new_base
        elif connection.parent is not None and connection.parent.id == self.line.id:
            connection.parent = new_base

    def only_delete_line_old(self):
        new_base = self.get_a_random_line()
        for connection in self.line.connections:
            self.replace_connection(connection, new_base)

    def only_delete_line(self):
        self.safe_remove(self.line, self.lines)
        for connection in self.line.connections:
            if len(connection.child.connections) <= 1:
                self.safe_remove(connection.child, self.lines)
        self.remove_every_lost_connection()

    def is_unvisited(self, connection):
        for line in self.visited_lines:
            if connection.root is not None and connection.child.id == line.id:
                return False
        return True

    def delete_everything_connected(self, line):
        if len(self.lines) <= 0:
            return
        self.visited_lines.append(line)
        for connection in list(filter(self.is_unvisited, line.connections)):
            if connection.child is not None and connection.child.id != connection.root.id:
                self.delete_everything_connected(connection.child)
        self.safe_remove(line, self.lines)

    def reset(self):
        self.found = False
        self.visited_lines = []

    def security_remove(self):
        for line in self.lines:
            if len(line.connections) == 0 and len(self.lines) > 1:
                self.safe_remove(line, self.lines)
                self.security_remove()
                return

    def remove_line(self):
        if len(self.line.connections) == 0:
            return
        self.look_for_line_looping(self.line)
        self.apply_remove()

    def evolve(self, line, lines):
        if line.id == lines[0].id or len(lines) <= 1:
            return False
        self.reset()
        self.line = line
        self.lines = lines
        self.remove_line()
        self.reset()
        return True
