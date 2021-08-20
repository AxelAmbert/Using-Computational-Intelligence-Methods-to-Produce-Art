from BiomorphIOConverter import *
from tkinter import PhotoImage

"""
    Override class of BiomorphIOConverter
    This class convert a Biomorph into a Postscript file
"""


class BiomorphIOConverterPostscript(BiomorphIOConverter):

    def __init__(self, canvas, path):
        BiomorphIOConverter.__init__(self, canvas, path)

    def encode(self):
        self.canvas.canvas.postscript(file=self.path, colormode='color')
