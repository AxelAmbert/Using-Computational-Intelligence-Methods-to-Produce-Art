from GeneticModifier import *
import Line
from Connection import *
import random


"""
    This class override GeneticModifier
    It is a Genetic Modifier that moves a line
"""


class LineMovingGM(GeneticModifier):

    def __init__(self, probability):
        GeneticModifier.__init__(self, probability)

    def evolve(self, line, _):
        xs = random.randint(-30, 30)
        ys = random.randint(-30, 30)
        xe = random.randint(-30, 30)
        ye = random.randint(-30, 30)

        line.move_pos(xs, ys, xe, ye)
