class GeneticModifier:

    def __init__(self, line, lines, propability):
        self.line = line
        self.lines = lines
        self.probability = propability

    def update(self, line, lines):
        self.line = line
        self.lines = lines
