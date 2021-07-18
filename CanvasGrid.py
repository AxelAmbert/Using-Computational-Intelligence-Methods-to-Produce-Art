import tkinter as tk
from CanvasHandler import *
import random
import time, threading


class CanvasGrid(tk.Frame):

    def init_canvas(self):
        for i in range(0, 3):
            for y in range(0, 3):
                c = CanvasHandler(self)
                c.set_size(100, 100)
                c.canvas.grid(column=i, row=y, columnspan=3)

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.init_canvas()
        self.grid_columnconfigure(0, weigth=1)
