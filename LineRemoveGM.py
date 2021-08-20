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

    #TODO look screenshot
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

    def not_a_connection(self, line):
        for connection in self.line.connections:
            if line.id == connection.child.id:
                return False
        return True

    def has_found_every_line(self):
        line_buff = list(filter(self.not_a_connection, self.lines))
        is_found = False
        self.visited_lines.append(self.line)

        for line in line_buff:
            for existing_line in self.visited_lines:
                if line.id == existing_line.id:
                    is_found = True
                    break
            if is_found is False:
                return False
            is_found = False
        return True

    def test(self):
        lines_to_remove = []

        for connection in self.line.connections:
            self.can_find_every_other_lines(connection.child)
            if self.has_found_every_line() is False:
                lines_to_remove.append(connection.child)
        for line in lines_to_remove:
            self.delete_everything_connected(line)

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
        #self.test()
        if self.found is True:
            print('Found')
            self.test()
            #self.only_delete_line()
            #self.safe_remove(self.line, self.lines)
            #self.remove_every_lost_connection()
        else:
            print('Not found')
            self.visited_lines = []
            self.delete_everything_connected(self.line)
            self.remove_every_lost_connection()
            self.security_remove()

    def evolve(self, line, lines):
        if line.id == lines[0].id or len(lines) <= 1:
            return False
        self.reset()
        self.line = line
        self.lines = lines
        self.remove_line()
        self.reset()
        return True
