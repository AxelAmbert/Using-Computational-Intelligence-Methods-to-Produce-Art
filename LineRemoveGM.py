from GeneticModifier import *
from Line import *
from Connection import *
import random


class LineRemoveGM(GeneticModifier):

    def __init__(self, line, lines, probability):
        self.visited_lines = []
        self.found = False
        GeneticModifier.__init__(self, line, lines, probability)

    def line_has_not_been_visited(self, line_to_test):
        for line in self.visited_lines:
            if line.id == line_to_test.id:
                return False
        return True

    def look_for_line_looping(self, line):
        for connection in list(filter(lambda c: c.connection_parent == 'end', line.connections)):
            if self.found == True or (connection.child is not None and connection.child.id == self.line.id):
                self.found = True
                return
            elif line.id != self.line.id:
                self.visited_lines.append(line)
            if self.line_has_not_been_visited(connection.child) is True:
                self.look_for_line_looping(connection.child)

    def get_a_random_line(self):
        connection = random.choice(list(filter(lambda c: c.connection_parent == 'end', self.line.connections)))
        if connection.child is not None and connection.child.id != self.line.id:
            return connection.child
        return connection.parent

    def is_not_the_owner_line(self, connection):
        if connection.child is not None and connection.child.id == self.line.id:
            return False
        elif connection.parent is not None and connection.parent.id == self.line.id:
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

    def only_delete_line(self):
        new_base = self.get_a_random_line()
        for connection in self.line.connections:
            self.replace_connection(connection, new_base)

    def is_unvisited(self, connection):
        for line in self.visited_lines:
            if connection.root is not None and connection.child.id == line.id:
                return False
        return True

    def delete_everything_connected(self, line):
        self.visited_lines.append(line)
        for connection in list(filter(self.is_unvisited, line.connections)):
            print('Im line ' + str(line.id) + ', lets go to ' + str(connection.child.id))
            if connection.child is not None and connection.child.id != connection.root.id:
                self.delete_everything_connected(connection.child)
        try:
            self.lines.remove(line)
        except:
            pass

    def remove_line(self):
        if len(self.line.connections) == 0:
            pass

        self.look_for_line_looping(self.line)
        if self.found is True:
            self.only_delete_line()
            self.lines.remove(self.line)
            self.remove_every_lost_connection()
        else:
            self.visited_lines = []
            self.delete_everything_connected(self.line)
            self.remove_every_lost_connection()
        self.security_remove()

    def reset(self):
        self.found = False
        self.visited_lines = []

    def security_remove(self):
        for line in self.lines:
            if len(line.connections) == 0 and len(self.lines) > 1:
                self.lines.remove(line)
                self.security_remove()
                return


    def apply_evolution(self, force=False):
        if (random.random() > self.probability and force is False) or len(self.lines) <= 1:
            return
        if self.line.id == self.lines[0].id:
            return
        self.remove_line()
        self.reset()
