import tkinter as tk
from CanvasHandler import *
import random
import time, threading
from CanvasGrid import *


class EvolutionView(tk.Frame):

    def init_canvas_array(self):
        for i in range(0, 3):
            for y in range(0, 3):
                tmp_canvas = CanvasHandler(self)
                tmp_canvas.set_size(250, 250)
                tmp_canvas.canvas.grid(column=i, row=y, padx=(50, 50), pady=(25, 25))
                #tmp_canvas.lock()
                self.canvas_array.append(tmp_canvas)

    def init_slider(self):
        s = Scale(self, from_=0, to=10, orient=HORIZONTAL)
        s.set(1)
        s.grid(column=1, row=4)
        return s

    def init_label(self):
        l = Label(self, text='Change speed')
        l.grid(column=1, row=3)


    def update_with_data(self, lines):
        if lines is None:
            return
        for canvas in self.canvas_array:
            canvas.reconstruct(lines, [100, 100])

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,  bg='#000000')
        self.controller = controller
        self.canvas_array = []
        self.init_canvas_array()
        self.init_label()
        self.slider = self.init_slider()

