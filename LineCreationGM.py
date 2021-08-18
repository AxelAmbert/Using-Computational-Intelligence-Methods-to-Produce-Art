from GeneticModifier import *
import Line
from Connection import *
import random
import LineSplitGM
import LineRemoveGM


class LineCreationGM(GeneticModifier):

    def __init__(self, probability):
        GeneticModifier.__init__(self, probability)

    def evolve(self, line, lines):

        random_creation = random.choice(['start', 'end'])
        new_line = None
        x_len, y_len = random.randrange(-100, 100), random.randrange(-100, 100)
        x_s, y_s, x_e, y_e = line.get_pos()
        if random_creation == 'start':
            new_line = Line.Line(-1, line, [x_s, x_s + x_len, y_s, y_s + y_len], None)
        else:
            new_line = Line.Line(-1, line, [x_e, x_e + x_len, y_e, y_e + y_len], None)
        new_connection = Connection().new(line, new_line, line, random_creation, 'start')

        line.add_connection(new_connection)
        new_line.add_connection(new_connection.reverse())
        lines.append(new_line)
        return True

