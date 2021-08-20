import tkinter as tk
from CanvasHandler import *
import random
import threading
from BiomorphIOConverterGCode import *
from BiomorphIOConverterPostscript import *
from LineRemoveGM import *


"""
    This class is representing the Tkinter view: BiomorphCreator.
    In this view the user design its Biomorph before sending it
    to the evolution process.
"""
class BiomorphCreator(tk.Frame):

    def get_a_line_to_modify(self, lines):
        if len(lines) == 0:
            return None
        return lines[random.randint(0, len(lines) - 1)]

    def apply_random_to_line(self, line):
        xs = random.randint(-30, 30)
        ys = random.randint(-30, 30)
        xe = random.randint(-30, 30)
        ye = random.randint(-30, 30)

        line.move_pos(xs, ys, xe, ye)

    def apply_random(self):
        lines = self.canvas.get_lines()
        line_to_modify = self.get_a_line_to_modify(lines)

        if line_to_modify is None:
            return
        self.apply_random_to_line(line_to_modify)
        self.canvas.recompute_canvas()

    def change_view(self):
        self.controller.show_frame('EvolutionView', self.canvas)

    def init_button(self):
        button = Button(self, text="Evolve", command=self.change_view)
        button.pack()
        return button

    def prev_and_next_buttons(self):
        Button(self, text="prev", command=lambda: self.canvas.history_jump(-1)).pack()
        Button(self, text="next", command=lambda: self.canvas.history_jump(1)).pack()

    def rand(self):
        self.apply_random()
        if self.sim is True:
            threading.Timer(0.05, self.rand).start()

    def wait_and_start(self):
        if self.sim is False:
            self.sim = True
            threading.Timer(0.05, self.rand).start()
        else:
            self.sim = False

    def update_with_data(self, data):
        pass

    def ok(self):
        k = LineRemoveGM(100)
        k.evolve(self.canvas.lines[3], self.canvas.lines)
        self.canvas.reconstruct(self.canvas.lines, self.canvas.size)

    def butt_g_code(self):
        pass
        #Button(self, text="g_code", command=lambda: BiomorphIOConverterGCode(self.canvas, 'test.txt').encode()).pack()
        #Button(self, text="png", command=lambda: BiomorphIOConverterPNG(self.canvas, 'test.eps').encode()).pack()
        Button(self, text="go", command=self.ok).pack()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.canvas = CanvasHandler(self)
        self.canvas.canvas.pack(expand=YES, fill=BOTH)
        self.button = self.init_button()
        self.prev_and_next_buttons()
        self.sim = False
        self.canvas.set_history_status(True)
        self.butt_g_code()
