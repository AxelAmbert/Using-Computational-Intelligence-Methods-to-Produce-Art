from tkinter import *
from Line import *
import random

class CanvasHandler:

    def random_color(self):
        t = '#'

        for i in range(0, 6):
            t += str(random.randint(0, 9))
        return t

    def remove_previous_joints(self):
        x = 1
        #print(self.canvas.find_withtag('joint'))

    def draw_joints(self):
        col = self.random_color()
        for line in self.lines:
            x, y = line.get_start()
            self.canvas.create_rectangle(x - 10, y - 10, x + 10, y + 10,  width=10, outline=col, fill=col, tags='joint')
            x, y = line.get_end()
            self.canvas.create_rectangle(x - 10, y - 10, x + 10, y + 10,  width=10, outline=col,fill=col, tags='joint')

    def redraw_joints(self):
        self.remove_previous_joints()
        self.draw_joints()

    def verify_line_validity(self, event):
        if len(self.lines) == 0:
            print("cua")
            return True
        overlaps = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        print(overlaps)
        if len(overlaps) > 0:
            print(overlaps[0])
            print(self.canvas.gettags(overlaps[0]))

    def on_press(self, event):
        self.verify_line_validity(event)
        self.allow_drawing = True
        self.x1, self.y1 = (event.x - 1), (event.y - 1)

    def on_release(self, _):
        self.allow_drawing = False
        self.lines.append(Line([self.x1, self.x2, self.y1, self.y2], self.drawn_line_tmp))
        self.redraw_joints()

    def on_move(self, event):
        if self.allow_drawing == False:
            return

        self.x2, self.y2 = (event.x + 1), (event.y + 1)
        self.canvas.delete(self.drawn_line_tmp)
        self.drawn_line_tmp = self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, width=4, fill="#476042")

    def overlap(self, event):
        print(self.canvas.find_overlapping(event.x, event.y, event.x, event.y))

    def init_canvas(self):
        self.canvas.pack(expand=YES, fill=BOTH)
        self.canvas.bind("<B1-Motion>", self.on_move)
        self.canvas.bind("<B1-ButtonRelease>", self.on_release)
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<ButtonPress-2>", self.overlap)

    def __init__(self, master):
        self.canvas = Canvas(master,
                             width=500,
                             height=500)
        self.init_canvas()
        self.allow_drawing = False
        self.x1, self.x2, self.y1, self.y2 = 0, 0, 0, 0
        self.drawn_line_tmp = 0
        self.lines = []
