from GeneticModifier import *
import Line
from Connection import *
import random
import LineSplitGM
import LineRemoveGM


class LineCreationGM(GeneticModifier):

    def __init__(self, line, lines, probability):
        GeneticModifier.__init__(self, line, lines, probability)

    def get_random_from(self):
        return random.choice(['start', 'end'])

    def create_new_line(self):
        x_len, y_len = random.randrange(-100, 100), random.randrange(-100, 100)
        x_s, y_s, x_e, y_e = self.line.get_pos()
        new_line = Line.Line(-1, self.line, [x_s, x_s + x_len, y_s, y_s + y_len], None)
        new_connection = Connection().new(self.line, new_line, self.line, random.choice(['start', 'end']), 'start')

        self.line.add_connection(new_connection)
        new_line.add_connection(new_connection.reverse())
        self.lines.append(new_line)


    def apply_evolution(self):
        if random.random() > self.probability:
            return
        self.create_new_line()
