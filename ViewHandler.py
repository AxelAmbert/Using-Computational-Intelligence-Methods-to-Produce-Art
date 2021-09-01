from tkinter import font as tkfont
from BiomorphCreator import *
from EvolutionView import *


class ViewHandler(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Using Computational Intelligence to Produce Art')
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.resizable(False, False)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (BiomorphCreator, EvolutionView):
            page_name = F.__name__
            frame = F(parent=container, controller=self, )
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("BiomorphCreator")

    def show_frame(self, page_name, data=None):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.update_with_data(data)
        frame.tkraise()


