from BiomorphIOConverter import *
from tkinter import PhotoImage

class BiomorphIOConverterPNG(BiomorphIOConverter):

    def __init__(self, canvas, path):
        BiomorphIOConverter.__init__(self, canvas, path)

    def encode(self):
        self.canvas.canvas.postscript(file=self.path, colormode='color')
