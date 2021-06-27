from tkinter import *
from CanvasHandler import *


class Main:

    def __init__(self):
        self.master = Tk()
        self.master.title("Biomorphs")
        self.canvas = CanvasHandler(self.master)

    def main(self):
        mainloop()


if __name__ == "__main__":
    Main().main()
