import random

class GeneticModifier:
    def __init__(self, propability):
        self.probability = propability

    def evolve(self, line, lines):
        return True

    def safe_remove(self, line, lines):
        try:
            lines.remove(line)
        except:
            pass

    def apply_evolution(self, lines):
        if len(lines) == 0:
            return False
        line = random.choice(lines)

        return self.evolve(line, lines)

