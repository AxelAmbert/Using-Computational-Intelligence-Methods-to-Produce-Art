from tkinter import *
from CanvasHandler import *
import random
import time, threading

class Main:

    def get_a_line_to_modify(self, lines):
        if len(lines) == 0:
            return None
        return lines[random.randint(0, len(lines) - 1)]

    def apply_random_to_line(self, line):
        xs = random.randint(-50, 50)
        ys = random.randint(-50, 50)
        xe = random.randint(-50, 50)
        ye = random.randint(-50, 50)

        line.move_pos(xs, ys, xe, ye)



    def apply_random(self):
        lines = self.canvas.get_lines()
        line_to_modify = self.get_a_line_to_modify(lines)

        if line_to_modify is None:
            return
        self.apply_random_to_line(line_to_modify)
        self.canvas.recompute_canvas(simulation=self.sim)



    def init_button(self):
        button = Button(self.master, text="Press to add random gen", command=self.wait_and_start)
        button.pack()
        return button

    def __init__(self):
        self.master = Tk()
        self.master.title("Biomorphs")
        self.canvas = CanvasHandler(self.master)
        self.button = self.init_button()
        self.sim = False

    def rand(self):
        self.apply_random()
        if self.sim is True:
            threading.Timer(0.1, self.rand).start()

    def wait_and_start(self):
        if self.sim is False:
            self.sim = True
            threading.Timer(0.0001, self.rand).start()
        else:
            self.sim = False


    def main(self):
        mainloop()


if __name__ == "__main__":
    Main().main()
