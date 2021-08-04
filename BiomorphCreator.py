import tkinter as tk
from CanvasHandler import *
import random
import time, threading


class BiomorphCreator(tk.Frame):
    def get_a_line_to_modify(self, lines):
        if len(lines) == 0:
            return None
        return lines[random.randint(0, len(lines) - 1)]

    def apply_random_to_line(self, line):
        xs = random.randint(-15, 15)
        ys = random.randint(-15, 15)
        xe = random.randint(-15, 15)
        ye = random.randint(-15, 15)

        line.move_pos(xs, ys, xe, ye)

    def apply_random(self):
        lines = self.canvas.get_lines()
        line_to_modify = self.get_a_line_to_modify(lines)

        if line_to_modify is None:
            return
        self.apply_random_to_line(line_to_modify)
        self.canvas.recompute_canvas(simulation=self.sim)

    def change_view(self):
        self.controller.show_frame('EvolutionView', self.canvas.lines)

    def init_button(self):
        button = Button(self, text="Press to add random gen", command=self.wait_and_start)
        button.pack()
        return button

    def rand(self):
        self.apply_random()
        if self.sim is True:
            threading.Timer(0.3, self.rand).start()

    def wait_and_start(self):
        if self.sim is False:
            self.sim = True
            threading.Timer(0.3, self.rand).start()
        else:
            self.sim = False

    def update_with_data(self, lines):
        pass

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.canvas = CanvasHandler(self)
        self.canvas.canvas.pack(expand=YES, fill=BOTH)
        self.button = self.init_button()
        self.sim = False
