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
        x_e = random.randint(-15, 15)
        y_e = random.randint(-15, 15)
        line.move_pos(x_e, y_e)



    def apply_random(self):
        lines = self.canvas.get_lines()
        line_to_modify = self.get_a_line_to_modify(lines)

        if line_to_modify is None:
            return
        self.apply_random_to_line(line_to_modify)
        self.canvas.recompute_canvas()



    def init_button(self):
        button = Button(self.master, text="Press to add random gen", command=self.wait_and_start)
        button.pack()
        return button

    def __init__(self):
        self.master = Tk()
        self.master.title("Biomorphs")
        self.canvas = CanvasHandler(self.master)
        self.button = self.init_button()

    def rand(self):
        self.apply_random()
        threading.Timer(0.01, self.rand).start()

    def wait_and_start(self):
        threading.Timer(0.01, self.rand).start()



    def main(self):
        mainloop()


if __name__ == "__main__":
    Main().main()
