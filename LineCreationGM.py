from GeneticModifier import *
from Line import *
from Connection import *
import random


class LineCreationGM(GeneticModifier):

    def __init__(self, line, lines, probability):
        GeneticModifier.__init__(self, line, lines, probability)

    def create_new_line(self):
        x_len, y_len = random.randrange(-100, 100), random.randrange(-100, 100)
        x_s, x_e, y_s, y_e = self.line.get_pos()
        new_line = Line(-1, self.line, [])

    def apply_evolution(self):
        if random.random() > self.probability:
            return
        self.create_new_line()
