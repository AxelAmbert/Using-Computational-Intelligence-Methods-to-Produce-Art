import math


class BiomorphIOConverter:

    def convert(self):
        pass

    def get_min_max_values(self):
        x_min, y_min, x_max, y_max = math.inf, math.inf, -math.inf, -math.inf

        for line in self.lines:
            x_s, y_s, x_e, y_e = line.get_pos()
            x_min = x_s if x_s < x_min else x_min
            x_min = x_e if x_e < x_min else x_min
            x_max = x_s if x_s > x_max else x_max
            x_max = x_e if x_e > x_max else x_max

            y_min = y_s if y_s < y_min else y_min
            y_min = y_e if y_e < y_min else y_min
            y_max = y_s if y_s > y_max else y_max
            y_max = y_e if y_e > y_max else y_max
        return [x_min, y_min, x_max, y_max]

    def encode_a_line(self, incoming_connection, pos, extremities):
        pass

    def reset_pos(self, connection, pos, extremities):
        pass

    def encode_recursively(self, line, incoming_connection, visited_lines, extremities):
        _, _, x_e, y_e = line.get_pos()
        visited_lines.append(line)

        self.encode_a_line(incoming_connection, line.get_pos(), extremities)
        for connection in line.connections:
            if connection.child not in visited_lines:
                self.reset_pos(connection, line.get_pos(), extremities)
                self.encode_recursively(connection.child, connection, visited_lines, extremities)

    def on_start(self, extremities):
        pass

    def on_finish(self):
        pass

    def modular_method(self):
        visited_lines = []
        extremities = self.get_min_max_values()
        if len(self.lines) < 1:
            return
        self.on_start(extremities)
        self.encode_recursively(self.lines[0], None, visited_lines, extremities)
        self.on_finish()

    def encode(self):
        pass

    def __init__(self, canvas, path):
        self.canvas = canvas
        self.lines = canvas.lines
        self.path = path
