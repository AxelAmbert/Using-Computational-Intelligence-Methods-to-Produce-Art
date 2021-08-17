from GeneticModifier import *
import Line
from Connection import *
import random


class LineMovingGM(GeneticModifier):

    def __init__(self, probability):
        GeneticModifier.__init__(self, probability)

    def evolve(self, line, _):
        print('Move')
        xs = random.randint(-30, 30)
        ys = random.randint(-30, 30)
        xe = random.randint(-30, 30)
        ye = random.randint(-30, 30)

        line.move_pos(xs, ys, xe, ye)
