from BiomorphIOConverter import *


class BiomorphIOConverterGCode(BiomorphIOConverter):

    def reset_needle(self, connection, pos, extremities):
        x_s, y_s, x_e, y_e = pos

        if connection.connection_parent == 'start':
            self.buffer.append('G0 X' + str(x_s - extremities[0]) + ' Y' + str(-y_s))
        else:
            self.buffer.append('G0 X' + str(x_e - extremities[0]) + ' Y' + str(-y_e))

    def print_a_line(self, incoming_connection, pos, extremities):
        x_s, y_s, x_e, y_e = pos

        if incoming_connection is None or incoming_connection.connection_child == 'start':
            self.buffer.append('G1 X' + str(x_e - extremities[0]) + ' Y' + str(-y_e))
        else:
            self.buffer.append('G1 X' + str(x_s - extremities[0]) + ' Y' + str(-y_s))

    def init_first_line(self, extremities):
        x_s, y_s, _, _ = self.lines[0].get_pos()

        self.buffer.append('G0 X' + str(x_s - extremities[0]) + ' Y' + str(-y_s))

    def write_to_file(self):
        with open(self.path, 'w') as file:
            for instruction in self.buffer:
                file.write(instruction + '\n')

    def __init__(self, canvas, path):
        BiomorphIOConverter.__init__(self, canvas, path)
        self.buffer = []
        self.on_start = self.init_first_line
        self.encode_a_line = self.print_a_line
        self.reset_pos = self.reset_needle
        self.on_finish = self.write_to_file

    def encode(self):
        self.modular_method()
