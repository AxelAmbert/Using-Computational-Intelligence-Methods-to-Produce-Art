import random


def randomize_probability(probability):
    probability += (probability * (random.randrange(-99, 99) / 100))
    return probability


"""
    This class handles genetic modifiers for a specific canvas
"""

class GeneticModifierHandler:

    def init_genetic_modifiers(self):
        modifiers = [('Creation', 0.005), ('Remove', 0.005), ('Split', 0.01), ('Moving', 0.01)]

        for (modifier_type, probability) in modifiers:
            fullname = 'Line' + modifier_type + 'GM'
            module = __import__(fullname)
            class_ = getattr(module, fullname)
            instance = class_(randomize_probability(probability))
            self.genetic_modifiers.append(instance)

    def sort_value(self, value):
        return value.probability

    def get_full_proabibilty_value(self):
        the_sum = 0.0

        for modifier in self.genetic_modifiers:
            the_sum += modifier.probability
        return the_sum

    def tower_sampling(self):
        i = 0
        tmp_sum = 0.0
        probability_sum = self.get_full_proabibilty_value()
        uniform_random = random.uniform(0, probability_sum)

        self.genetic_modifiers.sort(key=self.sort_value, reverse=True)
        for modifier in self.genetic_modifiers:
            i += 1
            tmp_sum += modifier.probability
            if tmp_sum >= uniform_random:
                return modifier
        return self.genetic_modifiers[len(self.genetic_modifiers) - 1]

    def start_evolution(self):
        choice = self.tower_sampling()
        choice.apply_evolution(self.canvas_handler.lines)
        self.canvas_handler.last_action = type(choice).__name__
        self.canvas_handler.recompute_canvas()

    def __init__(self, canvas_handler):
        self.genetic_modifiers = []
        self.init_genetic_modifiers()
        self.canvas_handler = canvas_handler
