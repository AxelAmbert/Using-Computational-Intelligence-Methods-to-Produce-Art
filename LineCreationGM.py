from GeneticModifier import *
import Line
from Connection import *
import random
import LineSplitGM
import LineRemoveGM

"""
    This class override GeneticModifier
    It is a Genetic Modifier that creates a new line
"""


class LineCreationGM(GeneticModifier):

    def __init__(self, probability):
        GeneticModifier.__init__(self, probability)

    def chose_a_fitting_line(self, lines):
        line = None
        point = None

        while line is None:
            rdm_line = random.choice(lines)
            for connection in rdm_line.connections:
                if connection.root.id == rdm_line.id:
                    line = rdm_line
                    point = connection.connection_parent
        return line, point



    def evolve(self, line, lines):
        line, point_of_creation = self.chose_a_fitting_line(lines)
        x_len, y_len = random.randrange(-50, 50), random.randrange(-50, 50)
        x_s, y_s, x_e, y_e = line.get_pos()

        if point_of_creation == 'start':
            new_line = Line.Line(-1, line, [x_s, x_s + x_len, y_s, y_s + y_len], None)
        else:
            new_line = Line.Line(-1, line, [x_e, x_e + x_len, y_e, y_e + y_len], None)
        new_connection = Connection().new(line, new_line, line, point_of_creation, 'start')

        line.add_connection(new_connection)
        new_line.add_connection(new_connection.reverse())
        lines.append(new_line)
        return True

