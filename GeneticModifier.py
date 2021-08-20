import random

"""
    Base class of every genetic modifier
    Override this class to create new genetic modifier
"""

class GeneticModifier:
    def __init__(self, probability):
        self.probability = probability
        self.deleted_line = []

    def evolve(self, line, lines):
        return True

    def safe_remove(self, line, lines):
        try:
            lines.remove(line)
            self.deleted_line.append(line)
        except:
            pass

    def apply_evolution(self, lines):
        if len(lines) == 0:
            return False
        line = random.choice(lines)

        return self.evolve(line, lines)

